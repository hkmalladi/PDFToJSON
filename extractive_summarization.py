from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from configuration import *
from utilities import *
import string
import os

def get_summarizer():
    if EXTRACTIVE_SUMMARIZATION_ALGO == 'luhn':
        return LuhnSummarizer()
    elif EXTRACTIVE_SUMMARIZATION_ALGO == 'kl':
        return KLSummarizer()
    elif EXTRACTIVE_SUMMARIZATION_ALGO == 'lsa':
        return LsaSummarizer()
    elif EXTRACTIVE_SUMMARIZATION_ALGO == 'textrank':
        return TextRankSummarizer()
    elif EXTRACTIVE_SUMMARIZATION_ALGO == 'lexrank':
        return LexRankSummarizer()

def summarization_based_heading_search():
    headings_set = detect_headings_using_summarization()
    root = Node('ROOT')
    headings_list = []
    for heading in headings_set:
        heading = heading.rstrip('.')
        node = Node(heading, root)
        headings_list.append(heading)
    print_tree(root)
    print headings_list
    return root, headings_list    

def terminate_sentences_with_fullstops(file, interfile):
    with open(file, 'r') as f:
        with open(interfile, 'w') as f2:
            lines = f.readlines()
            for line in lines:
                line.rstrip()
                c = line[len(line) - 2]
                if not c in string.punctuation:
                    line = line.rstrip() + '.'
                f2.write(line + '\n')

def detect_headings_using_summarization():
    filename = FILENAME    
    os.system(PDFTOTEXTCONVERSION_TRIMMED + filename )
    remove_spaces_from_text_file(filename, NOSPACES_FILENAME_TRIMMED)
    file = NOSPACES_FILENAME
    interfile = file + '.inter'
    
    terminate_sentences_with_fullstops(file, interfile)
    
    parser = PlaintextParser.from_file(interfile, Tokenizer("english"))
    summarizer = get_summarizer()
    
    summary = summarizer(parser.document, SUMMARIZATION_THRESHOLD)
    headings_set = set()
    
    for sentence in summary:
        if len(str(sentence)) < SUMMARIZATION_SENTENCE_LIMIT and len(str(sentence)) > SUMMARIZATION_SENTENCE_LOWER_BOUND:
            sentence_str = str(sentence)
            with open(file, 'r') as f2:
                lines = f2.readlines()
                for line in lines:
                    if line[0].isupper() and not line.startswith(' ') and line.rstrip().lstrip() == sentence_str.rstrip().lstrip().rstrip('.') and line[len(line) - 2] not in string.punctuation:
                        # Assume that headings dont end in punctuation and dont start with spaces
                        if sentence_str in headings_set:
                            headings_set.remove(sentence_str) # Remove header, footer etc. Premise is that headings dont re-occur.
                        else:
                            headings_set.add(sentence_str)
    return headings_set

