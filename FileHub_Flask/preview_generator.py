import os
from io import BytesIO

import comtypes.client
import docx
import fitz  # PyMuPDF
from PIL import Image


def get_pdf_preview(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)  # 第一页
    pix = page.get_pixmap()
    img = Image.open(BytesIO(pix.tobytes()))
    preview_path = pdf_path + "_preview.png"
    img.save(preview_path)
    return preview_path


def get_doc_preview(doc_path):
    doc = docx.Document(doc_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
        if len(' '.join(text)) > 50:
            break
        preview_text = ' '.join(text)[:50]
        preview_path = doc_path + "_preview.txt"
        with open(preview_path, 'w', encoding='utf-8') as file:
            file.write(preview_text)
            return preview_path


def pptx_to_jpg(pptx_path, output_folder):
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    deck = powerpoint.Presentations.Open(pptx_path)
    slide = deck.Slides[0]
    slide.Export(os.path.join(output_folder, "slide1.jpg"), "JPG", 1920, 1080)
    deck.Close()
    powerpoint.Quit()

    return os.path.join(output_folder, "slide1.jpg")


def generate_preview(file_path):
    """
    Generate a preview for the given file based on its type.

    :param file_path: The path to the file
    :return: The path to the generated preview file
    """
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() in ['.pdf']:
        return get_pdf_preview(file_path)
    elif file_extension.lower() in ['.doc', '.docx']:
        return get_doc_preview(file_path)
    elif file_extension.lower() in ['.ppt', '.pptx']:
        return pptx_to_jpg(file_path, os.path.dirname(file_path))
    else:
        return None  # Return None if no preview is available for the file type
