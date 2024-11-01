import fitz
from PIL import Image
import os
import pytesseract
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

# ------------------------------------------- Pick PDF -------------------------------------------

def select_pdf():
    pdf_path = filedialog.askopenfilename(
        title="Select PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )
    pdf_entry.delete(0, tk.END)
    pdf_entry.insert(0, pdf_path)

# ------------------------------------------- Pick PDF -------------------------------------------


# ------------------------------------------- Path -------------------------------------------

def select_output_folder():
    folder_path = filedialog.askdirectory(title="Select Output Folder")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, folder_path)

# ------------------------------------------- Path -------------------------------------------


# ------------------------------------------- Process PDF -------------------------------------------

def process_pdf():
    pdf_path = pdf_entry.get()
    output_folder = output_entry.get()
    if not pdf_path or not output_folder:
        messagebox.showerror("Error", "Please provide both the PDF file path and output folder.")
        return

    try:
        os.makedirs(output_folder, exist_ok=True)
        document = fitz.open(pdf_path)
        text_brackets = []
        for page_num in range(document.page_count):
            page = document[page_num]
            zoom = 2.0
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            output_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
            img.save(output_path, "PNG")
            print(f"Saved page {page_num + 1} as {output_path}")
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            extracted_text = pytesseract.image_to_string(img)
            text_brackets.append(extracted_text)
            os.remove(output_path)
            print(f"Deleted image: {output_path}")
        text_file_path = os.path.join(output_folder, "extracted_text.txt")
        with open(text_file_path, "w", encoding="utf-8") as text_file:
            for page_index, text in enumerate(text_brackets, start=1):
                text_file.write(f"Text from Page {page_index}:\n{text}\n\n")
        subprocess.Popen(["notepad.exe", text_file_path])
        messagebox.showinfo("Success", "PDF processed and OCR text extracted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# ------------------------------------------- Process PDF -------------------------------------------


# ------------------------------------------- Interface -------------------------------------------

ascii_cat = r"""
 /\_/\  
( o.o ) 
 > ^ <  
"""

root = tk.Tk()
root.title("PDF OCR Extractor")
root.geometry("500x560")
root.configure(bg="#FFEBEE")
tk.Label(root, text="PDF OCR Extractor", bg="#FFEBEE", font=("Helvetica Neue", 18, "bold"), fg="#C2185B").pack(pady=10)
tk.Label(root, text=ascii_cat, bg="#FFEBEE", font=("Courier New", 14), fg="#880E4F", justify=tk.LEFT).pack(pady=10)
tk.Label(root, text="PDF File Path:", bg="#FFEBEE", font=("Helvetica Neue", 12), fg="#880E4F").pack(pady=5)
pdf_entry = tk.Entry(root, width=50, font=("Helvetica Neue", 12), bd=2, relief=tk.SUNKEN)
pdf_entry.pack(pady=5)
tk.Button(root, text="Browse PDF", bg="#E91E63", fg="white", font=("Helvetica Neue", 12), padx=10, pady=5, command=select_pdf).pack(pady=5)
tk.Label(root, text="Output Folder:", bg="#FFEBEE", font=("Helvetica Neue", 12), fg="#880E4F").pack(pady=5)
output_entry = tk.Entry(root, width=50, font=("Helvetica Neue", 12), bd=2, relief=tk.SUNKEN)
output_entry.pack(pady=5)
tk.Button(root, text="Browse Folder", bg="#E91E63", fg="white", font=("Helvetica Neue", 12), padx=10, pady=5, command=select_output_folder).pack(pady=5)
tk.Button(root, text="Process PDF", bg="#4CAF50", fg="white", font=("Helvetica Neue", 14), padx=20, pady=10, command=process_pdf).pack(pady=20)
root.mainloop()


# ------------------------------------------- Interface -------------------------------------------
