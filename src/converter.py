import subprocess


def convert(extension_output, original_file, converted_file):
    # list of extensions that needs to be ignored.
    # ignored_extensions = ["pdf"]
    ignored_extensions = []

    if extension_output in ignored_extensions:
        return

    subprocess.call(["ebook-convert", original_file, converted_file], timeout=150)
