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

from os import path

# Debug and Caching Config
DEBUG = True
DEBUG_LEVEL = 3
CACHE_DIR = "file_cache/"
CACHE_FILE = path.join(CACHE_DIR, "ooni_cache.json")
PREPROCESS_DUMP_FILE = path.join(CACHE_DIR, "preprocessing_dump.json")

# OONI Config
OONI_MEASUREMENTS_URL = "https://api.ooni.io/api/v1/measurements"
OONI_RAW_MEASUREMENT_URL = "https://api.ooni.io/api/v1/raw_measurement"