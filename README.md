# ZIPARSER - unzip and sort
#### Python 3.x program which unzip a .zip file and then sorts its content into different folders. 
For sorting procedure here is used shell's **file** command.

### USED LIBRARIES

zipfile, sys, os, shutil, subprocess and BeautifulSoup (bs4)<br>
P.S.: bs4 is not a built-in library. You can install it using pip install beautifulsoup4 (Linux)
more about bs4: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

### HOW TO RUN?

1. chmod +x ziparser.py 
2. ./ziparser [zip-file-name]
