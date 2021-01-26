"""ocrarian file manager class"""
from pathlib import Path
from shutil import move

import filetype
from PyPDF2 import PdfFileReader, PdfFileWriter

from ocrarian.common.types.supported_types import SupportedTypes
from ocrarian.common.file_manager.exceptions import FileNotFound, UnknownFileType, UnsupportedFile


class FileManager:
    """FileManager class is responsible for handling files tasks such as:
    - Detecting filetype and check if it iss support
    - Dealing with PDF files, in terms of splitting and merging"""

    def __init__(self, config, export_format, file: Path):
        self.config = config
        self.export_format = export_format
        self.file = file
        self.out_file = Path(
            f"{self.config.user_docs_dir}/{self.file.stem}.{export_format.lower()}").absolute()
        self.tmp_file = Path(
            f"{self.config.user_cache_dir}/{self.file.stem}.{export_format.lower()}").absolute()
        if not self.file.exists():
            raise FileNotFound(self.file)
        self.extension = None
        self.is_supported()
        self.is_pdf = False
        self.is_image = False
        self.set_type()
        self.parts = []

    def is_supported(self):
        """check if input file is supported"""
        kind = filetype.guess(str(self.file))
        if kind is None:
            raise UnknownFileType(self.file)
        valid_input_format = [i for i in SupportedTypes
                              if i.name == kind.extension.upper()
                              and i.value == kind.MIME]
        if not valid_input_format:
            raise UnsupportedFile(kind.extension.upper(),
                                  kind.MIME, [i.name for i in SupportedTypes])
        self.extension = kind.extension
        return True

    def set_type(self):
        """Set the given file type property."""
        if self.extension == "pdf":
            self.is_pdf = True
        else:
            self.is_image = True

    def split_pdf(self):
        """Split PDF file into smaller pieces
        Since Google Docs support PDF to text conversion for files less than 80 pages,
        it's safer to split the PDF file into a smaller piece (20 pages per part)"""
        pdf = PdfFileReader(str(self.file))
        pages_count = pdf.getNumPages()
        if pages_count > 20:
            ranges = []
            to_split = pages_count
            processed = 0
            while processed != pages_count:
                if to_split - 20 > 0:
                    ranges.append((processed + 1, processed + 20))
                    to_split = to_split - 20
                    processed = processed + 20
                else:
                    ranges.append((processed + 1, pages_count))
                    to_split = 0
                    processed = pages_count
            for pages_range in ranges:
                pdf_writer = PdfFileWriter()
                for page in range(pages_range[0] - 1, pages_range[1]):
                    pdf_writer.addPage(pdf.getPage(page))
                output_filename = f"{self.config.user_cache_dir}/" \
                                  f"{self.file.stem}_{pages_range[0]}-{pages_range[1]}.pdf"
                with open(output_filename, 'wb') as out:
                    pdf_writer.write(out)
                self.parts.append(Path(output_filename))
        else:
            self.parts.append(self.file)
        return self.parts

    def merge(self):
        """Merge OCR output files"""
        if not self.parts:
            move(self.tmp_file, self.out_file)
            return self.out_file
        if self.export_format == "TXT":
            self.merge_txt()
        return self.out_file

    def merge_txt(self):
        """Merge text files into a single text file."""
        out_files = sorted([i for i in self.config.user_cache_dir.iterdir()
                            if i.is_file() and str(i.name).startswith(f"{self.out_file.stem}_")
                            and str(i.name).endswith(self.out_file.suffix)],
                           key=lambda x: int(x.name.split('_')[-1].split('-')[0]))
        # TODO: Handle PermissionError: [WinError 5] Access is denied on Windows 10
        # A temporary workaround is to allow python from controlled access in windows security.
        with open(self.out_file, "w", encoding="utf-8", newline='\n') as out:
            for part in out_files:
                with open(str(part), "r") as file:
                    out.write(file.read())
                part.unlink()

    def cleanup(self):
        """Cleanup temporary files"""
        if self.parts:
            for item in self.config.user_cache_dir.iterdir():
                item.unlink()
