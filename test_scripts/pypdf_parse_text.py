from pypdf import PdfReader

reader = PdfReader("TrentRiversResume.pdf")
for page in reader.pages:
	print(page.extract_text())