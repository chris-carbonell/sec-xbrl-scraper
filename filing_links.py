# general
from datetime import datetime
import sys

# scrape
from bs4 import BeautifulSoup
import requests

# sec
import sec_common as sc

# funcs

def get_filings(cik, type, dateb = None, filing_limit = None):
    """
    get list of filings matching the provided criteria

    Parameters
    ----------
    cik : str
        CIK number of company (eg 0000051143)
    type : str
        filing type (eg 10-K)
    dateb: str
        YYYYMMDD of date before to filter EDGAR search results
        defaults to today if not provided

    Returns
    -------
    ls of dict
        list of dicts of filings details (eg links, etc)
    """
    
    ls_return = []
    
    # assumptions
    if dateb is None:
        dateb = datetime.now().strftime("%Y%m%d")
    
    # Obtain HTML for search page
    base_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}&dateb={}".format(cik, type, dateb)
    # print(base_url)
    edgar_resp = requests.get(base_url)
    edgar_str = edgar_resp.text

    # Find the document link
    doc_link = ''
    soup = BeautifulSoup(edgar_str, 'html.parser')
    table_tag = soup.find('table', class_='tableFile2')
    rows = table_tag.find_all('tr')
    filing_counter = 0 # compare against filing_limit
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 3:

            # get
            doc_link = 'https://www.sec.gov' + cells[1].a['href']
            
            # save
            ls_return.append(
                {
                    'CIK': cik,
                    'Filing': type,
                    'Filing Date': cells[3].text,
                    'Filing Link': doc_link,
                    'Search Results': base_url
                }
            )

            # console
            # print(doc_link)

            # test limit
            filing_counter += 1
            if filing_limit is not None:
                if filing_counter >= filing_limit:
                    break # just give me the latest one
        
    return ls_return

if __name__ == "__main__":

    # testing
    # I just wanted to demonstrate how to use these funcs

    if len(sys.argv) > 1:
        cik = sys.argv[1]
    else:
        cik = '0000051143'
    
    cik = cik.zfill(10)  # 10 digit
    type = '10-K'

    # get filings
    ls_filings = get_filings(cik, type)

    # save
    sc.ls_of_dicts_to_csv(ls_filings, cik + ".csv")