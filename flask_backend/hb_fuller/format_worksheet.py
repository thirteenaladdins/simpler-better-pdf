import sys, os
import pandas as pd
import numpy as np
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

# Get the absolute path to the parent directory of the current file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory and worksheet_validation directory to the Python path
sys.path.append(parent_dir)
worksheet_validation_dir = os.path.join(parent_dir, 'worksheet_validation')
sys.path.append(worksheet_validation_dir)

from worksheet_validation.row_schema import row_data_schema
from worksheet_validation.header_schema import headers_schema

# print(sys.path)
# from ..utils.helpers import load_file
# from worksheet_validation.row_schema 
# from ..worksheet_validation.row_schema import row_data_schema

# sys.path.append(os.path.abspath(os.path.join('..', 'worksheet_validation')))
# from ..worksheet_validation.row_schema import row_data_schema

# # from "../row_schema" import row_schema_data 

# # this isn't going to be a cmd line script anyway
# # if len(sys.argv) != 2:

# df = pd.read_excel(sys.argv[1], dtype=str)
# print(df)
# # read worksheets, select worksheet to parse information

# # Open the Excel file using the ExcelFile class
excel_file = pd.ExcelFile(sys.argv[1])

# # Get a list of the sheet names
sheet_names = excel_file.sheet_names

# # TODO: in frontend choose which worksheet you want to format
print(sheet_names)

# # Read the first sheet into a pandas dataframe
df = excel_file.parse(sheet_names[0], dtype=str)

# filter by week and by delivery terms. group them all together.

# # input worksheet
# if 912/914 use the following headers
# if 3rd party use the other headers

# Define a custom function to classify each country of origin value
def classify_country_of_origin(country):
    if country in ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 
                    'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV',
                      'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK',
                        'SI', 'ES', 'SE']:
        return 'Country of Preferential Origin'
    else:
        return 'Origin Country'


header_names = "Plant Nbr", "Plant Name", "Sales Order Nbr", "Sales Order Item Nbr", "Customer Nbr", "Customer Name", \
                "Material Nbr", "Material Name", "General description", "Qty Shipped Net Weight KG", \
                "Packaging Net Weight", "Number Pieces", "Material Type", "Material value", "Freight Cost", \
                "Customs Value", "Currency", "Date Shipped", "Date Creation Record", "Estimated arrival date", \
                "Calendar Week", "Incoterms", "Commodity Code", "10-Digit UK Import", "Country Of Origin", \
                "Union status", "Duty free - TCA", "Grouped Deliveries", "Delivery Type Name", "Sales Org", \
                "Named Importer", "Name of Importer", "EORI Nbr", "Importer VAT Nbr", "Customs procedure code"


# output excel sheet mapping columns from excel to CDS worksheet columns
df_subset = df[["Plant Name", "Currency", "General description", "Qty Shipped Net Weight KG", 
  "Sales Order Nbr", "Number Pieces", "Date Creation Record", "Customs Value", 
  "10-Digit UK Import", "Country Of Origin", "EORI Nbr"]]

row_data_schema.keys()

# Create an empty DataFrame with the column headers

headers_df = pd.DataFrame(columns=headers_schema.keys())
rows_df = pd.DataFrame(columns=row_data_schema.keys())

# add additional columns with the same names
# this should be outside of this script? This is a primitive way to do it

# rows_df['Line Number'] = range(1, len(rows_df) + 1)

rows_df["Goods Description"] = df_subset["General description"]
rows_df["Currency"] = df_subset["Currency"]
rows_df["Net Mass"] = df_subset["Qty Shipped Net Weight KG"]
rows_df["Gross Mass"] = df_subset["Qty Shipped Net Weight KG"]
rows_df["Quantity"] = df_subset["Number Pieces"]
rows_df["Total Value"] = df_subset["Customs Value"] 
rows_df["Commodity"] =  df_subset["10-Digit UK Import"] 
rows_df["Procedure"] = "4000"
rows_df["Add Procedure Code"] = "000"
rows_df["Valuation Method"] = "1"
rows_df["Valuation Indicators"] = "0000"
rows_df["Package Kind"] = "PK"
rows_df["Package Number"] = df_subset["Number Pieces"]
rows_df["Package Marks"] = "As addressed"

rows_df["Prev Doc Category"] = "Z"
rows_df["Prev Doc Type"] = "380"

# format the date properly
rows_df["Prev Doc Reference"] = df_subset['Sales Order Nbr'].str.cat(df['Date Creation Record'], sep=' ')

# define the list of EU countries
# eu_countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 
#                 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany',
#                   'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania',
#                   'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal',
#                     'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden']

# eu_countries = ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 
#                     'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV',
#                       'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK',
#                         'SI', 'ES', 'SE']

eu_countries = ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 
                    'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV',
                      'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK',
                        'SI', 'ES', 'SE']

def categorize_country(country):
    if country in eu_countries:
        return 'Country of Preferential Origin'
    else:
        return 'Origin Country'

origin_df = pd.DataFrame(index=df_subset.index)
origin_df =  df_subset['Country Of Origin'].apply(categorize_country)

print(origin_df)

df_subset['Country Of Origin']






# view the modified rows_df
# print(rows_df)



# create duplicate columns

# create new df

# so you have to specify the number of rows
rows_df_2 = pd.DataFrame(index=df_subset.index)
rows_df_2["Prev Doc Category"] = "Y"
rows_df_2["Prev Doc Type"] = "CLE"
rows_df_2["Prev Doc Reference"] = df_subset["Date Creation Record"]
rows_df_2["Doc Type"] = "N935"
rows_df_2["Doc Status"] = "AE"
rows_df_2["Doc Reference"] = df_subset['Sales Order Nbr'].str.cat(df['Date Creation Record'], sep=' ')

# Country Of Origin

# define the dataframe
# df = pd.DataFrame({'Country': ['France', 'Spain', 'Australia', 'Italy']})



# rows_df_3 = pd.DataFrame(index=df_subset.index)
# rows_df_3["Doc Type"] = "U112"
# rows_df_3["Doc Status"] = "JP"
# rows_df_3["Doc Reference"] = df_subset['Sales Order Nbr'].str.cat(df['Date Creation Record'], sep=' ')
# rows_df_3["Doc Reason"] = "Importers Knowledge"

rows_df_4 = pd.DataFrame(index=df_subset.index)
rows_df_4["Doc Type"] = "C514"
rows_df_4["Doc Reference"] = "EIDR REF"

# TODO: 
# 100, 300
# countries of origin
# check plant name and assign addresses

# add A00 - E for non EU
# add C505, C506 for non EU and dutiable 

# header page should be the only thing you have to fill out

# add commodity validation for 
# check table first, if not present then fetch from the api. 
# but then if the data is present in the table but has been updated this won't work


# depends on the origin
# rows_df[] = df_subset["Country Of Origin"]

# Write the DataFrame to an Excel file
with pd.ExcelWriter('output.xlsx') as writer:
    headers_df.to_excel(writer, sheet_name='Header', index=False)
    rows_df.to_excel(writer, sheet_name='Rows', index=False)


# print(df_subset)



# Plant Name - to exporter - match data from table

# General description   to description
# Qty Shipped Net Weight KG   - net weight gross weight

# Sales Order Nbr - Z 380 previous doc
# Number Pieces   - packages
# Date Creation Record   - Y CLE date + to invoice

# Customs Value   - value

# 10-Digit UK Import   - commodity

# Country Of Origin    - origin country of preferential origin

# "EORI Nbr", "Importer VAT Nbr"
# check that this matches 912 or 914 so we don't double enter the data like it happened that time
