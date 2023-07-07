# ***CBRENAME*** (**Content-Based Renamer**)
A Python script for extracting and renaming files based on regex patterns in a specified folder.

## STILL EARLY...

**THIS IS A VERY EMBRYONIC VERSION OF A RENAMING SCRIPT I BUILT FOR PERSONAL USE. I'LL EDIT IT HERE AS I TEST FOR ITS ACTUAL FUNCTIONALITY WITH DIFFERENT FILE EXTENSIONS. AS OF NOW, IT WORKS WELL TO RENAME .PDF FILES CONTAINING GROUPS OF DATES TO BE USED WHEN RENAMING THEM FOR SORTING AND/OR STORING PURPOSES.**

**It may eventually be turned into a python module in the future. You will notice it here.**

### Python version

Written in `Python 3.10.9`

## Description

The Conbase Rename script is a Python program designed to help you rename multiple files in a directory based on Regular Expressions (regex). The script reads files, searches for specific patterns defined by the user in the form of regular expressions, and then renames the files based on the matched patterns.

It is especially useful when dealing with files that contain dates or other standardized data within their content, and these data need to be included in the file's name for sorting or other purposes.

## Features

- Support for *PDF*, *Text* (*.txt*, *.md*, *.rmd*, *.quarto*, *.yml*, *.xml*, *.tex*, *.cls*, .*py*, *.r*, *.docx*, *.odt*, *.ods*, *.odf*), and **Excel** (`.xlsx`) files.
- *Customizable regular expression pattern.*
- *Customizable file name prefix.*

## How it Works

The Conbase Rename script employs regular expressions to search and extract specific patterns from the content of the files in the specified directory.

For instance, I created this script because I had a folder containing a group of bills named after unclear alphanumeric strings, but I needed to sort them by date, from the older to the newer, so I picked a line which was similar for each of them "Periodo di fatturazione: dal [date in dd-mm-YYYY format] al [date in dd-mm-YYYY format]" (which means "Billing period: from [date in dd-mm-YYYY format] to [date in dd-mm-YYYY format]" in Italian) and used the following regex to match the line for each file: `Periodo di fatturazione: dal (\d{2}/\d{2}/\d{4}) al (\d{2}/\d{2}/\d{4})`. I eventually stumbled upon another similar group of bills which for some reason would not match that regex, so I had to use a more complex one: `Periodo di fatturazione:\s*dal\s*(\d{2}/\d{2}/\d{4})\s*al\s*(\d{2}/\d{2}/\d{4})`

For instance, if you need to extract a date interval in the format dd/mm/yyyy separated by a hyphen, you can use the following regex pattern:

```regex

(\d{2}/\d{2}/\d{4})-(\d{2}/\d{2}/\d{4})

```

Here, `(\d{2}/\d{2}/\d{4})` captures the first date, and the second set of parentheses captures the second date. The hyphen - in the middle is a delimiter between the two dates.

When a match is found, the first and second dates are returned as a tuple by the `extract_date_interval` function. If no match is found, the function returns None.

The script then uses these dates to rename the file with the help of the `rename_file` function. This function takes three arguments: the file path, the date interval (start and end dates), and a custom prefix for the new file name.

The renaming process follows the format "prefix-startdate-enddate.file_ext", where the start and end dates are in the "YYYYMMDD" format.

## Usage

1. Set the target directory containing the files to be processed.
2. Define the regular expression pattern to search for in the files.
3. Enter a custom prefix for the new file names.

These settings can be provided interactively, or passed as arguments when running the script.

### Interactive Mode

Run the script without any arguments to access the interactive mode:

```bash

python conbaserename.py

```

Follow the prompts to enter the directory path, regex pattern, and custom file prefix.

### Argument Mode

You can also pass these settings as arguments when running the script:

```bash

python conbaserename.py --folder_path./path_to_folder --regex_patternregex_pattern_here --custom_prefixmy_prefix

```

Replace `./path_to_folder` with your folder path, `regex_pattern_here` with your regex pattern, and `my_prefix` with your desired file prefix.

### Additional Features

- Use `--instructions` to print a detailed help dialog.
- Use `--examples` to print a list of example regex patterns.

## Notes

- Ensure that your regex pattern is correctly defined and captures the data you wish to include in the file name.
- The script renames the files in place, so make sure you have a backup if necessary.
- The regex pattern and the new file name prefix are case-sensitive.

## Dependencies (requirements)

The script requires the following Python libraries:

- `pdfplumber==0.9.0`
- `openpyxl==3.1.2`
