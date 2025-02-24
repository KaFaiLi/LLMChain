import os
import csv
import fitz  # PyMuPDF for PDF processing
import cv2
import pytesseract
import re

# Uncomment and modify this if Tesseract is not in your system's PATH:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def pdf_to_images(pdf_path, output_folder):
    """
    Converts a multi-page PDF to images and saves them.
    Returns a list of saved image file paths.
    """
    print(f"Debug: Starting pdf_to_images with pdf_path: {pdf_path}, output_folder: {output_folder}") # Debug print
    doc = fitz.open(pdf_path)
    images = []
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]  # Get PDF file name without extension
    print(f"Debug: PDF '{pdf_path}' opened, number of pages: {doc.page_count}") # Debug print

    for i, page in enumerate(doc):
        print(f"Debug: Processing page {i+1} of PDF '{pdf_path}'") # Debug print
        pix = page.get_pixmap()
        img_path = os.path.join(output_folder, f"{pdf_name}_page_{i+1}.png")
        print(f"Debug: Saving page {i+1} as image to: {img_path}") # Debug print
        pix.save(img_path)  # Save image
        images.append(img_path)
    print(f"Debug: Finished converting PDF '{pdf_path}' to images. Total images saved: {len(images)}") # Debug print
    return images

def preprocess_image(image_path):
    """
    Enhances an image for better OCR accuracy.
    - Converts to grayscale
    - Denoises the image
    - Applies adaptive thresholding
    """
    print(f"Debug: Starting preprocess_image with image_path: {image_path}") # Debug print
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read {image_path}")
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print(f"Debug: Image converted to grayscale") # Debug print
    gray = cv2.bilateralFilter(gray, 9, 75, 75)  # Denoising
    print(f"Debug: Image denoised using bilateral filter") # Debug print
    processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, 11, 2)  # Improve contrast
    print(f"Debug: Image processed with adaptive thresholding") # Debug print
    print(f"Debug: Finished preprocess_image for {image_path}") # Debug print
    return processed

def extract_transaction_info(text):
    """
    Extracts transaction details from OCR text using regex.
    """
    print(f"Debug: Starting extract_transaction_info with text: \n-----\n{text}\n-----") # Debug print
    sender_pattern = r"送信者\s*[:\-]\s*(.+)"  # Sender (送信者)
    receiver_pattern = r"受信者[s]?\s*[:\-]\s*(.+)"  # Receiver (受信者)
    amount_pattern = r"金額\s*[:\-]\s*¥?([\d,]+\.?\d*)"  # Amount (金額)
    date_pattern = r"(?:日付|取引日)\s*[:\-]\s*([\d]{4}[-/][\d]{1,2}[-/][\d]{1,2})"  # Date (日付/取引日)

    sender = re.search(sender_pattern, text, re.IGNORECASE)
    receiver = re.search(receiver_pattern, text, re.IGNORECASE)
    amount = re.search(amount_pattern, text, re.IGNORECASE)
    date = re.search(date_pattern, text, re.IGNORECASE)

    sender_value = sender.group(1).strip() if sender else ""
    receiver_value = receiver.group(1).strip() if receiver else ""
    amount_value = amount.group(1).strip() if amount else ""
    date_value = date.group(1).strip() if date else ""

    print(f"Debug: Extracted Sender: '{sender_value}', Receiver: '{receiver_value}', Amount: '{amount_value}', Date: '{date_value}'") # Debug print
    return (
        sender_value,
        receiver_value,
        amount_value,
        date_value
    )

def process_documents(input_folder, image_output_folder, output_csv):
    """
    Processes all PDFs in the input folder:
    - Converts PDFs to images
    - Enhances images using OpenCV
    - Extracts text using OCR (Tesseract)
    - Parses transaction details using regex
    - Saves results to a CSV file
    """
    print(f"Debug: Starting process_documents with input_folder: {input_folder}, image_output_folder: {image_output_folder}, output_csv: {output_csv}") # Debug print
    os.makedirs(image_output_folder, exist_ok=True)  # Ensure output folder exists
    print(f"Debug: Image output folder '{image_output_folder}' created or already exists.") # Debug print

    with open(output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Original File", "Page Image", "Sender", "Receiver", "Amount", "Transaction Date", "Raw OCR Output"])
        print(f"Debug: CSV file '{output_csv}' opened for writing.") # Debug print

        for filename in os.listdir(input_folder):
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(input_folder, filename)
                print(f"Processing PDF file: {filename}") # Keep original print for user info
                print(f"Debug: Full PDF path: {pdf_path}") # Debug print

                # Convert PDF to images
                image_paths = pdf_to_images(pdf_path, image_output_folder)
                print(f"Debug: Number of images generated from PDF '{filename}': {len(image_paths)}") # Debug print

                for img_path in image_paths:
                    print(f"Debug: Processing image: {img_path}") # Debug print
                    processed_img = preprocess_image(img_path)
                    if processed_img is None:
                        print(f"Debug: preprocess_image returned None for {img_path}, skipping OCR.") # Debug print
                        continue

                    # Perform OCR with Japanese language
                    print(f"Debug: Starting OCR on {img_path}...") # Debug print
                    text = pytesseract.image_to_string(processed_img, lang='jpn')
                    print(f"Debug: OCR completed for {img_path}. Text length: {len(text)}") # Debug print
                    # print(f"Debug: OCR Output: \n-----\n{text}\n-----") # Print raw OCR text if needed for very detailed debug

                    # Extract relevant transaction details
                    print(f"Debug: Extracting transaction info from OCR text for {img_path}...") # Debug print
                    sender, receiver, amount, date = extract_transaction_info(text)

                    # Save results to CSV, including the raw OCR output
                    writer.writerow([filename, img_path, sender, receiver, amount, date, text])
                    print(f"Debug: Wrote data to CSV for {img_path}") # Debug print

                    print(f"Extracted from {img_path}: Sender='{sender}', Receiver='{receiver}', Amount='{amount}', Date='{date}'") # Keep original print for user info

                print(f"Debug: Finished processing PDF file: {filename}") # Debug print
        print(f"Debug: Finished processing all PDF files in input folder.") # Debug print
    print("Transaction data extraction complete. Results saved to", output_csv) # Keep original print for user info

if __name__ == "__main__":
    input_folder = "path/to/pdf_folder"  # Change to your actual folder path
    image_output_folder = "path/to/output_images"  # Folder where images will be saved
    output_csv = "transaction_data.csv"

    print(f"Debug: Input folder: {input_folder}") # Debug print
    print(f"Debug: Image output folder: {image_output_folder}") # Debug print
    print(f"Debug: Output CSV file: {output_csv}") # Debug print
    process_documents(input_folder, image_output_folder, output_csv)
    print("Transaction data extraction process completed.") # More explicit completion message
