from calendar import c
from csv import list_dialects
import fitz
import sys
import re
from itertools import combinations
import pandas as pd

from numpy import extract, full

# web version
# make an interface to simplify the process

# prepend each item with invoice number
# get only matches after -Tariff Code- # get descriptions from each invoice from this point forward 
# get net weight from this point forward

alpha = re.compile('[a-zA-Z]')
num = re.compile('\d')
tariff = re.compile('\d{8}')

def load_pdf(path_to_pdf):
    doc = fitz.open(stream=path_to_pdf, filetype="pdf")
    
    full_text = ""
    for page in doc:
        text = page.get_text("text")
        full_text += text
    
    # print(full_text)
    # print(full_text.split('\n'))
    # doc.close()
    return full_text

def extract_items(full_text):
    all_matches = re.findall(r'Item .*?Made .*?[A-Z]\n', full_text, re.DOTALL)
    return all_matches
    
# It's also possible that the first page may not be an invoice page
# TODO make this more robust
def extract_invoice_no(path_to_pdf):
    doc = fitz.open(stream=path_to_pdf, filetype="pdf")  
    first_page = doc[0].get_text("text")

    split = first_page.split('\n')
    index_no = split.index('INVOICE')
    invoice_no = split[index_no + 1]
    # print(index_no)
    return invoice_no
    

# search the tariff section here instead?
# or am I overcomplicating it?

def extract_net_weight(full_text):
    # 'TOTAL NW'

    search_net_weight = re.findall(r'TOT. CRTS. .*?NW.*?KG', full_text, re.DOTALL)

    # this does not always get the correct data
    net_weight = search_net_weight[0].split('\n')[-1]
    formatted_net_weight = net_weight.replace(',', '.').replace('KG', ' ')
    


    return formatted_net_weight
    # invoice_no = re.findall(r'INVOICE', full_text)
    # return invoice_no

# TODO following tariff number

# so we have a tariff to compare to


# TODO - looks like this won't work evey time because the discount is calculated on the total 
# invoice cost and not on the individual items, which somehow doesn't give us the correct value. 

# the value for this is entirely dependent on the comma in the value

# only two values should be passed in here - they are the ones with the commas
# I just realised I don't need all that other complicated code - 
# 
# 
def calculate_value(items_list):
    # print(items_list, flush=True)
    find_value = []
    
    for value in items_list:
        if ',' in value:
            if not re.search(alpha, value):
                find_value.append(float(value.replace('.', "").replace(',', '.')))

    # value = max(find_value)
    max_value = max(find_value)
    min_value = min(find_value)

    print(max_value, min_value, flush=True)
    if (max_value / min_value < 1.5):
        # print('MIN VALUE', flush=True)
        value = min_value
    else:
        # print('MAX VALUE', flush=True)
        value = max_value
    
    # print('TRUE VALUE', value)
    return value

def calculate_quantity(item_list, value):
    # first - get only the numbers - so where there is an alpha - remove it
    # filtered_list = [i for i in item_list if not i.isalpha()]
    
    final_list = []

    for item in item_list:
        filtered_list = []
        new_list = item.split('\n')
        
        # FIND VALUE - have to remove percent
        item_list_to_process = [k for k in new_list if '%' not in k]
        # print(item_list_to_process)
        
        # discount = [k for k in new_list if '%' in k]

        # index = item_list_to_process.index('Made in')
        value = calculate_value(item_list_to_process)

        for new_item in item_list_to_process:
            if not re.search(alpha, new_item):
                if re.search(num, new_item):
                    if not re.search(tariff, new_item):
                        
                        # TODO filter any characters that aren't commas and full stops?
                        filtered_list.append(new_item.replace(' ', '').replace('_', '').replace('.', '').replace(',', '.'))
                        remove_duplicates = sorted(set(filtered_list))
                        remove_leading_zeroes = [i for i in remove_duplicates if i[0] != '0']
        
                                                           
        all_comb = list(combinations(remove_leading_zeroes, 2))      

        # this is for each item - a number of combinations for each item.
        list_calculated_values = {}
        list_compare_values = {}

        # these seems to work anyway, because when I multiply the values out
        # the correct value is always the smallest somehow
        for ind, each_value in enumerate(all_comb):
            x, y = each_value
            
            multiply_value = float(x) * float(y)
            # store this value and the tuple together
            list_calculated_values[multiply_value] = each_value
            
            # list of calculated values 
            keys_list = list(list_calculated_values.keys()) 

            # the difference that is closest to zero is the winner
            for key in keys_list:
                # this should equal zero or be close to zero
                # for each 
                difference = float(key) - float(value)
                
                # add the difference here - against the multiplied value
                list_compare_values[difference] = key
            
            compare_keys = list(list_compare_values.keys())

        # TODO get the smallest value? Or really it should be the one that is closest to zero
        min_delta = min(compare_keys)

        get_delta_key = list_compare_values[min_delta]
        
        quantity_pair = list_calculated_values[get_delta_key]
        
        # at this point in our journey we have a whole number and a number with a decimal
        # I want the one that has no dot
        # print(quantity_pair)
                
        for y in quantity_pair:
            if '.' not in y:
                final_list.append(y)

        # list_types = [type(k) for k in compare_keys]

    return final_list

