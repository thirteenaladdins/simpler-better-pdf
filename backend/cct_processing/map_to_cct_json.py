# take excel data, convert to CCT JSON

import os
import json
from datetime import datetime

# LUXURY GOODS
additional_header_data = {
    "interfaceVersion": "4.5",  
    "customerIdCCT": "GBPFEWIT01",
    "customerEmail": "mamer@als-cs.com",  
    "customerReference": 'TESTREFERENCE001',  
    "deliveryTerm_SAD20": "EXW",
    "deliveryTermPlace_SAD20": "CHSBO",
    "countryOfExport_SAD15": "CH",  
    "countryOfDestination_SAD17": "GB",

    # sum of cartons
    "totalPackages_SAD06": "",  
    "totalAmountInvoiced_SAD22": "",

    # highlight if there are multiple currencies in worksheet
    "totalAmountInvoicedCurrency_SAD22": "GBP",
    "totalGrossMass": "",
}


# TODO: this is specific to this one customer but I should separate the rest out later
def map_df_to_cct_json(input_data):

    input_data = input_data.reset_index(drop=True)
    input_data['sequentialNo'] = input_data.index + 1

    # Move the 'sequentialNo' column to the beginning of the DataFrame
    cols = input_data.columns.tolist()
    cols.insert(0, cols.pop(cols.index('sequentialNo')))
    input_data = input_data[cols]

    input_data = input_data.rename(columns={
        "Commodity Code": "customerHSCode_SAD33im",
        "Value": "itemPrice_SAD42",
        "Invoice": "invoiceNo",
        "Country of Origin": "countryOfOrigin_SAD34",
        "Description": "goodsDescription_SAD31",
        "Quantity": "noOfPackages_SAD31",
        "Pro-rated Net Weight": "netMass_SAD38",
        "Pro-rated Gross Weight": "grossMass_SAD35",
    })

    input_data["goodsValueCurrency"] = "GBP"

    # Calculate the sum of gross weights
    total_gross_weight = input_data["grossMass_SAD35"].astype(float).sum()
    
    # Update the additional_header_data with the totalGrossMass
    additional_header_data["totalGrossMass"] = total_gross_weight

    # add sum of invoices
    sum_values = total_gross_weight = input_data["itemPrice_SAD42"].astype(float).sum()
    additional_header_data["totalAmountInvoiced_SAD22"] = sum_values

    # add sum of cartons
    sum_cartons = total_gross_weight = input_data["Total Cartons"].astype(float).sum()
    additional_header_data['totalPackages_SAD06'] = sum_cartons

    columns_to_drop =  [
        "Total Net Weight",
        "Total Gross Weight",
        "Total Cartons"
    ]

    input_data.drop(columns=columns_to_drop, inplace=True)

    positions = input_data.to_dict(orient="records")

    # Group by invoiceNo and sum itemPrice_SAD42
    grouped = input_data.groupby('invoiceNo').agg({'itemPrice_SAD42': 'sum', 'goodsValueCurrency': 'first'}).reset_index()

    # Get today's date in the required format
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Format the data
    invoices = [
        {
            "invoiceNo": row['invoiceNo'],
            "invoiceDate": current_date,
            "invoiceAmount": row['itemPrice_SAD42'],
            "invoiceCurrency": row['goodsValueCurrency']
        } for index, row in grouped.iterrows()
    ]


    # Copy the constant header data to start building the CustomsOrder dictionary
    customs_order_data = additional_header_data.copy()

    # invoices = [{"invoiceNo":"SI-A014216","invoiceDate":"2022-11-16","invoiceAmount":27089.0,"invoiceCurrency":"EUR"}]

    customs_order_data.update({
        "addresses": [
            {
                "role": "CZ",
                "eoriNo": "GB162990737000",
                "vatNo": "GB162990737",
                "name1": "IFOR WILLIAMS TRAILERS LTD",
                "street": "CYNWYD",
                "zipcode": "LL21 0LB",
                "city": "CORWEN",
                "country": "GB"
            },
            {
                "role": "CN",
                "name1": "HBL TRADING",
                "street": "SCHERPENZEELSEWEG 1",
                "zipcode": "6741",
                "city": "LUNTEREN",
                "country": "NL"
            },
        ],
        "positions": positions,
        "invoices": invoices
    })

    # Construct the final desired JSON structure
    result = {
        "CustomsOrder": customs_order_data

    }

    return result