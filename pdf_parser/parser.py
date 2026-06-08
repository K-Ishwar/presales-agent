import io
import pdfplumber


def extract_pdf_data(pdf_path):

    result = {
        "text": [],
        "tables": []
    }

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if text:
                result["text"].append(text)

            table = page.extract_table()

            if table:
                result["tables"].append(table)

    return result


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extracts all text from PDF bytes.
    """
    text_content = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)
    return "\n".join(text_content)