import struct

packet = b''

# Data items that should be checked (you can adjust this list as per your protocol)
data_items = {
    'ds_iden': True,
    'target_rep_descriptor': False,
    'track_num': True,
    'service_identification': False,
    'time_appli_position': True,
    'pos_coordi': False,
    'pos_coordi_high_res': False,
    'fx1': True,
    'time_appli_velocity': True,
    'air_speed': False,
    'true_air_speed': False,
    'target_adr': True,
    'time_receptn_position': True,
    'time_receptn_position_high_res': True,
    'time_receptn_velocity': True,
    'fx2': True,
    'time_receptn_velocity_high_res': False,
    'geo_height': True,
    'quality_indicatr': False,
    'mops_version': False,
    'mod_3a_code': False,
    'roll_angle': False,
    'flight_lvl': True,
    'fx3': True,
    'mag_heading': True,
    'target_status': False,
    'baro_rate': True,
    'geo_rate': True,
    'airborne_grnd_vectr': False,
    'track_angle_rate': False,
    'time_report_tx': False,
    'fx4': True,
    'target_iden': False,
    'emittr_cat': False,
    'met_info': False,
    'selectd_alti': False,
    'final_state_alti': False,
    'trajectry_intent': False,
    'service_managemnt': False,
    'fx5': True,
    'aircraft_oper_stat': False,
    'surface_cap_and_char': False,
    'msg_ampli': True,
    'mode_smb_data': False,
    'ACAS_resol_advisry_rep': False,
    'recievr_id': False,
    'data_ages': False,
    'fx6': False
}

# Function to create the raw binary FSPEC
def create_raw_binary_fspec(data_items):
    fspec = []
    byte = 0
    bit_count = 0

    for item, present in data_items.items():
        if present:
            byte |= (1 << (6 - bit_count))  # Set the appropriate bit to 1
        bit_count += 1
        
        # After processing 7 bits, add the byte to the list and reset
        if bit_count == 7:
            fspec.append(byte)
            byte = 0  # Reset byte
            bit_count = 0

    # If there are remaining bits, add the final byte
    if bit_count > 0:
        fspec.append(byte)

    # Now, apply continuation flag (MSB = 1 for all bytes except the last one)
    for i in range(len(fspec) - 1):
        fspec[i] |= 0x80  # Set the MSB (most significant bit) for continuation

    return bytes(fspec)

# Create the raw binary FSPEC
raw_binary_fspec = create_raw_binary_fspec(data_items)

# Print the raw binary FSPEC in hexadecimal and its byte representation
print("Raw Binary FSPEC (bytes):", raw_binary_fspec)
print("Hexadecimal Representation:", raw_binary_fspec.hex())
print("Binary Representation (for visualization):", ' '.join(format(byte, '08b') for byte in raw_binary_fspec))


# Constructing the other packet elements (same as in your original code)
cat = 21
cat_byte = cat.to_bytes(1, byteorder='big', signed=False)
track_num = 2004
track_bytes = track_num.to_bytes(2, byteorder='big', signed=False)
sac = 0x14
sic = 0x13
ds_iden_bytes = (sac.to_bytes(1, byteorder='big', signed=False)) + (sic.to_bytes(1, byteorder='big', signed=False))
time_appli_position = 43574.94531
time_appli_position_bytes = round(time_appli_position / (1 / 128)).to_bytes(3, byteorder='big', signed=False)
lat = 39.134628307043
lat_bytes = round(lat / (180 / 2**30)).to_bytes(4, byteorder='big', signed=True)
lon = -7.33791181817651
lon_bytes = round(lon / (180 / 2**30)).to_bytes(4, byteorder='big', signed=True)
time_appli_velocity = 43574.94531
time_appli_velocity_byte = round(time_appli_velocity / (1 / 128)).to_bytes(3, byteorder='big', signed=False)
target_adr = 0x40797a
target_adr_bytes = target_adr.to_bytes(3, byteorder='big', signed=False)
time_receptn_position = 43574.94531
time_receptn_position_bytes = round(time_receptn_position / (1 / 128)).to_bytes(3, byteorder='big', signed=False)
geo_height = 35950
geo_height_bytes = round(geo_height / 6.25).to_bytes(2, byteorder='big', signed=True)
flight_lvl = int(geo_height / 100)
flight_lvl_bytes = round(flight_lvl / (1 / 4)).to_bytes(2, byteorder='big', signed=True)
mag_heading = 243.98
mag_heading_bytes = round(mag_heading / (360 / 2**16)).to_bytes(2, byteorder='big', signed=False)
baro_rate = -62.5
baro_rate_bytes = ((round(baro_rate / 6.25)) & 0x7fff).to_bytes(2, byteorder='big', signed=True)
geo_rate = -62.5
geo_rate_bytes = ((round(geo_rate / 6.25)) & 0x7fff).to_bytes(2, byteorder='big', signed=True)
msg_ampli = 81
msg_ampli_bytes = msg_ampli.to_bytes(1, byteorder='big', signed=False)

# Construct the packet without FSPEC first
packet = ds_iden_bytes + track_bytes + time_appli_position_bytes + lat_bytes + lon_bytes + time_appli_velocity_byte + target_adr_bytes + time_receptn_position_bytes + geo_height_bytes + flight_lvl_bytes + mag_heading_bytes + baro_rate_bytes + geo_rate_bytes + msg_ampli_bytes
print("Packet without FSPEC:", packet)
print(packet.hex())

# FSPEC (Field Specification) - Add FSPEC bytes based on data items
fspec_bytes = create_raw_binary_fspec(data_items)
print("FSPEC bytes:", fspec_bytes)
print(fspec_bytes.hex())

# Calculate the length of the packet and add it (2-byte length prefix)
len_byte = len(packet).to_bytes(2, byteorder='big', signed=False)
print("Length byte:", len_byte)
print(len_byte.hex())

# Final packet: Insert FSPEC after the length bytes
packet = cat_byte + len_byte + fspec_bytes + packet
print("Final packet with FSPEC:", packet)
print(packet.hex())

