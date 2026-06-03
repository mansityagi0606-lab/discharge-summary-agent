import fitz
import pytesseract
from PIL import Image
import io

# Update if your installation path differs
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

def extract_pdf_text(pdf_path: str):

    doc = fitz.open(pdf_path)

    full_text = ""

    for page_num in range(len(doc)):

        page = doc[page_num]

        # Higher resolution for better OCR
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

        img_bytes = pix.tobytes("png")

        image = Image.open(io.BytesIO(img_bytes))

        text = pytesseract.image_to_string(image)

        full_text += f"\n\n--- PAGE {page_num + 1} ---\n\n"
        full_text += text

    doc.close()

    return full_text