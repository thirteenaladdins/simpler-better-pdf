
row_data_schema = {
    # the values must be sequential here
    'Line Number': {'type': 'integer', "required": True, "coerce": int},
    "Order Number": {"type": "string", "maxlength": 20},
    "Product Code": {"type": "string", "maxlength": 30},
    "SKU": {"type": "string", "maxlength": 30},
    "Serial Number": {"type": "string", "maxlength": 20},
    "Purchase Order": {"type": "string", "maxlength": 20},
    "Invoice Number": {"type": "string", "maxlength": 20},
    
    # TODO: is there a reason this is alphanum and not just integer?
    # import 10 digit, export 8 digit
    "Commodity": {"type": "string", "regex": r"^[0-9]{10}$", "required": True},

    "Add Commodity Code": {"type": "string", "regex": r"^[A-Za-z0-9]{4}$"},
    "Procedure": {"type": "string", "regex": r"^[A-Za-z0-9]{4}$", "required": True},
    "Add Procedure Code": {"type": "string", "regex": r"^[A-Za-z0-9]{3}$", "required": True},
    "Goods Description": {"type": "string", "maxlength": 512, "required": True},
    
    "CUS Code": {"type": "integer", "minlength": 8, "maxlength": 8},

    # "CUS Code": {"type": "integer", "min": 1000000, "max": 99999999},
    
    # 'Origin Country': {'type': 'string', 'regex': r'^[A-Z]{2}$', 'required': False},
    # 'Country of Preferential Origin': {'type': 'string', 'regex': r'^[A-Z]{2}$', 'required': False},
    # 'anyof': [
    #     {'required': ['Origin Country']},
    #     {'required': ['Country of Preferential Origin']}
    # ],
    
    # I can just create a workaround here

    'Origin Country': {'type': 'string', 'regex': r'^[A-Z]{2}$', 'required': True},
    'Country of Preferential Origin': {'type': 'string', 'regex': r'^[A-Z]{2}$', 'required': True},
    # 'anyof': [
    #     {'empty': ['Origin Country']},
    #     {'empty': ['Country of Preferential Origin']}
    # ],


    # 'all': [
    #     {'required': ['Origin Country', 'Country of Preferential Origin']}
    # ],

    # TODO: check required to be uppercase?

    # TODO: accoring to ASM this is up to 4 letter alphanum. check this?
    # "Country of Preferential Origin": {"type": "string", "regex": r"^[A-Za-z0-9]{4}$"},
    

    # TODO: all codes are 3 digits, why is this alphanum?
    "Preference": {"type": "string", "regex": r"^[A-Za-z0-9]{3}$"},

    "Quota": {"type": "string", "regex": r"^[A-Za-z0-9]{6}$"},
    
    # this is for the supplementary units
    "Quantity": {"type": "float", "regex": r"^\d{1,16}\.\d{6}$", "coerce": float, "required": True},

    "Currency": {"type": "string", "regex": r"^[A-Za-z]{3}$", "required": True},
    "Unit Price": {"type": "float", "regex": r"^\d{1,16}\.\d{2}$"},
    "Total Value": {"type": "float", "regex": r"^\d{1,16}\.\d{2}$", "coerce": float, "required": True},
    "Statistical Value": {"type": "float", "regex": r"^\d{1,16}\.\d{2}$", "coerce": float},
    "Net Mass": {"type": "float", "regex": r"^\d{1,16}\.\d{6}$", "coerce": float},
    "Gross Mass": {"type": "float", "regex": r"^\d{1,16}\.\d{6}$", "coerce": float},

    "Valuation Method": {"type": "integer", "max": 1, "required": True, "coerce": int},
    
    # only 1s and 0s accept
    "Valuation Indicators": {"type": "string", "regex": "^[01]{4}$", "required": True},
    
    # Can be headr or item level
    "Dispatch Country": {"type": "string", "regex": r"^[A-Z]{2}$"},
    "Destination Country": {"type": "string", "regex": r"^[A-Z]{2}$"},
    
    # TODO: technically correct...?
    "Transaction Nature": {"type": "integer", "min": 0, "max": 99, "coerce": int},

    # EXPORT ONLY?
    # TODO: throw error if it's an import 
    "Consignor EORI": {"type": "string", "regex": r"^[A-Za-z0-9]{1,17}$"},
    "Consignor Name": {"type": "string", "maxlength": 70},
    "Consignor Street": {"type": "string", "maxlength": 70},
    "Consignor City": {"type": "string", "maxlength": 35},
    "Consignor PostCode": {"type": "string", "maxlength": 9},
    "Consignor Country": {"type": "string", "regex": r"^[A-Z]{2}$"},
    "Consignor ShortCode": {"type": "string", "maxlength": 20},
    "Consignor External ID": {"type": "string", "maxlength": 20},

    "Consignee EORI": {"type": "string", "regex": r"^[A-Za-z0-9]{1,17}$"},
    "Consignee Name": {"type": "string", "maxlength": 70},
    "Consignee Street": {"type": "string", "maxlength": 70},
    "Consignee City": {"type": "string", "maxlength": 35},
    "Consignee PostCode": {"type": "string", "maxlength": 9},
    "Consignee Country": {"type": "string", "regex": r"^[A-Z]{2}$"},
    "Consignee ShortCode": {"type": "string", "maxlength": 20},
    "Consignee External ID": {"type": "string", "maxlength": 20},

    # IMPORT ONLY
    "Exporter EORI": {"type": "string", "regex": r"^[A-Za-z0-9]{1,17}$"},
    "Exporter Name": {"type": "string", "maxlength": 70},
    "Exporter Street": {"type": "string", "maxlength": 70},
    "Exporter City": {"type": "string", "maxlength": 35},
    "Exporter PostCode": {"type": "string", "maxlength": 9},
    "Exporter Country": {"type": "string", "regex": r"^[A-Z]{2}$"},
    "Exporter ShortCode": {"type": "string", "maxlength": 20},
    "Exporter External ID": {"type": "string", "maxlength": 20},

    "Seller EORI": {"type": "string", "regex": r"^[A-Za-z0-9]{1,17}$"},
    "Seller Name": {"type": "string", "maxlength": 70},
    "Seller Street": {"type": "string", "maxlength": 70},
    "Seller City": {"type": "string", "maxlength": 35},
    "Seller PostCode": {"type": "string", "maxlength": 9},
    "Seller Country": {"type": "string", "regex": r"^[A-Z]{2}$"},
    "Seller ShortCode": {"type": "string", "maxlength": 20},
    "Seller External ID": {"type": "string", "maxlength": 20},
    
    "Buyer EORI": {"type": "string", "regex": r"^[A-Za-z0-9]{1,17}$"},
    "Buyer Name": {"type": "string", "maxlength": 70},
    "Buyer Street": {"type": "string", "maxlength": 70},
    "Buyer City": {"type": "string", "maxlength": 35},
    "Buyer PostCode": {"type": "string", "maxlength": 9},
    "Buyer Country": {"type": "string", "regex": r"^[A-Z]{2}$"},
    "Buyer ShortCode": {"type": "string", "maxlength": 20},
    "Buyer External ID": {"type": "string", "maxlength": 20},

    "Tax Type": {"type": "string", "regex": r"^[A-Za-z0-9]{3}$"},
    "MoP": {"type": "string", "regex": r"^[A-Z]{1}$"},
    "MoP": {"type": "string", "maxlength": 1},
    "Measurement Unit": {"type": "string", "regex": r"^[A-Za-z0-9]{1,4}$"},
    
    "Tax Base Quantity": {"type": "float", "regex": r"^\d{1,16}\.\d{2}$"},
    "Tax Currency": {"type": "string", "regex": r"^[A-Z]{3}$"},
    "Tax Base Amount": {"type": "float", "regex": r"^\d{1,16}\.\d{2}$"},
    "Tax Payable": {"type": "float", "regex": r"^\d{1,16}\.\d{2}$"},
    "Tax Total": {"type": "float", "regex": r"^\d{1,16}\.\d{2}$"},

    # a lot of these can appear more than once
    "Package Kind": {"type": "string", "regex": r"^[A-Za-z0-9]{2}$", "required": True},
    "Package Number": {"type": "integer", "min": 0, "max": 99999999, "coerce": int, "required": True},
    
    "Package Marks": {"type": "string", "maxlength": 512, "required": True},
    "Prev Doc Category": {"type": "string", "regex": r"^[A-Z]{1}$", "required": True},
    "Prev Doc Type": {"type": "string", "maxlength": 3, "required": True},
    "Prev Doc Reference": {"type": "string", "maxlength": 35, "required": True},
    "Prev Doc Identifier": {"type": "integer", "max": 99999},

    # TODO: depends on other factors, such as 300 pref codes etc.
    "Doc Type": {"type": "string", "regex": r"^[A-Za-z0-9]{4}$"},
    "Doc Status": {"type": "string", "regex": r"^[A-Za-z]{2}$"},
    "Doc Reference": {"type": "string", "maxlength": 35},
    "Doc Units": {"type": "string", "regex": r"^[A-Za-z0-9]{1,4}$"},
    "Doc Quantity": {"type": "float", "regex": r"^\d{1,16}\.\d{2}$"},
    
    # TODO: might just not validate this one, or do it as a string 
    # need more details on the format ASM accepts
    # "Doc Validity Date": {"type": "datetime"},
    "Doc Validity Date": {"type": "string"},
    
    # TODO: floats have a max value 
    # strings are able to have regex applied to them, need to pick one. 
    # I'll come back to this.

    "Doc Issuing Auth": {"type": "string", "maxlength": 70},
    "Doc Reason": {"type": "string", "maxlength": 35},
    "Add Deduct Code": {"type": "string", "regex": r"^[A-Z]{2}$"},
    "Add Deduct Currency": {"type": "string", "regex": r"^[A-Z]{3}$"},
    "Add Deduct Amount": {"type": "float", "regex": r"^\d{1,16}\.\d{2}$"},
    "AI Code": {"type": "string", "regex": r"^[A-Za-z0-9]{5}$"},
    "AI Text": {"type": "string", "maxlength": 512},
    "Fiscal Ref Role": {"type": "string", "regex": r"^[A-Za-z0-9]{3}$}"},
    "Fiscal Ref Identifier": {"type": "string", "regex": r"^[A-Za-z0-9]{17}$"},
    "Supply Chain Role": {"type": "string", "regex": r"^[A-Za-z0-9]{3}$"},
    "Supply Chain Identifier": {"type": "string", "regex": r"^[A-Za-z0-9]{17}$"},
    "Container Number": {"type": "string", "regex": r"^[A-Za-z0-9]{17}$"},
    "Customer Defined Type": {"type": "string"},
    "Customer Defined Value": {"type": "string"}
}

