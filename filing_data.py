# scrape
from bs4 import BeautifulSoup
import requests

# sec
import sec_common as sc

# funcs

def get_xml_link(doc_link):
    # Obtain HTML for document page
    doc_resp = requests.get(doc_link)
    doc_str = doc_resp.text

    # Find the XBRL link
    xbrl_link = ''
    soup = BeautifulSoup(doc_str, 'html.parser')
    table_tag = soup.find('table', class_='tableFile', summary='Data Files')
    rows = table_tag.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 3:
            # print(cells[1].text) # testing
            if 'XBRL INSTANCE DOCUMENT' in cells[1].text:
                xbrl_link = 'https://www.sec.gov' + cells[2].a['href']

    return None if xbrl_link == '' else xbrl_link 

def get_xbrl_text(xbrl_link):
    # Obtain XBRL text from document
    try:
        xbrl_resp = requests.get(xbrl_link)
        xbrl_str = xbrl_resp.text
        return xbrl_str
    except:
        return None

def get_tag_list(xbrl_str):
    soup = BeautifulSoup(xbrl_str, 'lxml')
    tag_list = soup.find_all()
    return tag_list

def get_tag_info_ls(xbrl_str, str_startswith = "us-gaap:"):
    
    # get tag list
    tag_list = get_tag_list(xbrl_str)
    
    # get tag info
    ls_tags = []
    for tag in tag_list:

        # find targets
        if tag.name.startswith(str_startswith):
            
            # for lxml, bs4 truncates tags at 100 for no reason
            # so I'm just going to remove them
            # they're usually TextBlock
            # https://stackoverflow.com/questions/50924694/python-beautifulsoup-lxml-parsing-crops-tag-name-at-100-chars
            if len(tag.name) < 100:
        
                # skip textblock (some get cut off and just say textbloc)
                if 'textbloc' not in tag.name:

                    # start dict with the info
                    dict_tag = {
                        'tag': tag.name,
                        'text': tag.text
                    }

                    # get all the other attributes
                    dict_tag.update(tag.attrs)

                    # save to list of dicts
                    ls_tags.append(dict_tag)
    
    return ls_tags

if __name__ == "__main__":

    # testing
    # I just wanted to demonstrate how to use these funcs

    # specify dict_filing
    # for this test, only Filing Link is really necessary
    dict_filing = {
        'CIK': '0000051143',
        'Filing': '10-K',
        'Filing Date': '2020-02-25',
        'Filing Link': 'https://www.sec.gov/Archives/edgar/data/51143/000155837020001334/0001558370-20-001334-index.htm',
        'Search Results': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000051143&type=10-K&dateb=20201116'
        }

    # get xbrl
    doc_link = dict_filing['Filing Link'] # get link to filing
    xbrl_link = get_xml_link(doc_link) # get xml link
    xbrl_str = get_xbrl_text(xbrl_link) # get text of xml link

    # save XBRL to CSV

    ls_tag_startswith = ["us-gaap:", "dei:"]

    for tag_startswith in ls_tag_startswith:
        ls_dicts_startswith = get_tag_info_ls(xbrl_str, tag_startswith)
        sc.ls_of_dicts_to_csv(ls_dicts_startswith, "./" + tag_startswith.replace(":","") + ".csv")