def extract_descriptions(full_text):
    # ENCLOSED TARIFF CODE
    # tariff_code_segment = re.findall((r'?<=ENCLOSED TARIFF CODE).*'), full_text, re.DOTALL)
    # print(full_text)
    
    tariff_code_segment = full_text.split('\n')
    index_of = tariff_code_segment.index("ENCLOSED TARIFF CODE")
    tariff_page_segment = tariff_code_segment[index_of:]
    rejoined_text =' '.join(tariff_page_segment)
    # print(rejoined_text)

    description_list = []

    all_items = re.findall(r'\d{8} .*?Kg', rejoined_text)
    for item in all_items:
        split = item.split(' ')

        GBP_index = split.index("GBP")

        description_list.append(split[:GBP_index-1])


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
        # print(commodity_code)
        # print(newlist)
        # commodity_code = 

        # sometimes there are discounts, sometimes there aren't. 
        # this messes up the whole thing

        # lets assume that the percentage
        # use the filter to remove anything with a percent symbol

        alpha = re.compile('[a-zA-Z]')
        find_value = []

        # for item in item_list:
        #     if ',' in item:
        #         if not re.search(alpha, item):
        #             find_value.append(float(item.replace('.', "").replace(',', '.')))

        
        
        value = calculate_value(item_list)
        
        country_of_origin = item_list[index + 1]
        
        item_information.append(commodity_code)
        item_information.append(value) 
        item_information.append(country_of_origin)
        full_list.append(item_information)
        
    return full_list


# TODO now we need to compare the two lists - 
# when I find the tariff code I want from the first list 
# search the second list - if its a match then get the rest of the list 

def match_descriptions(all_items, descriptions):
    final_list = []
    # for each item in the list - get item at index 0
    # then compare that item to the second list 
    # if the item from the first list matches the item in the second - get index
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
    full_text = load_pdf(file)
    invoice_no = extract_invoice_no(file)

    # pro rata net weight
    # net_weight = extract_net_weight(full_text)
    
    descriptions_list = extract_descriptions(full_text)
    
    all_matches = extract_items(full_text)
    
    formatted_items = format_items(all_matches)
    
    for item in formatted_items:
        item.append(invoice_no)

    # run the below and output into excel format
    quantity = calculate_quantity(all_matches, 1)
    
    add_descriptions = match_descriptions(formatted_items, descriptions_list)
    
    # add the quantity items to the original list
    for i, j in zip(add_descriptions, quantity):
        i.append(j)
        item_list.append(i)
        

    df = pd.DataFrame(item_list)

    # Rearrange these into the correct order
    df.columns = ["Commodity Code", "Value", "Country of Origin", "Invoice", "Description", "Quantity"]

    # value_sum = round(df.iloc[:, 1].sum(), 2)

    # df['Net Weight'] = (float(net_weight) / float(value_sum)) * df.iloc[:,1] 

    # output file
    # df.to_csv("output.csv")

    return df
    

    