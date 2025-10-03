from textnode import *
from filemover import copy_fs
from generate_page import generate_page, generate_pages_recursive

print("hello world")
def main():
    # handles nuking and rebuilding public
    copy_fs("./static", "./public")
    generate_pages_recursive("content", "template.html", "public")

main()