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