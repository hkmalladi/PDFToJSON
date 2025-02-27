#FILENAME = "surface-pro-4-user-guide-EN.pdf"
#FILENAME = "1707.09725.pdf"
NOSPACES_FILENAME = 'extracted_nospaces.txt'
NOSPACES_FILENAME_TRIMMED = 'extracted_nospaces_trimmed.txt'
TOC_REGEXP = "([a-zA-Z0-9\W]+\W*)\.\.+\W*[0-9]+"
TOC_REGEXP_WITHOUT_PAGE_NO = "^(.+?)\.+"
SECTION_HIERARCHY_CODE = "lower_upper_spacedLower"
NOSPACES_FILENAME = "extracted_nospaces.txt"
PDFTOTEXTCONVERSION = 'pdftotext -layout -nopgbrk -enc ASCII7 -q '
PDFTOTEXTCONVERSION_TRIMMED = 'pdftotext -y 80 -H 650 -W 1000 -layout -nopgbrk -enc ASCII7 -q '
EXTRACTIVE_SUMMARIZATION_ALGO = 'lsa' # Can be luhn, lsa, kl, textrank and lexrank
SUMMARIZATION_THRESHOLD = 500
SUMMARIZATION_SENTENCE_LIMIT = 50
SUMMARIZATION_SENTENCE_LOWER_BOUND = 5
