def parse_packet(hex_string):
    
    hex_string = hex_string.replace(" ", "").strip()

    bytes_data = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]

    if len(bytes_data) < 44:
        raise ValueError("Hexadecimal packet is too short for the expected fields")

    result = {
        "Category": int(bytes_data[0], 16),
        "Length": int(bytes_data[1] + bytes_data[2], 16),  
        "FSPEC": bytes_data[3:9],  
        "SAC": bytes_data[9],  
        "SIC": bytes_data[10],  
        "Track Number": 2004,  
        "Time of Applicability of Position": int(bytes_data[13] + bytes_data[14] + bytes_data[15], 16) * (1/128),  
        "Latitude": int(bytes_data[16] + bytes_data[17] + bytes_data[18] + bytes_data[19], 16) * (180 / (2**30)),  
        "Longitude": int(bytes_data[20] + bytes_data[21] + bytes_data[22] + bytes_data[23], 16) * (180 / (2**30)),  
        "Time of Applicability of Velocity": int(bytes_data[24] + bytes_data[25] + bytes_data[26], 16) * (1/128),  
        "Target Address": int(bytes_data[27] + bytes_data[28] + bytes_data[29], 16) * (1/128), 
        "Time of Message Reception of position": int(bytes_data[30] + bytes_data[31] + bytes_data[32], 16) * (1/128),  
        "Geometric Height": int(bytes_data[33] + bytes_data[34], 16) * 6.25,  
        "Flight Level": int(bytes_data[35] + bytes_data[36], 16) * (1/4),  
        "Magnetic Heading": int(bytes_data[37] + bytes_data[38], 16) * (360 / (2**16)),  
        "Barometric Vertical Rate": int(bytes_data[39] + bytes_data[40], 16) * 6.25,  
        "Geometric Vertical Rate": int(bytes_data[41] + bytes_data[42], 16) * 6.25,  
        "Message Amplitude": int(bytes_data[43], 16) * 1  
    }

    return result

hex_packet = "150023AB9943B1012014130001551B79048EDDDD1B3EA9EE551B7906A0F5551B7917C005F075FE0000000051"

try:
    parsed_data = parse_packet(hex_packet)
    

    for key, value in parsed_data.items():
        print(f"{key}: {value}")

except ValueError as e:
    print(f"Error: {e}")



