import math
import time
import socket
import struct
from datetime import datetime

binary_string = ""

# Function to append a bit to the binary string
def append_bit(binary_string, bit):
    if bit not in (0, 1):
        raise ValueError("Bit must be 0 or 1")
    return binary_string + str(bit)


# Function to convert binary string to hex
def binary_string_to_hex(binary_string):
    """
    Converts a binary string to a hexadecimal string.

    Args:
        binary_string (str): A string of bits (0s and 1s).

    Returns:
        str: The hexadecimal representation of the binary string.
    """
    # Convert the binary string to an integer
    integer_value = int(binary_string, 2)

    # Convert the integer to a hexadecimal string
    hex_string = hex(integer_value)[2:].upper()  # Remove the '0x' prefix and convert to uppercase

    # Ensure the hex string has an even number of characters (2 characters per byte)
    if len(hex_string) % 2 != 0:
        hex_string = '0' + hex_string

    return hex_string

def create_cat21_packet(sic,sac,track_no,ser_id,latitude1,longitude1,latitude2,longitude2,hex_icao,time_of_pos,time_of_vel,
                        geometric_ht, geometric_vertical_rate,ground_speed,track_angle,time_of_ast,altitude,amplitude_dbm):
    binary_string = ""
    packet = b''

    # 1 -Data Source identifier (I021/010)
    packet += struct.pack('>B', sic)
    packet += struct.pack('>B', sac)
    binary_string = append_bit(binary_string, 1)

    # 2 - Target Report identifier (I021/040)
    binary_string = append_bit(binary_string, 0)

    # 3 - Track no (I021/161)
    packet += struct.pack('>h', track_no)
    binary_string = append_bit(binary_string, 1)

    # 4 - service identification (I021/15)
    packet += struct.pack('>B', ser_id)
    binary_string = append_bit(binary_string, 1)

    #5 - Time of Applicability for Position (I021/71)
    binary_string = append_bit(binary_string, 0)

    #6 - latitude and longitude in wgs  (I021/130)
    lsb_value = 180 / (2 ** 23)
    lat_wgs84 = int(latitude1/lsb_value)
    lon_wgs84 = int(longitude1/lsb_value)
    lat = lat_wgs84.to_bytes(4, byteorder='big', signed=True)[1:]
    lon = lon_wgs84.to_bytes(4, byteorder='big', signed=True)[1:]
    packet += lat + lon
    binary_string = append_bit(binary_string, 1)


    #7 - latitude and longitude in wgs high precision  (I021/131)
    lsb_value2 = 180 / (2 ** 30)
    lat_wgs84_2 = int(latitude2 / lsb_value2)
    lon_wgs84_2 = int(longitude2 / lsb_value2)
    lat_2 = lat_wgs84_2.to_bytes(4, byteorder='big', signed=True)
    lon_2 = lon_wgs84_2.to_bytes(4, byteorder='big', signed=True)
    packet += lat_2 + lon_2
    binary_string = append_bit(binary_string, 1)

    #FX
    binary_string = append_bit(binary_string, 1)  # Field extension indicator

    #8 - Time of Applicability for Velocity  (I021/072)
    binary_string = append_bit(binary_string, 0)

    #9 - Air Speed  (I021/150)
    binary_string = append_bit(binary_string, 0)

    #10- True Air Speed  (I021/151)
    binary_string = append_bit(binary_string, 0)

    #11- Target address  (I021/080)
    icao = bytes.fromhex(hex_icao)
    packet += icao
    binary_string = append_bit(binary_string, 1)

    #12- Time of reception of position  (I021/073)
    lsb_time = 1/128  # Scaling factor to convert to 24-bit range within one day (86400 seconds)    scaled_time = int(time_of_pos * scaling_factor)
    scaled_time_pos= int(time_of_pos/lsb_time)
    time_pos = scaled_time_pos.to_bytes(3, byteorder='big', signed=False)
    packet+=time_pos
    binary_string = append_bit(binary_string, 1)

    #13- Time of reception of position-high precision  (I021/074)
    binary_string = append_bit(binary_string, 0)


    #14- Time of reception of velocity  (I021/076)
    scaled_time_vel = int(time_of_vel / lsb_time)
    time_vel = scaled_time_vel.to_bytes(3, byteorder='big', signed=False)
    packet += time_vel
    binary_string = append_bit(binary_string, 1)

    # FX
    binary_string = append_bit(binary_string, 1)  # Field extension indicator

    #15- Time of reception of velocity  (I021/076)
    binary_string = append_bit(binary_string, 0)

    #16- Geometric height (I021/140)
    lsb_height=6.25
    scaled_height=int(geometric_ht/lsb_height)
    height= scaled_height.to_bytes(2, byteorder='big', signed=True)
    packet += height
    binary_string = append_bit(binary_string, 1)

    #17- Quality Indicators (I021/090)
    binary_string = append_bit(binary_string, 0)

    #18 - MOPS Version (I021/210)
    packet += struct.pack('>B', 18)
    binary_string = append_bit(binary_string, 1)

    #19 - Mode 3A code (I021/070)
    packet += struct.pack('>h', 2735)
    binary_string = append_bit(binary_string, 1)

    #20 Roll Angle (I021/230)
    binary_string = append_bit(binary_string, 0)

    #21 Flight level (I021/145)
    lsb_fl = 0.25
    scaled_fl = int(round(geometric_ht/100)/lsb_fl)
    FL = scaled_fl.to_bytes(2, byteorder='big', signed=True)
    packet += FL
    binary_string = append_bit(binary_string, 1)

    #FX
    binary_string = append_bit(binary_string, 1)  # Field extension indicator

    #22 Magnetic Heading (I021/152)
    binary_string = append_bit(binary_string, 0)

    #23 Target status (I021/200)
    packet += struct.pack('>B', 00)
    binary_string = append_bit(binary_string, 1)

    #24 Barometric vertical rate (I021/155)
    binary_string = append_bit(binary_string, 0)

    #25 Geometrical vertical rate (I021/157)
    magnitude=int(abs(geometric_vertical_rate) / 6.25)
    sign_bit = 0
    if geometric_vertical_rate < 0:
        sign_bit = 1
    encoded_value = (sign_bit << 15) | magnitude
    if sign_bit == 1:
        # Two's complement for a 16-bit number
        encoded_value = (1 << 16) - encoded_value
    vertical_rate = struct.pack('>h', encoded_value)
    packet += vertical_rate
    binary_string = append_bit(binary_string, 1)

    #26 Airborne ground vector (I021/160)
    ground_speed_nms=ground_speed/3600
    scaled_speed = int(ground_speed_nms / 2**-14)
    speed = scaled_speed.to_bytes(2, byteorder='big', signed=True)
    packet += speed
   
    lsb_heading=360/(2**16)
    scaled_heading = int(track_angle / lsb_heading)
    heading = scaled_heading.to_bytes(2, byteorder='big', signed=False)
    packet += heading
    binary_string = append_bit(binary_string, 1)
    
    #27 Track Angle Rate (I021/165)
    binary_string = append_bit(binary_string, 0)

    #28 Time of asterix tx (I021/077)
    scaled_time_ast = int(time_of_ast / lsb_time)
    time_ast = scaled_time_ast.to_bytes(3, byteorder='big', signed=False)
    packet += time_ast
    binary_string = append_bit(binary_string, 1)

    #FX
    binary_string = append_bit(binary_string, 1)  # Field extension indicator

    #29 Target ID (I021/170)
    target_id=1
    id_byte = target_id.to_bytes(6, byteorder='big', signed=False)
    packet += id_byte
    binary_string = append_bit(binary_string, 1)

    #30 Emitter Category (I021/020)
    emitter_type = 5
    emitter = emitter_type.to_bytes(1, byteorder='big', signed=False)
    packet += emitter
    binary_string = append_bit(binary_string, 1)

    #31 Met Information (I021/220)
    binary_string = append_bit(binary_string, 0)

    #32 Selected Altitude (I021/146)
    scaled_altitude = int(altitude / 25)
    altitude = scaled_altitude.to_bytes(2, byteorder='big', signed=False)
    packet += altitude
    binary_string = append_bit(binary_string, 1)

    #33 Final State Selected Altitude (I021/148)
    binary_string = append_bit(binary_string, 0)

    #34 Trajecory Intent (I021/110)
    binary_string = append_bit(binary_string, 0)

    #35 service management (I021/016)
    packet += struct.pack('>B', 00)
    binary_string = append_bit(binary_string, 1)

    #FX
    binary_string = append_bit(binary_string, 1)  # Field extension indicator

    #36 AIrcraft operational status (I021/008)
    packet += struct.pack('>B', 00)
    binary_string = append_bit(binary_string, 1)

    #37 Surface capabilities and characteristics (I021/271)
    binary_string = append_bit(binary_string, 0)

    #38 message amplitude(1021/132)
    amplitude=int(abs(amplitude_dbm))
    encoded_value_amp = (1 << 8) | amplitude
    encoded_value_amp = (1 << 8) - encoded_value_amp
    amplitude_hex = struct.pack('>b', encoded_value_amp)
    packet += amplitude_hex
    binary_string = append_bit(binary_string, 1)

    #39 ModeS MB Data (I021/250)
    binary_string = append_bit(binary_string, 0)

    #40 ACAS Resolution Advisory report (I021/260)
    binary_string = append_bit(binary_string, 0)

    #41 Receiver ID (I021/400)
    packet += struct.pack('>B', 2)
    binary_string = append_bit(binary_string, 1)

    #42 Data Ages (1021/295)
    binary_string = append_bit(binary_string, 1)

    #FX
    binary_string = append_bit(binary_string, 1)  # Field extension indicator
   
    binary_string = append_bit(binary_string, 0)
    binary_string = append_bit(binary_string, 0)
    binary_string = append_bit(binary_string, 0)
    binary_string = append_bit(binary_string, 0)
    binary_string = append_bit(binary_string, 0)
    binary_string = append_bit(binary_string, 1)
    binary_string = append_bit(binary_string, 0)
    binary_string = append_bit(binary_string, 0)

    integer_value = int(binary_string, 2)
    cat21=21
    data_ages = 0
    cat21_byte=cat21.to_bytes(1, byteorder='big', signed=False)
    fspec = integer_value.to_bytes(7, byteorder='big', signed=False)
    data_ages_byte = data_ages.to_bytes(4, byteorder='big', signed=False)
    packet1=fspec+packet+data_ages_byte
    length = len(packet1)
    length_byte=length.to_bytes(2, byteorder='big', signed=False)

    packet = cat21_byte + length_byte + packet1
    
    return packet

