import re
from configuration import *
from anytree import Node, RenderTree, PreOrderIter
import string
from copy import deepcopy
import os
import json

def create_json(heading_content_dict, tree_of_headings):
    list_of_nodes = []
    final_dict = {}
    inter_json = ''
    json_str = ''
    brace_count = 0
    prev_node = None
    for node in PreOrderIter(tree_of_headings):
        if not node.parent is None :
            if len(node.children) > 0:
                if level_in_a_tree(node) == 1:
                    for iter in range(0, brace_count):
                        inter_json += ']}'
                    if len(json_str) > 0:
                        json_str += ','
                    json_str += inter_json
                    inter_json = ''
                    brace_count = 0
                elif level_in_a_tree(node) < level_in_a_tree(prev_node):
                    brace_count -= 1
                    inter_json += ']}'
                prev_node = node
                brace_count += 1
                if len(inter_json) > 0 and inter_json[len(inter_json) - 1] <> ':':
                    inter_json += ','
                inter_json += '{"' + node.name + '":["' + heading_content_dict[node.name] +'"'
            else:
                if level_in_a_tree(node) == 1:
                    for iter in range(0, brace_count):
                        inter_json += ']}'
                    if len(json_str) > 0:
                        json_str += ','
                    json_str +=  inter_json
                    inter_json = ''
                    brace_count = 0
                elif level_in_a_tree(node) < level_in_a_tree(prev_node):
                    brace_count -= 1
                    inter_json += ']}'
                prev_node = node
                if len(inter_json) > 0 and inter_json[len(inter_json) - 1] <> ':':
                    inter_json += ','
                inter_json += '{"' + node.name + '":["' + heading_content_dict[node.name] + '"]}'
    return '[' + json_str + ']'

def level_in_a_tree(node):
    if node is None:
        return 9999
    level = -1
    while node is not None:
        node = node.parent
        level += 1
    return level

def create_heading_content_dict(list_of_contents, list_of_headings):
    heading_content_dict = {}
    for iter in range(0, len(list_of_headings)):
        heading_content_dict[list_of_headings[iter].rstrip().lstrip()] = list_of_contents[iter]
    return heading_content_dict

def remove_spaces_from_text_file(filename, output_filename):
    with open(os.path.splitext(filename)[0] + '.txt','r') as file:
        with open(output_filename,'w') as file2:
            for line in file.readlines():
                if not line.isspace():
                    file2.write(line)

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
            if line == str(heading.lower()).translate(None, string.punctuation) or (line + ' ' + next_line) == str(heading.lower()).translate(None, string.punctuation) :
                if retries == 0:
                    heading_found = True
                else:
                    retries -= 1
            elif next_heading_exists and (line == str(next_heading.lower()).translate(None, string.punctuation) or (line + ' ' + next_line) == str(next_heading.lower()).translate(None, string.punctuation)):
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
    print 'hello2'
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

def regexp_based_heading_search():
    print 'Outlines based search could not detect a table of contents. Looking for headings using regular expressions.'
    list_of_headings = []
    pattern = re.compile(TOC_REGEXP)
    with open(NOSPACES_FILENAME,'r') as file:
        lines = file.readlines()
        for line in lines:
            if pattern.match(str(line)):
                m = re.search(TOC_REGEXP_WITHOUT_PAGE_NO, line)
                if m:
                    found = m.group(1)
                    list_of_headings.append(found)

    tree_of_headings = build_tree_from_headings(list_of_headings)
#    print_tree(tree_of_headings)
    return tree_of_headings, list_of_headings

def outlines_based_heading_search(toc):
    print 'Outlines based search detected a table of contents. Going ahead with that.'
    root = Node('ROOT')
    list_of_headings = []
    tree_of_headings, list_of_headings  = generate_heading_tree_from_outlines(toc, root, list_of_headings)
#    print_tree(tree_of_headings)
    return tree_of_headings, list_of_headings

def generate_heading_tree_from_outlines(toc, root, list_of_headings):
    for iter in range(0, len(toc)):
        if not isinstance(toc[iter], list): # Create a node for each section heading.
            node = Node(toc[iter]['/Title'].rstrip().lstrip(), root)
            list_of_headings.append(toc[iter]['/Title'])
        else: # If there are a list of headings, they are subheadings of the previous heading. Recur on that.
            node, list_of_headings_output = generate_heading_tree_from_outlines(toc[iter], node, list_of_headings)
            node.parent = root
            list_of_headings = list_of_headings_output
    return root, list_of_headings

def print_tree(tree):
    for pre, fill, node in RenderTree(tree):
         print("%s%s" % (pre, node.name))
