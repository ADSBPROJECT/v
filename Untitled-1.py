def hex_to_bin(hex_value):
    """Convert hex to binary string, ensuring 8-bit representation for each hex byte"""
    return bin(int(hex_value, 16))[2:].zfill(8 * len(hex_value))

def decode_fspec_and_extract(hex_packet):
    """Decode FSPEC and extract values from the hex packet based on LSBs"""
    # FSPEC is the first byte of the packet (2 hex characters, 8 bits)
    fspec_hex = hex_packet[:2]
    binary_fspec = hex_to_bin(fspec_hex)
    
    # List of items corresponding to FSPEC bits
    items = [
        "Time of Message Reception for Position",
        "Time of Message Reception of Position–High Precision",
        "Time of Message Reception for Velocity",
        "Time of Applicability for Position",
        "Geometric Height",
        "Flight level",
        "Magnetic Heading",
        "Barometric Vertical Rate",
        "Geometric Vertical Rate",
        "Message Amplitude"
    ]
    
    # Define the LSB values for each item
    lsb_values = {
        "Time of Message Reception for Position": 1 / 128,
        "Time of Message Reception of Position–High Precision": 180 / (2 ** 30),
        "Time of Message Reception for Velocity": 1 / 128,
        "Time of Applicability for Position": 1 / 128,
        "Geometric Height": 6.25,
        "Flight level": 1 / 4,
        "Magnetic Heading": 1,  # Assuming 1 degree per unit (needs clarification)
        "Barometric Vertical Rate": 1,  # Needs clarification
        "Geometric Vertical Rate": 1,  # Needs clarification
        "Message Amplitude": 1  # Needs clarification
    }
    
    # Print FSPEC in binary
    print(f"Hexadecimal FSPEC: {fspec_hex}")
    print(f"Binary FSPEC: {binary_fspec}")
    
    # Decode each field based on binary FSPEC
    decoded_values = []
    for i, field in enumerate(items):
        # Check if the field is present (bit is 1)
        if binary_fspec[i] == '1':
            # Here, you would extract the corresponding value from the packet
            # This is where you would extract the specific bits based on the protocol
            # For now, we'll assume a dummy value of 100 for illustration purposes.
            field_value = 100  # This is a placeholder. Replace it with actual extraction logic.

            # Apply the LSB value
            actual_value = field_value * lsb_values[field]
            
            decoded_values.append(f"{field}: {actual_value}")
        else:
            decoded_values.append(f"{field}: Not present")
    
    # Output the decoded results
    print("\nDecoded FSPEC items with values:")
    for value in decoded_values:
        print(value)

# Example usage: Replace this with your actual hex packet
hex_packet = "150023AB9943B1012014130001551B79048EDDDD1B3EA9EE551B7906A0F5551B7917C005F074920000000051"
decode_fspec_and_extract(hex_packet)
