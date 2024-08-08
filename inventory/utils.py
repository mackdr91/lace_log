import os
import qrcode

def generate_qr_code(sneaker):
    # Define the path to the QR code file
    qr_code_path = f'static/qr_codes/{sneaker.id}.png'

    # Delete the existing QR code file if it exists
    if os.path.exists(qr_code_path):
        os.remove(qr_code_path)

    # Collect the sneaker details
    details = f"Name: {sneaker.name}\n"
    details += f"Brand: {sneaker.brand}\n"
    details += f"Price: ${sneaker.price}\n"
    details += f"Release Date: {sneaker.release_date}\n"
    details += f"Is New: {'Yes' if sneaker.is_new else 'No'}\n"
    if sneaker.purchase_date:
        details += f"Purchase Date: {sneaker.purchase_date}\n"
    if sneaker.color:
        details += f"Color: {sneaker.color}\n"
    if sneaker.location:
        details += f"Location: {sneaker.location}\n"
    if sneaker.description:
        details += f"Description: {sneaker.description}\n"

    # Include sizes and quantities
    details += "Sizes and Quantities:\n"
    for variation in sneaker.variations.all():
        details += f"  - Size: {variation.size}, Quantity: {variation.quantity}\n"

    # Generate the QR code with the detailed text
    qr = qrcode.make(details)

    # Save the QR code image (overwrite if it exists)
    qr.save(qr_code_path)