import os


# Constants for file paths
UPLOAD_FOLDER = "./uploads/"
OUTPUT_PATH = './output/'
TEMP_FOLDER = './temp/'

PAGES_THRESHOLD_TO_BREAK = 15

HIGH_CONFIDENCE_THRESHOLD = 65
MEDIUM_CONFIDENCE_THRESHOLD = 50

ALLOWED_FILE_TYPES = ['pdf'] #['pdf', 'jpg', 'jpeg', 'png', 'webp']
MAX_FILE_UPLOAD = 1


if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)
else:
    for filename in os.listdir(TEMP_FOLDER):
        file_path = os.path.join(TEMP_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
else:
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
