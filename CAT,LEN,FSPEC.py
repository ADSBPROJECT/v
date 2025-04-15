import tkinter as tk
from tkinter import messagebox

def parse_packet(hex_string):
    # Remove any potential spaces or unwanted characters in the input
    hex_string = hex_string.replace(" ", "").strip()

    # Convert the hex string into a list of bytes
    bytes_data = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]

    # Ensure the packet has enough bytes to prevent index errors
    if len(bytes_data) < 44:
        raise ValueError("Hexadecimal packet is too short for the expected fields")

    # Parse the fields based on the byte positions you described
    result = {
        "Category": int(bytes_data[0], 16),
        "Length": int(bytes_data[1] + bytes_data[2], 16),  # Combine second and third byte as length
        "FSPEC": bytes_data[3:9],  # Fourth to ninth byte
        "SAC": bytes_data[9],  # Tenth byte (SAC) (no conversion)
        "SIC": bytes_data[10],  # Eleventh byte (SIC) (no conversion)
        "Track No": 1,  # Track Number (always 1)
        "Time of Applicability of Position": int(bytes_data[13] + bytes_data[14], 16) * (1/128),  # Converted
        "Latitude": int(bytes_data[16] + bytes_data[17] + bytes_data[18] + bytes_data[19], 16) * (180 / (2**30)),  # Converted
        "Longitude": int(bytes_data[20] + bytes_data[21] + bytes_data[22] + bytes_data[23], 16) * (180 / (2**30)),  # Converted
        "Time of Applicability of Velocity": int(bytes_data[24] + bytes_data[25], 16) * (1/128),  # Converted
        "Target Address": 1,  # Target Address (always 1)
        "Time of Message Reception": int(bytes_data[30] + bytes_data[31] + bytes_data[32], 16) * (1/128),  # Converted
        "Geometric Height": int(bytes_data[33] + bytes_data[34], 16) * 6.25,  # Converted
        "Flight Level": int(bytes_data[35] + bytes_data[36], 16) * (1/4),  # Converted
        "Magnetic Heading": int(bytes_data[37] + bytes_data[38], 16) * (360 / (2**16)),  # Converted
        "Barometric Vertical Rate": int(bytes_data[39] + bytes_data[40], 16) * 6.25,  # Converted
        "Geometric Vertical Rate": int(bytes_data[41] + bytes_data[42], 16) * 6.25,  # Converted
        "Message Amplitude": int(bytes_data[43], 16) * 1  # No conversion
    }

    return result

def show_decoded_values():
    hex_packet = entry_hex.get()

    try:
        parsed_data = parse_packet(hex_packet)
        
        # Extract and print the real aircraft location
        latitude = parsed_data["Latitude"]
        longitude = parsed_data["Longitude"]
        
        # Output the aircraft location
        result_text.delete(1.0, tk.END)  # Clear the previous text
        result_text.insert(tk.END, f"Latitude: {latitude}\n")
        result_text.insert(tk.END, f"Longitude: {longitude}\n")
        
        # Also print the full decoded data
        for key, value in parsed_data.items():
            result_text.insert(tk.END, f"{key}: {value}\n")
        
    except ValueError as e:
        messagebox.showerror("Error", f"Error: {e}")

# Create the main window
root = tk.Tk()
root.title("Hexadecimal Packet Decoder")
root.configure(bg="lightblue")  # Set background color of the window

# Create and place the widgets
label = tk.Label(root, text="Enter Hexadecimal Packet:", fg="darkblue", bg="lightblue")
label.pack(pady=10)

entry_hex = tk.Entry(root, width=80, bg="lightyellow")
entry_hex.pack(pady=5)

decode_button = tk.Button(root, text="Decode", command=show_decoded_values, bg="lightgreen")
decode_button.pack(pady=10)

result_text = tk.Text(root, height=20, width=80, bg="lightgray")
result_text.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