# schema = {
#     'Line Number': {'type': 'integer'},
#     "Order Number": {"type": "string", "maxlength": 20},
#     "Product Code": {"type": "string", "maxlength": 30},
#     "SKU": {"type": "string", "maxlength": 30},
#     "Serial Number": {"type": "string", "maxlength": 20},
#     "Purchase Order": {"type": "string", "maxlength": 20},
#     "Invoice Number": {"type": "string", "maxlength": 20},

#     "Commodity": {"type": "string", "regex": r"^[A-Za-z0-9]{10}$"},

#     "Add Commodity Code": {"type": "string", "regex": r"^[A-Za-z0-9]{4}$"},
#     "Procedure": {"type": "string", "regex": r"^[A-Za-z0-9]{1,4}$"},
#     "Add Procedure Code": {"type": "string", "regex": r"^[A-Za-z0-9]{1,3}$"},
#     "Goods Description": {"type": "string", "maxlength": 512},
#     # this needs to be fixed at 8 digits
#     "CUS Code": {"type": "integer", "minlength:": 8, "maxlength": 8},
#     "Origin Country": {"type": "string", "regex": r"^[A-Za-z]{2}$"}


#     # "Order Number": (lambda x: x[:20] if len(x) > 20 else x),
#     # "Product Code": (lambda x: x[:30] if len(x) > 30 else x),
#     # "SKU": (lambda x: x[:30] if len(x) > 30 else x),
#     # "Serial Number": (lambda x: x[:20] if len(x) > 20 else x),
#     # "Purchase Order": (lambda x: x[:20] if len(x) > 20 else x),
#     # "Invoice Number": (lambda x: x[:20] if len(x) > 20 else x),
#     # "Commodity": (lambda x: x if len(x) <= 10 and x.isalnum() else None),
#     # "Add Commodity Code": (lambda x: x if len(x) <= 4 and x.isalnum() else None),
#     # "Procedure": (lambda x: x if len(x) <= 4 and x.isalnum() else None),
#     # "Add Procedure Code": (lambda x: x if len(x) <= 3 and x.isalnum() else None),
#     # "Goods Description": (lambda x: x[:512] if len(x) > 512 else x),
#     # "CUS Code": lambda x: int(x) if x.isdigit() and len(x) == 8 else None,
#     # "Origin Country": lambda x: str(x) if re.match(r"^[A-Za-z]{2}$", x) else None,
#     "Country of Preferential Origin": str,

