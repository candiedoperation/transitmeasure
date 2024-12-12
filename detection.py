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

import requests

def geolocate_ipv4(address):
    if not address:
        raise "Invalid IP Address"

    # Using the ip2c.org API (Change Backend, if needed)
    response = requests.get(f'https://ip2c.org/{address}')
    response.raise_for_status()

    # Parse Result. Sample Format: 1;RU;RUS;Russian Federation (the)
    geo_result = response.text.split(';')
    country_code = geo_result[1]
    return country_code

def detect_transit_censorship(raw_measurement, httpOnly=True):
    # Statistics
    total_measurements = 0
    transit_censored = 0

    # Test Parameters
    destination: str = raw_measurement["input"]
    origin_country = raw_measurement["probe_cc"]
    measurement_requests = raw_measurement["requests"]

    for req in []: #measurement_requests
        # Apply TCP Transport Filter
        if req['request']['x_transport'] != 'tcp':
            continue

        # Apply HTTP Only Filters
        if httpOnly and (not destination.startswith("http://")):
            continue

        # We're using this measurement
        total_measurements += 1

        # Check for block page content
        response_body = req['response'].get('body', '')
        if "Blocked by Russian Federation" in response_body:
            print("Block page detected indicating Russian Federation censorship.")

            # Geolocate IPs involved in this request/response cycle
            request_ip = req['request']['headers'].get('Host', '')
            response_ip = req['response']['headers'].get('Location', '')

            # Geolocate both IPs
            request_country = geolocate_ipv4(request_ip)
            response_country = geolocate_ipv4(response_ip)

            # Check for transit censorship
            if request_country != origin_country and request_country is not None:
                print(
                    f"Transit censorship detected: Request originated from {origin_country}, but was redirected through {request_country}.")

            if response_country != origin_country and response_country is not None:
                print(
                    f"Transit censorship detected: Response was served from {response_country}, differing from origin {origin_country}.")

    return { total_measurements, transit_censored }
