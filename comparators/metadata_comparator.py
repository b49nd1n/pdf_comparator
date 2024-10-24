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
    matching_fields = 0
    total_fields = 0

    all_keys = set(metadata1.keys()).union(set(metadata2.keys()))
    total_fields = len(all_keys)

    for key in all_keys:
        value1 = metadata1.get(key)
        value2 = metadata2.get(key)
        if value1 == value2:
            matching_fields += 1
        else:
            differences[key] = (value1, value2)

    if total_fields == 0:
        similarity = 100.0
    else:
        similarity = (matching_fields / total_fields) * 100

    return similarity, differences