#     "Preference": lambda x: int(x) if x.isdigit() and len(x) <= 3 else None,
#     "Quota": str,
    
#     "Quantity": lambda x: float(x) if re.match(r"^[0-9]+(\.[0-9]{1,6})?$", x) else None,
#     "Currency": lambda x: str(x) if re.match(r"^[A-Za-z]{3}$", x) else None,
#     "Unit Price": lambda x: float(x) if re.match(r"^[0-9]+(\.[0-9]{1,2})?$", x) else None,
#     "Total Value": lambda x: float(x) if re.match(r"^[0-9]+(\.[0-9]{1,2})?$", x) else None,
#     "Statistical Value": lambda x: float(x) if re.match(r"^[0-9]+(\.[0-9]{1,2})?$", x) else None,
#     "Net Mass": lambda x: float(x) if re.match(r"^[0-9]+(\.[0-9]{1,6})?$", x) else None,

#     "Gross Mass": "float:..16,6",


#     "Valuation Method": "int:1",
#     "Valuation Indicators": "int:4",
#     "Dispatch Country": "str:2",
#     "Destination Country": "str:2",
#     "Transaction Nature": "int:..2",
#     "Consignor EORI": "alphanum:..17",
#     "Consignor Name": "str:..70",
#     "Consignor Street": "str:..70",
#     "Consignor City": "str:..35",
#     "Consignor PostCode": "str:..9",
#     "Consignor Country": "alpha:2",
#     "Consignor ShortCode": "str:..20",
#     "Consignor External ID": "str:..20",
#     "Consignee EORI": "alphanum:..17",
#     "Consignee Name": "str:..70",
#     "Consignee Street": "str:70",
#     "Consignee City": "str:..35",
#     "Consignee PostCode": "str:..9",
#     "Consignee Country": "alpha:2",
#     "Consignee ShortCode": "str:..20",
#     "Consignee External ID": "str:..20",
#     "Exporter EORI": "alphanum:..17",
#     "Exporter Name": "str:..70",
#     "Exporter Street": "str:..70",
#     "Exporter City": "str:..35",
#     "Exporter PostCode": "str:..9",
#     "Exporter Country": "alpha:2",
#     "Exporter ShortCode": "str:..20",
#     "Exporter External ID": "str:..20",
#     "Seller EORI": "alphanum:..17",
#     "Seller Name": "str:..70",
#     "Seller Street": "str:..70",
#     "Seller City": "str:..35",
#     "Seller PostCode": "str:..9",
#     "Seller Country": "alpha:2",
#     "Seller ShortCode": "str:..20",
#     "Seller External ID": "str:..20",
#     "Buyer EORI": "alphanum:..17",
#     "Buyer Name": "str:..70",
#     "Buyer Street": "str:..70",
#     "Buyer City": "str:..35",
#     "Buyer PostCode": "str:..9",
#     "Buyer Country": "alpha:2",
#     "Buyer ShortCode": "str:..20",
#     "Buyer External ID": "str:..20",

