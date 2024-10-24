# comparators/text_comparator.py

from PyPDF2 import PdfReader

def extract_text(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def compare_text(file1, file2):
    text1 = extract_text(file1)
    text2 = extract_text(file2)
    return text1 == text2
