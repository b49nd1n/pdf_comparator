# pdf_compare.py

import argparse
import html
from pdf_comparator.comparators import metadata_comparator
from pdf_comparator.comparators import text_comparator
from pdf_comparator.comparators import image_hash_comparator

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


# pdf_compare/pdf_compare.py

def compare_documents(file1, file2):
    from pdf_comparator.comparators import metadata_comparator
    from pdf_comparator.comparators import text_comparator
    from pdf_comparator.comparators import image_hash_comparator


    total_similarity = 0
    modules_used = 0

    similarity, _ = metadata_comparator.compare_metadata(file1, file2)
    total_similarity += similarity
    modules_used += 1

    similarity, _ = text_comparator.compare_text(file1, file2)
    total_similarity += similarity
    modules_used += 1

    similarity, _ = image_hash_comparator.compare_image_hashes(file1, file2)
    total_similarity += similarity
    modules_used += 1

    overall_similarity = total_similarity / modules_used
    return overall_similarity

import re

def escape_markdown(text):
    # return text
    """
    Экранирует специальные символы в тексте для использования с MarkdownV2.
    """
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(r'([%s])' % re.escape(escape_chars), r'\\\1', text)

def compare_documents_detailed(file1, file2, allowable_size_difference=1024):
    from pdf_comparator.comparators import metadata_comparator
    from pdf_comparator.comparators import text_comparator
    from pdf_comparator.comparators import image_hash_comparator

    total_similarity = 0
    modules_used = 0
    detailed_info = ""

    # Сравнение метаданных
    similarity, metadata_details = metadata_comparator.compare_metadata(file1, file2, allowable_size_difference)
    total_similarity += similarity
    modules_used += 1
    detailed_info += f"<b>Метаданные совпадают на {similarity:.2f}%</b>\n\n"

    # Обработка результатов сравнения размеров файлов
    size_comp = metadata_details['size_comparison']
    size1 = size_comp['size1']
    size2 = size_comp['size2']
    size_difference = size_comp['size_difference']
    allowable_difference = size_comp['allowable_difference']

    detailed_info += f"<b>Сравнение размеров файлов:</b>\n"
    detailed_info += "<pre>\n"
    detailed_info += f"{'Параметр':<20} {'Ваш документ':<15} {'Оригинал':<15} {'Разница'}\n"
    detailed_info += f"{'-'*60}\n"
    detailed_info += f"{'Размер (байт)':<20} {size1:<15} {size2:<15} {size_difference}\n"
    detailed_info += "</pre>\n"
    if size_comp['within_limit']:
        detailed_info += f"Изменение размера в пределах допустимых {allowable_difference} байт\n\n"
    else:
        detailed_info += f"Изменение размера превышает допустимые {allowable_difference} байт\n\n"

    # Обработка результатов сравнения порядка метаданных
    order_comp = metadata_details['order_comparison']
    detailed_info += f"<b>Сравнение порядка метаданных:</b>\n"
    if order_comp['order_matching']:
        detailed_info += "Порядок метаданных совпадает\n\n"
    else:
        detailed_info += "Порядок метаданных различается\n\n"

    # Различия в метаданных
    differences = metadata_details['metadata_differences']
    if differences:
        detailed_info += "<b>Различия в метаданных:</b>\n"
        detailed_info += "<pre>\n"
        detailed_info += f"{'Ключ':<20} Ваш документ\n"
        detailed_info += f"{'-'*50}\n"
        for key, (val1, _) in differences.items():
            key_escaped = html.escape(str(key))
            val1_escaped = html.escape(str(val1))
            detailed_info += f"{key_escaped:<20} {val1_escaped}\n"
        detailed_info += "</pre>\n\n"

    # Сравнение текста
    similarity_text, differences_text = text_comparator.compare_text(file1, file2)
    total_similarity += similarity_text
    modules_used += 1
    detailed_info += f"<b>Текстовое содержимое совпадает на {similarity_text:.2f}%</b>\n"
    if differences_text:
        detailed_info += "<b>Изменения в вашем документе:</b>\n"
        differences_text_limited = differences_text[:1000]
        differences_text_escaped = html.escape(differences_text_limited)
        detailed_info += f"<pre>{differences_text_escaped}</pre>\n"
        if len(differences_text) > 1000:
            detailed_info += "...(изменения сокращены)\n"

    # Сравнение изображений
    similarity_image, differences_image = image_hash_comparator.compare_image_hashes(file1, file2)
    total_similarity += similarity_image
    modules_used += 1
    detailed_info += f"\n<b>Изображения совпадают на {similarity_image:.2f}%</b>\n"
    if differences_image:
        detailed_info += "Найдены различия в изображениях вашего документа.\n"

    overall_similarity = total_similarity / modules_used
    detailed_info += f"\n<b>Общая метрика соответствия: {overall_similarity:.2f}%</b>\n"

    return overall_similarity, detailed_info



if __name__ == "__main__":
    main()
