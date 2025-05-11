from textnode import *
from fileutilities import *


if __name__ == "__main__":
    rootdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    copy_static(rootdir)
    from_path = os.path.abspath(os.path.join(rootdir, "content"))
    template_path = os.path.abspath(os.path.join(rootdir, "template.html"))
    dest_path = os.path.abspath(os.path.join(rootdir, "public"))
    generate_pages_recursively(from_path, template_path, dest_path)