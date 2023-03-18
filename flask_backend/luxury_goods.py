import fitz
import re
from itertools import combinations
import pandas as pd
from utils.helpers import Helpers

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
        return invoice_no
    except:
        # return 'No Invoice Number found'
        return 'No invoice number found'


# 'TOTAL NW'
def extract_net_weight(full_text):
    search_net_weight = re.findall(r'TOT. CRTS. .*?NW.*?KG', full_text, re.DOTALL)

    # this does not always get the correct data
    net_weight = search_net_weight[0].split('\n')[-1]
    formatted_net_weight = net_weight.replace(',', '.').replace('KG', ' ')    
    return formatted_net_weight
    
# 'TOTAL GW'
def extract_gross_weight(full_text):
    search_gross_weight = re.findall(r'TOT. CRTS. .*?NW.*?KG', full_text, re.DOTALL)
    print(search_gross_weight, flush=True)

    # this does not always get the correct data
    gross_weight = search_gross_weight[0].split('\n')[-4]
    formatted_gross_weight = gross_weight.replace(',', '.').replace('KG', ' ')    
    
    return formatted_gross_weight

def extract_total_packages(full_text):

    search_total_packages = re.findall(r'TOT. CRTS. .*?NW.*?KG', full_text, re.DOTALL)

    # this does not always get the correct data
    total_packages = search_total_packages[0].split('\n')[-7]
    formatted_total_packages = total_packages.replace(',', '.').replace('KG', ' ')    
    
    return formatted_total_packages
    
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
    try:
        index_of = tariff_code_segment.index("ENCLOSED TARIFF CODE")
        tariff_page_segment = tariff_code_segment[index_of:]
        rejoined_text =' '.join(tariff_page_segment)
    except:
        pass

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
    final_list = []

    for item in item_list:
        new_list = item.split('\n')
        item_list_to_process = [k for k in new_list if '%' not in k]
        value = find_value(item_list_to_process)

        filtered_list = filter_numbers(item_list_to_process)
        remove_duplicates = sorted(set(filtered_list))
        remove_leading_zeroes = [i for i in remove_duplicates if i[0] != '0']

        all_combinations = list(combinations(remove_leading_zeroes, 2))  

        list_calculated_values = {}
        list_compare_values = {}

        for each_value in all_combinations:
            x, y = each_value
            multiply_value = float(x) * float(y)
            list_calculated_values[multiply_value] = each_value

            for key in list_calculated_values.keys():
                difference = float(key) - float(value)
                list_compare_values[abs(difference)] = key

        value_closest_to_zero = min(list_compare_values.keys())
        get_delta_key = list_compare_values[value_closest_to_zero]
        quantity_pair = list_calculated_values[get_delta_key]

        for y in quantity_pair:
            if '.' not in y:
                final_list.append(y)

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

    total_net_weight = extract_net_weight(full_text)
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
        
    df = pd.DataFrame(item_list)
    
    # Set initial values for Total Net Weight, Total Gross Weight, and Total Cartons
    df.at[0, 'Total Net Weight'] = total_net_weight
    df.at[0, 'Total Gross Weight'] = total_gross_weight
    df.at[0, 'Total Cartons'] = total_cartons

    # Rename the columns
    df.columns = [
        "Commodity Code", "Value", "Country of Origin", "Invoice", "Description",
        "Quantity", "Total Net Weight", "Total Gross Weight", "Total Cartons"
    ]

    # Calculate the pro-rated weights
    total_value = df['Value'].sum()
    pro_rated_net_weight = (float(df.at[0, 'Total Net Weight']) / total_value) * df['Value']
    pro_rated_gross_weight = (float(df.at[0, 'Total Gross Weight']) / total_value) * df['Value']

    # Insert the pro-rated weight columns at loc 6 and 7
    df.insert(loc=6, column='Pro-rated Net Weight', value=pro_rated_net_weight)
    df.insert(loc=7, column='Pro-rated Gross Weight', value=pro_rated_gross_weight)

    return df


# # TODO: reimplement quantity extraction:
# def find_quantity_in_list(item_list, value):
#     # first - get only the numbers - so where there is an alpha - remove it
#     # filtered_list = [i for i in item_list if not i.isalpha()]
    
#     final_list = []

#     # item list? What is item list? 
#     for item in item_list:
#         filtered_list = []
#         new_list = item.split('\n')
        
#         # FIND VALUE - have to remove percent
#         # percent always refers to a discount value
#         item_list_to_process = [k for k in new_list if '%' not in k]
#         # print(item_list_to_process)
        
#         # discount = [k for k in new_list if '%' in k]

#         # index = item_list_to_process.index('Made in')
#         value = find_value(item_list_to_process)
#         # print('VALUE', value, flush=True)

