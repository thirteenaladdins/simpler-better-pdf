import fitz
import re
from itertools import combinations
import pandas as pd
from utils.helpers import Helpers
import unittest

# add conversion of country of origins to 2 letter country codes
# change output file name 
# output worksheet - give a second option to output ASM worksheet

alpha = re.compile('[a-zA-Z]')
num = re.compile('\d')
tariff = re.compile('\d{8}')

def extract_items(full_text):
    all_matches = re.findall(r'Item .*?Made .*?[A-Z]\n', full_text, re.DOTALL)
    return all_matches
    
def extract_invoice_no(path_to_pdf):
    doc = fitz.open(stream=path_to_pdf, filetype="pdf")  
    first_page = doc[0].get_text("text")

    split = first_page.split('\n')

    try:
        index_no = split.index('INVOICE')
        invoice_no = split[index_no + 1]
        new_invoice_no = invoice_no.replace('*', '')
        return new_invoice_no
    
    except ValueError:
        return "INVOICE not found in list"
    
    except IndexError:
        return "No element after INVOICE in list"


# 'TOTAL NW'
def extract_net_weight(full_text):
    search_net_weight = re.findall(r'TOT. CRTS. .*?NW.*?KG', full_text, re.DOTALL)

    # TODO: fix - this does not always get the correct data
    if search_net_weight:
        net_weight = search_net_weight[0].split('\n')[-1]
        formatted_net_weight = net_weight.replace('.','').replace(',', '.').replace('KG', ' ')    
        return formatted_net_weight
    else:
        formatted_net_weight = None
    
# 'TOTAL GW'
def extract_gross_weight(full_text):
    search_gross_weight = re.findall(r'TOT. CRTS. .*?NW.*?KG', full_text, re.DOTALL)
    # print(search_gross_weight, flush=True)

    # TODO: fix - this does not always get the correct data
    if search_gross_weight:
        gross_weight = search_gross_weight[0].split('\n')[-4]
        formatted_gross_weight = gross_weight.replace('.','').replace(',', '.').replace('KG', ' ')    
        return formatted_gross_weight
    else: 
        formatted_gross_weight = None


# 'TOTAL PACKAGES'
def extract_total_packages(full_text):

    search_total_packages = re.findall(r'TOT. CRTS. .*?NW.*?KG', full_text, re.DOTALL)

    # TODO: fix - this does not always get the correct data
    if search_total_packages:
        total_packages = search_total_packages[0].split('\n')[-7]
        formatted_total_packages = total_packages.replace(',', '.').replace('KG', ' ')    
        
        return formatted_total_packages
    else: 
        formatted_total_packages = None
    
def find_value(items_list):
    # print(items_list, flush=True)
    number_array = []

    for value in items_list:
        if ',' in value:
            if not re.search(alpha, value):
                number_array.append(float(value.replace('.', "").replace(',', '.')))

    # value = max(number_array)
    max_value = max(number_array)
    min_value = min(number_array)

    # print(max_value, min_value, flush=True)
    if (max_value / min_value < 1.5):
        # print('MIN VALUE', flush=True)
        value = min_value
    else:
        # print('MAX VALUE', flush=True)
        value = max_value
    
    # print('TRUE VALUE', value)
    return value

def format_number(number):
    try:
        remove_dot = number.replace('.', '')
        replace_comma = remove_dot.replace(',', '.')
        return replace_comma
    except:
        return number

def extract_total_table_data(full_text):
    totals = []

    tariff_code_segment = full_text.split('\n')
    index_of = tariff_code_segment.index("ENCLOSED TARIFF CODE")
    tariff_page_segment = tariff_code_segment[index_of:]
    rejoined_text = ' '.join(tariff_page_segment)

    all_items = re.findall(r'\d{8} .*?GBP .*?Kg', rejoined_text)

    for item in all_items:
        split = item.split(' ')
        GBP_index = split.index("GBP")

        try:
            commodity_code = split[0]
            description = ' '.join(split[1:GBP_index-1])
            value = split[GBP_index-1]
            total_quantity = split[GBP_index + 1]
            total_net_weight = split[GBP_index + 2]

            item_list = [
                commodity_code,
                description,
                format_number(total_quantity),
                format_number(total_net_weight),
                format_number(value)
            ]
            totals.append(item_list)

        except:
            continue

    df = pd.DataFrame(totals)
    df.columns = ["Commodity Code", "Description", "Quantity", "Net Weight", "Value"]

    return df

