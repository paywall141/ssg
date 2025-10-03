import os
from extract_title import extract_title
from markdown_blocks import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # validate src and dest paths
    if not os.path.exists(from_path):
        raise ValueError(f"Invalid source path: {from_path}")
    if not os.path.exists(template_path):
        raise ValueError(f"Invalid template path: {template_path}")

    with open(from_path, "r") as f:
        markdown_content = f.read()

    with open(template_path, "r") as f:
        template_content  = f.read()
    
    content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)

    final_html  = template_content.replace("{{ Title }}", title).replace("{{ Content }}", content)

    try:
        # check if directory is valid/acceptable
        dest_dir = os.path.dirname(dest_path)
        if dest_dir:
            # mkdir if valid extractable dirs
            os.makedirs(dest_dir, exist_ok=True)

        # if you want additional file_name validation you can use this before saving
        # file_name = os.path.basename(dest_path)
        with open(dest_path, "w") as f:
            f.write(final_html)
    except OSError as e:
        raise ValueError(f"Cannot write to destination path '{dest_path}': {e}")
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    all_entries = os.listdir(dir_path_content)

    for entry in all_entries:
        source_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile( source_path ):
            if source_path.endswith(".md"):
                dest_path = dest_path.replace(".md", ".html")
                generate_page(source_path, template_path, dest_path)
        elif os.path.isdir(source_path):
            generate_pages_recursive(source_path, template_path, dest_path)