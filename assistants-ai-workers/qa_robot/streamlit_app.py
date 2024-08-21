import streamlit as st
import os
import pandas as pd

from constants import TEMP_FOLDER, UPLOAD_FOLDER, ALLOWED_FILE_TYPES, MAX_FILE_UPLOAD
from faq_engin import process_input_text_file, save_to_excel_with_format
from qa_bot import get_answer
from extract_texts_from_file import check_if_pdf_has_too_much_pages, split_pdf
from create_prompt import instruction_to_generate_qa_lists_from_text_en, instruction_to_generate_qa_lists_from_text_vi
from streamlit_helpers import create_download_link, upload_files
from constants import PAGES_THRESHOLD_TO_BREAK


st.title("🤖 QA Document Robot")
st.write("Transform PDFs into Interactive Q&A Session, and downloadable Q&A Excel file")

# Simplified session state initialization
if 'init_done' not in st.session_state:
    st.session_state.update({
        'select_language': 'English', 'confirm_language': False, 'start_process': False,
        'is_scanned': False, 'start_qa': False, 'processing': False, 'messages': [], 'qa_df': None,
        'confirm_pages_slided': False, 'init_done': True
    })

def reset_session_state():
    st.session_state.update({
        'select_language': 'English', 'confirm_language': False, 'start_process': False,
        'is_scanned': False, 'start_qa': False, 'processing': False, 'messages': [], 'qa_df': None,
        'confirm_pages_slided': False
    })

uploaded_files = upload_files(UPLOAD_FOLDER, ALLOWED_FILE_TYPES, accept_multiple=False, max_files=MAX_FILE_UPLOAD)

# Ensure 'basename' and 'qa_df' are initialized
basename = ''
qa_df = None

if uploaded_files:
    uploaded_file = uploaded_files[0]
    basename_with_extension = os.path.basename(uploaded_file)
    basename, file_extension = os.path.splitext(basename_with_extension)
    file_extension = file_extension.lstrip('.').lower()
    file_path = uploaded_file

    st.session_state['is_scanned'] = st.checkbox('Is this a scanned document?')
    target_language = st.radio('Choose your preferred language for the Q&A session:', ('English', 'Vietnamese', 'French'), index=0, horizontal=True)
    st.session_state['select_language'] = target_language

    if st.button('Start process'):
        st.session_state['start_process'] = True

if st.session_state.get('start_process', False):
    instruction = instruction_to_generate_qa_lists_from_text_en
    if target_language == 'Vietnamese':
        instruction = instruction_to_generate_qa_lists_from_text_vi

    page_from, page_to = 1, PAGES_THRESHOLD_TO_BREAK  # Default values

    st.session_state['confirm_pages_slided'] = False
    if file_extension == 'pdf':
        is_too_long, page_number = check_if_pdf_has_too_much_pages(uploaded_file)
        if is_too_long:
            page_from, page_to = st.slider('Select the pages you want to process (< 20)', 1, page_number, (1, min(page_number, 20)))
            # Move the 'Confirm Pages' button outside the 'if is_too_long' condition to ensure it's always evaluated
            st.session_state['confirm_pages_slided'] = st.button('Confirm Pages')
            if st.session_state['confirm_pages_slided'] or not is_too_long:
                file_path = split_pdf(uploaded_file, page_from, page_to)
                st.session_state['confirm_pages_slided'] = True
        
        if st.session_state['confirm_pages_slided'] == True:
            with st.spinner('Processing...'):
                qa_df = process_input_text_file(file_path, instruction, target_language, st.session_state.get('is_scanned', False), page_from, page_to)
                st.session_state['start_process'] = False  # Resetting here to prevent re-entrance
        
        if st.session_state['confirm_pages_slided'] == False and not is_too_long:
            with st.spinner('Processing...'):
                qa_df = process_input_text_file(file_path, instruction, target_language, st.session_state.get('is_scanned', False), page_from, page_to)
                st.session_state['start_process'] = False  # Resetting here to prevent re-entrance
               
    # Resetting the start_process state to allow for new processing
    if qa_df is not None:
        st.session_state['qa_df'] = qa_df
        


if st.session_state['qa_df'] is not None:
    target_language = st.session_state['select_language']
    edited_qa_df = st.data_editor(st.session_state['qa_df'])
    
    if not edited_qa_df.empty:
        excel_file_path = save_to_excel_with_format(edited_qa_df, basename)
        saved_filename = basename + '_faq.xls'
        file_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        st.markdown(create_download_link(excel_file_path, file_type, saved_filename, 'Download Q&A Excel file'), unsafe_allow_html=True)

    if st.button('Start Q&A'):
        st.session_state['start_qa'] = True
        st.session_state['start_process'] = False

    if st.session_state['start_qa']:
        
        for message in st.session_state['messages']:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask your questions from PDF "):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                answers = get_answer(prompt, edited_qa_df, target_language)
                message_placeholder.markdown(answers[0])
    
            st.session_state.messages.append({"role": "assistant", "content": answers})

    st.write("======== ho.tuong.vinh@gmail.com ========")
    st.button("Re-start", on_click=reset_session_state)