def extract_descriptions(full_text):
    tariff_code_segment = full_text.split('\n')
    rejoined_text = ""  # Default value

    try:
        index_of = tariff_code_segment.index("ENCLOSED TARIFF CODE")
        tariff_page_segment = tariff_code_segment[index_of:]
        rejoined_text = ' '.join(tariff_page_segment)
    except ValueError as e:
        print(f"Error: {e}. 'ENCLOSED TARIFF CODE' not found.")
        return []  # Return an empty list

    description_list = []
    all_items = re.findall(r'\d{8} .*?GBP .*?Kg', rejoined_text)
    
    for item in all_items:
        split = item.split(' ')
        try:
            GBP_index = split.index("GBP")
            description_list.append(split[:GBP_index-1])
        except:
            continue

    return description_list


def format_items(all_items):
    
    full_list = []

    for item in all_items:
        item_information = []
        
        item_list = item.split('\n')
        
        # filter a list element where the string contains a specific character
        item_list = [k for k in item_list if '%' not in k]
        # print(item_list)
        index = item_list.index('Made in')

        r = re.compile("\d{8}")
        commodity_code = list(filter(r.match, item_list))[0] # Read Note below
        
        value = find_value(item_list)
        
        country_of_origin = item_list[index + 1]
        
        item_information.append(commodity_code)
        item_information.append(value) 
        item_information.append(country_of_origin)
        full_list.append(item_information)
        
    return full_list

def filter_numbers(item_list):
    alpha = re.compile('[a-zA-Z]')
    num = re.compile('\d')
    tariff = re.compile('tariff')
    filtered_list = []
    
    for item in item_list:
        if not re.search(alpha, item) and re.search(num, item) and not re.search(tariff, item):
            filtered_list.append(item.replace(' ', '').replace('_', '').replace('.', '').replace(',', '.'))
    
    return filtered_list

def find_quantity_in_list(item_list, value):

    # change this. we need to do this in reverse
    def apply_discount(value, discount):
        return value * (1 - discount)

    # what does this do?
    def approximate_equal(a, b, tolerance=0.01):
        return abs(a - b) <= tolerance

    def parse_discount(discount_str):
        # Convert comma to dot and remove % sign, then split on slash
        return [float(d.replace(',', '.')) for d in discount_str.replace('%', '').split('/')]
    
    def apply_all_discounts(value, discounts):
        if not discounts:
            return value
        
        discount = discounts[0]
        discounted_value = apply_discount(value, discount / 100)
        return apply_all_discounts(discounted_value, discounts[1:])


    def find_quantity_and_unit_price(numbers, total_value, full_list):

        # Extract integers from the full_list
        # int_values = [float(item) for item in full_list if re.match(r'^\d+$', item)]
        print('total_value', total_value)
        # Get all combinations of two numbers from the list
        for a, b in combinations(numbers, 2):
            product = float(a) * float(b)
            # print(product, a, b)
            if abs(product - total_value) < 0.01:
                # so return both a and b here - as these will be the correct values
                # return the quantity here?
                string_a = str(a)
                string_b = str(b)
                print('candidates', string_a, string_b)
                # keep only integers, then fetch the final number from the list
                if '.' not in string_a:
                    quantity = string_a
                    return quantity
                
                else:
                    quantity = string_b
                    return quantity
                # if the strings are exact then return


                
                
        # If direct multiplication didn't give the expected total_value, consider the discounts
        discounts = [item for item in full_list if '%' in item]
        
        if discounts:
            discount_values = parse_discount(discounts[0])
            print("discounts", discount_values)

            # for each combination of the values, apply the discounts
            for a, b in combinations(numbers, 2):
                product = float(a) * float(b)
                discounted_value = apply_all_discounts(product, discount_values)
                
                if approximate_equal(total_value, discounted_value):
                    # here - remove the final value from a and b
                    # retain only the integer
                    if '.' not in a:
                        print('a', a)
                        return a
                    
                    else:
                        print('b', b)
                        return b
                
        return None

    final_list = []

    for item in item_list:
        new_list = item.split('\n')
        full_list = [k for k in new_list if not re.fullmatch(r'\d{8}', k)] # retain discounts for later use
        item_list_to_process = [k for k in full_list if '%' not in k]

        value = find_value(item_list_to_process)

        filtered_list = filter_numbers(item_list_to_process)
        remove_duplicates = sorted(set(filtered_list))

        value_str = "{:.2f}".format(float(value))
        while value_str in remove_duplicates:
            remove_duplicates.remove(value_str)

        print('Processed items:', remove_duplicates)
        remove_leading_zeroes = [i for i in remove_duplicates if i[0] != '0']

        potential_quantity = find_quantity_and_unit_price(remove_leading_zeroes, float(value), full_list)

        if potential_quantity: 
            final_list.append(potential_quantity)

    return final_list


