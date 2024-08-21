import os
import base64
import streamlit as st


from constants import *

# Read a file
def read_file(file_path):
    """
    Reads and returns the content of a file in binary mode.

    This function is designed to read a file's content into memory and should be used with caution
    when dealing with very large files to avoid memory issues.

    Parameters:
    - file_path (str): The path to the file to be read.

    Returns:
    - bytes: The content of the file in binary form.
    """
    with open(file_path, "rb") as file:
        return file.read()


def create_download_link(file_to_download, file_type, saved_filename, text):
    """
    Create a download link for a file, allowing it to be downloaded from a web page.

    Parameters:
    - file_to_download (str or bytes): The file to be downloaded. This can be a path to a file (str) or the binary data of the file (bytes).
    - file_type (str): The MIME type of the file, used for the browser to handle the file correctly. Example: 'application/pdf' for PDF files.
    - saved_filename (str): The filename to suggest when the user downloads the file. This does not have to match the original filename.
    - text (str): The text to be displayed as the download link.

    Returns:
    - str: An HTML anchor (<a>) element as a string that constitutes the download link. When clicked, it will download the file with the provided `saved_filename` and display the given `text`.

    Note:
    - If `file_to_download` is a string, the function assumes it's a file path, opens the file in binary read mode, and reads its content.
    - If `file_to_download` is already binary data (bytes), it uses it directly.
    """
    # Determine if the input is a file path and read the file, if necessary
    if isinstance(file_to_download, str):
        with open(file_to_download, "rb") as file:
            data = file.read()
    else:
        # Assume the input is already the binary data
        data = file_to_download

    # Encode the file data
    encoded_data = base64.b64encode(data).decode()

    # Create and return the download link HTML element
    return f'<a href="data:{file_type};base64,{encoded_data}" download="{saved_filename}">{text}</a>'


def upload_files(upload_folder, allowed_types, accept_multiple=False, max_files = None):
    """
    Upload files using Streamlit and save them to the specified folder. Supports both single and multiple file uploads.

    Parameters:
    - upload_folder (str): The path to the folder where uploaded files should be saved.
    - allowed_types (list): A list of allowed file types for the upload.
    - accept_multiple (bool): Whether to accept multiple files for upload.

    Returns:
    - A list of paths to the uploaded files, or an empty list if no files were uploaded.
    """
    st.subheader(f"Choose files (max = {max_files})")
    uploaded_files = st.file_uploader(f" ", type=allowed_types, accept_multiple_files=accept_multiple)
    saved_files_paths = []

    if uploaded_files is not None:
        uploaded_files = [uploaded_files] if not accept_multiple else uploaded_files  # Ensure consistency in handling
        if len(uploaded_files) > max_files:
            st.warning(f"Max File Upload = {max_files}. Only the first {max_files} files will be processed.")
            uploaded_files = uploaded_files[:max_files]
        for uploaded_file in uploaded_files:
            # Create a file path in the upload folder
            temp_file_path = os.path.join(upload_folder, uploaded_file.name)
            # Write the uploaded file to the new file path
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            saved_files_paths.append(temp_file_path)
    
    return saved_files_paths


