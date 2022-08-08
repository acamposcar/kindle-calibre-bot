from os import listdir, rename, remove
from os.path import isfile, join
import subprocess


# return name of file to be kept after conversion.
# we are just changing the extension
def get_final_filename(f, extension_output):
    f = f.split(".")
    filename = ".".join(f[0:-1])
    processed_file_name = filename+extension_output
    return processed_file_name

# return file extension
def get_file_extension(f):
    return f.split(".")[-1]


def convert(extension_output):
    # list of extensions that needs to be ignored.
    #ignored_extensions = ["pdf"]
    ignored_extensions = []

    # here all the downloaded files are kept
    path = "ebook/"

    # path where converted files are stored
    path_converted = "ebook/converted/"

    raw_files = [f for f in listdir(path) if isfile(join(path, f))]
    converted_files = [f for f in listdir(
        path_converted) if isfile(join(path_converted, f))]

    for f in raw_files:
        final_file_name = get_final_filename(f, extension_output)
        extension = get_file_extension(f)
        if final_file_name not in converted_files and extension not in ignored_extensions:
            print("Converting : "+f)
            subprocess.call(["ebook-convert", path+f,
                            path_converted+final_file_name])
        else:
            print("Skipped: "+final_file_name)
