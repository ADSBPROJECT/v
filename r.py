# def parse_packet(hex_string):
#     # Remove spaces and strip the string
#     hex_string = hex_string.replace(" ", "").strip()

#     # Convert hex string to list of byte values (two characters = one byte)
#     bytes_data = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]

#     if len(bytes_data) < 44:
#         raise ValueError("Hexadecimal packet is too short for the expected fields")

#     # Start by parsing the basic fields
#     result = {
#         "Category": int(bytes_data[0], 16),
#         "Length": int(bytes_data[1] + bytes_data[2], 16),
#     }

#     # FSPEC Parsing - Checking if FSPEC extends beyond byte 9
#     fspec_end_index = 9
#     if int(bytes_data[8], 16) & 0x01:  # Check last bit of byte 9 (index 8)
#         fspec_end_index = 10  # If last bit is 1, FSPEC extends to byte 10

#     fspec = bytes_data[3:fspec_end_index]
#     result["FSPEC"] = fspec

#     # Field Extension Indicator
#     fei_index = fspec_end_index
#     field_extension_indicator = int(bytes_data[fei_index], 16)
   

#     # Define all 49 fields
#     fields = {
#         1: "Data Source Identification",
#         2: "Target Report Descriptor",
#         3: "Track Number",
#         4: "Service Identification",
#         5: "Time of Applicability for Position",
#         6: "Position in WGS-84 coordinates",
#         7: "Position in WGS-84 coordinates, high res.",
#         0:  "Field Extension Indicator",
#         8: "Time of Applicability for Velocity",
#         9: "Air Speed",
#         10: "True Air Speed",
#         11: "Target Address",
#         12: "Time of Message Reception of Position",
#         13: "Time of Message Reception of Position-High Precision",
#         14: "Time of Message Reception of Velocity",
#         0 : "Field Extension Indicator",
#         15: "Time of Message Reception of Velocity-High Precision",
#         16: "Geometric Height",
#         17: "Quality Indicators",
#         18: "MOPS Version",
#         19: "Mode 3/A Code",
#         20: "Roll Angle",
#         21: "Flight Level",
#         0 : "Field Extension Indicator",
#         22: "Magnetic Heading",
#         23: "Target Status",
#         24: "Barometric Vertical Rate",
#         25: "Geometric Vertical Rate",
#         26: "Airborne Ground Vector",
#         27: "Track Angle Rate",
#         28: "Time of Report Transmission",
#         0 :"Field Extension Indicator",
#         29: "Target Identification",
#         30: "Emitter Category",
#         31: "Met Information",
#         32: "Selected Altitude",
#         33: "Final State Selected Altitude",
#         34: "Trajectory Intent",
#         35: "Service Management",
#         0 :"Field Extension Indicator",
#         36:" Aircraft Operational Status",
#         37:"Surface Capabilities and Characteristics",
#         38:"Message Amplitude",
#         39:"Mode S MB Data",
#         40:"ACAS Resolution Advisory Report",
#         41:"Receiver ID",
#         42:"Data Ages",
#         0 :"Field Extension Indicator",
#         43:"Not Used",
#         44:"Not Used",
#         45:"Not Used",
#         46:"Not Used",
#         47:"Not Used",
#         48:"Reserved Expansion Field",
#         49:"Special Purpose Field",
#         0 :"Field Extension Indicator",



#     }

#     # Parsing based on FSPEC and Field Extension Indicator (FEI)
#     index = fei_index + 1  # Start after FEI byte
    
