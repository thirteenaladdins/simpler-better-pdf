import sys
import pandas as pd
import logging
from cerberus import Validator
from row_schema import row_data_schema
import numpy as np 
import time
import re

# TODO: I need more descriptive outputs, 
# maybe group by row and not by item

# TODO: regex error messages should be translated to something
# more informative

# TODO: if a column is not marked as required
# then we should not output any error messages

# Check if the file path is provided
if len(sys.argv) !=2:
    print("Error: Excel file path is not provided.")
    sys.exit()

# Initialize the logging module
logging.basicConfig(level=logging.ERROR)

# Read the 'Header' and 'Rows' sheets from the Excel file
try:
    headers_sheet = pd.read_excel(sys.argv[1], sheet_name='Header')
    rows_sheet = pd.read_excel(sys.argv[1], sheet_name='Rows')
except Exception as e:
    logging.error(f"Error: Could not read Excel file. {e}")
    sys.exit(1)

# Check if all the column headers in 'Rows' are valid
for col in rows_sheet.columns:
    if col not in row_data_schema:
        print(f"Error: Column header {col} is not valid.")
        sys.exit()

print('All column headers are valid.')

# Read the 'Rows' sheet into a pandas DataFrame
df = pd.read_excel(sys.argv[1], sheet_name='Rows', dtype=str)

# Initialize a validator with the schema
v = Validator(row_data_schema)

# def validate_error(row):
#     is_valid = v.validate(row.to_dict())
#     if not is_valid:
#         return v.errors

# how do I know this is doing what I want it to do?
# is it row or is it a cell?
# why does this only look for required columns?

def validate_error(row):    
    errors = {}
    for key in row_data_schema.keys():
        if key in row and pd.notna(row[key]):
            is_valid = v.validate({key: row[key]}, schema={key: row_data_schema[key]})
            if not is_valid:
                errors.update(v.errors)
        
        if key in row and row_data_schema[key].get('required'):
            is_valid = v.validate({key: row[key]}, schema={key: row_data_schema[key]})
            if not is_valid:
                errors.update(v.errors)

    if errors:
        return errors


    # if column not required then return nothing.
    # perhaps we could validate only columns that are required?
    # also what if people forget to fill some column in ...
    # some columns aren't required for some jobs and then required for others

# here's what we'll do here. Suppress error messages for 
# country of origin / preferential country of origin

# if we receive an error message for one and not the other, 
# then remove the error message

# if we receive an error message for both
# create custom error message - this should say "either COO or PCOO should be filled in"

# so if the format is wrong then submit the standard error message
# somehow as we loop through each column one at a time - 
# but we need to get the COO and PCOO messages after
# as we loop through, create a new array
# add COO and PCOO messages
# then based on the message we create a new set of messages.

def format_errors(errors, schema):
    error_messages = []
    country_of_origin_array = []

    for key, messages in errors.items():
        # Get the schema for the current key
        field_schema = schema.get(key, {})
        
        # Check if the field is required
        is_required = field_schema.get('required', False)

        # Create a formatted error message for each message
        for message in messages:
            # Extract the value from within curly braces {} if it exists
            # COO = re.search(r"Origin Country", message)
            # Pref_COO = re.search(r"Country of Preferential Origin", message)
            match = re.search(r"\{(.+?)\}", message)
            value = match.group(1) if match else "unknown"

            if is_required:
                if key == "Origin Country":
                    error_message = f"{key}: is required."
                    country_of_origin_array.append(error_message)
                elif key == "Country of Preferential Origin":
                    error_message = f"{key}: is required."
                    country_of_origin_array.append(error_message)
                else:
                    error_message = f"{key}: is required."
                
            else:
                # Check if the error message is a regex pattern error
                regex_error = re.match(r"value does not match regex '(.+)'", message)

                # Create the error message based on the regex pattern and the extracted value
                if regex_error:
                    if '[0-9]' in message:
                        error_message = f"{key}: must be a number, length {value}"
                    elif '[A-Za-z0-9]' in message:
                        error_message = f"{key}: must be alphanumeric characters, length {value}"
                    elif '[A-Za-z]' in message:
                        error_message = f"{key}: must be alphabetical characters a-z, A-Z, length {value}"
                    elif '[A-Z]' in message:
                        error_message = f"{key}: must be alphabetical characters A-Z, length {value}"
                    elif '[01]' in message:
                        error_message = f"{key}: must be 0 or 1, length {value}"
                    else:
                        error_message = f"{key}: must match the pattern {regex_error.group(1)}."
                else:
                    error_message = f"{key}: {message}"
            
            
            if key == "Origin Country":
                # error_messages.append(error_message)
                pass
            elif key == "Country of Preferential Origin":
                pass
            else:
                error_messages.append(error_message)
            # if key != "Country of Preferential Origin":
                
    # if len(country_of_origin_array) == 0:
    #     error_message = "Both Country of Origin and Country of Preferential Origin are complete. Was this intentional?"
    #     error_messages.append(error_message)
    
    # if len(country_of_origin_array) == 1:
    #     pass
    
    if len(country_of_origin_array) == 2:
        error_message = "Country of Origin or Country of Preferential Origin is required"
        error_messages.append(error_message)
    

    # if len is 1 - do not return an error message
    
    # if len is 0 - that means both are filled in: provide provisional error message
    # only 1 is required but 2 have been filled in - did you mean to do this?
    # some circumstances that acts as a workaround for some errors

    # put the array in the right place. 
    # it should clear after every new line item

    


    return error_messages


# def validate_all(df):
#     # Validate each row against the schema and print out any errors
#     # start_time = time.time()

#     errors = df.apply(validate_error, axis=1)

#     for i, error in enumerate(errors):
#         if error is not None:
#             for key, messages in error.items():
#                 print(f"Validation failed for Line {i+1}: {key}: {', '.join(messages)}")
#     end_time = time.time()
#     # print("time elapsed", end_time - start_time)

def validate_all(df):
    # Validate each row against the schema and print out any errors
    start_time = time.time()

    errors = df.apply(validate_error, axis=1)

    for i, error in enumerate(errors):
        if error is not None:
            formatted_errors = format_errors(error, row_data_schema)
            for error_message in formatted_errors:
                print(f"Validation failed for Line {i+1}: {error_message}")
    end_time = time.time()
    print("time elapsed", end_time - start_time)

validate_all(df)

# only after validation is completed successfully
# print("All columns are of correct format.")