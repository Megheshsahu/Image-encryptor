import tkinter as tk
from tkinter import filedialog, simpledialog

def choose_file(title="Select File", root=None):
    if root is None:
        root = tk.Tk()
        root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(title=title)

    return file_path

def choose_save_file(title="Save Encrypted Image As", defaultextension=".png", filetypes=[("PNG files", "*.png")], root=None):
    if root is None:
        root = tk.Tk()
        root.withdraw()  # Hide the main window

    file_path = filedialog.asksaveasfilename(defaultextension=defaultextension, filetypes=filetypes, title=title)

    return file_path

def get_encryption_key():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    encryption_key = simpledialog.askstring("Input", "Enter the encryption key:")
    
    root.destroy()  # Close the root window

    return encryption_key.encode('utf-8') if encryption_key else None

def encrypt_image(input_path, output_path, key):
    try:
        with open(input_path, 'rb') as f:
            image_data = bytearray(f.read())

        # XOR each byte of the image data with the corresponding byte of the key
        encrypted_data = bytes(image_byte ^ key_byte for image_byte, key_byte in zip(image_data, key * (len(image_data) // len(key) + 1)))

        with open(output_path, 'wb') as f:
            f.write(encrypted_data)

        print("Encryption is done.")
    except Exception as e:
        print(f"Encryption failed: {e}")

def decrypt_image(input_path, output_path, key):
    try:
        with open(input_path, 'rb') as f:
            encrypted_data = bytearray(f.read())

        # XOR each byte of the encrypted data with the corresponding byte of the key
        decrypted_data = bytes(encrypted_byte ^ key_byte for encrypted_byte, key_byte in zip(encrypted_data, key * (len(encrypted_data) // len(key) + 1)))

        with open(output_path, 'wb') as f:
            f.write(decrypted_data)

        print("Decryption is done.")
    except Exception as e:
        print(f"Decryption failed: {e}")

# Create the root window (Tk) once
root = tk.Tk()
root.withdraw()  # Hide the main window

# Choose input image file interactively
input_image_path = choose_file("Select Input Image", root)

# Check if a file was chosen
if not input_image_path:
    print("No file chosen.")
    root.destroy()  # Close the root window
    exit()

# Choose output image file interactively
output_image_path = choose_save_file("Save Encrypted Image As", root=root)

# Check if a file was chosen
if not output_image_path:
    print("No output file chosen.")
    root.destroy()  # Close the root window
    exit()

# Get user input for the encryption key
encryption_key = get_encryption_key()

# Check if the user provided an encryption key
if encryption_key is None:
    print("No encryption key provided. Exiting.")
    root.destroy()  # Close the root window
    exit()

# Example usage
encrypt_image(input_image_path, output_image_path, encryption_key)
# For decryption, use decrypt_image instead
# decrypt_image(input_image_path, output_image_path, encryption_key)

# Close the root window
root.destroy()
