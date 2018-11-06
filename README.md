# PDFToJSON - PDF to JSON Convertor

This utility converts a pdf file into a JSON. This JSON follows the hierarchy of the sections and subsections of the pdf.

## Usage:

Change the input filename in configuration.py and run `python pdf_extraction.py`.

### The utility has the following requirements:
1. If the pdf file contains a well-formatted table of contents (that can be read by pyPDF2), it will be used.
2. If there is no such table of contents, the user has to fill up the regular expression in the *configuration.py* file that helps in recognizing the table of contents.
3. If no such regular expression is provided, it does extractive text summarization (Luhn's algorithm as implemented in sumy) to find concise statements that are most likely to be section headings.

### The limitations of the utility are:
1. It requires the heading to be on a separate line and cannot process files where headings are embedded in the paragraph.
2. In all situations but the first two mentioned above, the section-subsection hierarchy will not be preserved.

