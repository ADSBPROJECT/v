# import math

# Nz=15
# lat=12.81958008
# nl_lat = math.floor(2*math.pi/math.acos(1-(1-math.cos(math.pi/(2*Nz)))/(math.cos(math.pi*lat/180))**2))
# print(nl_lat)

# import math
# def convert_to_hex(value, lsb):
#     scaled_value = round(value / lsb)  
#     hex_value = hex(scaled_value)[2:].upper()
    
#     return hex_value

# time_position = float(input("enter the time of applicability for position:"))

# time_applicability_pos = convert_to_hex(time_position, 180/(2**30))
# print(time_applicability_pos)

def bin_to_hex(binary_value):
    integer_value = int(binary_value, 2)
    hex_value = hex(integer_value)[2:]
    return hex_value.upper()

binary_value=input("enter: ")
value=bin_to_hex(binary_value)
print(value)




