from app.tools.diagnosis_extractor import DiagnosisExtractor

with open("ocr_output.txt", "r", encoding="utf-8") as f:
    text = f.read()

extractor = DiagnosisExtractor()

print(extractor.run(text))