def extract_bits(binary_message, start_bit, length):
    """Extract a sequence of bits from the binary message."""
    return binary_message[start_bit:start_bit + length]

def decode_type_code(hex_message):
    bin_message = hex_to_bin(hex_message)
    type_code = int(bin_message[32:37], 2)
    return type_code

def hex_to_bin(hex_string):
    return bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)

def get_downlink_format(hex_message):
    """Extracts and identifies the Downlink Format (DF) from an ADS-B hex message."""
    bin_message = hex_to_bin(hex_message)
    df_bits = bin_message[:5]  # First 5 bits represent the DF
    df = int(df_bits, 2)  # Convert binary to decimal
    return df

def get_icao_address(hex_message):
    """Extracts the ICAO Address from a binary ADS-B message."""
    bin_message = hex_to_bin(hex_message)
    icao_bits = bin_message[8:32]  # Bits 9-32 represent the ICAO Address
    icao = hex(int(icao_bits, 2))[2:].upper()  # Convert binary to hex and format
    return icao

def identify_df_type(df):
    """Identifies the type of Downlink Format (DF) based on the DF value."""
    df_types = {
        0: "Short Air-Air Surveillance",
        4: "Surveillance, Altitude Reply",
        5: "Surveillance, Identity Reply",
        11: "All-Call Reply",
        16: "Long Air-Air Surveillance",
        17: "ADS-B Message",
        18: "Extended Squitter",
        19: "Military Extended Squitter",
        20: "Comm-B, Altitude Reply",
        21: "Comm-B, Identity Reply",
        22: "Comm-C, ELM",
        24: "Comm-D",
    }
    return df_types.get(df, "Unknown DF")

