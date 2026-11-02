import fitz

class PDFProcessor:
    @staticmethod 
    #We don't need to create an object of PDFProcessor to call this method.
    def extract_text(file_path):
        extracted_pages = []
        try:
            with fitz.open(file_path) as pdf:
                for page_index in range(len(pdf)):
                    page = pdf.load_page(page_index)
                    text = page.get_text("text").strip()

                    if text:
                        extracted_pages.append({
                            "page_number": page_index+1,
                            "content": text
                        })
            if not extracted_pages:
                raise ValueError("NO extractable text found in this pdf.")
            return extracted_pages
        except fitz.FileDateError as error:
            raise ValueError(
                "Unablr to read the Pdf file."
            )from error