# comparators/text_comparator.py

from PyPDF2 import PdfReader
import difflib

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
    # print(text1)
    # print(text2)
    
    if text1 == text2:
        return True, None
    else:
        diff = difflib.unified_diff(
            text1.splitlines(keepends=True),
            text2.splitlines(keepends=True),
            fromfile='Файл 1',
            tofile='Файл 2',
            lineterm=''
        )
        differences = ''.join(diff)
        return False, differences
