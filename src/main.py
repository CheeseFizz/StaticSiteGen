from textnode import *
from fileutilities import *


if __name__ == "__main__":
    rootdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    copy_static(rootdir)