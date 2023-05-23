# Import the required modules
import os
import re
from datetime import datetime
import argparse
import pdfplumber
import openpyxl

# Function to extract text from a PDF file
def extract_text_from_pdf(file_path):
    # Open the PDF file using pdfplumber
    with pdfplumber.open(file_path) as pdf:
        text = ''
        # Iterate through all the pages in the PDF
        for page in pdf.pages:
            # Extract text from each page and concatenate it
            text += page.extract_text()
    return text

# Function to extract text from plain text files
def extract_text_from_txt(file_path):
    # Open the file with utf-8 encoding and read its content
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Function to extract text from Excel files
def extract_text_from_xlsx(file_path):
    # Load the workbook in read-only mode
    workbook = openpyxl.load_workbook(file_path, read_only=True)
    text = ''
    # Iterate through all the sheets in the workbook
    for sheet in workbook:
        # Iterate through all the rows in each sheet
        for row in sheet.iter_rows():
            # Iterate through all the cells in each row
            for cell in row:
                # Check if the cell has a value
                if cell.value:
                    # Append the cell value to the text string
                    text += str(cell.value) + ' '
    return text

def extract_date_interval(text, regex_pattern):
    # Search for the pattern in the text
    match = re.search(regex_pattern, text, re.IGNORECASE)
    # If a match is found, return all groups as a tuple
    if match:
        return match.groups()
    # If no match is found, return None
    return None

# Function to extract text from a file based on its extension
def extract_text(file_path):
    # Get the file extension of the input file
    _, file_extension = os.path.splitext(file_path)
    # Determine the appropriate function to call based on the file extension
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension in ['.txt', '.md', '.rmd', '.quarto', '.yml', '.xml', '.tex', '.cls', '.py', '.r', '.docx', '.odt', '.ods', '.odf']:
        return extract_text_from_txt(file_path)
    elif file_extension == '.xlsx':
        return extract_text_from_xlsx(file_path)
    else:
        # Return None if the file type is unsupported
        return None
        # Raise an error if the file type is unsupported
        #raise ValueError(f'Unsupported file type: {file_extension}')
    
# Function to rename the file based on the date interval and custom prefix
def rename_file(file_path, groups, custom_prefix):
    # Define the date format used in the groups
    date_format = "%d/%m/%Y"
    # Initialize a list for the new parts of the filename
    new_parts = []
    # Loop over each group in the groups
    for group in groups:
        # Convert the date to the required format and append it to new_parts
        new_parts.append(datetime.strptime(group, date_format).strftime('%Y%m%d'))
    # Create the new file name using the custom prefix and groups
    new_name = f'{custom_prefix}-{"-".join(new_parts)}.pdf'
    # Rename the file with the new name
    os.rename(file_path, os.path.join(os.path.dirname(file_path), new_name))

# Main function to process all files in a folder
def process_files(folder_path, regex_pattern, custom_prefix):
    # Iterate through all the files in the folder
    for file_name in os.listdir(folder_path):
        # Get the full file path
        file_path = os.path.join(folder_path, file_name)
        print(f'Processing file: {file_name}')
        # Extract text from the file
        text = extract_text(file_path)
        if text is not None:
            print(f'Extracted text: {text[:100]}...')  # Print the first 100 characters of the text
            # Find the date interval in the extracted text
            date_interval = extract_date_interval(text, regex_pattern)
            print(f'Found date interval: {date_interval}')
            # Rename the file if a date interval is found
            if date_interval:
                rename_file(file_path, date_interval, custom_prefix)
                print(f'Renamed file: {file_name} -> {custom_prefix}-{date_interval[0].replace("/", "")}-{date_interval[1].replace("/", "")}.pdf')
            else:
                print(f'No date interval found in file: {file_name}')
        else:
            print(f'Skipping unsupported file type: {file_name}')

def get_user_input():
    try:
        folder_path = input("Enter the path to the folder containing the files to be processed: ")
        regex_pattern = input("Enter the regular expression pattern to search for in the files. Remember to use parentheses () to define the groups in your pattern: ")
        custom_prefix = input("Enter the custom prefix for the file names (default: 'file'): ") or 'file'
        return folder_path, regex_pattern, custom_prefix
    except KeyboardInterrupt:
        print("Exiting the program")  # Print empty line if Ctrl+C is pressed
        exit(0)  # Exit the program

