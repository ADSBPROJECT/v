import struct
def convert_to_hex(value, lsb, length, signed=False):
    scaled_value = round(value / lsb)
    if signed:
        if length == 1:
            fmt = ">b" 
        elif length == 2:
            fmt = ">h"  
        elif length == 3:
            fmt = ">i"  
        else:
            fmt = ">i"  
    else:
        if length == 1:
            fmt = ">B"  
        elif length == 2:
            fmt = ">H"  
        elif length == 3:
            fmt = ">3B"  
            return struct.pack(fmt, (scaled_value >> 16) & 0xFF, (scaled_value >> 8) & 0xFF, scaled_value & 0xFF).hex().upper()
        else:
            fmt = ">I"  
    return struct.pack(fmt, scaled_value).hex().upper()

def bin_to_hex(value,length):
    integer_value = int(value, 2)
    hex_value = hex(integer_value)[2:]
    hex_value = hex_value.zfill(length)
    if len(hex_value) > length:
        return hex_value[:length]
    return hex_value

def change_first_bit_to_zero(value):
    int_value = int(value, 2)
    mask = (1 << (len(value) - 1)) - 1
    new_int_value = int_value & mask
    new_bin_value = bin(new_int_value)[2:]
    new_bin_value = new_bin_value.zfill(len(value))
    return new_bin_value

def final_value(value): 
    int_value = int(value, 16)
    bin_value = f"{int_value:016b}"
    if bin_value[0]=='1':
        bin_num=change_first_bit_to_zero(bin_value)
        return bin_to_hex(bin_num,4)
    else:
        return bin_to_hex(bin_value,4)

cat21=21
msg_length=35
fspec="AB9943B10120"
SAC=14
SIC=13
track_no=2004
time_position=43574.94531
lat=39.134628307043
long=-7.33791181817651
target_adr =0x06A0F5
geo_height=35950
flight_lvl=geo_height//100
mag_heading=243.98
geo_rate=-62.5
msg_amp=81
time_velocity=timeof_res_position=time_position
baro_rate=geo_rate

track_num=f"{track_no:04X}"
print(track_num)
time_applicability_pos=convert_to_hex(time_position,1/128,3)
print(time_applicability_pos)
high_res_lat=convert_to_hex(lat, 180/(2**30),4, signed=False)
high_res_long=convert_to_hex(long, 180/(2**30),4, signed=True)
print(high_res_lat)
print(high_res_long)
time_applicability_vel=convert_to_hex(time_velocity,1/128,3)
print(time_applicability_vel)
target_adress = f"{target_adr:06X}"
print(target_adress)
time_res_position=convert_to_hex(timeof_res_position,1/128,3)
print(time_res_position)
geometric_height=convert_to_hex(geo_height,6.25,2,signed=True)
print(geometric_height)
flight_level=convert_to_hex(flight_lvl,1/4,2,signed=True)
print(flight_level)
magnetic_heading = f"{int(mag_heading / (360 / (2**16))):04x}"
print(magnetic_heading)
geo_ver_rate1=convert_to_hex(geo_rate,6.25,2,signed=True)
geo_ver_rate= final_value(geo_ver_rate1)
print(geo_ver_rate)
baro_ver_rate1=convert_to_hex(baro_rate,6.25,2,signed=True)
baro_ver_rate= final_value(baro_ver_rate1)
print(baro_ver_rate)
msg_amplitude=convert_to_hex(msg_amp,1,1,signed=True)
print(msg_amplitude)

# final_packet=(cat21+msg_length+fspec+data_src_iden+track_num+time_applicability_pos+high_res_lat+
#               high_res_long+time_applicability_vel+target_adress+time_res_position+geometric_height+flight_level+
#               magnetic_heading+geo_ver_rate+baro_ver_rate+msg_amplitude)
# print("\nFINAL CAT21 PACKET(HEX, Byte by Byte):")
# print(" ".join(final_packet[i:i+2]for i in range(0, len(final_packet),2)))


final_packet = (cat21 + msg_length + fspec + data_src_iden + track_num + time_applicability_pos + 
                high_res_lat + high_res_long + time_applicability_vel + target_adress + 
                time_res_position + geometric_height + flight_level + magnetic_heading + 
                geo_ver_rate + baro_ver_rate + msg_amplitude)

# Create the formatted packet in hexadecimal format
formatted_packet = ["0x" + final_packet[i:i+2] for i in range(0, len(final_packet), 2)]

print("\nFINAL CAT21 PACKET (HEX, Byte by Byte):")
print(", ".join(formatted_packet))


