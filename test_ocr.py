from app.tools.pdf_reader import extract_pdf_text

PDF_PATH = r"data\patient.pdf"

text = extract_pdf_text(PDF_PATH)

print("Characters:", len(text))

print("\nFIRST 2000 CHARACTERS:\n")
print(text[:2000])

with open("ocr_output.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("\nSaved OCR output to ocr_output.txt")