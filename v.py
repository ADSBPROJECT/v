
result = {
    "Category": int(bytes_data[0], 16),
    "Length": int(bytes_data[1] + bytes_data[2], 16),
    "FSPEC": bytes_data[3:9],
    "Data Source Information": {
        "SAC": int(bytes_data[9]),
        "SIC": int(bytes_data[10])
    },
    "Track Number": 1,
    "Time of Applicability of Position": int(bytes_data[13] + bytes_data[14] + bytes_data[15], 16) * (1 / 128),
    "Position in WGS-84 coordinates, high resolution": {
        "Latitude": int(bytes_data[16] + bytes_data[17] + bytes_data[18] + bytes_data[19], 16) * (180 / (2 ** 30)),
        "Longitude": int(bytes_data[20] + bytes_data[21] + bytes_data[22] + bytes_data[23], 16) * (180 / (2 ** 30))
    },
    "Time of Applicability of Velocity": int(bytes_data[24] + bytes_data[25] + bytes_data[26], 16) * (1 / 128),
    "Target Address": 1,
    "Time of Message Reception of position": int(bytes_data[30] + bytes_data[31] + bytes_data[32], 16) * (1 / 128),
    "Geometric Height": int(bytes_data[33] + bytes_data[34], 16) * 6.25,
    "Flight Level": int(bytes_data[35] + bytes_data[36], 16) * (1 / 4),
    "Magnetic Heading": int(bytes_data[37] + bytes_data[38], 16) * (360 / (2 ** 16)),
    "Barometric Vertical Rate": int(bytes_data[39] + bytes_data[40], 16) * 6.25,
    "Geometric Vertical Rate": int(bytes_data[41] + bytes_data[42], 16) * 6.25,
    "Message Amplitude": int(bytes_data[43], 16) * 1
}

ordered_keys = [
    "Category", "Length", "FSPEC", "Data Source Information", "Track Number", "Time of Applicability of Position",
    "Position in WGS-84 coordinates, high resolution", "Time of Applicability of Velocity", "Target Address",
    "Time of Message Reception of position", "Geometric Height", "Flight Level", "Magnetic Heading",
    "Barometric Vertical Rate", "Geometric Vertical Rate", "Message Amplitude"
]

for key in ordered_keys:
    value = result[key]
    if isinstance(value, dict):
        print(f"{key}:")
        for sub_key, sub_value in value.items():
            print(f"  {sub_key}: {sub_value}")
    else:
        print(f"{key}: {value}")
