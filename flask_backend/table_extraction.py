from tabula import read_pdf
# from tabulate import tabulate
# import camelot

import pandas as pd

# mismatch in number of columns
dfs = read_pdf("./pdf/447193_INV.pdf", pages="4", stream=True, output_format='dataframe', multiple_tables=True ) #address of pdf file
print(f"Found {len(dfs)} tables")


for df in dfs:
    print(df.size)
    print(df)

# 

# output pandas dataframe to csv
# manipulate dataframes to get the data we want. 
# group the data by  

remove_na_df = df.dropna()
print(remove_na_df)

# df.to_csv('output.csv', index=False)

# from the start - 10.0 down to line 4 with Hs Code - get the 4 lines there
# group each of the lines together
# is there a non-rule based system of analyse rows of data in a dataframe


