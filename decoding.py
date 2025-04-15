import math

# Function to calculate latitude and longitude
def calculate_position(j, Nz, LATcpr_even, LATcpr_odd):
    LAT_even = (360 / (4 * Nz)) * ((j % 60) + LATcpr_even)
    LAT_odd = (360 / (4 * Nz - 1 )) * ((j % 59) + LATcpr_odd)

    # Avoid division by zero or invalid input to acos
    def get_NL(lat):
        if abs(lat) >= 87:
            return 1
        a = 1 - math.cos(math.pi / (2 * Nz))
        b = math.cos(math.pi / 180 * lat) ** 2
        denominator = 1 - a / b
        return math.floor(2 * math.pi / math.acos(denominator))

    NL_LAT_even = get_NL(LAT_even)
    NL_LAT_odd = get_NL(LAT_odd)

    return LAT_even, LAT_odd, NL_LAT_even, NL_LAT_odd

# Function to decode velocity message
def decode_velocity_message(binary_msg, ST):
   # print(f"ST:{ST}")
    if ST == 1:
        S_ew = int(binary_msg[45:46], 2)
        V_ew = int(binary_msg[46:56], 2)
        S_ns = int(binary_msg[56:57], 2)
        V_ns = int(binary_msg[57:67], 2)

        if S_ew == 0:
            V_x = V_ew - 1
        else:
            V_x = -(V_ew - 1)

        if S_ns == 0:
            V_y = V_ns - 1
        else:
            V_y = -(V_ns - 1)

        V = math.sqrt(V_x**2 + V_y**2)

        # print(f"S_ew: {S_ew}")
        # print(f"V_ew: {V_ew}")
        # print(f"S_ns: {S_ns}")
        # print(f"V_ns: {V_ns}")
        # print(f"V_x: {V_x}")
        # print(f"V_y: {V_y}")
        print(f"THE FINAL GROUND SPEED OF THE AIRCRAFT: {V:.2f} ft/min")

    elif ST == 3:
        T = binary_msg[56:57]
        SH = int(binary_msg[45:46], 2)
        AS = int(binary_msg[57:67], 2)
        # print(f"T: {T}")
        # print(f"SH: {SH}")
        # print(f"AS: {AS}")
        if SH == 1:
            HDG = int(binary_msg[46:56], 2)
            mag_heading = HDG * (360 / 1024)
            Vas = AS - 1
            print(f"HDG: {HDG}")
            print(f"Magnetic Heading: {mag_heading:.2f}°")
            print(f"Airspeed: {Vas}")
        else:
            print("Heading data not available.")
    else:
        print("Unsupported subtype for velocity message.")

# Function to decode ADS-B message
def decode_adsb(hex_message):
    binary_msg = bin(int(hex_message, 16))[2:].zfill(len(hex_message) * 4)
    type_code = int(binary_msg[32:37], 2)
    icao_address = hex_message[2:8]
    print(f"ICAO_address :{icao_address}")

    if 9 <= type_code <= 18:
        print(f"\nRaw Message: {hex_message}")
        print(f"Type code: {type_code}")
        F = int(binary_msg[53], 2)

        Alt = binary_msg[40:52]
        bit_value = Alt[7]
        N = int((Alt[:7] + Alt[8:12]), 2)
        #print(f"N: {N}")
        h = 25 * N - 1000
        print(f"ALTITUDE : {h} ft")

        if F == 0:
            Ncpr_lat1 = int(binary_msg[54:71], 2)
            LATcpr_even = Ncpr_lat1 / 2 ** 17
            Ncpr_lon1 = int(binary_msg[71:88], 2)
            print(f"Ncpr_lat1: {Ncpr_lat1}")
            LONcpr_even = Ncpr_lon1 / 2 ** 17
            return 'even', LATcpr_even, LONcpr_even
        elif F == 1:
            Ncpr_lat2 = int(binary_msg[54:71], 2)
            LATcpr_odd = Ncpr_lat2 / 2 ** 17
            Ncpr_lon2 = int(binary_msg[71:88], 2)
            LONcpr_odd = Ncpr_lon2 / 2 ** 17
            return 'odd', LATcpr_odd, LONcpr_odd

    elif type_code == 19:
        print(f"\nRaw Message: {hex_message}")
        print(f"Type code: {type_code}")
        print("Velocity message")
        ST = int(binary_msg[37:40], 2)
        decode_velocity_message(binary_msg, ST)
        return 'Velocity', None, None

    return None, None, None

# Function to process list of ADS-B messages
def proccess_adsb_messages(messages):
    icao_data = {}

    for msg in messages:
        binary_msg = bin(int(msg, 16))[2:].zfill(len(msg) * 4)
        icao_address = msg[2:8]

        format_type, LATcpr, LONcpr = decode_adsb(msg)

        if icao_address not in icao_data:
            icao_data[icao_address] = {
                'even': None,
                'odd': None,
                'velocity': None
            }

        if format_type == 'even':
            icao_data[icao_address]['even'] = (LATcpr, LONcpr)
        elif format_type == 'odd':
            icao_data[icao_address]['odd'] = (LATcpr, LONcpr)
        elif format_type == 'Velocity':
            # We'll store velocity messages as printed by decode_velocity_message
            icao_data[icao_address]['velocity'] = 'captured'

    # Now process ICAO addresses that have both even & odd positions
    Nz = 15
    for icao, data in icao_data.items():
        even = data['even']
        odd = data['odd']
        vel = data['velocity']

        print(f"\n--- ICAO Address: {icao} ---")
        if even and odd:
            LATcpr_even, LONcpr_even = even
            LATcpr_odd, LONcpr_odd = odd

            j = math.floor((59 * LATcpr_even - 60 * LATcpr_odd) + 0.5)

            LAT_even, LAT_odd, NL_lat_even, NL_lat_odd = calculate_position(j, Nz, LATcpr_even, LATcpr_odd)
            m = math.floor((LONcpr_even * (NL_lat_even - 1) - LONcpr_odd * (NL_lat_odd)) + 0.5)
            n_even = max(NL_lat_even, 1)
            LON = 360 / n_even * ((m % n_even) + LONcpr_even)

            print(f"Position => LAT: {LAT_even:.6f}, LON: {LON:.6f}")
        else:
            print("Incomplete position data (need both even and odd)")

        if vel:
            print("Velocity message captured")
        else:
            print("No velocity message")


# Sample ADS-B messages
sample_adsb_messages = [
    "8D40621D58C382D690C8AC2869A7",  # even
    "8D40621D58C386435CC412692AD6",  # odd
    "8D485020994409940838175B284F",  # velocity ST=1
    "8DA05F219B06B6AF189400CBC33F"   # velocity ST=3
]

proccess_adsb_messages(sample_adsb_messages)