def match_descriptions(all_items, descriptions):
    final_list = []

    for item in all_items:
        tariff = item[0]
        # print(item)
        for x, description in enumerate(descriptions):
            if tariff == description[0]:
                fetch_description = descriptions[x]
                description_only = fetch_description[1:]
                
                joined_desc = ' '.join(description_only)
                
                # insert description into item
                item.append(joined_desc)
                
                final_list.append(item)    
                
    return final_list

def extract_luxury_goods_data(file):
    item_list = []
    # for path in files:
    full_text = Helpers.convert_all_pages_to_text(file)
    invoice_no = extract_invoice_no(file)

    descriptions_list = extract_descriptions(full_text)
    
    all_matches = extract_items(full_text)

    # extract net weight
    total_net_weight = extract_net_weight(full_text)

    # extract gross weight
    total_gross_weight = extract_gross_weight(full_text)

    total_cartons = extract_total_packages(full_text)
    # print(total_net_weight, total_gross_weight, total_cartons)
    
    formatted_items = format_items(all_matches)
    
    for item in formatted_items:
        item.append(invoice_no)

    # run the below and output into excel format

    quantity = find_quantity_in_list(all_matches, 1)
    
    add_descriptions = match_descriptions(formatted_items, descriptions_list)
    
    # add the quantity items to the original list
    for i, j in zip(add_descriptions, quantity):
        i.append(j)
        item_list.append(i)
        
    # print("item_list:", item_list)

    df = pd.DataFrame(item_list)
    
    # Set initial values for Total Net Weight, Total Gross Weight, and Total Cartons
    df.at[0, 'Total Net Weight'] = total_net_weight
    df.at[0, 'Total Gross Weight'] = total_gross_weight
    df.at[0, 'Total Cartons'] = total_cartons


    new_columns = ["Commodity Code", "Value", "Country of Origin", "Invoice", "Description",
        "Quantity", "Total Net Weight", "Total Gross Weight", "Total Cartons"]
    
    # Rename the columns
    if len(new_columns) == len(df.columns):
        df.columns = new_columns
    else:
        print(f"Length mismatch: DataFrame has {len(df.columns)} columns, but you're trying to assign {len(new_columns)} new column names.")

    # Calculate the pro-rated weights
    if 'Value' in df.columns:
        total_value = df['Value'].sum()

        pro_rated_net_weight = round((float(df.at[0, 'Total Net Weight']) / total_value) * df['Value'], 3)
        pro_rated_gross_weight = round((float(df.at[0, 'Total Gross Weight']) / total_value) * df['Value'], 3)


        # Insert the pro-rated weight columns at loc 6 and 7
        df.insert(loc=6, column='Pro-rated Net Weight', value=pro_rated_net_weight)
        df.insert(loc=7, column='Pro-rated Gross Weight', value=pro_rated_gross_weight)

    # remove this as the value is not always calculated correctly
    # df.drop(['Quantity'], axis=1, inplace=True)
    
    # df.drop("Quantity")
    # print(df)
    return df
