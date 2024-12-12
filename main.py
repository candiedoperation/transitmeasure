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
from cli import ANSIEscape
from detection import detect_transit_censorship
from ooniapi import fetch_measurements_with_cache, preprocess_data

def main():
    # Example usage: Specify country code, timeline filters, and vantage point ASN
    probe_cc = 'EE'  # Country code of the probe (e.g., FI for Finland)
    start_date = '2023-03-01'  # Start date for filtering measurements
    end_date = '2023-12-01'  # End date for filtering measurements
    probe_asn = None  # Optional: ASN of the vantage point (e.g., 'AS57043')

    # Step 1: Obtain censorship data with caching and filters
    print(ANSIEscape.BOLD + "Step #1: Applying Filters and Fetching OONI Data" + ANSIEscape.END)
    measurements = fetch_measurements_with_cache(probe_cc, start_date, end_date, probe_asn)

    # Step 2: Preprocess data
    print(ANSIEscape.BOLD + "\nStep #2: Data Preprocessing" + ANSIEscape.END)
    raw_measurements = preprocess_data(measurements, usedump=True)

    # Step 3: Identify transit censorship
    print(ANSIEscape.BOLD + "\nStep #3: Detecting Transit Censorship" + ANSIEscape.END)
    transit_censorship_cases = detect_transit_censorship(raw_measurements, httpOnly=True)

    # Step 4: Validate transit path analysis
    # validated_results = validate_transit_path(transit_censorship_cases)

    # Output results for analysis
    # print("\nValidated Transit Censorship Cases:")
    # for result in validated_results:
    #     print(result)

    # Step 5: Generate the Report
    print(ANSIEscape.BOLD + "\nFinal Report:" + ANSIEscape.END)
    print("To be Implemented")

if __name__ == "__main__":
    main()