def decode_message_type(hex_message):
    type_code = decode_type_code(hex_message)

    if 1 <= type_code <= 4:
        return "Aircraft Identification and Category"
    elif 5 <= type_code <= 8:
        return "Surface Position Message"
    elif 9 <= type_code <= 18:
        return "Airborne Position Message with Barometric Altitude"
    elif type_code == 19:
        return "Airborne Velocity Message"
    elif 20 <= type_code <= 22:
        return "Airborne Position Message with GNSS Height"
    elif 23 <= type_code <= 27:
        return "Reserved for Future Use"
    elif type_code == 28:
        return "Aircraft Status"
    elif type_code == 29:
        return "Target State and Status"
    elif type_code == 31:
        return "Aircraft Operational Status"
    else:
        return "Unknown Type"

def decode_altitude(hex_message):
    bin_message = hex_to_bin(hex_message)
    q_bit = int(bin_message[47])

    if q_bit == 0:
        altitude = int(bin_message[40:47] + bin_message[48:51], 2) * 100 - 1000
    elif q_bit == 1:
        altitude = int(bin_message[40:51], 2) * 25 - 1100

    return altitude

def decode_position(hex_message_even, T_even, hex_message_odd, T_odd):
    # Extract latitude and longitude
    bin_message_even = hex_to_bin(hex_message_even)
    bin_message_odd = hex_to_bin(hex_message_odd)

    latitude_even = int(bin_message_even[54:71], 2) / 131072.0
    longitude_even = int(bin_message_even[71:88], 2) / 131072.0

    latitude_odd = int(bin_message_odd[54:71], 2) / 131072.0
    longitude_odd = int(bin_message_odd[71:88], 2) / 131072.0

    j = math.floor(59 * latitude_even - 60 * latitude_odd + 0.5)
    DLatE = 360.0 / 60
    DLatO = 360.0 / 59

    latitude_even = DLatE * ((j % 60) + latitude_even)
    latitude_odd = DLatO * ((j % 59) + latitude_odd)

    a = 1 - math.cos(math.pi / (2 * 15))
    b_even = math.cos(latitude_even * math.pi / 180) ** 2
    b_odd = math.cos(latitude_odd * math.pi / 180) ** 2
    c_even = math.acos(1 - a / b_even)
    c_odd = math.acos(1 - a / b_odd)
    NL_even = math.floor(2 * math.pi / c_even)
    NL_odd = math.floor(2 * math.pi / c_odd)

    if T_even > T_odd:
        ni = max(NL_even, 1)
        Dlon = 360.0 / ni
        m = math.floor(longitude_even * (NL_even - 1) - longitude_odd * NL_even + 0.5)
        longitude = Dlon * ((m % ni) + longitude_even)
        latitude = latitude_even
    elif T_odd > T_even:
        ni = max(NL_odd - 1, 1)
        Dlon = 360.0 / ni
        m = math.floor(longitude_even * (NL_odd - 1) - longitude_odd * NL_odd + 0.5)
        longitude = Dlon * ((m % ni) + longitude_odd)
        latitude = latitude_odd
    now=datetime.now()
    time_of_pos=now.hour*3600 + now.minute*60 + now.second + now.microsecond/1_000_000
    return {
        "Latitude": latitude,
        "Longitude": longitude,
        "Time_of_pos": time_of_pos
    }



