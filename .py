def convert_fspec_items(fspec):
    """Convert each item in FSPEC from hex to decimal."""

fspec_items = []
 for i in range(0, len(fspec), 2):  # Each FSPEC item is 2 characters (1 byte)
        hex_item = fspec[i:i+2]
        decimal_value = hex_to_decimal(hex_item)
        fspec_items.append(decimal_value)
    return fspec_items


def print_fspec_items(fspec_items):
    """Print the decimal values of FSPEC items with names."""
    fspec_names = [
        'Data Source Information',
        'Track Number',
        'Position in WGS-84 Coordinates (High Precision)',
        'Time of Application Velocity',
        'Target Address',
        'Time of Message Reception of Position',
        'Geometric Height',
        'Flight Level',
        'Magnetic Heading',
        'Barometric Vertical Rate',
        'Geometric Vertical Rate',
        'Message Amplitude'
    ]

def process_hex_packet(hex_packet):
    """Process the hex packet and display results."""

    category = hex_packet[:2]  # Assuming category is the first 2 bytes
    length = int(hex_packet[2:4], 16)  # Assuming length is the next 2 bytes
    print(f'Category: {category} Length: {length}')
    
    fspec = extract_fspec(hex_packet)
    print(f'FSPEC: {fspec}')

    fspec_items = convert_fspec_items(fspec)

    print('FSPEC Items:')
    print_fspec_items(fspec_items)
    