import os


def _file_path(file_path, filename):
    return file_path + "/" + filename  # FIXME unix specific


def read_files(file_path):
    """ reads not recursively files under a path, yielding a tuple with the filename and file content """

    for root, dirs, files in os.walk(file_path):
        for filename in files:
            with open(file_path+"/"+filename) as infile:
                yield (filename, infile.read())
