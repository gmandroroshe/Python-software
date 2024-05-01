import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from PIL import ImageTk, Image

def generate_qr_code():
    data = entry.get()  # Get the input from the entry field
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Resize the image for display
    img = img.resize((200, 200), Image.ANTIALIAS) if hasattr(Image, 'ANTIALIAS') else img.resize((200, 200))

    # Convert the image to a format that tkinter can display
    qr_img = ImageTk.PhotoImage(img)

    # Display the QR code image on the GUI
    qr_code_label.config(image=qr_img)
    qr_code_label.image = qr_img

    # Display a message box indicating the QR code generation is successful
    messagebox.showinfo("QR Code Generated", "QR Code has been generated successfully!")

    # Return the PIL image data
    return img

def save_qr_code():
    # Generate the QR code image
    img = generate_qr_code()

    # Ask the user to select the file path for saving the QR code image
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

    if file_path:
        # Save the image to the specified file path
        img.save(file_path)
        messagebox.showinfo("QR Code Saved", f"QR Code has been saved successfully to:\n{file_path}")

# Create the main application window
root = tk.Tk()
root.title("QR Code Generator")

# Create a label
label = tk.Label(root, text="Enter comma-separated values:")
label.pack()

# Create an entry field
entry = tk.Entry(root)
entry.pack()

# Create a button to generate the QR code
generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr_code)
generate_button.pack()

# Create a button to save the QR code
save_button = tk.Button(root, text="Save QR Code", command=save_qr_code)
save_button.pack()

# Create a label to display the QR code image
qr_code_label = tk.Label(root)
qr_code_label.pack()

# Run the main event loop
root.mainloop()
