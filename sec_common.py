# general
import pandas as pd
import os

# funcs

def ls_of_dicts_to_csv(ls_of_dicts, filename, mode = "a+"):
    """
    save filing details to CSV


    Parameters
    ----------
    ls_of_dicts : list of dicts
        each item in list is a dict where key = header, value = value
    filename : str
        CSV filename
    mode: str
        file mode
        defaults to open for reading/appending

    Returns
    -------
    None
    """
    df = pd.DataFrame(ls_of_dicts)
    if os.path.exists(filename):
        df.to_csv(filename, mode = mode, header = False, index = False)
    else:
        df.to_csv(filename, mode = mode, header = True, index = False)
    return