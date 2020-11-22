# Overview

**sec-xbrl-scraper** scrapes XBRLs of financial statements (e.g., 10-K) from the **SEC's EDGAR database**. This script stacks all of the data from the XBRLs for any number of filings across any number of companies and filing years.

# Executive Summary

* Creates a CSV of all of the filing information/data for any number of companies and filing years 

# Prerequisites

1. Operating System\
   This code has only been tested on Windows 10 Home (64-bit).
2. Infrastructure
   Python 3.8.5
3. Knowledge
   - requests
   - beautifulsoup4
   - financial statements (US GAAP)

# Example

1. Create CSV of all filings with the given CIK:<br>
`python filing_links.py 0000051143`

2. Create CSV of all tags starting with `us-gaap:` and `dei:` from a given filing:<br>
`python filing_data.py https://www.sec.gov/Archives/edgar/data/51143/000155837020001334/0001558370-20-001334-index.htm`

3. Create CSV of all tags starting with `us-gaap:` and `dei:` for a given list of CIKs:<br>
`python company_filngs.py 0001018724 0001652044 0000789019`

Notes:
* See `./output/example/` for the example output. The output there combines data from AMZN, GOOG, and MSFT as of 11/20/20.
* You'll see that each company can use their own contexts - lookup field that identifies the as of date (e.g., 2019). Therefore, `get_data.ipynb` provides an example of how to scrub the resulting data into a more digestible format. The result is `df_final.xlsx`.
* From there, you can read the data in Excel and play around with it as you please!

# References

* [https://www.codeproject.com/Articles/1227765/Parsing-XBRL-with-Python](https://www.codeproject.com/Articles/1227765/Parsing-XBRL-with-Python)