#     # Set count will help to track which set we are on (1 to 7)
#     set_count = 1
#     while set_count <= 7:
#         # Check if the field is present in FSPEC and set accordingly
#         if set_count == 1:
#             # Process first set
#             if int(fspec[0], 16) & 0x80:
#                 result[fields[1]] = int(bytes_data[index], 16)
#             if int(fspec[0], 16) & 0x40:
#                 result[fields[2]] = int(bytes_data[index + 1], 16)
#             if int(fspec[0], 16) & 0x20:
#                 result[fields[3]] = int(bytes_data[index + 2], 16)
#             if int(fspec[0], 16) & 0x10:
#                 result[fields[4]] = int(bytes_data[index + 3], 16)
#             if int(fspec[0], 16) & 0x08:
#                 result[fields[5]] = int(bytes_data[index + 4] + bytes_data[index + 5] + bytes_data[index + 6], 16) * (1/128)
#             if int(fspec[0], 16) & 0x04:
#                 result[fields[6]] = int(bytes_data[index + 7] + bytes_data[index + 8] + bytes_data[index + 9] + bytes_data[index + 10], 16) * (180 / (2**30))
#             if int(fspec[0], 16) & 0x02:
#                 result[fields[7]] = int(bytes_data[index + 11] + bytes_data[index + 12] + bytes_data[index + 13] + bytes_data[index + 14], 16) * (180 / (2**30))
#             index += 15
#         elif set_count == 2:
#             # Process second set
#             if field_extension_indicator == 1:
#                 if int(fspec[1], 16) & 0x80:
#                     result[fields[8]] = int(bytes_data[index], 16)
#                 if int(fspec[1], 16) & 0x40:
#                     result[fields[9]] = int(bytes_data[index + 1] + bytes_data[index + 2] + bytes_data[index + 3], 16) * (1/128)
#                 if int(fspec[1], 16) & 0x20:
#                     result[fields[10]] = int(bytes_data[index + 4] + bytes_data[index + 5] + bytes_data[index + 6], 16) * (1/128)
#                 if int(fspec[1], 16) & 0x10:
#                     result[fields[11]] = int(bytes_data[index + 7] + bytes_data[index + 8] + bytes_data[index + 9], 16) * (1/128)
#                 if int(fspec[1], 16) & 0x08:
#                     result[fields[12]] = int(bytes_data[index + 10] + bytes_data[index + 11] + bytes_data[index + 12], 16) * (1/128)
#                 if int(fspec[1], 16) & 0x04:
#                     result[fields[13]] = int(bytes_data[index + 13] + bytes_data[index + 14] + bytes_data[index + 15], 16) * (1/128)
#                 if int(fspec[1], 16) & 0x02:
#                     result[fields[14]] = int(bytes_data[index + 16] + bytes_data[index + 17] + bytes_data[index + 18], 16) * (1/128)
#                 index += 19
        
#         elif set_count == 3:
#             # Process third set
#             if field_extension_indicator == 1:
#                 if int(fspec[2], 16) & 0x80:
#                     result[fields[15]] = int(bytes_data[index], 16)
#                 if int(fspec[2], 16) & 0x40:
#                     result[fields[16]] = int(bytes_data[index + 1], 16)
#                 if int(fspec[2], 16) & 0x20:
#                     result[fields[17]] = int(bytes_data[index + 2], 16)
#                 if int(fspec[2], 16) & 0x10:
#                     result[fields[18]] = int(bytes_data[index + 3], 16)
#                 if int(fspec[2], 16) & 0x08:
#                     result[fields[19]] = int(bytes_data[index + 4], 16)
#                 if int(fspec[2], 16) & 0x04:
#                     result[fields[20]] = int(bytes_data[index + 5], 16)
#                 if int(fspec[2], 16) & 0x02:
#                     result[fields[21]] = int(bytes_data[index + 6], 16)
#                 index += 7
        
#         elif set_count == 4:
#             # Process fourth set
#             if field_extension_indicator == 1:
#                 if int(fspec[3], 16) & 0x80:
#                     result[fields[22]] = int(bytes_data[index], 16)
#                 if int(fspec[3], 16) & 0x40:
#                     result[fields[23]] = int(bytes_data[index + 1], 16)
#                 if int(fspec[3], 16) & 0x20:
#                     result[fields[24]] = int(bytes_data[index + 2], 16)
#                 if int(fspec[3], 16) & 0x10:
#                     result[fields[25]] = int(bytes_data[index + 3], 16)
#                 if int(fspec[3], 16) & 0x08:
#                     result[fields[26]] = int(bytes_data[index + 4], 16)
#                 if int(fspec[3], 16) & 0x04:
#                     result[fields[27]] = int(bytes_data[index + 5], 16)
#                 if int(fspec[3], 16) & 0x02:
#                     result[fields[28]] = int(bytes_data[index + 6], 16)
#                 index += 7
        
#         elif set_count == 5:
#             # Process fifth set
#             if field_extension_indicator == 1:
#                 if int(fspec[4], 16) & 0x80:
#                     result[fields[29]] = int(bytes_data[index], 16)
#                 if int(fspec[4], 16) & 0x40:
#                     result[fields[30]] = int(bytes_data[index + 1], 16)
#                 if int(fspec[4], 16) & 0x20:
#                     result[fields[31]] = int(bytes_data[index + 2], 16)
#                 if int(fspec[4], 16) & 0x10:
#                     result[fields[32]] = int(bytes_data[index + 3], 16)
#                 if int(fspec[4], 16) & 0x08:
#                     result[fields[33]] = int(bytes_data[index + 4], 16)
#                 if int(fspec[4], 16) & 0x04:
#                     result[fields[34]] = int(bytes_data[index + 5], 16)
#                 if int(fspec[4], 16) & 0x02:
#                     result[fields[35]] = int(bytes_data[index + 6], 16)
#                 index += 7

