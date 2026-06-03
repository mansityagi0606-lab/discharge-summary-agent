from app.tools.medication_extractor import MedicationExtractor

with open("ocr_output.txt", "r", encoding="utf-8") as f:
    text = f.read()

extractor = MedicationExtractor()

meds = extractor.run(text)

for med in meds:
    print(med)