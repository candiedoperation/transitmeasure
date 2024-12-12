"""
    TransitMeasure
    Copyright (C) 2024  Atheesh Thirumalairajan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import json
import config
import requests
from tqdm import tqdm
from cli import ANSIEscape
from caching import load_cache, save_cache
from datetime import datetime, timezone

# Fetch measurements with caching, timeline, and vantage point filtering
def fetch_measurements_with_cache(probe_cc, start_date, end_date, probe_asn=None, confirmed=True):
    # Debug, List Step
    print(ANSIEscape.BOLD + "Step #1: Applying Filters and Fetching OONI Data" + ANSIEscape.END)
    
    cache = load_cache()
    cache_key = f"{probe_cc}_{start_date}_{end_date}_{probe_asn}_{confirmed}"

    if cache_key in cache:
        print("Using cached results for:", cache_key)
        return cache[cache_key]

    params = {
        'test_name': 'web_connectivity',
        'confirmed': confirmed,
        'probe_cc': probe_cc,
        'since': start_date,
        'until': end_date
    }

    if probe_asn:
        params['probe_asn'] = probe_asn  # Add ASN filter if provided

    print(f"Downloading OONI Measurements for {cache_key}...")
    response = requests.get(config.OONI_MEASUREMENTS_URL, params=params)
    response.raise_for_status()
    results = response.json()['results']

    # Save to cache
    cache[cache_key] = results
    save_cache(cache)

    # Highly Likely that Preprocess Dump is Expired
    if os.path.exists(config.PREPROCESS_DUMP_FILE):
        os.rename(
            config.PREPROCESS_DUMP_FILE, 
            f"{config.PREPROCESS_DUMP_FILE.replace('.json', '')}" + 
            f"_bkp_{datetime.now(timezone.utc)}.json"
        )

    return results

# Preprocess data: filter relevant blockpages
def preprocess_data(measurements, usedump=False):
    # Log Step Progress
    print(ANSIEscape.BOLD + "\nStep #2: Data Preprocessing" + ANSIEscape.END)
    if usedump and os.path.exists(config.PREPROCESS_DUMP_FILE):
        print("Using Pre-process Dump File for further analysis...")
        with open(config.PREPROCESS_DUMP_FILE, 'r') as file:
            return json.load(file)
    
    raw_reports = []
    total_measurements = len(measurements)

    # Initialize tqdm progress bar
    with tqdm(total=total_measurements, desc="Fetching Raw Reports", unit="measurement") as pbar:
        for measurement in measurements:
            # Fetch Raw Report from the OONI Raw Measurement URL
            raw_report_res = requests.get(measurement['measurement_url'])
            raw_report_res.raise_for_status()
            raw_reports.append(raw_report_res.json())

            # Update progress bar
            pbar.update(1)
            pbar.set_postfix(current=len(raw_reports))

    # If Dump Requested, save the results
    if usedump:
        with open(config.PREPROCESS_DUMP_FILE, "w") as file:
            json.dump(raw_reports, file, indent=4)

    print(f"Downloaded {len(raw_reports)} Raw Reports for Analysis")
    return raw_reports