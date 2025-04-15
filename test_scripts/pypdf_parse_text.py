from pypdf import PdfReader
"""
reader = PdfReader("TrentRiversResume.pdf")
for page in reader.pages:
	print(page.extract_text())
"""

reader = PdfReader("9a1e0e4d-7f23-4afd-9698-0ab93c74d4e4.pdf")
for page in reader.pages:
	print(page.extract_text())