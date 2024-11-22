import os
import tkinter as tk
from tkinter import filedialog
import PyPDF2
import re
import json
from drive_integration import list_drive_files, download_file

# Function to convert PDF to text and append to vault.txt
def convert_pdf_to_text(file_path):
    if file_path.endswith(".pdf"):
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            text = ''
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                if page.extract_text():
                    text += page.extract_text() + " "

            # Normalize whitespace and clean up text
            text = re.sub(r'\s+', ' ', text).strip()

            # Split text into chunks by sentences, respecting a maximum chunk size
            sentences = re.split(r'(?<=[.!?]) +', text)
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 < 1000:  # +1 for the space
                    current_chunk += (sentence + " ").strip()
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:
                chunks.append(current_chunk)

            # Append chunks to vault.txt
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    vault_file.write(chunk.strip() + "\n")
            print(f"PDF content from '{file_path}' appended to vault.txt.")

# Function to upload a text file and append to vault.txt
def upload_txtfile(file_path):
    if file_path.endswith(".txt"):
        with open(file_path, 'r', encoding="utf-8") as txt_file:
            text = txt_file.read()

            # Normalize whitespace and clean up text
            text = re.sub(r'\s+', ' ', text).strip()

            # Split text into chunks by sentences, respecting a maximum chunk size
            sentences = re.split(r'(?<=[.!?]) +', text)
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 < 1000:  # +1 for the space
                    current_chunk += (sentence + " ").strip()
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:
                chunks.append(current_chunk)

            # Append chunks to vault.txt
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    vault_file.write(chunk.strip() + "\n")
            print(f"Text file content from '{file_path}' appended to vault.txt.")

# Function to upload a JSON file and append to vault.txt
def upload_jsonfile(file_path):
    if file_path.endswith(".json"):
        with open(file_path, 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)

            # Flatten the JSON data into a single string
            text = json.dumps(data, ensure_ascii=False)

            # Normalize whitespace and clean up text
            text = re.sub(r'\s+', ' ', text).strip()

            # Split text into chunks by sentences, respecting a maximum chunk size
            sentences = re.split(r'(?<=[.!?]) +', text)
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 < 1000:  # +1 for the space
                    current_chunk += (sentence + " ").strip()
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:
                chunks.append(current_chunk)

            # Append chunks to vault.txt
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    vault_file.write(chunk.strip() + "\n")
            print(f"JSON file content from '{file_path}' appended to vault.txt.")

# Function to download and process files from Google Drive
def download_and_process_drive_files():
    drive_files = list_drive_files()
    if drive_files:
        for file in drive_files:
            file_id = file['id']
            file_name = file['name']
            download_file(file_id, file_name)
            print(f"Downloaded file: {file_name}")
            # Process based on file type
            if file_name.endswith(".pdf"):
                convert_pdf_to_text(file_name)
            elif file_name.endswith(".txt"):
                upload_txtfile(file_name)
            elif file_name.endswith(".json"):
                upload_jsonfile(file_name)
            else:
                print(f"Unsupported file type: {file_name}")

# Create the main window for manual file upload
def create_gui():
    root = tk.Tk()
    root.title("Upload .pdf, .txt, or .json")

    # Button to upload PDF
    pdf_button = tk.Button(root, text="Upload PDF", command=lambda: convert_pdf_to_text(filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])))
    pdf_button.pack(pady=10)

    # Button to upload Text file
    txt_button = tk.Button(root, text="Upload Text File", command=lambda: upload_txtfile(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])))
    txt_button.pack(pady=10)

    # Button to upload JSON file
    json_button = tk.Button(root, text="Upload JSON File", command=lambda: upload_jsonfile(filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])))
    json_button.pack(pady=10)

    # Button to download and process files from Google Drive
    drive_button = tk.Button(root, text="Download and Process Drive Files", command=download_and_process_drive_files)
    drive_button.pack(pady=10)

    # Run the GUI loop
    root.mainloop()

if __name__ == "__main__":
    create_gui()
