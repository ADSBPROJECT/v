import math

# Function to calculate position based on the j index and CPR encoding
def calculate_position(j, Nz, LATcpr_even, LATcpr_odd):
    # Calculate the latitude and longitude based on the j index and the CPR encoding
    LAT_even = (360 / (4 * Nz)) * ((j % 60) + LATcpr_even)
    LAT_odd = (360 / (4 * Nz - 1)) * ((j % 59) + LATcpr_odd)
    
    # Calculate NL_lat based on even and odd latitudes
    NL_lat_even = math.floor(2 * math.pi / (math.acos(1 - (1 - math.cos(math.pi / (2 * Nz))) / math.cos(math.pi / 180 * LAT_even) ** 2)))
    NL_lat_odd = math.floor(2 * math.pi / (math.acos(1 - (1 - math.cos(math.pi / (2 * Nz))) / math.cos(math.pi / 180 * LAT_odd) ** 2)))

    return LAT_even, LAT_odd, NL_lat_even, NL_lat_odd
# def calculate_vertical_rate(Vr):
#     VS_0=64(Vr-1)  # Svr=0
#     VS_1=-64(Vr-1)  # Svr=1
# Function to decode the ADS-B message
def decode_adsb(hex_message):
    binary_msg = bin(int(hex_message, 16))[2:].zfill(len(hex_message) * 4)
    type_code = int(binary_msg[32:37], 2)  # Extract type code from the message
    
    # If it's a position message (Type code between 9 and 18)
    
    
    if 9 <= type_code <= 18:
        print(f"\nRaw Message: {hex_message}")
        print(f"Type code: {type_code}")
        F = int(binary_msg[53], 2)  # Flag for even or odd format
        
        Alt=binary_msg[40:52]
        bit_value=Alt[7]
        N=int((Alt[:7]+Alt[8:12]),2)
        print(f"N:{N}")
        h=25*N-1000
        print(f"ALTITUDE:{h} ft")

        # Initialize LATcpr values
        # LATcpr_even = 0
        # LONcpr_even = 0
        # LATcpr_odd = 0
        # LONcpr_odd = 0

        # Extract CPR values based on format
        if F == 0:  # Even format
            Ncpr_lat1 = int(binary_msg[54:71], 2)
            LATcpr_even = Ncpr_lat1 / 2 ** 17
            Ncpr_lon1 = int(binary_msg[71:88], 2)
            LONcpr_even = Ncpr_lon1 / 2 ** 17
            return 'even', LATcpr_even, LONcpr_even  # Return 'even' format data
        elif F == 1:  # Odd format
            Ncpr_lat2 = int(binary_msg[54:71], 2)
            LATcpr_odd = Ncpr_lat2 / 2 ** 17
            Ncpr_lon2 = int(binary_msg[71:88], 2)
            LONcpr_odd = Ncpr_lon2 / 2 ** 17
        return 'odd', LATcpr_odd, LONcpr_odd  # Return 'odd' format data
    elif type_code==19:
        print(f"\nRaw Message: {hex_message}")
        print(f"Type code: {type_code}")
        print(f"Velocity message")
        ST =int(binary_msg[37:40],2)
        
        
        if ST==1:
            print(f"ST : {ST}")
            #For subsonic speed, speed component is
            S_ew=int(binary_msg[45:46],2)
            V_ew=int(binary_msg[46:56],2)
            S_ns=int(binary_msg[56:57],2)
            V_ns=int(binary_msg[57:67],2)
            if S_ew==0:
                V_x=V_ew-1  
            else: 
                V_x=-(V_ew-1)
            print(f"V_x: {V_x}")
            if S_ns==0:
                V_y=V_ns-1
            else:
                V_y=-(V_ns-1)
            print(f"V_y: {V_y}")
            
            #THE FINAL GROUND SPEED OF AIRCRAFT
            V=math.sqrt(V_x**2+V_y**2)
            print(f"THE FINAL GROUND SPEED OF AIRCRAFT: {V}")
        elif ST==3:
            T=binary_msg[56:57]
            SH=int(binary_msg[45:46])
            AS=int(binary_msg[57:67],2)

            #print(f"T :{T}")
            #print(f"SH:{SH}")
            #print(f"AS:{AS}")
            if SH==1:
                HDG=int(binary_msg[46:56],2)
                print(f"HDG:{HDG}")
                mag_heading=HDG*(360/1024)
                print(f"magnetic heading={mag_heading}")
                Vas=AS-1
                print(f"Vertical speed:{Vas}")   
        else:
            print("Other ADS-B message type")
        return 'velocity', None, None
    return None, None, None  # If not a position message
    # Main function to process multiple messages
def process_adsb_messages(messages):
    even_format_data = None  # To store even format data (LATcpr_even, LONcpr_even)
    odd_format_data = None   # To store odd format data (LATcpr_odd, LONcpr_odd)
    
    for msg in messages:
        format_type, LATcpr, LONcpr = decode_adsb(msg)
        
        # If it's a position message (even or odd format)
        if format_type == 'even':
            # Store even format data
            even_format_data = (LATcpr, LONcpr)
            # print(f"format type:{format_type}")
            # print(f"LATcpr:{LATcpr}")
            # print(f"LONcpr:{LONcpr}")
            continue  # Skip further processing and move to the next message
        
        elif format_type == 'odd':
            # Store odd format data
            odd_format_data = (LATcpr, LONcpr)
            # print(f"format type:{format_type}")
            # print(f"LATcpr:{LATcpr}")
            # print(f"LONcpr:{LONcpr}")
        
        # Once both even and odd formats are available, calculate the position
        if even_format_data and odd_format_data:
            LATcpr_even, LONcpr_even = even_format_data
            LATcpr_odd, LONcpr_odd = odd_format_data
            # Calculate the 'j' value combining even and odd formats
            Nz = 15  # Fixed value for Nz (compression factor)
            j = math.floor(59 * LATcpr_even - 60 * LATcpr_odd + 1 / 2)
            #print(f"j:{j}")
            # Call the function to calculate latitude and longitude
            LAT_even, LAT_odd, NL_lat_even, NL_lat_odd = calculate_position(j, Nz, LATcpr_even, LATcpr_odd)
            #print(f"NL_lat_even: {NL_lat_even}")
            #print(f"NL_lat_odd: {NL_lat_odd}")
            #print(f"LONcpr_even:{LONcpr_even}")           
            #print(f"LONcpr_odd:{LONcpr_odd}")
            #print(f"LAT_even: {LAT_even}")
            #print(f"LAT_odd: {LAT_odd}")
            m=math.floor(LONcpr_even*(NL_lat_even-1) - LONcpr_odd*(NL_lat_odd) + 1/2)
            print(f"m:{m}")
            n_even=max(NL_lat_even,1)
            print(f"n_even:{n_even}")
            LON=360/n_even*((m%n_even) + LONcpr_even )
            print(f"LONGITUDE:{LON}")
            # Reset the data after processing
            even_format_data = None
            odd_format_data = None
    
########################################

# Example usage with your sample ADS-B messages
sample_adsb_messages = [
    "8D40621D58C386435CC412692AD6",  # Example message 1 (Even format)
    "8D40621D58C382D690C8AC2863A7",
    "8D485020994409940838175B284F",  # Example message 3 (velocity ST 1)
    "8DA05F219B06B6AF189400CBC33F"
      # Example message 2 (Odd format)
      # Example message 3 (velocity ST 1)
     # Example message 4 (velocity ST 3)
]

process_adsb_messages(sample_adsb_messages)