def decode_velocity(hex_message):
    bin_message = hex_to_bin(hex_message)
    subtype = int(bin_message[37:40], 2)

    if subtype == 1 or subtype == 2:
        intent_change = int(bin_message[40], 2)
        nac_v = int(bin_message[41], 2)
        s_bit = int(bin_message[42], 2)
        s_h = int(bin_message[43], 2)
        east_west_velocity = int(bin_message[46:56], 2)
        east_west_sign = int(bin_message[45], 2)
        north_south_velocity = int(bin_message[57:67], 2)
        north_south_sign = int(bin_message[56], 2)
        vertical_rate_source = int(bin_message[67], 2)
        vertical_rate_sign = int(bin_message[68], 2)
        vertical_rate = int(bin_message[69:78], 2)

        if east_west_sign == 1:
            east_west_velocity = -east_west_velocity
        if north_south_sign == 1:
            north_south_velocity = -north_south_velocity
        vertical_rate = (vertical_rate -1)* 64

        if vertical_rate_sign == 1:
            vertical_rate = -vertical_rate

        ground_speed = round(math.sqrt(east_west_velocity**2 + north_south_velocity**2),2)


        track_angle = round(math.atan2( east_west_velocity,north_south_velocity) * 180.0 / math.pi,2)
        now=datetime.now()
        time_of_vel=now.hour*3600 + now.minute*60 + now.second + now.microsecond/1_000_000
        if track_angle>=0:
            track_angle=track_angle
        else:
            track_angle=track_angle+360
        return {
                "Ground Speed": ground_speed,
                "Track Angle": track_angle,
                "Vertical Rate": vertical_rate,
                "Time_of_vel":time_of_vel
            }
    else:
        return None



