# To extract texts from PDF, Scanned, and Image files

import pytesseract
import fitz
from PIL import Image
from pdf2image import convert_from_path

from qa_robot.constants import *


def clean_text(text):
    text = text.replace('\n', '')
    text = text.replace('\xa0', '')
    
    return text



def extract_text_from_file(file_path, file_type):
    if file_type == 'pdf':
        text_page_list = convert_pdf_to_text(file_path)
    elif file_type == 'scanned':
        text_page_list = convert_scanned_to_text(file_path)
    elif file_type == 'image':
        text_page_list = convert_image_to_text(file_path)
    else:
        text_page_list = convert_txt_to_text(file_path)

    return text_page_list


def convert_pdf_to_text(file_path):
    """
    Extract text from each page of a PDF file.

    Parameters:
    - file_path (str): The path to the PDF file from which to extract text.

    Returns:
    - list of str: A list containing the extracted text from each page of the PDF.
    """
    text_page_list = []
    with fitz.open(file_path) as doc:
        for idx, page in enumerate(doc.pages()):
            text = page.get_text()
            text = clean_text(text)
            text_page_list.append((idx, text))

    return text_page_list

def convert_txt_to_text(file_path):
    """
    Extract text from each page of a TXT file.

    Parameters:
    - file_path (str): The path to the PDF file from which to extract text.

    Returns:
    - list of str: A list containing the extracted text from each page of the TXT.
    """
    text_page_list = []
    with open(file_path,'r') as file:
        page_num = 1
        for line in file:
            if line.strip():
                text = line.strip()
                text = clean_text(text)
                text_page_list.append((page_num, text))
                page_num += 1

    return text_page_list

def convert_scanned_to_text(file_path):
    """
    Convert scanned document pages to text using OCR.

    Parameters:
    - file_path (str): The path to the scanned document (PDF) from which to extract text.

    Returns:
    - list of str: A list containing the extracted text from each page of the scanned document.
    """
    pages = convert_from_path(file_path, 300)  # dpi=300 for better OCR accuracy
    text_page_list = []
    for idx, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        text = clean_text(text)
        text_page_list.append((idx, text))
    return text_page_list


def convert_image_to_text(file_path):
    """
    Extract text from an image file using OCR.

    Parameters:
    - file_path (str): The path to the image file from which to extract text.

    Returns:
    - list of str: A list containing the extracted text from the image, wrapped in a list for consistency.
    """
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    text = clean_text(text)
    return [(0, text)]


def split_pdf(input_pdf_path, start_page, end_page):
    basename = os.path.basename(input_pdf_path)
    basename = basename.split('.')[0]
    output_pdf_path = f'{TEMP_FOLDER}{basename}_{start_page}_{end_page}.pdf'

    # Open the source PDF.
    doc = fitz.open(input_pdf_path)
    
    # Create a new PDF to write the selected pages.
    writer = fitz.open()

    # Iterate through the specified range of pages and add them to the new document.
    for page_num in range(start_page, end_page + 1):
        # Ensure the page number is within the total number of pages in the document.
        if page_num < doc.page_count:
            page = doc.load_page(page_num)
            writer.insert_pdf(page.parent, from_page=page_num, to_page=page_num)

    # Save the new PDF to the specified output path.
    writer.save(output_pdf_path)
    writer.close()
    doc.close()

    return output_pdf_path


def check_if_pdf_has_too_much_pages(pdf_file_path):

    page_number = 0
    try: 
        doc = fitz.open(pdf_file_path)
        page_number = doc.page_count
    except:
        pass

    if page_number > PAGES_THRESHOLD_TO_BREAK:
        return True, page_number
    else:
        return False, page_number