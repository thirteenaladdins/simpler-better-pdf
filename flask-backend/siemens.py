import logging
import fitz
import re
import pandas as pd

import sys
import pprint


# helper function
def is_number(x):
    try:
        # only integers and float converts safely
        num = float(x)
        return True
    except ValueError as e: # not convertable to float
        return False

# I have no real reason to use classes at the moment but my code is terrible

class Siemens:
    def __init__(self):
        pass

    def str_list(x):
        return str(x)

    # primitive sorting function
    def item_sorter(item):
        try:
            value = item[-1]
            description = item[-5]
            quantity = item[-4]
            return [description, quantity, value]

        # what exception am I looking for?
        # so we were trying to skip items where the index did not exist - I don't really know how to fix this
        except IndexError as error:
            # Output expected IndexErrors.
            logging.log_exception(error)
        except Exception as exception:
            # Output unexpected Exceptions.
            logging.log_exception(exception, False)

    """ The amount of times I transform the types here is ridiculous. Is there a simpler way? 
		A method I have used before is locating the index of an element and gettinig all that precedes it
	"""

# TODO: extract_siemens

    def extract_siemens(path_to_pdf):
    
        # doc = fitz.open(path_to_pdf)
        doc  = fitz.open(stream=path_to_pdf, filetype="pdf")
        # doc.authenticate()``

        # create a list comprehension, that appends page data to the list
        pages = [doc[i] for i in range(len(doc))]

        full_list = []
        tariff_list = []
        gross = ""
        net = ""

        # search_pattern = ''
        # re.compile(search_pattern, '')
        # count = int()

        # def replace_comma_with_dot(x):
        #     y = x.replace(",", ".")
        #     return y

        for page in pages:
            text = page.get_text("text")
            # pprint.pprint(text)
            # print(text)
            text_split = text.split("\n")
            # print(text_split)
            item_list = []

            for item in text_split:
                if "Material" in item:
                    # find material - the preceding values are for this item, the following HS Code
                    item_index = text_split.index(item)

                    value = text_split[item_index - 1]
                    # fixed_value = value.replace(".", "").replace(",", ".")

                    # if the description and quantity are glued together
                    # check if the value is a number - if not it is a description
                    if is_number(text_split[item_index - 5]):
                        # all but the final item count as the description
                        desc_split = text_split[item_index - 4].split(" ")
                        description = " ".join(desc_split[:-1])
                        # and the final item is the quantity
                        # quantity = remove_commas(desc_split[-1])
                        qty = desc_split[-1]
                        # qty = replace_comma_with_dot(quantity)
                        # print(qty)

                    else:
                        description = text_split[item_index - 5]
                        qty = text_split[item_index - 4]
                        # print(quantity)
                        # qty = replace_comma_with_dot(quantity)
                        # print(qty)

                    item_list = [description, qty, gross, net, value]
                    full_list.append(item_list)

                if "HS Code" in item:
                    item = item.replace("HS Code: ", "")
                    tariff_list.append([item])

        # combines two lists together - well nested lists in this case
        full_list = [i + j for i, j in zip(tariff_list, full_list)]

        for i in full_list:
            print(i)
        

        df = pd.DataFrame(full_list)

        return df

# for testing purposes
# if __name__ == "__main__":
#     Siemens.extract_siemens(sys.argv[1])