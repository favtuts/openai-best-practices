import pandas as pd
import os
import glob
import sys

from faq_engin import save_to_excel_with_format

# Assuming OUTPUT_PATH is defined in your 'constants.py'
from constants import OUTPUT_PATH

# Example usage: python script.py input_folder output_file.xlsx
input_folder = sys.argv[1]
output_file = sys.argv[2]

# Building the path for all xlsx files in the input_folder
all_files = glob.glob(os.path.join(input_folder, "*.xlsx"))

# Concatenating all found DataFrames into one
# Note the use of brackets [] around the generator expression for pd.concat
df = pd.concat([pd.read_excel(file) for file in all_files])

# Saving the concatenated DataFrame to an Excel file without the index
save_to_excel_with_format(df, output_file)
