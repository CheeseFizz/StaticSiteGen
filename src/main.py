import sys

from textnode import *
from fileutilities import *


def main():
    if not sys.argv[1]:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    rootdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)

    # Copy static resources
    static_source = os.path.join(rootdir, "static")
    static_dest = os.path.join(rootdir, "docs")
    copy_static(static_source, static_dest)

    # Build and write HTML resources
    from_path = os.path.abspath(os.path.join(rootdir, "content"))
    template_path = os.path.abspath(os.path.join(rootdir, "template.html"))
    dest_path = os.path.abspath(os.path.join(rootdir, "docs"))
    generate_pages_recursively(basepath, from_path, template_path, dest_path)


if __name__ == "__main__":
    main()