# import tkinter as tk
# from tkinter import messagebox
# from tkinter import ttk

# def parse_packet(hex_string):
#     # Remove any potential spaces or unwanted characters in the input
#     hex_string = hex_string.replace(" ", "").strip()

#     # Ensure the hex string has an even length
#     if len(hex_string) % 2 != 0:
#         raise ValueError("Hexadecimal string has an odd number of characters.")

#     # Convert the hex string into a list of bytes
#     bytes_data = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]

#     # Ensure the packet has enough bytes to prevent index errors
#     if len(bytes_data) < 44:
#         raise ValueError("Hexadecimal packet is too short for the expected fields")

#     # Parse the fields based on the byte positions you described
#     result = {
#         "Category": int(bytes_data[0], 16),
#         "Length": int(bytes_data[1] + bytes_data[2], 16),  
#         "FSPEC": bytes_data[3:9], 
#         "SAC": bytes_data[9], 
#         "SIC": bytes_data[10], 
#         "Track No": 1,  
#         "Time of Applicability of Position": int(bytes_data[13] + bytes_data[14] + bytes_data[15], 16) * (1/128),  
#         "Latitude": int(bytes_data[16] + bytes_data[17] + bytes_data[18] + bytes_data[19], 16) * (180 / (2**30)),  
#         "Longitude": int(bytes_data[20] + bytes_data[21] + bytes_data[22] + bytes_data[23], 16) * (180 / (2**30)), 
#         "Target Address": 1, 
#         "Time of Message Reception": int(bytes_data[30] + bytes_data[31] + bytes_data[32], 16) * (1/128), 
#         "Geometric Height": int(bytes_data[33] + bytes_data[34], 16) * 6.25,  
#         "Flight Level": int(bytes_data[35] + bytes_data[36], 16) * (1/4), 
#         "Magnetic Heading": int(bytes_data[37] + bytes_data[38], 16) * (360 / (2**16)), 
#         "Barometric Vertical Rate": int(bytes_data[39] + bytes_data[40], 16) * 6.25, 
#         "Geometric Vertical Rate": int(bytes_data[41] + bytes_data[42], 16) * 6.25,  
#         "Message Amplitude": int(bytes_data[43], 16) * 1 
#     }

#     return result

# def show_decoded_values():
#     hex_packet = entry_hex.get()

#     try:
#         parsed_data = parse_packet(hex_packet)
       
#         result_text.delete(1.0, tk.END) 
#         for key, value in parsed_data.items():
#             result_text.insert(tk.END, f"{key}: {value}\n")
#     except ValueError as e:
#         messagebox.showerror("Error", f"Error: {e}")

# def clear_input():
#     entry_hex.delete(0, tk.END)
#     result_text.delete(1.0, tk.END)


# root = tk.Tk()
# root.title("Circular Shaped Packet Decoder")

# root.geometry("500x500")
# root.config(bg="white")


# canvas = tk.Canvas(root, width=500, height=500, bg="white", bd=0, highlightthickness=0)
# canvas.pack()


# canvas.create_oval(25, 25, 475, 475, fill="#2C3E50", outline="#1ABC9C", width=5)


# frame = tk.Frame(root, bg="white", bd=0)
# frame.place(relx=0.5, rely=0.5, anchor="center")


# header_label = tk.Label(frame, text="Enter Hexadecimal Packet:", font=("Helvetica", 14, "bold"), fg='#ECF0F1', bg='#2C3E50')
# header_label.pack(pady=10)

# entry_hex = tk.Entry(frame, width=50, font=("Helvetica", 12), bg='#34495E', fg='#ECF0F1', relief="flat")
# entry_hex.pack(pady=10)


# button_frame = tk.Frame(frame, bg='#2C3E50')
# button_frame.pack(pady=10)

# decode_button = tk.Button(button_frame, text="Decode", command=show_decoded_values, font=("Helvetica", 12), fg='#2C3E50', bg='#1ABC9C', relief="flat", width=15)
# decode_button.pack(side="left", padx=10)

# clear_button = tk.Button(button_frame, text="Clear", command=clear_input, font=("Helvetica", 12), fg='#2C3E50', bg='#E74C3C', relief="flat", width=15)
# clear_button.pack(side="left", padx=10)


# result_frame = tk.Frame(frame, bg='#2C3E50')
# result_frame.pack(pady=10)

# result_text = tk.Text(result_frame, height=10, width=50, font=("Helvetica", 12), bg='#34495E', fg='#ECF0F1', wrap=tk.WORD, relief="flat")
# result_text.pack(side="left")

# scrollbar = tk.Scrollbar(result_frame, command=result_text.yview)
# scrollbar.pack(side="right", fill="y")
# result_text.config(yscrollcommand=scrollbar.set)


# root.mainloop()

