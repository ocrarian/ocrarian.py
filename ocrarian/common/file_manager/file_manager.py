"""ocrarian file manager class"""
from glob import glob
from pathlib import Path
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
        self.out_file = Path(f"{self.config.user_docs_dir}/{self.file.stem}.{export_format.lower()}").absolute()
        if not self.file.exists():
            raise FileNotFound(self.file)
        self.extension = None
        self.is_supported()
        self.is_pdf = None
        self.is_image = None
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
            raise UnsupportedFile(kind.extension.upper(), kind.MIME, [i.name for i in SupportedTypes])
        self.extension = kind.extension
        return True

    def set_type(self):
        """Set the given file type property."""
        if self.extension == "pdf":
            self.is_pdf = True
            self.is_image = False
        else:
            self.is_image = True
            self.is_pdf = False

    def split_pdf(self):
        """Split PDF file into smaller pieces
        Since Google Docs support PDF to text conversion for files less than 80 pages,
        it's safer to split the PDF file into a smaller piece (75 pages per part)"""
        pdf = PdfFileReader(str(self.file))
        pages_count = pdf.getNumPages()
        if pages_count > 75:
            ranges = []
            to_split = pages_count
            processed = 0
            while processed != pages_count:
                if to_split - 75 > 0:
                    ranges.append((processed + 1, processed + 75))
                    to_split = to_split - 75
                    processed = processed + 75
                else:
                    ranges.append((processed + 1, pages_count))
                    to_split = 0
                    processed = pages_count
            for pages_range in ranges:
                pdf_writer = PdfFileWriter()
                for page in range(pages_range[0] - 1, pages_range[1]):
                    pdf_writer.addPage(pdf.getPage(page))
                output_filename = f"{self.file.parent}/{self.file.stem}_{pages_range[0]}-{pages_range[1]}.pdf"
                with open(output_filename, 'wb') as out:
                    pdf_writer.write(out)
                self.parts.append(Path(output_filename))
        else:
            self.parts.append(self.file)
        return self.parts

    def merge(self):
        """Merge OCR output files"""
        if len(self.parts) < 2:
            return self.out_file
        if self.export_format == "TXT":
            self.merge_txt()
        return self.out_file

    def merge_txt(self):
        """Merge text files into a single text file."""
        out_files = sorted([i for i in self.out_file.parent.iterdir()
                            if i.is_file() and str(i.name).startswith(f"{self.out_file.stem}_")],
                           key=lambda x: int(x.name.split('_')[-1].split('-')[0]))

        with open(self.out_file, "w") as out:
            for part in out_files:
                with open(str(part), "r") as file:
                    out.write(file.read())
                part.unlink()