#         elif set_count == 6:
#             # Process sixth set
#             if field_extension_indicator == 1:
#                 if int(fspec[5], 16) & 0x80:
#                     result[fields[36]] = int(bytes_data[index], 16)
#                 if int(fspec[5], 16) & 0x40:
#                     result[fields[37]] = int(bytes_data[index + 1], 16)
#                 if int(fspec[5], 16) & 0x20:
#                     result[fields[38]] = int(bytes_data[index + 2], 16)
#                 if int(fspec[5], 16) & 0x10:
#                     result[fields[39]] = int(bytes_data[index + 3], 16)
#                 if int(fspec[5], 16) & 0x08:
#                     result[fields[40]] = int(bytes_data[index + 4], 16)
#                 if int(fspec[5], 16) & 0x04:
#                     result[fields[41]] = int(bytes_data[index + 5], 16)
#                 if int(fspec[5], 16) & 0x02:
#                     result[fields[42]] = int(bytes_data[index + 6], 16)
#                 index += 7

#         elif set_count == 7:
#             # Process seventh set
#             if field_extension_indicator == 1:
#                 if int(fspec[6], 16) & 0x80:
#                     result[fields[43]] = int(bytes_data[index], 16)
#                 if int(fspec[6], 16) & 0x40:
#                     result[fields[44]] = int(bytes_data[index + 1], 16)
#                 if int(fspec[6], 16) & 0x20:
#                     result[fields[45]] = int(bytes_data[index + 2], 16)
#                 if int(fspec[6], 16) & 0x10:
#                     result[fields[46]] = int(bytes_data[index + 3], 16)
#                 if int(fspec[6], 16) & 0x08:
#                     result[fields[47]] = int(bytes_data[index + 4], 16)
#                 if int(fspec[6], 16) & 0x04:
#                     result[fields[48]] = int(bytes_data[index + 5], 16)
#                 if int(fspec[6], 16) & 0x02:
#                     result[fields[49]] = int(bytes_data[index + 6], 16)
#                 index += 7

#         # Increment the set count for the next set
#         set_count += 1

#     return result

# # Test the parsing
# hex_packet = "150023AB9943B1012014130001551B79048EDDDD1B3EA9EE551B7906A0F5551B7917C005F075FE0000000051"
# parsed_data = parse_packet(hex_packet)

# # Print parsed fields
# for key, value in parsed_data.items():
#     print(f"{key}: {value}")


# # def hex_to_binary(hex_value):
# #     """Converts a hexadecimal value to a binary string."""
# #     return bin(int(hex_value, 16))[2:].zfill(8) 

# # fspec_hex = ['AB', '99', '43', 'B1', '01', '20']

# # fspec_binary = [hex_to_binary(byte) for byte in fspec_hex]

# # for byte in fspec_binary:
# #     print(f"Binary: {byte}")

# # fields = {
# #         1: "Data Source Identification",
# #         2: "Target Report Descriptor",
# #         3: "Track Number",
# #         4: "Service Identification",
# #         5: "Time of Applicability for Position",
# #         6: "Position in WGS-84 coordinates",
# #         7: "Position in WGS-84 coordinates, high res.",
# #         8:  "Field Extension Indicator",
# #         9: "Time of Applicability for Velocity",
# #         10: "Air Speed",
# #         11: "True Air Speed",
# #         12: "Target Address",
# #         13: "Time of Message Reception of Position",
# #         14: "Time of Message Reception of Position-High Precision",
# #         15: "Time of Message Reception of Velocity",
# #         16: "Field Extension Indicator",
# #         17: "Time of Message Reception of Velocity-High Precision",
# #         18: "Geometric Height",
# #         19: "Quality Indicators",
# #         20: "MOPS Version",
# #         21: "Mode 3/A Code",
# #         22: "Roll Angle",
# #         23: "Flight Level",
# #         24: "Field Extension Indicator",
# #         25: "Magnetic Heading",
# #         26: "Target Status",
# #         27: "Barometric Vertical Rate",
# #         28: "Geometric Vertical Rate",
# #         29: "Airborne Ground Vector",
# #         30: "Track Angle Rate",
# #         31: "Time of Report Transmission",
# #         32:"Field Extension Indicator",
# #         33: "Target Identification",
# #         34: "Emitter Category",
# #         35: "Met Information",
# #         36: "Selected Altitude",
# #         37: "Final State Selected Altitude",
# #         38: "Trajectory Intent",
# #         39: "Service Management",
# #         40:"Field Extension Indicator",
# #         41:" Aircraft Operational Status",
# #         42:"Surface Capabilities and Characteristics",
# #         43:"Message Amplitude",
# #         44:"Mode S MB Data",
# #         45:"ACAS Resolution Advisory Report",
# #         46:"Receiver ID",
# #         47:"Data Ages",
# #         48:"Not Used",
# #         49:"Not Used",
# #         50:"Not Used",
# #         51:"Not Used",
# #         52:"Not Used",
# #         53:"Reserved Expansion Field",
# #         54:"Special Purpose Field",
# #         55:"Field Extension Indicator",
# # }