def print_help_dialog():
    print('''
    Use --folder_path, --regex_pattern, and --custom_prefix
    to directly run the renaming process, SKIPPING
    INTEREACTIVE MODE like so: 'cbrename.py --folder_path
    <./path_to_folder> --regex_pattern <regex_pattern_here>
    --custom_prefix <my_prefix>'

    This script will rename all the files in the provided
    folder based on a regular expression pattern that you
    provide.
    You need to use parentheses () to define groups in
    your regular expression pattern. For example, if you
    want to extract two dates in the format dd/mm/yyyy
    separated by a hyphen, you can use the following regex
    pattern:
    (\d{2}/\d{2}/\d{4})-(\d{2}/\d{2}/\d{4})
    In this pattern, (\d{2}/\d{2}/\d{4}) captures the first
    date, and the second set of parentheses captures the
    second date. The hyphen - in the middle is a delimiter
    between the two dates.
    The script will then rename the files in the format:
    'chosen_prefix-group1-group2'
    or, if your regex pattern only contains one group, the
    files will be renamed as: 'chosen_prefix-group1'
    ''')

# A function to print examples of regex patterns
def print_regex_examples():
    print('''
    Here are some examples of regex patterns you could use:

    1. To extract a date in the format dd/mm/yyyy:
    \\d{2}/\\d{2}/\\d{4}

    2. To extract a date in the format dd-mm-yyyy:
    \\d{2}-\\d{2}-\\d{4}

    3. To extract a date in the format yyyy-mm-dd:
    \\d{4}-\\d{2}-\\d{2}

    4. To extract a time in the format HH:MM (24-hour format):
    \\d{2}:\\d{2}

    5. To extract two dates in the format dd/mm/yyyy separated by a hyphen:
    (\\d{2}/\\d{2}/\\d{4})-(\\d{2}/\\d{2}/\\d{4})

    6. To extract a US phone number in the format (ddd) ddd-dddd:
    \\(\\d{3}\\) \\d{3}-\\d{4}

    7. To extract an email address:
    [\\w.-]+@[\\w.-]+\\.\\w+

    8. To extract a URL:
    http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))

    9. To extract an IP address:
    \\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b

    10. To extract a MAC address:
    ([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})

    11. To extract a social security number (SSN):
    \\d{3}-\\d{2}-\\d{4}

    12. To extract a credit card number:
    (?:4[0-9]{12}(?:[0-9]{3})?          # Visa
    |  (?:5[1-5][0-9]{2}                # MasterCard
    |  222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}
    |  3[47][0-9]{13}                   # American Express
    |  3(?:0[0-5]|[68][0-9])[0-9]{11}   # Diners Club
    |  6(?:011|5[0-9]{2})[0-9]{12}      # Discover
    |  (?:2131|1800|35\\d{3})\\d{11})   # JCB

    Remember to always enclose your groups in parentheses.
    ''')

def main():
    try:
        parser = argparse.ArgumentParser(description='''
This script uses regex patterns (text) inside the files
in a selected folder to rename them. Run the script with
--instructions for a detailed guide.
                        ''')
        parser.add_argument('--instructions', action='store_true', help='Print the detailed help dialog with instructions.')
        parser.add_argument('--examples', action='store_true', help='Print a list of regex examples to help with finding the patterns you need to match.')
        parser.add_argument('--folder_path', default=None, help='Path to the folder containing the files to be processed.')
        parser.add_argument('--regex_pattern', default=None, help='Regular expression pattern to search for in the files.')
        parser.add_argument('--custom_prefix', default='file', help='Custom prefix for the file names. (default: "file")')

        args = parser.parse_args()

        if args.instructions:
            print_help_dialog()
        elif args.examples:
            print_regex_examples()
        else:
            if args.folder_path is None or args.regex_pattern is None:
                print('''
This script uses regex patterns (text) inside the files
in a selected folder to rename them. Run the script with
--help to see its usage, with --instructions for a
detailed guide, with '--examples' to print a list of regex
examples to help with finding the patterns you need to match.
                        ''')
                while True:
                    user_choice = input('''
Do you want to continue (Y),
get instructions (I),
get examples (E),
or exit (N)? (default=Y): ''')
                    user_choice = user_choice.lower()

                    if user_choice == '' or user_choice == 'y':
                        folder_path, regex_pattern, custom_prefix = get_user_input()
                        process_files(folder_path, regex_pattern, custom_prefix)
                        break
                    elif user_choice == 'n':
                        print("Exiting the program.")
                        break
                    elif user_choice == 'i':
                        print_help_dialog()
                    elif user_choice == 'e':
                        print_regex_examples()
                    else:
                        print("Invalid input! Please enter either 'Y' (continue), 'I' (instructions), or 'N' (exit).")
            else:
                process_files(args.folder_path, args.regex_pattern, args.custom_prefix)

    except KeyboardInterrupt:
        print("Exiting the program")  # Print empty line if Ctrl+C is pressed
        exit(0)  # Exit the program

if __name__ == "__main__":
    main()