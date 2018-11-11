# PDFToJSON - PDF to JSON Convertor

This utility converts a pdf file into a JSON. This JSON follows the hierarchy of the sections and subsections of the pdf.

## Usage:

Change the input filename in configuration.py and run `python pdf_extraction.py`.

The utility is developed using Python 2.7 and will also work with Python 3 with minimal changes. It uses the following libraries.
`re, sumy, anytree, string. copy, PyPDF2, os, poppler`. It also uses the `pdftotext` utility from poppler to convert the pdf file into a text file.

### The utility has the following requirements:
1. If the pdf file contains a well-formatted table of contents (that can be read by pyPDF2), it will be used.
2. If there is no such table of contents, the user has to fill up the regular expression in the *configuration.py* file that helps in recognizing the table of contents.
3. If no such regular expression is provided, it does extractive text summarization to find concise statements that are most likely to be section headings. In this case, it makes the following assumptions about headings to eliminate noise.
    a. Headings are on new lines and do not end in a fullstop.
    b. Headings are less than 50 characters long (configurable parameter).
    c. Headings start with a capital letter.
    d. Headings don't repeat.

### The limitations of the utility are:
1. It requires the heading to be on a separate line and cannot process files where headings are embedded in the paragraph.
2. In all situations but the first two mentioned above, the section-subsection hierarchy will not be preserved.

### The utility handles the following:
1. The headings can differ from the table of contents in case and punctuation marks such as colons or periods.
2. The heading can be split in two lines in the document.
3. The heading can have any preceeding or trailing spaces or new lines.
4. The case of the content is well preserved.

### Output

When the tool is run on the surface-pro-4-user-guide-EN.pdf file, the following JSON output is generated:

```
[{"About this guide":["This guide is designed to get you up and running with the key features of your new Surface Pro 4..."]},{"Meet Surface Pro 4":["Get acquainted with the features built in to your Surface Pro 4...."]},{"Set up your Surface Pro 4":["",{"CHARGE YOUR SURFACE PRO 4":["    1. Connect the two parts of the power cord.
    2. Connect the power cord securely to the charging port.
    3. Plug the power supply into an electrical outlet...."]},
....

,{"REPAIR":["Before sending your Surface in for service, you can check out the Surface troubleshooting articles on Surface.com. If you can't solve the problem with troubleshooting, contact us through Surface.com. ...."]},{"WARRANTY":["For warranty info, see Surface warranty and Surface warranty documents on Surface.com."]},{"SAFETY AND REGULATORY INFORMATION":["See Safety and regulatory information on Surface.com."]}]}]
```

The section-subsection hierarchy of the headings can be visualized using the following code snippet. This uses anytree's RenderTree function to render the tree.

```
from utilities import *
# Create the tree using any of the other functions. Alternatively, insert this code wherever the need to visualize the tree arises.
print_tree(tree)
```

When this is run on the surface-pro-4-user-guide-EN.pdf file, the output is the following:

```
ROOT
├── About this guide
├── Meet Surface Pro 4
├── Set up your Surface Pro 4
│   ├── CHARGE YOUR SURFACE PRO 4
│   ├── CONNECT THE COVER
│   └── SET UP YOUR SURFACE PRO 4
├── The basics
│   ├── POWER AND CHARGING
│   │   ├── Check the battery level
│   │   ├── Lock screen
│   │   ├── Desktop taskbar
│   │   └── Make your battery last
│   └── TOUCH, KEYBOARD, PEN, AND MOUSE
...
```

## Inner Workings:

This utility works in 4 basic steps:
1. Extract the table of contents from the pdf file.
2. Construct a tree using the headings that preserve the section-subsection relationships.
3. Iterate over all the headings and search for them in the file. All the text following it, till the next heading is its corresponding content. Construct a heading - content map.
4. Use the tree generated in step 2 and the map from step 3 to assemble the JSON.

At present, LSA based text summarization is used. A configuration parameter enables several other algorithms to be used. The threshold for the number of statements in the summary is set to 500. Out of these, only short, standalone sentences that don't end up in a fullstop are used as headings. On the surface-pro-4-user-guide-EN.pdf file, it demonstrated decent precision and recall.

## Ongoing Work:

A naive bayes classifier is being trained using a 200 document dataset from arXiv. This dataset has been acquired using a scraper code from this repository. As the arXiv documents are well formatted, their headings and contents can easily be extracted using this tool. Features such as the presence of a fullstop, sentence length in characters and words, number of vowels in the sentence and the presence of numbers are used to train the classifier. 