# # field_indices = list(range(1, 50))

# # present_fields = []

# # bit_index = 0
# # for byte in fspec_binary:
# #     for bit in byte:
# #         if bit == '1':
# #             present_fields.append(fields[field_indices[bit_index]])
# #         bit_index += 1

# # print("\nFields Present in the FSPEC:")
# # for field in present_fields:
# #     print(field)

# def parse_packet(hex_string):
#     """Parse a single hexadecimal packet into its fields."""
#     hex_string = hex_string.replace(" ", "").strip()
    
#     # Split the hex string into bytes (2 hex digits per byte)
#     bytes_data = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]

#     # Validate packet length
#     if len(bytes_data) < 44:
#         raise ValueError("Hexadecimal packet is too short for the expected fields")

#     # Extract fields from the packet
#     result = {
#         "Category": int(bytes_data[0], 16),
#         "Length": int(bytes_data[1] + bytes_data[2], 16),  
#         "FSPEC": bytes_data[3:9],  
#         "SAC": bytes_data[9],  
#         "SIC": bytes_data[10],  
#         "Track Number": 2004,  
#         "Time of Applicability of Position": int(bytes_data[13] + bytes_data[14] + bytes_data[15], 16) * (1/128),  
#         "Latitude": int(bytes_data[16] + bytes_data[17] + bytes_data[18] + bytes_data[19], 16) * (180 / (2**30)),  
#         "Longitude": int(bytes_data[20] + bytes_data[21] + bytes_data[22] + bytes_data[23], 16) * (180 / (2**30)),  
#         "Time of Applicability of Velocity": int(bytes_data[24] + bytes_data[25] + bytes_data[26], 16) * (1/128),  
#         "Target Address": int(bytes_data[27] + bytes_data[28] + bytes_data[29], 16) * (1/128), 
#         "Time of Message Reception of position": int(bytes_data[30] + bytes_data[31] + bytes_data[32], 16) * (1/128),  
#         "Geometric Height": int(bytes_data[33] + bytes_data[34], 16) * 6.25,  
#         "Flight Level": int(bytes_data[35] + bytes_data[36], 16) * (1/4),  
#         "Magnetic Heading": int(bytes_data[37] + bytes_data[38], 16) * (360 / (2**16)),  
#         "Barometric Vertical Rate": int(bytes_data[39] + bytes_data[40], 16) * 6.25,  
#         "Geometric Vertical Rate": int(bytes_data[41] + bytes_data[42], 16) * 6.25,  
#         "Message Amplitude": int(bytes_data[43], 16) * 1  
#     }

#     return result


# def parse_multiple_packets(hex_packets):
#     """Parse a list of hexadecimal packets using a while loop, only for Category 21."""
#     results = []
#     idx = 0  # Initialize packet index
#     while idx < len(hex_packets):
#         hex_packet = hex_packets[idx]
#         try:
#             # Parse the packet
#             parsed_data = parse_packet(hex_packet)
            
#             # Only add packets that belong to Category 21
#             if parsed_data["Category"] == 21:
#                 results.append(parsed_data)
#             else:
#                 print(f"Skipping packet {idx + 1} (Category: {parsed_data['Category']})")
#         except ValueError as e:
#             print(f"Error parsing packet {hex_packet}: {e}")
#         idx += 1  # Move to the next packet
    
#     return results


# # List of multiple hex packets (example)
# hex_packets = [
#     "180023AB9943B1012014130001551B79048EDDDD1B3EA9EE551B7906A0F5551B7917C005F075FE0000000051",  # Category 21
#     "150023AB9943B1012014130001551B79048EDDDD1B3EA9EE551B7906A0F5551B7917C005F075FE0000000052",  # Category 21
#     "180023AB9943B1012014130001551B79048EDDDD1B3EA9EE551B7906A0F5551B7917C005F075FE0000000050",  # Not Category 21
#     "180023AB9943B1012014130001551B79048EDDDD1B3EA9EE551B7906A0F5551B7917C005F075FE0000000054"   # Not Category 21
# ]

# # Parse the multiple packets using a while loop
# parsed_packets = parse_multiple_packets(hex_packets)

