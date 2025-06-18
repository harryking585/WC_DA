'''
    Debugging environment for manipulating data
    Strictly for testing purposes only, not intended for final build/prod
'''

import pandas as pd
import os


def main():
    os.makedirs("WC_DA/testdata", exist_ok=True)
    df = pd.read_csv("WC_DA/testdata/raw_bestruns.csv")

    return 0

if __name__ == "__main__":
    main()