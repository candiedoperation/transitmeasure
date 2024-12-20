# TransitMeasure
An approach to measure transit censorhip using OONI-provided datasets. To learn more about the approach, 
its core ideas and the implementation methodologies, read the paper [_Do Transit Countries Censor Traffic? Measuring Internet Censorship in Transit_](https://www.overleaf.com/read/xvrvzrwmkdsz#4f19ea)  by clicking on the link.

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
Fetching Raw Reports: 100%|██████████████| 66/66 [01:09<00:00,  1.05s/measurement, current=66]
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

# Sample Test Results
```
==== TEST 01 ====
probe_cc = 'FI'
start_date = '2024-01-01'
end_date = '2024-12-31'

22 Raw Reports
Transit Censored Requests: 7/22 (31.818181818181817%)
Confidence Score: 4.2/7 (60.0%)
Censoring Country: Russia (Translation Auto-detect, Regex Match)

==== TEST 02 ====
probe_cc = 'JP'                                                    
start_date = '2023-01-01'                                         
end_date = '2023-12-31'   

27 Raw Reports
Transit Censored Requests: 1/27 (3.7037037037037033%)
Confidence Score: 0.2/1 (20.0%)
Censoring Country: Turkey (Translation API auto-detect)

==== TEST 03 ====
probe_cc = 'EE'
start_date = '2023-03-01'
end_date = '2023-12-31'

6 Raw Reports
Transit Censored Requests: 3/6 (50.0%)
Confidence Score: 2.4000000000000004/3 (80.00000000000001%)
Censoring Country: Russia (Translation Auto-detect, Regex Match)

==== TEST 04 ====
probe_cc = 'LU'
start_date = '2023-03-01'
end_date = '2023-12-31'

166 Raw Reports
Transit Censored Requests: 100/166 (60.24096385542169%)
Confidence Score: 83.571428571428545/100 (83.57142857142854%)
Censoring Country: Belgium (Regex Match)
```

<br>
© Copyright 2024 Atheesh Thirumalairajan<br>
This is a free and open-source project