# # Print the parsed data for each packet (only Category 21)
# idx = 0  # Initialize index for printing
# while idx < len(parsed_packets):
#     packet_data = parsed_packets[idx]
#     print(f"\nParsed Packet {idx + 1}:")
#     for key, value in packet_data.items():
#         print(f"{key}: {value}")
#     idx += 1  # Move to the next packet

# def hex_to_binary(hex_byte):
#     return bin(int(hex_byte, 16))[2:].zfill(8)

# # All 56 possible FSPEC fields in order (7 bits per FSPEC byte + 1 FX bit)
# fspec_fields = [
#     "Data Source Identification", "Target Report Descriptor", "Track Number", "Service Identification",
#     "Time of Applicability for Position", "Position in WGS-84 co-ordinates", "Position in WGS-84 co-ordinates, high res.",
#     "FX",  # Byte 1

#     "Time of Applicability for Velocity", "Air Speed", "True Air Speed", "Target Address",
#     "Time of Message Reception of Position", "Time of Message Reception of Position-High Precision",
#     "Time of Message Reception of Velocity", "FX",  # Byte 2

#     "Time of Message Reception of Velocity-High Precision", "Geometric Height", "Quality Indicators", "MOPS Version",
#     "Mode 3/A Code", "Roll Angle", "Flight Level", "FX",  # Byte 3

#     "Magnetic Heading", "Target Status", "Barometric Vertical Rate", "Geometric Vertical Rate",
#     "Airborne Ground Vector", "Track Angle Rate", "Time of Report Transmission", "FX",  # Byte 4

#     "Target Identification", "Emitter Category", "Met Information", "Selected Altitude",
#     "Final State Selected Altitude", "Trajectory Intent", "Service Management", "FX",  # Byte 5

#     "Aircraft Operational Status", "Surface Capabilities and Characteristics", "Message Amplitude", "Mode S MB Data",
#     "ACAS Resolution Advisory Report", "Receiver ID", "Data Ages", "FX",  # Byte 6

#     "Not Used", "Not Used", "Not Used", "Not Used", "Not Used", "Reserved Expansion Field", "Special Purpose Field", "FX"  # Byte 7
# ]

# def get_present_fields(fspec_hex_list):
#     binary_list = [hex_to_binary(byte) for byte in fspec_hex_list]
#     present_fields = []
#     field_index = 0

#     for byte_binary in binary_list:
#         for i in range(8):
#             if field_index >= len(fspec_fields):
#                 break
#             bit = byte_binary[i]
#             field = fspec_fields[field_index]
#             if i == 7:
#                 if bit == '0':
#                     return present_fields
#             else:
#                 if bit == '1' and "FX" not in field:
#                     present_fields.append(field)
#             field_index += 1
#     return present_fields

# def parse_packet(hex_string):
#     hex_string = hex_string.replace(" ", "").strip()
#     if len(hex_string) % 2 != 0:
#         raise ValueError("Invalid hex string (must be even length).")

#     bytes_data = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]

#     if len(bytes_data) < 44:
#         raise ValueError("Packet too short to decode essential fields.")

#     category = int(bytes_data[0], 16)
#     if category != 21:
#         print(f"Skipping packet: Category {category} is not 21.")
#         return None

#     fspec_hex = bytes_data[3:9]
#     present_fields = get_present_fields(fspec_hex)

#     result = {"Category": category, "Length": int(bytes_data[1] + bytes_data[2], 16)}
    
#     if "Data Source Identification" in present_fields:
#         result["SAC"] = int(bytes_data[9], 16)
#         result["SIC"] = int(bytes_data[10], 16)

#     if "Time of Applicability for Position" in present_fields:
#         result["Time of Applicability of Position"] = int(bytes_data[13] + bytes_data[14] + bytes_data[15], 16) * (1/128)

#     if "Position in WGS-84 co-ordinates" in present_fields:
#         result["Latitude"] = int(''.join(bytes_data[16:20]), 16) * (180 / (2**30))
#         result["Longitude"] = int(''.join(bytes_data[20:24]), 16) * (180 / (2**30))

#     if "Time of Applicability for Velocity" in present_fields:
#         result["Time of Applicability of Velocity"] = int(''.join(bytes_data[24:27]), 16) * (1/128)

#     if "Target Address" in present_fields:
#         result["Target Address"] = int(''.join(bytes_data[27:30]), 16)

#     if "Time of Message Reception of Position" in present_fields:
#         result["Time of Message Reception of position"] = int(''.join(bytes_data[30:33]), 16) * (1/128)

#     if "Geometric Height" in present_fields:
#         result["Geometric Height"] = int(''.join(bytes_data[33:35]), 16) * 6.25

