# pdf_compare.py

import argparse
from comparators import metadata_comparator
from comparators import text_comparator
from comparators import image_hash_comparator

def main():
    parser = argparse.ArgumentParser(description="Сравнение PDF-документов на оригинальность")
    parser.add_argument('file1', help='Путь к первому PDF-файлу')
    parser.add_argument('file2', help='Путь ко второму PDF-файлу')
    parser.add_argument('--metadata', action='store_true', help='Сравнить метаданные документов')
    parser.add_argument('--text', action='store_true', help='Сравнить текстовое содержимое')
    parser.add_argument('--images', action='store_true', help='Сравнить изображения в документах')

    args = parser.parse_args()

    total_similarity = 0
    modules_used = 0

    if args.metadata:
        similarity, differences = metadata_comparator.compare_metadata(args.file1, args.file2)
        total_similarity += similarity
        modules_used += 1
        print(f"Метаданные совпадают на {similarity:.2f}%")
        if differences:
            print("Различия в метаданных:")
            for key, (val1, val2) in differences.items():
                print(f"{key}:")
                print(f"  Файл 1: {val1}")
                print(f"  Файл 2: {val2}")
    else:
        similarity = None

    if args.text:
        similarity, differences = text_comparator.compare_text(args.file1, args.file2)
        total_similarity += similarity
        modules_used += 1
        print(f"Текстовое содержимое совпадает на {similarity:.2f}%")
        if differences:
            print("Текстовое содержимое различается. Различия:")
            print(differences)
    else:
        similarity = None

    if args.images:
        similarity, differences = image_hash_comparator.compare_image_hashes(args.file1, args.file2)
        total_similarity += similarity
        modules_used += 1
        print(f"Изображения совпадают на {similarity:.2f}%")
        if differences:
            print("Найдены различия в изображениях:")
            for idx, hash_value in differences:
                print(f"  Изображение {idx + 1} в первом файле не имеет соответствия во втором файле. Хэш: {hash_value}")
    else:
        similarity = None

    if modules_used > 0:
        overall_similarity = total_similarity / modules_used
        print(f"\nОбщая метрика соответствия: {overall_similarity:.2f}%")
    else:
        print("Не выбрано ни одного метода сравнения.")

if __name__ == "__main__":
    main()
