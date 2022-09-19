from tabula import read_pdf
from tabulate import tabulate
# import camelot

import pandas as pd

dfs = read_pdf("./pdf/396844 GAI.pdf",pages="all", output_format='dataframe') #address of pdf file
print(f"Found {len(dfs)} tables")

for df in dfs:
    print(df.size)
    print(df)

# output pandas dataframe to csv
df.to_csv('output.csv', index=False)