#     if "Flight Level" in present_fields:
#         result["Flight Level"] = int(''.join(bytes_data[35:37]), 16) * 0.25

#     if "Magnetic Heading" in present_fields:
#         result["Magnetic Heading"] = int(''.join(bytes_data[37:39]), 16) * (360 / (2**16))

#     if "Barometric Vertical Rate" in present_fields:
#         result["Barometric Vertical Rate"] = int(''.join(bytes_data[39:41]), 16) * 6.25

#     if "Geometric Vertical Rate" in present_fields:
#         result["Geometric Vertical Rate"] = int(''.join(bytes_data[41:43]), 16) * 6.25

#     if "Message Amplitude" in present_fields:
#         result["Message Amplitude"] = int(bytes_data[43], 16)

#     return result


# # Example Hex Packet (Category 21)
# hex_packet = "150023AB9943B1012014130001551B79048EDDDD1B3EA9EE551B7906A0F5551B7917C005F075FE0000000051"

# decoded = parse_packet(hex_packet)

# if decoded:
#     print("\n✅ Decoded Packet:")
#     for key, value in decoded.items():
#         print(f"{key}: {value}")
# def hex_to_binary(hex_value):
#     return bin(int(hex_value, 16))[2:].zfill(8)

# # Mapping of field numbers to names (not all used here, but can be extended)
# field_names = {
#     1: "Data Source Identification",
#     3: "Track Number",
#     5: "Time of Applicability for Position",
#     6: "Position in WGS-84 coordinates",
#     8: "Time of Applicability for Velocity",
#     11: "Target Address",
#     12: "Time of Message Reception of Position",
#     16: "Geometric Height",
#     21: "Flight Level",
#     22: "Magnetic Heading",
#     24: "Barometric Vertical Rate",
#     25: "Geometric Vertical Rate",
#     38: "Message Amplitude"
# }

# def parse_packet(hex_string):
#     hex_string = hex_string.replace(" ", "").strip()

#     if len(hex_string) % 2 != 0:
#         raise ValueError("Hex string must have even length")

#     # Convert hex string to a list of bytes
#     bytes_data = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]

#     category = int(bytes_data[0], 16)
#     if category != 21:
#         print("Not a Category 21 packet")
#         return None

#     length = int(bytes_data[1] + bytes_data[2], 16)

#     # Read FSPEC bytes
#     fspec_fields = []
#     fspec_index = 3
#     field_index = 1

#     while True:
#         byte = hex_to_binary(bytes_data[fspec_index])
#         fspec_index += 1

#         for i in range(7):  # only 7 field bits
#             if field_index in field_names:
#                 if byte[i] == '1':
#                     fspec_fields.append(field_index)
#             field_index += 1

#         if byte[7] == '0':  # no more FSPEC bytes
#             break

#     # Start decoding after FSPEC
#     current_index = fspec_index
#     result = {
#         "Category": category,
#         "Length": length,
#         "FSPEC": [bytes_data[i] for i in range(fspec_index - len(fspec_fields), fspec_index)],
#         "Fields Present": [field_names[f] for f in fspec_fields]
#     }

#     for field in fspec_fields:
#         try:
#             if field == 1:  # Data Source Identification (SAC, SIC)
#                 result["SAC"] = int(bytes_data[current_index], 16)
#                 result["SIC"] = int(bytes_data[current_index+1], 16)
#                 current_index += 2

#             elif field == 3:  # Track Number
#                 result["Track Number"] = int(bytes_data[current_index] + bytes_data[current_index+1], 16)
#                 current_index += 2

#             elif field == 5:  # Time of Applicability of Position
#                 val = int("".join(bytes_data[current_index:current_index+3]), 16)
#                 result["Time of Applicability of Position"] = round(val * (1/128), 6)
#                 current_index += 3

#             elif field == 6:  # Position in WGS-84 coordinates
#                 lat = int("".join(bytes_data[current_index:current_index+4]), 16)
#                 current_index += 4
#                 lon = int("".join(bytes_data[current_index:current_index+4]), 16)
#                 current_index += 4
#                 result["Latitude"] = round(lat * (180 / (2**30)), 6)
#                 result["Longitude"] = round(lon * (180 / (2**30)), 6)

#             elif field == 8:  # Time of Applicability of Velocity
#                 val = int("".join(bytes_data[current_index:current_index+3]), 16)
#                 result["Time of Applicability of Velocity"] = round(val * (1/128), 6)
#                 current_index += 3

#             elif field == 11:  # Target Address
#                 val = int("".join(bytes_data[current_index:current_index+3]), 16)
#                 result["Target Address"] = val
#                 current_index += 3

