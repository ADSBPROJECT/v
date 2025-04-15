from datetime import timedelta

# Mapping of CAT21 Field IDs to their descriptions
CAT21_FIELDS = {
    1:  "Data Source Identifier (SAC/SIC)",
    2:  "Target Report Descriptor",
    3:  "Track Number",
    4:  "Service Identification",
    5:  "Time of Applicability for Position",
    6:  "Position in WGS-84 Coordinates",
    7:  "Position in WGS-84 Coordinates (High Precision)",
    8:  "Time of Applicability for Velocity",
    9:  "Air Speed",
    10: "True Air Speed",
    11: "Target Address (24-bit ICAO)",
    12: "Time of Message Reception (Position)",
    13: "Time of Message Reception of Position - High Resolution",
    14: "Time of Message Reception of Velocity",
    15: "Time of Message Reception of Velocity - High Resolution",
    16: "Geometric Height",
    17: "Quality Indicators",
    18: "MOPS Version",
    19: "Mode 3/A Code",
    20: "Roll Angle",
    21: "Flight Level",
    22: "Magnetic Heading",
    23: "Target Status",
    24: "Barometric Vertical Rate",
    25: "Geometric Vertical Rate",
    26: "Airborne Ground Vector",
    27: "Track Angle Rate",
    28: "Time of Report Transmission",
    29: "Target Identification (Callsign)",
    30: "Emitter Category",
    31: "Met Information",
    32: "Selected Altitude",
    33: "Final State Selected Altitude",
    34: "Trajectory Intent",
    35: "Service Management",
    36: "Aircraft Operational Status",
    37: "Surface Capabilities and Characteristics",
    38: "Message Amplitude",
    39: "Mode S MB Data",
    40: "ACAS Resolution Advisory Report",
    41: "Receiver ID",
    42: "Reserved",
    43: "Data Ages",
    44: "Not Used",
    45: "Not Used",
    46: "Not Used",
    47: "Not Used",
    48: "Reserved Expansion Field",
    49: "Special Purpose Field"
}

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
        if field_ptr + n > len(bytes_data):
            raise ValueError(f"Not enough bytes left to read {n} bytes at position {field_ptr}.")
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
            field_name = CAT21_FIELDS.get(field_id, f"Field {field_id}")
            result["Fields Present"].append(field_name)

            try:
                if field_id == 1:
                    sac = int(read_bytes(1)[0], 16)
                    sic = int(read_bytes(1)[0], 16)
                    result["SAC"] = sac
                    result["SIC"] = sic

                elif field_id == 2:
                    result["Target Report Descriptor"] = to_uint(read_bytes(1))

                elif field_id == 3:
                    result["Track Number"] = to_uint(read_bytes(2))

                elif field_id == 4:
                    result["Service Identification"] = to_uint(read_bytes(1))

                elif field_id == 5:
                    seconds = to_uint(read_bytes(3)) / 128
                    result["Time of Applicability of position"] = seconds

                elif field_id == 6:
                    lat = to_int(read_bytes(3), 24) * (180 / (2 ** 23))
                    lon = to_int(read_bytes(3), 24) * (180 / (2 ** 23))
                    result["Latitude"] = round(lat, 6)
                    result["Longitude"] = round(lon, 6)

                elif field_id == 7:
                    lat = to_int(read_bytes(4), 32) * (180 / (2 ** 31))
                    lon = to_int(read_bytes(4), 32) * (180 / (2 ** 31))
                    result["Latitude"] = round(lat, 6)
                    result["Longitude"] = round(lon, 6)

                elif field_id == 8:
                    seconds = to_uint(read_bytes(3)) / 128
                    result["Time of Applicability of Velocity"] = seconds

                elif field_id == 9:
                    result["Air Speed"] = to_uint(read_bytes(2))

                elif field_id == 10:
                    result["True Air Speed"] = to_uint(read_bytes(2))

                elif field_id == 11:
                    val = to_uint(read_bytes(3))
                    result["Target Address"] = f"{val} (hex: {hex(val)[2:].upper()})"

                elif field_id == 12:
                    seconds = to_uint(read_bytes(3)) / 128
                    result["Time of message Reception (position)"] = seconds

                elif field_id == 13:
                    result["Time of Message Reception of Position-High"] = to_uint(read_bytes(4))

                elif field_id == 14:
                    result["Time of Message Reception of Velocity"] = to_uint(read_bytes(3))

                elif field_id == 15:
                    result["Time of Message Reception of Velocity-High"] = to_uint(read_bytes(4))

                elif field_id == 16:
                    val = to_int(read_bytes(2), 16)
                    result["Geometric Height (ft)"] = round(val * 6.25, 2)

                elif field_id == 17:
                    result["Quality Indicators"] = to_uint(read_bytes(1))

                elif field_id == 18:
                    result["MOPS Version"] = to_uint(read_bytes(1))

                elif field_id == 19:
                    result["Mode 3/A Code"] = to_uint(read_bytes(2))

                elif field_id == 20:
                    result["Roll Angle"] = to_uint(read_bytes(2))

                elif field_id == 21:
                    val = to_uint(read_bytes(2)) * 0.25
                    result["Flight Level"] = f"FL{int(val)} ({int(val * 100)} ft)"

                elif field_id == 22:
                    val = to_uint(read_bytes(2)) * (360 / 65536)
                    result["Magnetic Heading"] = round(val, 3)

                elif field_id == 23:
                    result["Target Status"] = to_uint(read_bytes(1))

                elif field_id == 24:
                    val = to_int(read_bytes(2), 16) * 6.25
                    result["Barometric Vertical Rate (ft/min)"] = val

                elif field_id == 25:
                    val = to_int(read_bytes(2), 16) * 6.25
                    result["Geometric Vertical Rate (ft/min)"] = val

                elif field_id == 26:
                    result["Airborne Ground Vector"] = to_uint(read_bytes(4))

                elif field_id == 27:
                    result["Track Angle Rate"] = to_uint(read_bytes(2))

                elif field_id == 28:
                    result["Time of Report Transmission"] = to_uint(read_bytes(3))

                elif field_id == 29:
                    result["Target Identification"] = to_uint(read_bytes(6))

                elif field_id == 30:
                    result["Emitter Category"] = to_uint(read_bytes(1))

                elif field_id == 31:
                    result["Met Information"] = to_uint(read_bytes(1))

                elif field_id == 32:
                    result["Selected Altitude"] = to_uint(read_bytes(2))

                elif field_id == 33:
                    result["Final State Selected Altitude"] = to_uint(read_bytes(2))

                elif field_id == 34:
                    result["Trajectory Intent"] = to_uint(read_bytes(1))

                elif field_id == 35:
                    result["Service Management"] = to_uint(read_bytes(1))

                elif field_id == 36:
                    result["Aircraft Operational Status"] = to_uint(read_bytes(1))

                elif field_id == 37:
                    result["Surface Capabilities and Characteristics"] = to_uint(read_bytes(1))

                elif field_id == 38:
                    result["Message Amplitude"] = int(read_bytes(1)[0], 16)

                elif field_id == 39:
                    n = 0  # Change according to real Mode S MB Data count
                    result["Mode S MB Data"] = to_uint(read_bytes(1 + n * 8))

                elif field_id == 40:
                    result["ACAS Resolution Advisory Report"] = to_uint(read_bytes(6))

                elif field_id == 41:
                    result["Receiver ID"] = to_uint(read_bytes(1))

                elif field_id == 43:
                    result["Data Ages"] = to_uint(read_bytes(1))

                elif field_id in (44, 45, 46, 47):
                    result[f"Not Used (Field {field_id})"] = "Skipped"

                elif field_id == 48:
                    result["Reserved Expansion Field"] = to_uint(read_bytes(1))

                elif field_id == 49:
                    result["Special Purpose Field"] = to_uint(read_bytes(1))

            except Exception as e:
                result[f"Field {field_id} Error"] = f"Parsing failed: {str(e)}"

    print("\n=== Decoded CAT21 Packet ===")
    for k, v in result.items():
        print(f"{k}: {v}")

    return result

# Example usage
hex_packet = "150023AB9943B1012014130001551B79048EDDDD1B3EA9EE551B7906A0F5551B7917C005F075FE0000000051"
parse_cat21_packet(hex_packet)

# Optional: keep console open if run from double-click
input("\nPress Enter to exit...")
