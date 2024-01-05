#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
heic2jpeg.py – HEIC to JPEG Converter 
"""

from PIL import Image
from multiprocessing import Pool
import argparse
import os
import pyheif


class Heic2Jpeg:
    def __init__(self, output_path=None, exif=False, force=False):
        self.output_path = output_path
        self.exif = exif
        self.force = force

    def convert(self, filename):
        if self.output_path is None:
            output_path = os.path.dirname(filename)
        else:
            output_path = self.output_path

            try:
                os.makedirs(output_path)
            except OSError:
                pass

        output_file = f"{os.path.splitext(os.path.basename(filename))[0]}.jpg"
        exif_data = b""

        if os.path.exists(os.path.join(output_path, output_file)) is False or self.force is True:
            try:
                heif_file = pyheif.read_heif(filename)
            except (FileNotFoundError, IsADirectoryError, pyheif.error.HeifError) as e:
                print(e)
                return False

            if self.exif is True:
                for metadata in heif_file.metadata or []:
                    if metadata["type"] == "Exif":
                        exif_data = metadata["data"]

            try:
                image = Image.frombytes(mode=heif_file.mode, size=heif_file.size, data=heif_file.data)
                image.save(os.path.join(output_path, output_file), "JPEG", exif=exif_data)

                print(output_file)
                return True
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

    heic2jpeg = Heic2Jpeg(output_path=args.output, exif=args.exif, force=args.force)

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

            Pool(processes=threads).map(heic2jpeg.convert, files)
    else:
        heic2jpeg.convert(args.filename)
