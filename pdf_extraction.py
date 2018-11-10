import re
from PyPDF2 import PdfFileReader
from configuration import *
from utilities import *
import os
from anytree import LevelOrderGroupIter, Node
from extractive_summarization import *


filename = FILENAME
reader = PdfFileReader(open(filename, 'rb'))

list_of_contents = []

os.system(PDFTOTEXTCONVERSION + filename )

remove_spaces_from_text_file(filename, NOSPACES_FILENAME)

toc = reader.outlines

if len(toc) == 0:
    if TOC_REGEXP == '':
        tree_of_headings, list_of_headings = summarization_based_heading_search()
    else:
        tree_of_headings, list_of_headings = regexp_based_heading_search()
else:
    tree_of_headings, list_of_headings = outlines_based_heading_search(toc)

with open(NOSPACES_FILENAME,'r') as file:
    list_of_contents = get_content_from_headings(list_of_headings, file)

heading_content_dict = create_heading_content_dict(list_of_contents, list_of_headings)

json_of_pdf = create_json(heading_content_dict, tree_of_headings)

print json_of_pdf

#print_title_content_list(list_of_contents, list_of_headings)
