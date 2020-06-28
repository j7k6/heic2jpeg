#!/usr/bin/env python3

"""
heic2jpeg.py – HEIC to JPEG Converter 
"""

from PIL import Image
from multiprocessing import Pool
import argparse
import os
import pyheif
import sys


def heic2jpeg(filename):
    output_file = f"{os.path.splitext(os.path.basename(filename))[0]}.jpg"
    exif_data = b""

    if os.path.exists(os.path.join(output_path, output_file)) is False or args.force is True:
        try:
            heif_file = pyheif.read_heif(filename)
        except (FileNotFoundError, IsADirectoryError, pyheif.error.HeifError) as e:
            print(e)
            return False

        if args.exif is True:
            for metadata in heif_file.metadata or []:
                if metadata["type"] == "Exif":
                    exif_data = metadata["data"]

        try:
            image = Image.frombytes(mode=heif_file.mode, size=heif_file.size, data=heif_file.data)
            image.save(os.path.join(output_path, output_file), "JPEG", exif=exif_data)

            print(output_file)
        except Exception as e:
            print(e)
            return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-b", "--batch", action="store_true")
    parser.add_argument("-e", "--exif", action="store_true")
    parser.add_argument("-f", "--force", action="store_true")
    parser.add_argument("-o", "--output", default=None)
    parser.add_argument("-t", "--threads", default=None, type=int)
    args = parser.parse_args()

    output_path = os.path.dirname(args.filename)

    if args.output is not None:
        try:
            os.makedirs(args.output)
        except OSError as e:
            pass

        output_path = args.output

    if args.batch is True:
        if os.path.isdir(args.filename):
            files = []

            for f in os.listdir(args.filename):
                if f.lower().endswith(".heic"): 
                    files.append(os.path.join(args.filename, f))

            threads = os.cpu_count()

            if args.threads is not None:
                if args.threads > 0:
                    threads = args.threads

            Pool(processes=threads).map(heic2jpeg, files)
    else:
        heic2jpeg(args.filename)