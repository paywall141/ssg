from textnode import *
from filemover import copy_fs
from generate_page import generate_page, generate_pages_recursive
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else: 
        basepath = "/"

    # handles nuking and rebuilding public
    copy_fs("./static", "./docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()