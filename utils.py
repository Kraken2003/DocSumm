from PyPDF2 import PdfReader 
import ocrmypdf
import tempfile
import os
import fitz  
#import time

def ocr_text(pdf_path):
    fd, temp_output_path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    ocrmypdf.ocr(pdf_path, temp_output_path, output_type='pdf', skip_text=True, deskew=True)

    with fitz.open(temp_output_path) as doc:
        extracted_text = "".join([page.get_text('text') for page in doc])

    os.remove(temp_output_path)
    return extracted_text

def conventional_text(path):
    document = PdfReader(path)
    text = ""
    for page in range(len(document.pages)):
        text += document.pages[page].extract_text()
    return text


#path = r'C:\Users\Prithvi\Desktop\PROJ2\sample.pdf'
#start_time = time.time()
#text = conventional_text(path)
#end_time = time.time()
#print(text)
#print(f"runtime was: {end_time-start_time}") 