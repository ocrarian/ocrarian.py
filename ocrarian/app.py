"""Text OCR using Google Docs API"""
from argparse import ArgumentParser
from pathlib import Path

from ocrarian import WORK_DIR
from ocrarian.classes.google_drive import GdriveClient


def main():
    """Google Docs OCR Tool"""
    flags = ArgumentParser(prog='ocrarian',
                           description="A simple OCR tool that utilizes Google Docs power")
    flags.add_argument('file', type=str, help='PDF file')
    args = flags.parse_args()
    client = GdriveClient()
    pdf_file = Path(f"{WORK_DIR}/{args.file}")
    ocr = client.ocr(pdf_file)
    if ocr:
        print(f"Text from {pdf_file} has been OCR'd successfully.\n"
              f"Output can be found in {ocr}")


if __name__ == '__main__':
    main()
