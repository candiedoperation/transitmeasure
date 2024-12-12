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
import re

import nltk
import requests
from easynmt import EasyNMT
from langdetect import detect
from bs4 import BeautifulSoup

# Initialize EasyNMT model for translation
nltk.download('punkt_tab')
model = EasyNMT('opus-mt')

# Base Censorship Phrases
BASE_CENSOR_PHRASES = [
    r"Blocked",
    r"Russian Federation",
    r"Ministry of Telecommunications",
    r"Court Decision",
    r"Access Restricted",
    r"Federal Service for Supervision"
]

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


def detect_transit_censorship(raw_measurements, httpOnly=True):
    # Statistics
    total_measurements = 0
    transit_censored = 0

    for raw_measurement in raw_measurements:
        # Test Parameters
        destination = raw_measurement['input']
        origin_country = raw_measurement['probe_cc']
        measurement_requests = raw_measurement['test_keys']['requests']

        for req in measurement_requests:
            # Apply TCP Transport Filter
            if req['request']['x_transport'] != 'tcp':
                continue

            # Apply HTTP Only Filters
            if httpOnly and (not destination.startswith("http://")):
                continue

            # We're using this measurement
            total_measurements += 1

            # Extract response body and parse HTML
            response_body = req['response'].get('body', '')
            soup = BeautifulSoup(response_body, 'html.parser')

            # Extract text from paragraph tags
            paragraphs = soup.find_all('p')
            paragraph_texts = [p.get_text() for p in paragraphs]

            # Translate each paragraph text up to 400 characters into English
            translated_paragraphs = []
            for text in paragraph_texts:
                if len(text) > 400:
                    text = text[:400]  # Limit to 400 characters

                # Detect language of the text
                detected_lang = detect(text)

                # Translate only if detected language is not English
                if detected_lang != 'en':
                    translated_text = model.translate(text, source_lang=detected_lang, target_lang='en')
                    translated_paragraphs.append(translated_text)

                else:
                    translated_paragraphs.append(text)

            for translated_text in translated_paragraphs:
                matches = [phrase for phrase in BASE_CENSOR_PHRASES if re.search(phrase, translated_text, re.IGNORECASE)]

                # If matches are found, analyze further
                if matches:
                    print(f"Censorship detected: {', '.join(matches)}")

                    # Geolocate IPs involved in redirection
                    request_ip = req['request']['headers'].get('Host', '')
                    response_ip = req['response']['headers'].get('Location', '')

                    # request_country = geolocate_ipv4(request_ip)
                    # response_country = geolocate_ipv4(response_ip)

                    # Check if redirection IPs belong to a different country than probe_ccL weight shuld be low
                    # if request_country and request_country != probe_cc:
                    #     print(f"Request redirected through {request_country}, differing from origin {probe_cc}.")
                    # if response_country and response_country != probe_cc:
                    #     print(f"Response served from {response_country}, differing from origin {probe_cc}.")

    if total_measurements < 1:
        print("No Measurements matched Applied Filters")

    else:
        print(
            f"Transit Censored Requests: {transit_censored}/{total_measurements}" +
            f"({(transit_censored / total_measurements) * 100}%)"
        )

    # Return a JSON-like object lol
    return {total_measurements, transit_censored}
