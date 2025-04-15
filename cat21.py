def parse_adsb_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    cat_type = packet[0]  
    length = int.from_bytes(packet[1:3], byteorder='big')
    fspec = packet[3:9] 

    return {
        "CAT Type ": cat_type,  
        "Length": length,
        "FSPEC ": fspec.hex()  
    }
hex_packet = input("Enter the ADS-B hex packet: ")
parsed_packet = parse_adsb_packet(hex_packet)
if parsed_packet:
    print("\nParsed ADS-B Packet Information:")
    for key, value in parsed_packet.items():
        print(f"{key}: {value}")
else:
    print("Invalid packet or parsing failed.")
#for data source identification
