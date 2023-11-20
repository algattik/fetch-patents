#!/usr/bin/env python

import sys
import re
from pathlib import Path
import glob
import time


import pandas as pd
from htmldocx import HtmlToDocx
from patent_client import Patent


# Define parameters
year_pattern = "????"
max_num = 10000

# Check if the required command-line argument is provided
if len(sys.argv) != 2:
    print("Argument expected: name of assignee")
    sys.exit(1)

assignee_filter = sys.argv[1]

# Create directories if they don't exist
Path("markers").mkdir(exist_ok=True)
Path("docx").mkdir(exist_ok=True)
Path("html").mkdir(exist_ok=True)

# Concatenate data from CSV files matching the specified pattern
file_pattern = f"index/{year_pattern}.csv"
frames = [pd.read_csv(f, usecols=['patent_number', 'assignee'], dtype={'patent_number': 'string'}) for f in sorted(glob.glob(file_pattern))]
if not frames:
    print(f"CSV files not found: {file_pattern}. Run download-index.sh first.")
    sys.exit(1)

df = pd.concat(frames, ignore_index=True)
print(f"Loaded {len(df)} patents")

# Define a function to process each patent
def process(patent_number):
    marker_file = Path(f"markers/{patent_number}.done")

    # Skip processing if a marker file already exists for the patent
    if marker_file.exists():
        return

    # Delay API call to avoid throttling
    time.sleep(10)

    # Retrieve patent information using the patent number
    try:
      patent_object = Patent.objects.get(patent_number)
    except Exception as e:
      print(f"Error retrieving patent information for {patent_number}: {e}")
      return

    # Print the patent ID for debugging purposes
    print(patent_object.guid)

    # Generate a valid filename for the document
    filename = re.sub(r'[^\w .-]', '_', f"{patent_object.guid} {patent_object.patent_title}")

    # Create HTML content for the document
    html_content = f"<h1>{patent_object.guid} {patent_object.patent_title}</h1>\n\n<p>{patent_object.document.brief_html}</p>"

    # Write HTML content to a file
    with open(f"html/{filename}.html", 'w') as file:
        file.write(html_content)

    # Convert HTML content to a Word document and save it
    HtmlToDocx().parse_html_string(html_content).save(f"docx/{filename}.docx")

    # Create a marker file to indicate that processing is complete for this patent
    marker_file.touch()

# Filter the DataFrame based on the assignee and select the top n rows
filtered_df = df[df.assignee.str.contains(assignee_filter, case=False, na=False)].head(max_num)

print(f"Downloading {len(filtered_df)} patents")

# Process the selected patents
for patent_number in list(filtered_df.patent_number):
  process(patent_number)
