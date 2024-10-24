# comparators/metadata_comparator.py

from PyPDF2 import PdfReader

def extract_metadata(file_path):
    reader = PdfReader(file_path)
    metadata = reader.metadata
    return metadata

def compare_metadata(file1, file2):
    metadata1 = extract_metadata(file1)
    metadata2 = extract_metadata(file2)
    differences = {}

    # Объединяем все ключи метаданных из обоих документов
    all_keys = set(metadata1.keys()).union(set(metadata2.keys()))
    for key in all_keys:
        value1 = metadata1.get(key)
        value2 = metadata2.get(key)
        if value1 != value2:
            differences[key] = (value1, value2)

    return differences
