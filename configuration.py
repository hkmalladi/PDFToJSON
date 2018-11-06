#FILENAME = "surface-pro-4-user-guide-EN.pdf"
FILENAME = "1707.09725.pdf"
TOC_REGEXP = "([a-zA-Z0-9\W]+\W*)\.\.+\W*[0-9]+"
TOC_REGEXP_WITHOUT_PAGE_NO = "^(.+?)\.+"
SECTION_HIERARCHY_CODE = "lower_upper_spacedLower"
NOSPACES_FILENAME = "extracted_nospaces.txt"
PDFTOTEXTCONVERSION = 'pdftotext -layout -nopgbrk -enc ASCII7 -q '
