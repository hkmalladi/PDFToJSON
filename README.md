# PDFToJSON - PDF to JSON Convertor

This utility converts a pdf file into a JSON. This JSON follows the hierarchy of the sections and subsections of the pdf.

## Usage:

Change the input filename in configuration.py and run `python pdf_extraction.py`.

The utility is developed using Python 2.7 and will also work with Python 3 with minimal changes. It uses the following libraries.
`re, anytree, string. copy, PyPDF2, os, pdfminer`. It also uses the `pdftotext` utility from pdfminer to convert the pdf file into a text file.

### The utility has the following requirements:
1. If the pdf file contains a well-formatted table of contents (that can be read by pyPDF2), it will be used.
2. If there is no such table of contents, the user has to fill up the regular expression in the *configuration.py* file that helps in recognizing the table of contents.
3. If no such regular expression is provided, it does extractive text summarization (Luhn's algorithm as implemented in sumy) to find concise statements that are most likely to be section headings.

### The limitations of the utility are:
1. It requires the heading to be on a separate line and cannot process files where headings are embedded in the paragraph.
2. In all situations but the first two mentioned above, the section-subsection hierarchy will not be preserved.

### The utility is immune to the following:
1. The headings can differ from the table of contents in case and punctuation marks such as colons or periods.
2. The heading can be split in two lines in the document.
3. The heading can have any preceeding or trailing spaces or new lines.
4. The case of the content is well preserved.

### Visualization
The section-subsection hierarchy of the headings can be visualized using the following code snippet. This uses anytree's RenderTree function to render the tree.

```
from utilities import *
# Create the tree using any of the other functions. Alternatively, insert this code wherever the need to visualize the tree arises.
print_tree(tree)
```

When this is run on the surface-pro-4-user-guide-EN.pdf file, the output is the following:

```

```

## Inner Workings:

This utility works in 4 basic steps:
1. Extract the table of contents from the pdf file.
2. Construct a tree using the headings that preserve the section-subsection relationships.
3. Iterate over all the headings and search for them in the file. All the text following it, till the next heading is its corresponding content. Construct a heading - content map.
4. Use the tree generated in step 2 and the map from step 3 to assemble the JSON.
