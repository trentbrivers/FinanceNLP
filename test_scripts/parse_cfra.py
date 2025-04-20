from pypdf import PdfReader
"""
reader = PdfReader("TrentRiversResume.pdf")
for page in reader.pages:
	print(page.extract_text())
"""

reader = PdfReader(r"C:\Users\trent\Downloads\Agilent_CFRA.pdf")
for page in reader.pages:
	print(page.extract_text())