def process_adsb_messages(messages):
    aircraft_positions = {}
    tracks = []

    for message in messages:
        hex_message = message['message']
        timestamp = message['timestamp']

        df = get_downlink_format(hex_message)
        tc = decode_type_code(hex_message)

        if df==17:
            icao_address_hex = get_icao_address(hex_message)
            if icao_address_hex not in aircraft_positions:
                aircraft_positions[icao_address_hex]={
                    'even':None,
                    'odd':None,
                    'position':None,
                    'altitude':None,
                    'velocity':None}

            
            if tc==11:
                          
                if extract_bits(hex_to_bin(hex_message), 53, 1) == '0':
                    aircraft_positions[icao_address_hex]['even'] = {'message': hex_message, 'timestamp': timestamp}
                else:
                    aircraft_positions[icao_address_hex]['odd'] = {'message': hex_message, 'timestamp': timestamp}

                if aircraft_positions[icao_address_hex]['even'] and aircraft_positions[icao_address_hex]['odd']:
                    position = decode_position(
                        aircraft_positions[icao_address_hex]['even']['message'],
                        aircraft_positions[icao_address_hex]['even']['timestamp'],
                        aircraft_positions[icao_address_hex]['odd']['message'],
                        aircraft_positions[icao_address_hex]['odd']['timestamp']
                        )
                    altitude = decode_altitude(aircraft_positions[icao_address_hex]['even']['message'])
                   
                    aircraft_positions[icao_address_hex]['position'] = position
                    aircraft_positions[icao_address_hex]['altitude'] = altitude
                    
                # Reset after processing
                    aircraft_positions[icao_address_hex]['even'] =  None
                    aircraft_positions[icao_address_hex]['odd'] =  None
            elif tc==19:
                velocity_data=decode_velocity(hex_message)
                aircraft_positions[icao_address_hex]['velocity'] =  velocity_data
            if aircraft_positions[icao_address_hex]['position'] and aircraft_positions[icao_address_hex]['velocity']:
                tracks.append({
                    "ICAO Address":icao_address_hex,
                    "Position":aircraft_positions[icao_address_hex]['position'],
                    "Altitude":aircraft_positions[icao_address_hex]['altitude'],
                    "Velocity":aircraft_positions[icao_address_hex]['velocity'],
                    })
                
                aircraft_positions[icao_address_hex]['position']=None
                aircraft_positions[icao_address_hex]['altitude']=None
                aircraft_positions[icao_address_hex]['velocity']=None

    return tracks  

def degrees_to_radians(degrees):
    return degrees*math.pi/180

track_numbers={}
current_track_no=1
 
def assign_track_no(hex_id):
   global current_track_no
     
   if hex_id not in track_numbers:
       track_numbers[hex_id]=current_track_no
       current_track_no +=1
   return track_numbers[hex_id]

           
def main():
    host = 'localhost'
    port = 30005
    UDP_IP = "10.188.135.100" #Change to the destination IP
    UDP_PORT = 5123      # Change to the destination port
    UDP_IP_RPET= "229.1.1.21"
    UDP_PORT_RPET = 6001
    
    sac=128
    sic=128
    ser_id=1
    amplitude_dbm=-50
    global track_no
    
    global tracks
 
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host,port))
            print(f"Connected to dump1090 on {host}:{port}")
            while True:
                start_time = time.time()
                hex_messages =[]
                while time.time() - start_time < 8 :
                    data=s.recv(4096)
                
                    if not data:
                        break
                
                    hex_message=data.decode().replace('*','').replace(';', '').replace('\n','')
                    hex_messages.append({'message':hex_message, 'timestamp':time.perf_counter()})
                
                tracks= process_adsb_messages(hex_messages)
                for track in tracks:
                    #print(f"ICAO Address: {track['ICAO Address']} Position: Latitude {track['Position']['Latitude']} Longitude {track['Position']['Longitude']} Altitude: {track['Altitude']}")
                    #print(f"Ground Velocity: {track['Velocity']['Ground Speed']}Knots, Heading:{ track['Velocity']['Track Angle']}°, Velocity Rate: {track['Velocity']['Vertical Rate']} ft/min")
                    now=datetime.now()
                    track_no=assign_track_no(track['ICAO Address'])
                    time_of_ast=now.hour*3600 + now.minute*60 + now.second + now.microsecond/1_000_000
                    cat21_packet = create_cat21_packet(sac,sic,track_no,ser_id,track['Position']['Latitude'],track['Position']['Longitude'],track['Position']['Latitude'],track['Position']['Longitude'],track['ICAO Address'],track['Position']['Time_of_pos'],
                                                       track['Velocity']['Time_of_vel'],track['Altitude'],track['Velocity']['Vertical Rate'],track['Velocity']['Ground Speed'],track['Velocity']['Track Angle'],time_of_ast,
                                                       track['Altitude'],amplitude_dbm)
                    print(cat21_packet.hex())
                    print(track_no, track['ICAO Address'])
                    
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
                    sock.sendto(cat21_packet, (UDP_IP, UDP_PORT))
                    sock.sendto(cat21_packet, (UDP_IP_RPET, UDP_PORT_RPET))
                    #sock.sendto(cat21_packet, ("229.1.1.21", 6001))
                    print("---------------------------------------------------------------------------------------------------------")
                       
                print("---------------------------------------------------------------------------------------------------------")
                
                
                
            
    except ConnectionRefusedError:
        print(f"Connection refused")
    except Exception as e:
        print(f"Error:{e}")
        


if __name__ == "__main__":
    main()