import tkinter as tk
from tkinter import messagebox
import turtle

def parse_packet(hex_string):
    """Parse a hexadecimal packet and return a dictionary of decoded values."""
    hex_string = hex_string.replace(" ", "").strip()
    
    if len(hex_string) % 2 != 0:
        raise ValueError("Hexadecimal string has an odd number of characters.")
    
    bytes_data = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
    
    if len(bytes_data) < 44:
        raise ValueError("Hexadecimal packet is too short for the expected fields")
    
    result = {
        "Category": int(bytes_data[0], 16),
        "Length": int(bytes_data[1] + bytes_data[2], 16),  
        "FSPEC": bytes_data[3:9], 
        "SAC": bytes_data[9], 
        "SIC": bytes_data[10], 
        "Track No": 1,  
        "Time of Applicability of Position": int(bytes_data[13] + bytes_data[14] + bytes_data[15], 16) * (1/128),  
        "Latitude": int(bytes_data[16] + bytes_data[17] + bytes_data[18] + bytes_data[19], 16) * (180 / (2**30)),  
        "Longitude": int(bytes_data[20] + bytes_data[21] + bytes_data[22] + bytes_data[23], 16) * (180 / (2**30)), 
        "Target Address": 1, 
        "Time of Message Reception": int(bytes_data[30] + bytes_data[31] + bytes_data[32], 16) * (1/128), 
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
        
        # Now draw the circle with latitude and longitude on the turtle window
        latitude = parsed_data["Latitude"]
        longitude = parsed_data["Longitude"]
        
        draw_circle(latitude, longitude)
        
    except ValueError as e:
        messagebox.showerror("Error", f"Error: {e}")

def clear_input():
    entry_hex.delete(0, tk.END)
    result_text.delete(1.0, tk.END)

def draw_circle(latitude, longitude):
    """Draw a circle using turtle and display latitude and longitude."""
    # Create a turtle screen object inside the tkinter canvas
    screen = turtle.TurtleScreen(canvas)
    
    # Create a turtle object
    t = turtle.Turtle()
    t.shape("turtle")
    t.speed(2)
    t.color("#1ABC9C")

    # Move the turtle to the starting position
    t.penup()
    t.goto(0, -150)  # Move turtle to the center of the circle
    t.pendown()

    # Draw a circle with radius 150
    t.circle(150)
    
    # Display Latitude and Longitude values on the turtle window
    t.penup()
    t.goto(0, 50)  # Position to show latitude and longitude
    t.pendown()
    t.write(f"Latitude: {latitude:.6f}", align="center", font=("Arial", 12, "normal"))
    
    t.penup()
    t.goto(0, 20)  # Position to show longitude
    t.pendown()
    t.write(f"Longitude: {longitude:.6f}", align="center", font=("Arial", 12, "normal"))
    
    t.hideturtle()

root = tk.Tk()
root.title("Circular Shaped Packet Decoder")

root.geometry("500x500")
root.config(bg="white")

# Create a Tkinter canvas for turtle drawing
canvas = tk.Canvas(root, width=500, height=500, bg="white", bd=0, highlightthickness=0)
canvas.pack()

# Create a frame for the UI elements
frame = tk.Frame(root, bg="white", bd=0)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Header Label
header_label = tk.Label(frame, text="Enter Hexadecimal Packet:", font=("Helvetica", 14, "bold"), fg='#ECF0F1', bg='#2C3E50')
header_label.pack(pady=10)

# Entry for Hexadecimal Packet
entry_hex = tk.Entry(frame, width=50, font=("Helvetica", 12), bg='#34495E', fg='#ECF0F1', relief="flat")
entry_hex.pack(pady=10)

# Buttons for Decode and Clear
button_frame = tk.Frame(frame, bg='#2C3E50')
button_frame.pack(pady=10)

decode_button = tk.Button(button_frame, text="Decode", command=show_decoded_values, font=("Helvetica", 12), fg='#2C3E50', bg='#1ABC9C', relief="flat", width=15)
decode_button.pack(side="left", padx=10)

clear_button = tk.Button(button_frame, text="Clear", command=clear_input, font=("Helvetica", 12), fg='#2C3E50', bg='#E74C3C', relief="flat", width=15)
clear_button.pack(side="left", padx=10)

# Text area to display results
result_frame = tk.Frame(frame, bg='#2C3E50')
result_frame.pack(pady=10)

result_text = tk.Text(result_frame, height=10, width=50, font=("Helvetica", 12), bg='#34495E', fg='#ECF0F1', wrap=tk.WORD, relief="flat")
result_text.pack(side="left")

scrollbar = tk.Scrollbar(result_frame, command=result_text.yview)
scrollbar.pack(side="right", fill="y")
result_text.config(yscrollcommand=scrollbar.set)

# Run the main loop
root.mainloop()