#             elif field == 12:  # Time of Message Reception of Position
#                 val = int("".join(bytes_data[current_index:current_index+3]), 16)
#                 result["Time of Message Reception"] = round(val * (1/128), 6)
#                 current_index += 3

#             elif field == 16:  # Geometric Height
#                 result["Geometric Height"] = int("".join(bytes_data[current_index:current_index+2]), 16) * 6.25
#                 current_index += 2

#             elif field == 21:  # Flight Level
#                 result["Flight Level"] = int("".join(bytes_data[current_index:current_index+2]), 16) * 0.25
#                 current_index += 2

#             elif field == 22:  # Magnetic Heading
#                 result["Magnetic Heading"] = int("".join(bytes_data[current_index:current_index+2]), 16) * (360 / 65536)
#                 current_index += 2

#             elif field == 24:  # Barometric Vertical Rate
#                 result["Barometric Vertical Rate"] = int("".join(bytes_data[current_index:current_index+2]), 16) * 6.25
#                 current_index += 2

#             elif field == 25:  # Geometric Vertical Rate
#                 result["Geometric Vertical Rate"] = int("".join(bytes_data[current_index:current_index+2]), 16) * 6.25
#                 current_index += 2

#             elif field == 38:  # Message Amplitude
#                 result["Message Amplitude"] = int(bytes_data[current_index], 16)
#                 current_index += 1

#         except Exception as e:
#             result[field_names[field]] = f"Error: {e}"

#     return result

# # 🧪 Sample Packet
# hex_packet = "150023AB9943B1012014130001551B79048EDDDD1B3EA9EE551B7906A0F5551B7917C005F075FE0000000051"

# decoded = parse_packet(hex_packet)

# if decoded:
#     print("\n=== Decoded Packet ===")
#     for k, v in decoded.items():
#         print(f"{k}: {v}")

from datetime import timedelta

def hex_to_binary(hex_value):
    return bin(int(hex_value, 16))[2:].zfill(8)

def twos_complement(val, bits):
    if val & (1 << (bits - 1)):
        val -= 1 << bits
    return val

def seconds_to_utc(seconds):
    return str(timedelta(seconds=seconds))

