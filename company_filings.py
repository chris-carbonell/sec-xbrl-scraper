# general
from datetime import datetime
from pathlib import Path
import pandas as pd
import os

# sec
import sec_common as sc
import filing_data as fd
import filing_links as fl

def print_log_message(str_main, str_msg):
    print(", ".join([str_main, str_msg]))
    return

if __name__ == "__main__":

    # testing
    # I just wanted to demonstrate how to use these funcs

    # company info
    # TODO: specify with command line args
    ls_cik = ["0001018724", "0001652044", "0000789019"]
    # AMZN = 0001018724
    # GOOG = 0001652044
    # MSFT = 0000789019
    
    # filing info
    type = '10-K'
    ls_filing_data = ['CIK', 'Filing', 'Filing Date', 'Filing Link']
    ls_tag_startswith = ["us-gaap:", "dei:"] # XBRL tags

    # make output folder
    output_dir_root = "./output/" + datetime.now().strftime("%Y%m%d%H%M") + "/"
    Path(output_dir_root).mkdir(parents=True, exist_ok=True)

    # for each CIK
    for cik in ls_cik:
        
        cik = cik.zfill(10)  # 10 digit

        # get filings
        ls_filings = fl.get_filings(cik, type)

        # save
        sc.ls_of_dicts_to_csv(ls_filings, output_dir_root + "filing_summary.csv")
        print_log_message("saved", "filing_summary.csv")

        # for each filing, get the data
        for dict_filing in ls_filings:

            # get xbrl
            # if error, we just continue on to the next one

            doc_link = dict_filing['Filing Link'] # get link to filing
            print_log_message("attempting to scrape", doc_link)
            
            try:
                xbrl_link = fd.get_xml_link(doc_link) # get xml link, returns None if nothing found
                if xbrl_link is None:
                    print_log_message("error", "xbrl_link failed (None)")
                    continue
            except:
                print_log_message("error", "xbrl_link failed (except)")
                continue
            
            xbrl_str = fd.get_xbrl_text(xbrl_link) # get text of xml link

            if xbrl_str is None: # invalid link or other error in getting xbrl so skip
                print_log_message("error", "xbrl_str failed (None)")
                continue # move on to next filing

            # get tag data
            for tag_startswith in ls_tag_startswith:
                
                print_log_message("processing", tag_startswith)

                # get attr df
                ls_dicts_startswith = fd.get_tag_info_ls(xbrl_str, tag_startswith)
                df = pd.DataFrame(ls_dicts_startswith)
                
                # add filing data at front
                
                ls_cols_attr = df.columns.tolist() # list of attribute columns

                # bring in filing data
                for col_filing_data in ls_filing_data:
                    df[col_filing_data] = dict_filing[col_filing_data]

                df = df[ls_filing_data + ls_cols_attr] # reorder

                # save
                filename = output_dir_root + tag_startswith.replace(":","") + ".csv"
                if os.path.exists(filename):
                    # exists so concat
                    df_orig = pd.read_csv(filename)
                    df_out = pd.concat([df_orig, df], axis = 0, ignore_index = True)
                    df_out.to_csv(filename, index = False) # overwrite
                else:
                    df.to_csv(filename, index = False) # create