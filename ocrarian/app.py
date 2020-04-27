"""Text OCR using Google Docs API"""
from argparse import ArgumentParser
from pathlib import Path

from ocrarian.common.file_manager.config import Config
from ocrarian.common.file_manager.file_manager import FileManager
from ocrarian.common.gdocs_client.google_docs_client import GDocsClient
from ocrarian.common.gdocs_client.settings import Settings


def main():
    """Google Docs OCR Tool"""
    flags = ArgumentParser(prog='ocrarian',
                           description="A simple OCR tool that utilizes Google Docs power")
    flags.add_argument('file', type=lambda p: Path(p).absolute(), help='PDF or Image file')
    args = flags.parse_args()
    config = Config()
    settings = Settings(config)
    client = GDocsClient(settings)
    input_file = args.file
    file = FileManager(config, settings.export_format, input_file)
    if file.is_pdf:
        parts = file.split_pdf()
        for part in parts:
            ocr = client.ocr(part)
    else:
        ocr = client.ocr(input_file)
    out_file = file.merge()
    file.cleanup()
    if out_file:
        print(f"Text from {input_file} has been OCR'd successfully.\n"
              f"Output can be found in {out_file}")


if __name__ == '__main__':
    main()