#     "Tax Type": "alphanum:3",
#     "MoP": "str:1",
#     "Measurement Unit": "alphanum:..4",
#     "Tax Base Quantity": "float:..16,2",
#     "Tax Currency": "alpha:3",
#     "Tax Base Amount": "float:..16,2",
#     "Tax Payable": "float:..16,2",
#     "Tax Total": "float:..16,2",
#     "Package Kind": "alpha:2",
#     "Package Number": "int:..8",
#     "Package Marks": "str:..512",
#     "Prev Doc Category": "alpha:1",
#     "Prev Doc Type": "alphanum:3",
#     "Prev Doc Reference": "str:..35",
#     "Prev Doc Identifier": "str:..5",
#     "Doc Type": "alphanum:4",
#     "Doc Status": "alpha:2",
#     "Doc Reference": "str:..35",
#     "Doc Units": "alphanum:..4",
#     "Doc Quantity": "float:..16,6",
#     "Doc Validity Date": "datetime",
#     "Doc Issuing Auth": "str:..70",
#     "Doc Reason": "str:..35",
#     "Add Deduct Code": "alpha:2",
#     "Add Deduct Currency": "alpha:3",
#     "Add Deduct Amount": "float:..16,2",
#     "AI Code": "alphanum:5",
#     "AI Text": "str:..512",
#     "Fiscal Ref Role": "alphanum:..3",
#     "Fiscal Ref Identifier": "alphanum:..17",
#     "Supply Chain Role": "alphanum:..3",
#     "Supply Chain Identifier": "alphanum:..17",
#     "Container Number": "alphanum:..17",
#     "Customer Defined Type": "str",
#     "Customer Defined Value": "str"
# }
