def parse_packet(hex_string):
    hex_string = hex_string.replace(" ", "").strip()
    bytes_data = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
    if len(bytes_data) < 44:
        raise ValueError("Hexadecimal packet is too short for the expected fields")

    result = {
        "Category": bytes_data[0],
        "Length": int(bytes_data[1] + bytes_data[2], 16), 
        "FSPEC": bytes_data[3:9], 
        "SAC": bytes_data[9], 
        "SIC": bytes_data[10], 
        "Track No": int(bytes_data[11] + bytes_data[12], 16),  
        "Time of Applicability of Position": bytes_data[13:16],  
        "Latitude": bytes_data[16:20],  
        "Longitude": bytes_data[20:24],  
        "Time of Applicability of Velocity": bytes_data[24:27],  
        "Target Address": bytes_data[27:30],  
        "Time of Message Reception": bytes_data[30:33], 
        "Geometric Height": int(bytes_data[33] + bytes_data[34], 16), 
        "Flight Level": int(bytes_data[35] + bytes_data[36], 16),  
        "Magnetic Heading": int(bytes_data[37] + bytes_data[38], 16), 
        "Barometric Vertical Rate": int(bytes_data[39] + bytes_data[40], 16), 
        "Geometric Vertical Rate": int(bytes_data[41] + bytes_data[42], 16),  
        "Message Amplitude": int(bytes_data[43], 16)  
    }

    return result

hex_packet = "150023AB9943B1012014130001551B79048EDDDD1B3EA9EE551B7906A0F5551B7917C005F075FE0000000051"

try:
    parsed_data = parse_packet(hex_packet)
    
    for key, value in parsed_data.items():
        print(f"{key}: {value}")

except ValueError as e:
    print(f"Error: {e}")
