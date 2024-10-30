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
    
    sm = difflib.SequenceMatcher(None, text1, text2)
    similarity = sm.ratio() * 100  # Процентное значение

    # Получаем различия в формате списка операций
    opcodes = sm.get_opcodes()
    changes_in_file1 = []

    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'replace' or tag == 'delete' or tag == 'insert':
            # Добавляем только изменения из загружаемого документа (file1)
            changed_text = text1[i1:i2]
            changes_in_file1.append(changed_text)

    # Формируем строку с изменениями, не раскрывая содержимое оригинала
    differences = "\n".join(changes_in_file1)

    return similarity, differences
