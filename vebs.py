import tkinter as tk
from tkinter import messagebox

def parse_packet(hex_string):
    hex_string = hex_string.replace(" ", "").strip()
    bytes_data = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]

    if len(bytes_data) < 44:
        raise ValueError("Hexadecimal packet is too short for the expected fields")

    result = {
        "Category": int(bytes_data[0], 16),
        "Length": int(bytes_data[1] + bytes_data[2], 16), 
        "FSPEC": bytes_data[3:9], 
        "SAC": bytes_data[9],  
        "SIC": bytes_data[10], 
        "Track Number": int(bytes_data[11] + bytes_data[12], 16),   
        "Time of Applicability of Position": int(bytes_data[13] + bytes_data[14] + bytes_data[15], 16) * (1/128),  
        "Latitude": int(bytes_data[16] + bytes_data[17] + bytes_data[18] + bytes_data[19], 16) * (180 / (2**30)),  
        "Longitude": int(bytes_data[20] + bytes_data[21] + bytes_data[22] + bytes_data[23], 16) * (180 / (2**30)),  
        "Time of Applicability of Velocity": int(bytes_data[24] + bytes_data[25] + bytes_data[26], 16) * (1/128),  
        "Target Address": int(bytes_data[27] + bytes_data[28] + bytes_data[29], 16),  
        "T\ime of Message Reception": int(bytes_data[30] + bytes_data[31] + bytes_data[32], 16) * (1/128),  
        "Geometric Height": int(bytes_data[33] + bytes_data[34], 16) * 6.25,  
        "Flight Level": int(bytes_data[35] + bytes_data[36], 16) * (1/4), 
        "Magnetic Heading": int(bytes_data[37] + bytes_data[38], 16) * (360 / (2**16)),  
        "Barometric Vertical Rate": int(bytes_data[39] + bytes_data[40], 16) * 6.25,  
        "Geometric Vertical Rate": int(bytes_data[41] + bytes_data[42], 16) * 6.25, 
        "Message Amplitude": int(bytes_data[43], 16) * 1  
    }

    return result   

def show_decoded_values():
    hex_packet = entry_hex.get()

    try:
        parsed_data = parse_packet(hex_packet)
        result_text.delete(1.0, tk.END)  
        for key, value in parsed_data.items():
            result_text.insert(tk.END, f"{key}: {value}\n")
    except ValueError as e:
        messagebox.showerror("Error", f"Error: {e}")

root = tk.Tk()
root.title("Hexadecimal Packet Decoder")

label = tk.Label(root, text="Enter Hexadecimal Packet:")
label.pack(pady=10)

entry_hex = tk.Entry(root, width=80)
entry_hex.pack(pady=5)

decode_button = tk.Button(root, text="Decode", command=show_decoded_values)
decode_button.pack(pady=10)

result_text = tk.Text(root, height=20, width=80)
result_text.pack(pady=5)
root.mainloop()
