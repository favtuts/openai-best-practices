import os, sys
import time
from datetime import datetime

import re


import pandas as pd
import openpyxl
from openpyxl.utils import get_column_letter

import streamlit as st

from qa_robot.gemini_engin import generate_text_from_text_file
from qa_robot.create_prompt import *

from qa_robot.constants import *


def get_basename(path):
    return os.path.splitext(os.path.basename(path))[0]

def custom_parse_qa(text):
    # Split the entire text by "question": (ignoring the very first split if it's empty)
    segments = [seg for seg in text.split('"question":') if seg.strip()]
    
    faqs = []
    for segment in segments:
        # Further split each segment by "answer":
        parts = segment.split('"answer":')
        question = parts[0].strip()
        answer = parts[1].strip() if len(parts) > 1 else ""
        
        # Append the parsed question and answer, cleaning up as necessary
        faqs.append({
            'question': question.replace('"', ''),
            'answer': answer.replace('"', '')
        })
    
    return faqs
def convert_text_to_faq_dataframe(text):
    
    # Initialize an empty DataFrame with columns for questions and answers
    faq_df = pd.DataFrame(columns=['question', 'answer'])

    faq_list = custom_parse_qa(text)

    # Convert the list of dictionaries to a DataFrame
    faq_df = pd.DataFrame(faq_list)

    if not faq_df.empty:
        # Removing rows where the combination of all column values is duplicated
        faq_df = faq_df.drop_duplicates(subset=['question'], keep='first')

        # Reset the index of the DataFrame and drop the old index
        faq_df = faq_df.reset_index(drop=True)

    return faq_df

def save_to_excel_with_format(faq_df, basename):
    # Create a folder named with basename if it doesn't exist
    if not os.path.exists(OUTPUT_PATH + basename):
        os.makedirs(OUTPUT_PATH + basename)
    output_folder = OUTPUT_PATH + basename
    #add time stamp to file name
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    basename = f'{basename}_{timestamp}'

    excel_file_path = f'{output_folder}/{basename}_faq.xlsx'
    # To fix the format
    # Specify your column widths here (in units of characters)
    column_widths = {'question': 65, 'answer': 75, 'page': 8, 'document': 50}

    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        faq_df.to_excel(writer, index=False)
        
        # Access the openpyxl workbook and sheet objects
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']
        
        # Set column widths and text wrap
        for column, width in column_widths.items():
            col_idx = faq_df.columns.get_loc(column) + 1  # Convert column name to Excel column index (1-based)
            column_letter = get_column_letter(col_idx)
            worksheet.column_dimensions[column_letter].width = width

            # Apply text wrap to each cell in the column
            for row in worksheet[column_letter]:
                row.alignment = openpyxl.styles.Alignment(wrapText=True, vertical='center')

    return excel_file_path


def find_text_index_frequency(answer, text_page_list):
    answer_words = answer.split()

    max_common_count = 0
    answer_index = -1  # Default to -1 if no text is found
    for index in range(len(text_page_list)):
        text = text_page_list[index][1]
        text_words = text.split()
        # Count how many times words in answer appear in the text
        common_words_count = sum(word in text_words for word in answer_words)
        if common_words_count > max_common_count:
            max_common_count = common_words_count
            answer_index = index

    return answer_index+1
    

def add_answer_sources(faq_df, text_page_list, filename, from_page, to_page):
    # Add the 'page' column by applying the function
    faq_df['page'] = faq_df['answer'].apply(lambda ans: find_text_index_frequency(ans, text_page_list))

    faq_df['page'] = faq_df['page'].apply(lambda x: f"{from_page}-{to_page}" if x == -1 else str(x + from_page))

    # Add column with filename
    faq_df['document'] = filename

    return faq_df

def clean_text(text):
    text = text.replace('\\n', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('\n0', '0')
    text = text.replace('\t', ' ')
    text = text.replace('\\t', ' ')
    text = text.replace('\u2013', '')
    text = text.replace('\u2019', '')
    
    # Remove ',' at the end
    if text.endswith(','):
        text = text[:-1]

    # text = re.sub(r'\\u[0-9a-fA-F]{4}', decode_unicode_escape, text)
    
    return text

# Generate FAQ
def generate_faq_from_pdf(file_path, instruction, target_language, is_scanned):
    qa_df = None
    file_type = 'pdf'
    if is_scanned:
        file_type = 'scanned'

    generated_text, text_page_list = generate_text_from_text_file(file_path, file_type, instruction, target_language)

    generated_text = clean_text(generated_text)

    qa_df = convert_text_to_faq_dataframe(generated_text)

    return qa_df, text_page_list

def generate_faq_from_txt(file_path, instruction, target_language):
    qa_df = None
    file_type = 'txt'

    generated_text, text_page_list = generate_text_from_text_file(file_path, file_type, instruction, target_language)

    generated_text = clean_text(generated_text)

    qa_df = convert_text_to_faq_dataframe(generated_text)

    return qa_df, text_page_list

def process_input_text_file(file_path, file_type, instruction, target_language, page_from, page_to, is_scanned):
    basename = os.path.basename(file_path)
    prompt = create_prompt(instruction, target_language)

    qa_df = None

    if file_type == 'pdf':
        qa_df, text_page_list = generate_faq_from_pdf(file_path, prompt, target_language, is_scanned)
    else:
        qa_df, text_page_list = generate_faq_from_txt(file_path, prompt, target_language)
    
    if not qa_df.empty:
        qa_df = add_answer_sources(qa_df, text_page_list, basename, page_from, page_to)
    
    return qa_df



# Main 
if __name__ == '__main__':
    file_path = sys.argv[1]
    file_type = sys.argv[2]

    target_language = sys.argv[3]

    from_page = int(sys.argv[4])
    to_page = int(sys.argv[5])

    instruction = instruction_to_generate_qa_lists_from_text_vi

    print(f"\n\nGenerate FAQ from file: {file_path}")
    
    qa_df = process_input_text_file(file_path, file_type, instruction, target_language, from_page, to_page, is_scanned=False)
    
    print(qa_df)
    print(f"\n\nGenerate FAQ ... Done\n\n")



        