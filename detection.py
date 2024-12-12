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

import ipaddress
import nltk
import requests
import dns.resolver
from cli import debug
from easynmt import EasyNMT
from langdetect import detect
from bs4 import BeautifulSoup

# Initialize EasyNMT model for translation
nltk.download('punkt_tab')
model = EasyNMT('opus-mt')

# Confidence Scores: Should Add up to 1
CONFIDENCE_SCORE_IPCHECK_WEIGHT = 0.3
CONFIDENCE_SCORE_BLKPAGE_WEIGHT = 0.7

# Base Censorship Phrases
BASE_CENSOR_PHRASES = [
    r"Blocked",
    r"Russian Federation",
    r"Ministry of Telecommunications",
    r"Court Decision",
    r"Access Restricted",
    r"Federal Service for Supervision"
]


def nslookup_v4(hostname):
    # Check if hostname is an IP Address
    try:
        ipaddress.ip_address(hostname)
        return hostname

    # If not an IP address, proceed with DNS resolution
    except ValueError:
        try:
            # Query for A records (IPv4 addresses)
            answers = dns.resolver.resolve(hostname, 'A')
            return answers[0].to_text()

        except Exception as e:
            return "0.0.0.0"


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
    tc_confidence_score = 0
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

            # DNS and IP Checks First
            request_ip = req['request']['headers'].get('Host', '')
            response_ip = req['response']['headers'].get('Location', '')

            serverhost_country = geolocate_ipv4(nslookup_v4(request_ip))
            actualresponse_country = geolocate_ipv4(nslookup_v4(response_ip))

            # Transit Detected State
            transit_detected = False

            # Check if redirection IPs belong to a different country than origin_country
            if serverhost_country != actualresponse_country:
                transit_detected = True
                transit_censored += 1
                tc_confidence_score += CONFIDENCE_SCORE_IPCHECK_WEIGHT

                # Log the Results, if needed
                debug(
                    f"Potential Transit Tampering: {origin_country} -> {serverhost_country} | {actualresponse_country} -> {origin_country} " +
                    f"instead of {origin_country} -> {serverhost_country} -> {origin_country}"
                )

            # If we got a censorship hint from the previous step, Prove it!
            if transit_detected:
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

                total_regexp_matches = 0
                for translated_text in translated_paragraphs:
                    matches = [phrase for phrase in BASE_CENSOR_PHRASES if
                               re.search(phrase, translated_text, re.IGNORECASE)]

                    # If matches are found, analyze further
                    if matches:
                        total_regexp_matches += 1
                        debug(f"Blockpage Parsing Detected Phrases: {', '.join(matches)}")

                # Update the Blockpage Score
                tc_confidence_score += (total_regexp_matches / len(BASE_CENSOR_PHRASES)) * CONFIDENCE_SCORE_BLKPAGE_WEIGHT;

    if total_measurements < 1:
        print("No Measurements matched Applied Filters")

    else:
        # Output Censored Request Count
        print(
            f"Transit Censored Requests: {transit_censored}/{total_measurements} " +
            f"({(transit_censored / total_measurements) * 100}%)"
        )

        # Output Confidence Score
        print(f"Confidence Score: {tc_confidence_score}/{transit_censored} ({(tc_confidence_score / transit_censored) * 100}%)")

    # Return a JSON-like object lol
    return {total_measurements, transit_censored, tc_confidence_score}
