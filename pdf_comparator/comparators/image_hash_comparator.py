# comparators/image_hash_comparator.py

import fitz  # PyMuPDF
from PIL import Image
import imagehash
import io

def extract_images(file_path):
    images = []
    with fitz.open(file_path) as doc:
        for page_index in range(len(doc)):
            page = doc[page_index]
            image_list = page.get_images(full=True)
            for img in image_list:
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                images.append(image)
    return images

def compute_image_hashes(images):
    hashes = []
    for img in images:
        hash_value = imagehash.average_hash(img)
        hashes.append(hash_value)
    return hashes

def compare_image_hashes(file1, file2):
    images1 = extract_images(file1)
    images2 = extract_images(file2)

    hashes1 = compute_image_hashes(images1)
    hashes2 = compute_image_hashes(images2)

    total_images = len(hashes1)
    if total_images == 0:
        similarity = 100.0  # Нет изображений для сравнения
        differences = []
        return similarity, differences

    matching_images = 0
    differences = []

    for idx, hash1 in enumerate(hashes1):
        found_match = False
        for hash2 in hashes2:
            if hash1 - hash2 <= 5:
                found_match = True
                matching_images += 1
                break
        if not found_match:
            differences.append((idx, hash1))

    similarity = (matching_images / total_images) * 100

    return similarity, differences
