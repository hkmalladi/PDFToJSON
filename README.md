# PDFToJSON - PDF to JSON Convertor

This utility converts a pdf file into a JSON. This JSON follows the hierarchy of the sections and subsections of the pdf.

## Usage:

Change the input filename in configuration.py and run `python pdf_extraction.py`.

The utility is developed using Python 2.7 and will also work with Python 3 with minimal changes. It uses the following libraries.
`re, anytree, string. copy, PyPDF2, os, pdfminer`. It also uses the `pdftotext` utility from pdfminer to convert the pdf file into a text file.

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

### Visualization
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
├── Keep your Surface up to date
├── Get online
│   └── BROWSING TIPS
├── Accounts and signing in
│   ├── USE THE SIGN-IN SCREEN
│   ├── USE WINDOWS HELLO TO SIGN IN
│   └── SIGN OUT
├── Get to know Windows 10
│   ├── GO TO START
│   ├── ACTION CENTER
│   ├── SEARCH
│   ├── TASK VIEW AND VIRTUAL DESKTOPS
│   └── SETTINGS
├── Type Cover for Surface Pro 4 keyboard and touchpad
├── Storage and OneDrive
│   └── ONEDRIVE
│       └── Save files you're working on to OneDrive
├── Surface Pen and OneNote
│   ├── SURFACE PEN FEATURES
│   ├── PAIR THE PEN WITH YOUR SURFACE
│   ├── TRY OUT FEATURES BUILT IN TO THE TOP BUTTON OF THE PEN
│   └── GET ACQUAINTED WITH ONENOTE
│       └── Send a page or share a notebook
├── Connect monitors, accessories, and other devices
│   ├── SET UP YOUR WORKSPACE WITH SURFACE DOCK
│   └── CONNECT OR PROJECT TO A MONITOR, SCREEN, OR OTHER DISPLAY
├── Cameras and the Camera app
│   └── VIEW PHOTOS AND VIDEOS
├── Apps on your Surface Pro 4
│   ├── THE SURFACE APP
│   └── GET MORE APPS
├── Personalization and settings
│   ├── WINDOWS SETTINGS
│   ├── ACTION CENTER
│   ├── CORTANA
│   ├── SURFACE APP
│   ├── SYNC YOUR SETTINGS
│   └── CHANGE SETTINGS IN WINDOWS APPS
├── Accessibility
│   ├── EASE OF ACCESS OPTIONS FOR SURFACE
│   ├── OTHER OPTIONS
│   └── CUSTOMIZE THE SIGN-IN SCREEN
├── Care and cleaning
│   ├── TOUCHSCREEN CARE
│   ├── COVER AND KEYBOARD CARE
│   └── POWER CORD CARE
├── Registration, repair, and warranty
│   ├── REGISTER YOUR SURFACE
│   ├── REPAIR
│   ├── WARRANTY
│   └── SAFETY AND REGULATORY INFORMATION
└── More help
```

## Inner Workings:

This utility works in 4 basic steps:
1. Extract the table of contents from the pdf file.
2. Construct a tree using the headings that preserve the section-subsection relationships.
3. Iterate over all the headings and search for them in the file. All the text following it, till the next heading is its corresponding content. Construct a heading - content map.
4. Use the tree generated in step 2 and the map from step 3 to assemble the JSON.

At present, LSA based text summarization is used. A configuration parameter enables several other algorithms to be used. The threshold for the number of statements in the summary is set to 500. Out of these, only short, standalone sentences that don't end up in a fullstop are used as headings. On the surface-pro-4-user-guide-EN.pdf file, it demonstrated decent precision and recall.

## Work to be done:

The ultimate general case can be approached using a trained classifier. No such classifier exists that will work for this particular usecase. A classifier using naive bayes or KNN, trained on a LaTeX-generated pdf document dataset (using the pyPDF2-extracted headings) can be used to train the model. The fact that pyPDF2 can effectively identify headings in LaTeX-generated documents greatly simplifies data preprocessing efforts.
