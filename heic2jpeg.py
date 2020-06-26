#!/usr/bin/env python3

"""
heic2jpeg.py – HEIC to JPEG Converter 
"""

from PIL import Image
import argparse
import os
import pyheif
import sys

parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("-e", "--exif", action="store_true")
args = parser.parse_args()

filename = args.filename

try:
    heif_file = pyheif.read_heif(filename)
except (FileNotFoundError, pyheif.error.HeifError) as e:
    print(e)
    sys.exit(1)

if args.exif is True:
    exif_data = heif_file.metadata[0]["data"]
else:
    exif_data = b""

try:
    image = Image.frombytes(mode=heif_file.mode, size=heif_file.size, data=heif_file.data)
    image.save(f"{os.path.splitext(filename)[0]}.jpg", "JPEG", exif=exif_data)
    sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(1)