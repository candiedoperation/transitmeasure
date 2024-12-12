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

if __name__ == "__main__":
    print(geolocate_ipv4('188.186.146.208'))