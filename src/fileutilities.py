import os, shutil

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


def copy_static(rootdir):
    source = os.path.join(rootdir, "static")
    dest = os.path.join(rootdir, "public")
    if os.path.exists(dest):
        shutil.rmtree(dest) # remove any existing data
    os.mkdir(dest)

    recursive_copy(source, dest)

    
    

