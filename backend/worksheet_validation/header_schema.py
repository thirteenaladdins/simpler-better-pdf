headers = {
    'Invoice Number': 'str:..20',
    'Purchase Order Number': 'str:..20',
    'Shipment Date': 'datetime',
    'Shipment Master': 'str:..25',
    'Shipment House': 'str:..25',
    'Transport ID': 'str:..27',
    'Supplier': 'str:..20',
    'Delivery Terms': 'alpha:3',
    'Delivery Terms UN/LOCODE *': 'alpha:5',
    'Delivery Terms Location*': 'str:2 + alphanum:..35',
    'Warehouse ID': 'str:1 + alphanum:..35',
    'Warehouse Site': 'alphanum:..20', 
    'Net Mass': 'float:..16,6',
    'Ignore Product Catalogue': 'bool'
}

headers_schema = {
    'Invoice Number': str,
    'Purchase Order Number': str,
    # 'Shipment Date': lambda x: datetime.strptime(x, '%Y-%m-%d').date(),
    'Shipment Date': str,
    'Shipment Master': str,
    'Shipment House': str,
    'Transport ID': str,
    'Supplier': str,
    'Delivery Terms': str,
    'Delivery Terms UN/LOCODE *': str,
    'Delivery Terms Location*': str,
    'Warehouse ID': str,
    'Warehouse Site': str, 
    'Net Mass': float,
    'Ignore Product Catalogue': bool
}