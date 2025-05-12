import os, shutil

from htmlnode import *
from textnode import * 
from utilities import *

def recursive_copy(source, dest):
    items = os.listdir(source)
    if len(items) == 0:
        return
    for item in items:
        newsource = os.path.join(source, item)
        if os.path.isfile(newsource):
            result = shutil.copy(newsource, dest)
            print(f"Copying {newsource} to {result}")
        elif os.path.isdir(newsource):
            newdest = os.path.join(dest, item)
            os.mkdir(newdest)
            print(f"mkdir {newdest}")
            recursive_copy(newsource, newdest)
    return

def copy_static(source, dest):
    
    if os.path.exists(dest):
        shutil.rmtree(dest) # remove any existing data
    os.mkdir(dest)

    recursive_copy(source, dest)

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"\nGenerating page from {from_path} to {dest_path} using {template_path}.")

    with open(from_path, "r") as f:
        markdown = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()

    node = markdown_to_html_node(markdown)
    html = node.to_html()

    title = extract_title(markdown)
    finalhtml = template.replace("{{ Title }}", title).replace("{{ Content }}", html).replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")

    dest_parent = os.path.abspath(os.path.join(dest_path, os.path.pardir))
    if not os.path.exists(dest_parent):
        os.makedirs(dest_parent)
    with open(dest_path, "w") as f:
        f.write(finalhtml)

def generate_pages_recursively(basepath, dir_path_content, template_path, dest_dir_path):
    items = os.listdir(dir_path_content)
    for item in items:
        itempath = os.path.join(dir_path_content, item)
        if os.path.isfile(itempath) and item[-3:] == '.md':
            dest_filename = item[0:-3] + ".html"
            dest_filepath = os.path.join(dest_dir_path, dest_filename)
            generate_page(basepath, itempath, template_path, dest_filepath)
        elif os.path.isdir(itempath):
            new_dest_path = os.path.join(dest_dir_path, item)
            generate_pages_recursively(basepath, itempath, template_path, new_dest_path)


