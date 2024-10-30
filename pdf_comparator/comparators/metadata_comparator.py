# comparators/metadata_comparator.py

from PyPDF2 import PdfReader
import os


def extract_metadata(file_path):
    reader = PdfReader(file_path)
    metadata = reader.metadata
    # Получаем порядок ключей метаданных
    if hasattr(reader.metadata, 'raw'):
        metadata_order = list(reader.metadata.raw.keys())
    else:
        metadata_order = list(metadata.keys())
    return metadata, metadata_order

def get_file_size(file_path):
    return os.path.getsize(file_path)

def compare_metadata(file1, file2, allowable_size_difference=1024):
    # Извлекаем метаданные и порядок ключей
    metadata1, order1 = extract_metadata(file1)
    metadata2, order2 = extract_metadata(file2)
    differences = {}
    matching_fields = 0
    total_fields = 0

    # Сравнение размеров файлов
    size1 = get_file_size(file1)
    size2 = get_file_size(file2)
    size_difference = abs(size1 - size2)

    size_within_limit = size_difference <= allowable_size_difference  # Допустимое изменение в байтах

    # Сравнение порядка метаданных
    order_matching = order1 == order2

    # Сравнение значений метаданных
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
        metadata_similarity = 100.0
    else:
        metadata_similarity = (matching_fields / total_fields) * 100

    # Учитываем все метрики в общей метрике соответствия
    total_similarity = (metadata_similarity * 0.8)  # Вес значений метаданных - 80%
    if size_within_limit:
        total_similarity += 10  # Вес размера файла - 10%
    if order_matching:
        total_similarity += 10  # Вес порядка метаданных - 10%

    return total_similarity, {
        'size_comparison': {
            'size1': size1,
            'size2': size2,
            'size_difference': size_difference,
            'within_limit': size_within_limit,
            'allowable_difference': allowable_size_difference
        },
        'order_comparison': {
            'order1': order1,
            'order2': order2,
            'order_matching': order_matching
        },
        'metadata_differences': differences
    }


