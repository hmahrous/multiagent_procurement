import json
import re
from markdown2 import markdown
import pdfkit
import os

# Ensure DISPLAY environment variable is set
os.environ["DISPLAY"] = ":0"  # Adjust if necessary

# Step 1: Read and Parse the JSON File
file_path = 'big_software_process_new_request.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Step 2: Infer Sections and Subsections
def infer_structure(text):
    sections = re.split(r'\n\n(\d+\.\s+)', text)
    structured_text = ""
    section_number = 1

    for section in sections:
        if section.isdigit():
            structured_text += f"# Section {section_number}\n"
            section_number += 1
        else:
            subsections = re.split(r'\n\t(\d+\.\s+)', section)
            subsection_number = 1
            for subsection in subsections:
                if subsection.isdigit():
                    structured_text += f"## Subsection {subsection_number}\n"
                    subsection_number += 1
                else:
                    subsection = re.sub(r'\n\t•\t', '\n- ', subsection)
                    subsection = re.sub(r'\n\t', '\n', subsection)
                    structured_text += subsection + "\n"

    return structured_text

# Convert JSON to structured Markdown text
markdown_content = ""
for entry in data:
    for key, value in entry.items():
        if key.isdigit():
            markdown_content += f"# {key}. {value}\n\n"
        else:
            markdown_content += infer_structure(value)

# Step 3: Convert Markdown to HTML
html_content = markdown(markdown_content)

# Step 4: Configure pdfkit
config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')  # Adjust the path as necessary

# Step 5: Generate PDF from HTML
pdf_path = 'big_software_process_new_request.pdf'
pdfkit.from_string(html_content, pdf_path, configuration=config)

print(f"PDF successfully created at: {pdf_path}")
