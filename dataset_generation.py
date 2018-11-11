from PyPDF2 import PdfFileReader
import os
import arxivpy
import numpy as np
import string
import pandas as pd
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB

os.system('ls *.pdf > list_of_files.txt')

def scrape_arxiv():
    articles = arxivpy.query(search_query=['cs.CV', 'cs.LG', 'cs.CL', 'cs.NE', 'stat.ML'],
                         start_index=0, max_index=200, results_per_iteration=100,
                         wait_time=5.0, sort_by='lastUpdatedDate') # grab 200 articles
    arxivpy.download(articles, path='arxiv_pdf')

def flatten_list(toc):
    flattened_toc = []
    for element in toc:
        if isinstance(element, list):
            flattened_toc_temp = flatten_list(element)
            flattened_toc += flattened_toc_temp
        else:
            flattened_toc.append(element)
    return flattened_toc

def vowel_counter(str):
    v = 0
    for c in str:
        if c == 'a' or c == 'e' or c == 'i' or c == 'o' or c == 'u':
            v += 1
    return v

def get_num_punctuations(str):
    count = 0
    for c in str:
        if c in string.punctuation:
            count += 1
    return count

def train_model(X,Y):
    gnb = GaussianNB()
    gnb.fit(X,Y)
    return gnb

def predict_headings(line, model):
    FV_t = create_feature_vector(line).split(',')
    FV = []
    for val in FV_t:
        FV.append(int(val))
    X = np.array(FV[:5])
    return model.predict(X.reshape(1, -1))[0]

def convert_to_np_array():
    input_file = "dataset.csv"
    df = pd.read_csv(input_file, header = 0)
    original_headers = list(df.columns.values)
    numeric_headers = list(df.columns.values)
    numpy_array = df.as_matrix()
    col_list = ['chars','words','vowels','num_of_punctuations','first_letter_caps']
    X_df = df[col_list]
    Y_df = df['is_heading']
    X = X_df.as_matrix()
    Y = Y_df.as_matrix()
    return numpy_array, X, Y

def is_first_letter_caps(str):
    for c in str:
        if c.isalpha():
            if c.islower():
                return 0
            else:
                return 1
    return 0

def create_feature_vector(h, outcome=0):
    chars = len(h)
    words = len(h.split(' '))
    vowels = vowel_counter(h)
    num_punctuations = get_num_punctuations(h)
    first_letter_caps = is_first_letter_caps(h)
    FV = str(chars) + ',' + str(words) + ',' + str(vowels) + ',' + str(num_punctuations) + ',' + str(first_letter_caps) + ',' + str(outcome) + '\n'
    return FV        

def process_dataset():
#    scrape_arxiv()
    os.system('ls *.pdf > list_of_files.txt')
    with open('list_of_files.txt','r') as f:
        lines = f.readlines()
    toc_of_dataset = []
    lines_of_dataset = []
    set_of_lines = set()
    count = 0
    for line in lines:
        filename = line.rstrip()
        reader = PdfFileReader(open(filename, 'rb'))
        toc = reader.outlines
        toc_of_article = []
        for item in flatten_list(toc):
            toc_of_article.append(item['/Title'])
        toc_of_dataset += toc_of_article
        os.system('pdftotext ' + filename + ' test.txt')
        with open('test.txt', 'r') as f:
            lines = f.readlines()
        lines_of_dataset += lines
    
    f = open('dataset.csv', 'w')
    f.write('chars,words,vowels,num_of_punctuations,first_letter_caps,is_heading\n')
    for h in lines_of_dataset:
        f.write(create_feature_vector(h,0))
    for h in toc_of_dataset:
        f.write(create_feature_vector(h,1))

