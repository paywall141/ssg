from textnode import *



print("hello world")
def main():
    first_node = TextNode(
        "test string",
        TextType.LINKS,
        "https://www.youtube.come"
    )
    print(f"variable {first_node} created")

main()