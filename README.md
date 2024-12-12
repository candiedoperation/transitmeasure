# TransitMeasure
An approach to measure transit censorhip using OONI-provided datasets. Add a Link to the paper here, in the future.

# Usage
Modify the `main()` function as described below. Create a virual environment and install the 
required packages listed in `requirements.txt`. Once the setup is complete, simply run the program
using `python main.py`

```python
def main():
    # Example usage: Specify country code, timeline filters, and vantage point ASN
    probe_cc = 'FI'  # Country code of the probe (e.g., FI for Finland)
    start_date = '2024-10-01'  # Start date for filtering measurements
    end_date = '2024-10-30'  # End date for filtering measurements
    probe_asn = None  # Optional: ASN of the vantage point (e.g., 'AS57043')
```

# Sample Output
```commandline
Step #1: Applying Filters and Fetching OONI Data
Downloading OONI Measurements for EE_2023-03-01_2023-12-01_None_True...

Step #2: Data Preprocessing
Fetching Raw Reports: 100%|█████████████████| 66/66 [01:09<00:00,  1.05s/measurement, current=66]
Downloaded 66 Raw Reports for Analysis

Step #3: Detecting Transit Censorship
Potential Transit Tampering: EE -> RU | XZ -> EE instead of EE -> RU -> EE
Blockpage Parsing Detected Phrases: gov.ru, Russian Federation, restricted, denied

Potential Transit Tampering: EE -> DE | XZ -> EE instead of EE -> DE -> EE
Potential Transit Tampering: EE -> RU | XZ -> EE instead of EE -> RU -> EE
Blockpage Parsing Detected Phrases: gov.ru, Russian Federation, restricted, denied

Potential Transit Tampering: EE -> US | XZ -> EE instead of EE -> US -> EE
Potential Transit Tampering: EE -> RU | XZ -> EE instead of EE -> RU -> EE
Blockpage Parsing Detected Phrases: gov.ru, Russian Federation, restricted, denied

Transit Censored Requests: 3/6 (50.0%)
Confidence Score: 2.4000000000000004/3 (80.00000000000001%)

Final Report:
To be Implemented
```