def parse_cat21_packet(hex_packet):
    hex_packet = hex_packet.replace(" ", "")
    bytes_data = [hex_packet[i:i+2] for i in range(0, len(hex_packet), 2)]

    category = int(bytes_data[0], 16)
    length = int("".join(bytes_data[1:3]), 16)

    fspec_bits = []
    fspec_index = 3
    while True:
        byte = hex_to_binary(bytes_data[fspec_index])
        fspec_bits.extend(byte[:7])
        cont = byte[7]
        fspec_index += 1
        if cont == '0':
            break

    field_ptr = fspec_index
    result = {
        "Category": category,
        "Length": length,
        "FSPEC Bytes": fspec_index - 3,
        "Fields Present": []
    }

    def read_bytes(n):
        nonlocal field_ptr
        val = bytes_data[field_ptr:field_ptr + n]
        field_ptr += n
        return val

    def to_uint(hexlist):
        return int("".join(hexlist), 16)

    def to_int(hexlist, bits):
        return twos_complement(int("".join(hexlist), 16), bits)

    for i, bit in enumerate(fspec_bits):
        if bit == '1':
            field_id = i + 1
            result["Fields Present"].append(f"Field {field_id}")

            if field_id == 1:
                # Keep SAC and SIC as raw decimal values
                sac = int(read_bytes(1)[0], 16)
                sic = int(read_bytes(1)[0], 16)
                result["SAC"] = sac
                result["SIC"] = sic

            
            elif field_id == 2:
                result["Target Report Descriptor"] = to_uint(read_bytes(1))    

            elif field_id == 3:
                result["Track Number"] = to_uint(read_bytes(2))

            elif field_id == 4:
                result["Service Identification "] = to_uint(read_bytes(1))     

            elif field_id == 5:
               seconds = to_uint(read_bytes(3)) / 128
               result["Time of Applicability of position"] = seconds


            elif field_id == 6 or field_id == 7:
                lat = to_int(read_bytes(4), 32) * (180 / (2 ** 31 ))
                lon = to_int(read_bytes(4), 32) * (180 / (2 ** 31))
                result["Latitude"] = round(lat, 6)
                result["Longitude"] = round(lon, 6)

            elif field_id == 8:
                seconds = to_uint(read_bytes(3)) / 128
                result["Time of Applicability of Velocity"] = seconds
            
            elif field_id == 9:
                result["Air Speed "] = to_uint(read_bytes(2)) 

            elif field_id == 10:
                result["True Air Speed "] = to_uint(read_bytes(2))     

            elif field_id == 11:
                val = to_uint(read_bytes(3))
                result["Target Address"] = f"{val} (hex: {hex(val)[2:].upper()})"

            elif field_id == 12:
               seconds = to_uint(read_bytes(3)) / 128
               result["Time of message Reception(position)"] = seconds

            elif field_id == 13:
                result["TTime of Message Reception of Position-High"] = to_uint(read_bytes(4)) 

            elif field_id == 14:
                result["Time of Message Reception of Velocity "] = to_uint(read_bytes(3)) 

            elif field_id == 15:
                result["Time of Message Reception of Velocity-High "] = to_uint(read_bytes(4))            

            elif field_id == 16:
                val = to_int(read_bytes(2), 16)
                result["Geometric Height (ft)"] = round(val * 6.25, 2)

            elif field_id == 17:
                result["Quality Indicators "] = to_uint(read_bytes(1)) 

            elif field_id == 18:
                result["MOPS Version "] = to_uint(read_bytes(1)) 

            elif field_id == 19:
                result["Mode 3/A Code "] = to_uint(read_bytes(2)) 

            elif field_id == 20:
                result["Roll Angle "] = to_uint(read_bytes(2))                 

            elif field_id == 21:
                val = to_uint(read_bytes(2)) * 0.25
                result["Flight Level"] = f"FL{int(val)} ({int(val * 100)} ft)"

            elif field_id == 22:
                val = to_uint(read_bytes(2)) * (360 / 65536)
                result["Magnetic Heading"] = round(val, 3)
            
            elif field_id == 23:
                result["Target Status "] = to_uint(read_bytes(1))     

            elif field_id == 24:
                val = to_int(read_bytes(2), 16) * 6.25
                result["Barometric Vertical Rate (ft/min)"] = val

            elif field_id == 25:
                val = to_int(read_bytes(2), 16) * 6.25
                result["Geometric Vertical Rate (ft/min)"] = val

            elif field_id == 26:
                result["Airborne Ground Vector "] = to_uint(read_bytes(4)) 

            elif field_id == 27:
                result["Track Angle Rate "] = to_uint(read_bytes(2)) 

            elif field_id == 28:
                result["Time of Report Transmission"] = to_uint(read_bytes(3)) 

            elif field_id == 29:
                result["Target Identification "] = to_uint(read_bytes(6)) 

            elif field_id == 30:
                result["Emitter Category "] = to_uint(read_bytes(1)) 

            elif field_id == 31:
                result["Met Information "] = to_uint(read_bytes(1)) 

            elif field_id == 32:
                result["Selected Altitude "] = to_uint(read_bytes(2)) 

            elif field_id == 33:
                result["Final State Selected Altitude "] = to_uint(read_bytes(2)) 

            elif field_id == 34:
                result["Trajectory Intent "] = to_uint(read_bytes(1)) 

            elif field_id == 35:
                result["Service Management "] = to_uint(read_bytes(1)) 

            elif field_id == 36:
                result["Aircraft Operational Status "] = to_uint(read_bytes(1)) 

            elif field_id == 37:
                result["Surface Capabilities and Characteristics "] = to_uint(read_bytes(1))                                                 

            elif field_id == 38:
                result["Message Amplitude"] = int(read_bytes(1)[0], 16)

            elif field_id == 39:
                result["Mode S MB Data "] = to_uint(read_bytes(1+n*8)) 

            elif field_id == 40:
                result["ACAS Resolution Advisory Report "] = to_uint(read_bytes(6)) 

            elif field_id == 41:
                result["Receiver ID "] = to_uint(read_bytes(1)) 

            elif field_id == 43:
                result["Data Ages "] = to_uint(read_bytes(1)) 

            elif field_id == 44:
                result["Not Used "] = to_uint(read_bytes(0)) 

            elif field_id == 45:
                result["Not Used "] = to_uint(read_bytes(0)) 

            elif field_id == 46:
                result["Not Used "] = to_uint(read_bytes(0)) 
            elif field_id == 47:
                result["Not Used "] = to_uint(read_bytes(0)) 

            elif field_id == 48:
                result["Reserved Expansion Field "] = to_uint(read_bytes(1)) 

            elif field_id == 49:
                result["Special Purpose Field "] = to_uint(read_bytes(1))                                         

    print("\n=== Decoded CAT021 Packet ===")
    for k, v in result.items():
        print(f"{k}: {v}")

    return result


#  Example usage
hex_packet = "150023AB9943B1012014130001551B79048EDDDD1B3EA9EE551B7906A0F5551B7917C005F075FE0000000051"
parse_cat21_packet(hex_packet)
          

