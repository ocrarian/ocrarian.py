"""Text OCR using Google Docs API"""
from argparse import ArgumentParser
from pathlib import Path

from ocrarian.common.google_drive import GdriveClient
from ocrarian.common.config import Config


def main():
    """Google Docs OCR Tool"""
    flags = ArgumentParser(prog='ocrarian',
                           description="A simple OCR tool that utilizes Google Docs power")
    flags.add_argument('file', type=lambda p: Path(p).absolute(), help='PDF or Image file')
    args = flags.parse_args()
    config = Config()
    client = GdriveClient(config)
    pdf_file = args.file
    ocr = client.ocr(pdf_file)
    if ocr:
        print(f"Text from {pdf_file} has been OCR'd successfully.\n"
              f"Output can be found in {ocr}")


if __name__ == '__main__':
    main()
