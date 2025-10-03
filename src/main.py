from textnode import *
from filemover import copy_fs
from generate_page import generate_page

print("hello world")
def main():
    # handles nuking and rebuilding public
    copy_fs("./static", "./public")
    generate_page("content/index.md", "template.html", "public/index.html")

main()