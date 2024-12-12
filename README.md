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
Using cached results for: FI_2024-10-01_2024-10-30_None_True

Step #2: Data Preprocessing
Using Pre-process Dump File for further analysis...

Step #3: Detecting Transit Censorship
Potential Transit Tampering: FI -> DE | XZ -> FI instead of FI -> DE -> FI
Potential Transit Tampering: FI -> US | XZ -> FI instead of FI -> US -> FI
Potential Transit Tampering: FI -> US | XZ -> FI instead of FI -> US -> FI
Transit Censored Requests: 3/4 (75.0%)
Confidence Score: 0.8999999999999999/3 (30.0%)

Final Report:
To be Implemented
```