import struct
packet=b''
# packet=0
cat=21
cat_byte=cat.to_bytes(1,byteorder='big',signed=False)
print("cat_byte: ",cat_byte)
fspec=0xab9943b10120
fspec_bytes=fspec.to_bytes(6,byteorder='big',signed=False)
print(fspec_bytes)
track_num=2004
track_bytes=track_num.to_bytes(2,byteorder='big',signed=False)
print("track_bytes :",track_bytes)
sac=0x14
sic=0x13
ds_iden_bytes=(sac.to_bytes(1,byteorder='big',signed=False))+(sic.to_bytes(1,byteorder='big',signed=False))
time_appli_position=43574.94531
time_appli_position_bytes=round(time_appli_position/(1/128)).to_bytes(3,byteorder='big',signed=False)
print("time_appli_position_bytes:",time_appli_position_bytes)
lat=39.134628307043
lon=-7.33791181817651
pos_coordi_high_res_bytes=(round(lat/(180/2**30)).to_bytes(4,byteorder='big',signed=True))+(round(lon/(180/2**30)).to_bytes(4,byteorder='big',signed=True))
print("pos_coordi_high_res_bytes: ",pos_coordi_high_res_bytes)
time_appli_velocity=43574.94531
time_appli_velocity_byte=round(time_appli_velocity/(1/128)).to_bytes(3,byteorder='big',signed=False)
print("time_appli_velocity_byte :",time_appli_velocity_byte)
target_adr=0x40797a
target_adr_bytes=target_adr.to_bytes(3,byteorder='big',signed=False)
print("target_adr:",target_adr_bytes)
time_receptn_position=43574.94531
time_receptn_position_bytes=round(time_receptn_position/(1/128)).to_bytes(3,byteorder='big',signed=False)
print("time_receptn_position_bytes :",time_receptn_position_bytes)
geo_height=35950
geo_height_bytes=round(geo_height/6.25).to_bytes(2,byteorder='big',signed=True)
print("geo_height_bytes :",geo_height_bytes)
flight_lvl=int(geo_height/100)
flight_lvl_bytes=round(flight_lvl/(1/4)).to_bytes(2,byteorder='big',signed=True)
print("flight_lvl_bytes :",flight_lvl_bytes)
mag_heading=243.98
mag_heading_bytes=round(mag_heading/(360/2**16)).to_bytes(2,byteorder='big',signed=False)
print("mag_heading_bytes :",mag_heading_bytes)
baro_rate=-62.5
baro_rate_bytes=((round(baro_rate/6.25))&0x7fff).to_bytes(2,byteorder='big',signed=True)
print("baro_rate_bytes :",baro_rate_bytes)
geo_rate=-62.5
geo_rate_bytes=((round(geo_rate/6.25))&0x7fff).to_bytes(2,byteorder='big',signed=True)
print("geo_rate_bytes :",geo_rate_bytes)
msg_ampli=81
msg_ampli_bytes=msg_ampli.to_bytes(1,byteorder='big',signed=False)
print("msg_ampli_bytes :",msg_ampli_bytes)

packet=ds_iden_bytes+track_bytes+time_appli_position_bytes+pos_coordi_high_res_bytes+time_appli_velocity_byte+target_adr_bytes+time_receptn_position_bytes+geo_height_bytes+flight_lvl_bytes+mag_heading_bytes+baro_rate_bytes+geo_rate_bytes+msg_ampli_bytes
print(packet)
print(packet.hex())
#  print(' '.join(f'\\x{byte:02x}' for byte in packet))
print(len(packet))

len_byte=len(packet).to_bytes(2,byteorder='big',signed=False)
print(len_byte)
# print(len_byte.hex())

packet=cat_byte+len_byte+fspec_bytes+ds_iden_bytes+track_bytes+time_appli_position_bytes+pos_coordi_high_res_bytes+time_appli_velocity_byte+target_adr_bytes+time_receptn_position_bytes+geo_height_bytes+flight_lvl_bytes+mag_heading_bytes+baro_rate_bytes+geo_rate_bytes+msg_ampli_bytes
print(packet)
# print(packet.hex())
# print(' '.join(f'\\x{byte:02x}' for byte in packet))
# a=len(target_adr)
# print(a)