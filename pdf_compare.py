# pdf_compare.py

import argparse
from comparators import metadata_comparator
from comparators import text_comparator  # Импортируем новый модуль

def main():
    parser = argparse.ArgumentParser(description="Сравнение PDF-документов на оригинальность")
    parser.add_argument('file1', help='Путь к первому PDF-файлу')
    parser.add_argument('file2', help='Путь ко второму PDF-файлу')
    parser.add_argument('--metadata', action='store_true', help='Сравнить метаданные документов')
    parser.add_argument('--text', action='store_true', help='Сравнить текстовое содержимое')  # Новый аргумент

    args = parser.parse_args()

    if args.metadata:
        differences = metadata_comparator.compare_metadata(args.file1, args.file2)
        if differences:
            print("Различия в метаданных:")
            for key, (val1, val2) in differences.items():
                print(f"{key}:")
                print(f"  Файл 1: {val1}")
                print(f"  Файл 2: {val2}")
        else:
            print("Метаданные совпадают.")

    if args.text:
        is_equal = text_comparator.compare_text(args.file1, args.file2)
        if is_equal:
            print("Текстовое содержимое совпадает.")
        else:
            print("Текстовое содержимое различается.")

if __name__ == "__main__":
    main()
