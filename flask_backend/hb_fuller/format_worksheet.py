import sys
import os
import pandas as pd

# Set up directories
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
worksheet_validation_dir = os.path.join(parent_dir, 'worksheet_validation')

sys.path.append(parent_dir)
sys.path.append(worksheet_validation_dir)

# Import custom modules
from worksheet_validation.row_schema import row_data_schema
from worksheet_validation.header_schema import headers_schema

# Read input file and clean data
input_file = sys.argv[1]
df = pd.read_excel(input_file, dtype=str)
valid_row_threshold = 10
df_cleaned = df.dropna(thresh=valid_row_threshold)

# Get sheet names
excel_file = pd.ExcelFile(input_file)
sheet_names = excel_file.sheet_names

# Define EU countries
eu_countries = ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 
                'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV',
                'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK',
                'SI', 'ES', 'SE']

# Select relevant columns
selected_columns = ["Plant Name", "Currency", "General description", "Qty Shipped Net Weight KG", 
                    "Sales Order Nbr", "Number Pieces", "Date Creation Record", "Customs Value", 
                    "10-Digit UK Import", "Country Of Origin", "EORI Nbr"]
df_subset = df_cleaned[selected_columns]

# Create DataFrames for headers and rows
headers_df = pd.DataFrame(columns=headers_schema.keys())
rows_df = pd.DataFrame(columns=row_data_schema.keys())

def add_address_data(row):
    pass


# Function to categorize country and create new rows
def categorize_country(row):
    new_rows = {'row1': {}, 'row2': {}}

    if row['Country Of Origin'] in eu_countries:
        new_rows['row1'] = {
            'Country of Preferential Origin': row['Country Of Origin'],
            'Preference': 300,
            'Doc Type': 'U112',
            'Doc Status': 'JP',
            'Doc Reference': row['Sales Order Nbr'] + ' ' + row['Date Creation Record'],
            'Doc Reason': 'IMPORTERS KNOWLEDGE',
        }
    else:
        new_rows['row1'] = {
            'Origin Country': row['Country Of Origin'],
            'Preference': 100,
            'Tax Type': 'A00',
            'MoP': 'E',
            'Doc Type': 'C505',
            'Doc Status': 'CC',
            'Doc Reference': 'GBCGUGARANTEENOTREQUIRED',
        }

        new_rows['row2'] = {
            'Doc Type': 'C506',
            'Doc Reference': 'GBDPO8115401',
        }

    return new_rows

# Set up basic row data
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

# Generate new rows based on country categorization
new_rows_list = []

for index, row in df_subset.iterrows():
    new_rows = categorize_country(row)
    new_rows_list.append(new_rows)

# Add new row data to rows_df
for index, new_rows in enumerate(new_rows_list):
    for column, value in new_rows['row1'].items():
        if column in rows_df.columns:
            rows_df.at[index, column] = value

# Create rows2_df with the data from new_rows['row2']
row2_list = [rows['row2'] for rows in new_rows_list]
rows_df_2 = pd.DataFrame(row2_list)

rows_df["Prev Doc Category"] = "Z"
rows_df["Prev Doc Type"] = "380"
rows_df["Prev Doc Reference"] = df_subset['Sales Order Nbr'].str.cat(df['Date Creation Record'], sep=' ')

rows_df_3 = pd.DataFrame(index=df_subset.index)
rows_df_3["Prev Doc Category"] = "Y"
rows_df_3["Prev Doc Type"] = "CLE"
rows_df_3["Prev Doc Reference"] = df_subset["Date Creation Record"]
rows_df_3["Doc Type"] = "N935"
rows_df_3["Doc Status"] = "AE"
rows_df_3["Doc Reference"] = df_subset['Sales Order Nbr'].str.cat(df['Date Creation Record'], sep=' ')

rows_df_4 = pd.DataFrame(index=df_subset.index)
rows_df_4["Doc Type"] = "C514"
rows_df_4["Doc Reference"] = "GBEIR570487130006I20220104092202"

# Concatenate all row DataFrames
final_rows_df = pd.concat([rows_df, rows_df_2, rows_df_3, rows_df_4], axis=1)
print(final_rows_df)

# Write output to Excel file
with pd.ExcelWriter('output.xlsx') as writer:
    headers_df.to_excel(writer, sheet_name='Header', index=False)
    final_rows_df.to_excel(writer, sheet_name='Rows', index=False)

