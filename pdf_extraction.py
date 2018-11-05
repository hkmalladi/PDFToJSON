import re
from PyPDF2 import PdfFileReader
from configuration import *
from utilities import *
import os
import anytree
#from anytree import Node, RenderTree, AsciiStyle

filename = FILENAME
reader = PdfFileReader(open(filename, 'rb'))

toc = reader.outlines
list_of_headings = []
list_of_contents = []

pattern = re.compile(TOC_REGEXP)

os.system('pdftotext -layout -nopgbrk -enc ASCII7 -q ' + filename )

with open(os.path.splitext(filename)[0] + '.txt','r') as file:
    with open('extracted_nospaces.txt','w') as file2:
        for line in file.readlines():
            if not line.isspace():
                file2.write(line)

with open(NOSPACES_FILENAME,'r') as file:
    lines = file.readlines()
    for line in lines:
        if pattern.match(str(line)):
            m = re.search(TOC_REGEXP_WITHOUT_PAGE_NO, line)
            if m:
                found = m.group(1)
                list_of_headings.append(found)

tree_of_headings = build_tree_from_headings(list_of_headings)
#for pre, fill, node in RenderTree(tree_of_headings):
#     print("%s%s" % (pre, node.name))

n = anytree.search.findall_by_attr(tree_of_headings,'Send a page or share a notebook')
print (str(n))

with open(NOSPACES_FILENAME,'r') as file:
    list_of_contents = get_content_from_headings(list_of_headings, file)

if len(toc) == 0:
    print 'TOC does not exist in the standard way. Using pattern matching'
else:
    print toc

print_title_content_list(list_of_contents, list_of_headings)
