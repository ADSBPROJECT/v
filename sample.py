import binascii
sample_adsb_messages = ["8D06A0F558C3808BE11FDBF5BF0A","8D06A0F558C3846792B0CAEE14B4", "8D71010658B50099670A711D80D5", "8D71010658B50474909C1452E426", "8D06A0F59915D81B100462992720"]
#Convert hex to binary
def hex_to_bin(hex_string):
    return bin(int(hex_string,16))[2:].zfill(len(hex_string)*4)
def decode_adsb(hex_message):
    binary_msg=hex_to_bin(hex_message)
    df= int(binary_msg[:5],2)
    ca= int(binary_msg[5:8],2)
    icao_address=hex_message[2:8]
    type_code=int(binary_msg[32:37],2)
    print(f"\nRaw Message:{hex_message}")
    print(f"Downlink Format (DF):{df}")
    print(f"CAPABILITY (CA):{ca}")
    if ca==0:
        print("Level 1 transponder")
    elif 1<=ca<=3:
        print("Reserved")
    elif ca==4:
        print("Level 2+ transponder, with ability to set CA to 7, on-ground")
    elif ca==5:
        print("Level 2+ transponder, with ability to set CA to 7, airborne")
    elif ca==6:
        print("Level 2+ transponder, with ability to set CA to 7, either on-ground or airborne")
    elif ca==7:
        print("Signifies the Downlink Request value is 0, or the Flight Status is 2,3,4 or 5, either airborne or on the ground")
    
    
    print(f"ICAO address:{icao_address}")
    print(f"Type code:{type_code}")
    if 1<=type_code<=4:
        print("Aircraft Identification Message(Callsign)")
    elif 9<=type_code<=18:
        print("Aircraft Position Message")
    elif 19==type_code:
        print("Aircraft Velocity Message")
    else:
        print("Other ADS-B message type")
for msg in sample_adsb_messages:decode_adsb(msg)