from PyPDF2 import PdfFileReader
import os
import arxivpy

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
            
def process_dataset():
#    scrape_arxiv()
    os.system('ls *.pdf > list_of_files.txt')
    with open('list_of_files.txt','r') as f:
        lines = f.readlines()
    toc_of_dataset = []

    for line in lines:
        filename = line.rstrip()
        reader = PdfFileReader(open(filename, 'rb'))
        toc = reader.outlines
        toc_of_article = []
        for item in flatten_list(toc):
            toc_of_article.append(item['/Title'])
        toc_of_dataset.append(toc_of_article)

    print len(toc_of_dataset)

process_dataset()