#         for new_item in item_list_to_process:
#             if not re.search(alpha, new_item):
#                 if re.search(num, new_item):
#                     if not re.search(tariff, new_item):
                        
#                         # TODO filter any characters that aren't commas and full stops?
#                         filtered_list.append(new_item.replace(' ', '').replace('_', '').replace('.', '').replace(',', '.'))
#                         remove_duplicates = sorted(set(filtered_list))
#                         remove_leading_zeroes = [i for i in remove_duplicates if i[0] != '0']
        

#                         #  the biggest problem is my code is hard to follow
#                         # none of it makes senses 
#         all_combinations = list(combinations(remove_leading_zeroes, 2))  
#         # print(all_combinations, flush=True)

#         # this is for each item - a number of combinations for each item.
#         list_calculated_values = {}
#         list_compare_values = {}

#         # these seems to work anyway, because when I multiply the values out
#         # the correct value is always the smallest somehow
#         for ind, each_value in enumerate(all_combinations):
#             x, y = each_value
            
#             # that might bring me closer to the correct value
#             multiply_value = float(x) * float(y)
#             # store this value and the tuple together
#             list_calculated_values[multiply_value] = each_value
            
#             # list of calculated values 
#             keys_list = list(list_calculated_values.keys()) 
#             # the difference that is closest to zero is the winner
#             for key in keys_list:
#                 # this should equal zero or be close to zero
#                 # for each 
#                 difference = float(key) - float(value)
#                 # print("key", float(key), "value", float(value), "difference", difference, flush=True)
#                 # print(difference, flush=True)
                
#                 # add the difference here - against the multiplied value
#                 # add the absolute value of the key here 
#                 # all that matters is how close the difference is to zero - whether it's positive or negative

#                 list_compare_values[abs(difference)] = key
            
#             compare_keys = list(list_compare_values.keys())
#             # print(compare_keys, flush=True)

#         # TODO: get the smallest value? Or really it should be the one that is closest to zero
#         # get difference between 0 and the value - the smallest difference is the winner

#         # FIXME: here we get min - but really we want the one that is closest to zero
#         # simplest way is to make all values positive - but in case the smallest value is the negative
#         # - think about this a bit more. 

#         # i know what to do. don't turn them all positive but instead get the absolute value
#         # FIXME: it works in some cases but not in others - look at this tomorrow. 

#         value_closest_to_zero = min(compare_keys)
#         # value_closest_to_zero = min(compare_keys)
#         # value_closest_to_zero = min(get_absolute_values)
#         # print(value_closest_to_zero, flush=True)

#         # get the key of the value that is closest to zero
#         get_delta_key = list_compare_values[value_closest_to_zero]
        
#         # what's this?
#         quantity_pair = list_calculated_values[get_delta_key]
        
#         # this is a complicated process - but it works
#         # at this point in our journey we have a whole number and a number with a decimal
#         # I want the one that has no dot
#         # print(quantity_pair)
                
#         for y in quantity_pair:
#             if '.' not in y:
#                 final_list.append(y)

#         # list_types = [type(k) for k in compare_keys]

#     return final_list





# ''' COMPARE TOTALS HERE '''
# TODO: Extra function here
#  items_sort = df.sort_values(by=['Commodity Code'])

#     # items_sort['Quantity'] = items_sort["Quantity"].apply(lambda x: float(x))
#     cols = ['Commodity Code', 'Quantity', 'Value']
#     items_sort[cols] = items_sort[cols].apply(pd.to_numeric, errors='coerce', axis=1)

#     manually_extracted_totals = items_sort.groupby(['Commodity Code'], as_index=False).sum()

#     manually_extracted_totals =  manually_extracted_totals.reindex(columns=['Commodity Code', 'Quantity', 'Value'])
#     print(manually_extracted_totals)
    
#     totals = extract_total_table_data(full_text)
    
#     totals = totals.drop(columns=['Description', 'Net Weight'])
#     totals[cols] = totals[cols].apply(pd.to_numeric, errors='coerce', axis=1)
    
#     # validate function here 
#     # compared = manually_extracted_totals.compare(totals, align_axis=0, keep_shape=False, keep_equal=False)
#     # print(compared)
#     manually_extracted_totals['quantities_match'] = np.where(manually_extracted_totals['Quantity'] == totals['Quantity'], 'True', 'False')
#     manually_extracted_totals['value_match'] = np.where(manually_extracted_totals['Value'] == totals['Value'], 'True', 'False')
#     # compare the two dataframes here - add an extra column to the totals dataframe
    
#     # this is complete spaghetti 
#     print(manually_extracted_totals)