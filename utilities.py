from configuration import *
from anytree import Node, RenderTree
import string
from copy import deepcopy


def get_content_from_headings(list_of_headings, file):
    lines = file.readlines()
    list_of_contents = []
    dict_of_headings = {}
    dict_of_next_headings = {}
    for iter in range(0,len(list_of_headings)):
        heading_found = False
        next_heading_exists = True
        next_heading_found = False
        content = ''
        heading = (list_of_headings[iter].rstrip()).lstrip().lower()
        if not heading in dict_of_headings:
            dict_of_headings[heading] = 0
        else:
            c = dict_of_headings[heading]
            c += 1
            dict_of_headings[heading] = c
        retries = dict_of_headings[heading]

        nh_retries = 0

        if iter < len(list_of_headings) - 1:
            next_heading = (list_of_headings[iter + 1].rstrip()).lstrip().lower()
            if not next_heading in dict_of_next_headings:
                dict_of_next_headings[next_heading] = 0
            else:
                c = dict_of_next_headings[next_heading]
                c += 1
                dict_of_next_headings[next_heading] = c
            nh_retries = dict_of_next_headings[next_heading]
        else:
            next_heading_exists = False

        for i in range(0,len(lines)):
            line = deepcopy(lines[i])
            line = (line.lower().rstrip().lstrip()).translate(None, string.punctuation)
            if i < len(lines) - 1:
                next_line = deepcopy(lines[i + 1])
                next_line = (next_line.lower().rstrip().lstrip()).translate(None, string.punctuation)
            else:
                next_line = ''
            if line == (heading.lower()).translate(None, string.punctuation) or (line + ' ' + next_line) == (heading.lower()).translate(None, string.punctuation) :
                if retries == 0:
                    heading_found = True
                else:
                    retries -= 1
            elif next_heading_exists and (line == (next_heading.lower()).translate(None, string.punctuation) or (line + ' ' + next_line) == (next_heading.lower()).translate(None, string.punctuation)):
                if nh_retries == 0:
                    next_heading_found = True
                else:
                    nh_retries -= 1
            elif (heading_found) and (not next_heading_found):
                content = content + lines[i]
        content.replace(' ','')
        list_of_contents.append(content)
    return list_of_contents


def print_title_content_list(list_of_contents, list_of_headings):
    for iter in range(0,len(list_of_contents)):
        print list_of_headings[iter] + ' : ' + list_of_contents[iter]

def build_tree_from_headings(list_of_headings):
    section_code = SECTION_HIERARCHY_CODE.split('_')
    root = Node('ROOT')
    section_list = list()
    subsection_list = list()
    subsubsection_list = list()
    for heading in list_of_headings:
        if heading.isupper(): # Subsections
            subsection = Node(heading.rstrip().lstrip(), section_list[len(section_list) - 1])
            subsection_list.append(subsection)
        elif (not heading.isupper()) and (not heading.islower()) and heading.startswith(' '): # Sub-subsection
            subsubsection = Node(heading.rstrip().lstrip(), subsection_list[len(subsection_list) - 1])
            subsubsection_list.append(subsubsection)
        else: # Sections
            section = Node(heading.rstrip().lstrip(), root)
            section_list.append(section)
    return root
