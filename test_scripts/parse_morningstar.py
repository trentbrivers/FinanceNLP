from pypdf import PdfReader
import re

reader = PdfReader(r"C:\Users\trent\Downloads\Agilent_MorningStar.pdf")

"""
for page in reader.pages:
	# if "Analyst Notes Archive" in page.extract_text():
	# 	print(page.extract_text()) 
	print(page.extract_text())
"""

all_text = [page.extract_text() for page in reader.pages]

footer_pattern = r"© Morningstar .*? at the end of this report." #Remove on every page
header_pattern = r"Morningstar Equity Analyst Report.*?;;;;;.*?, UTC\s*" #Remove on every page
page_1_pattern = r".*?Sustainalytics . ESG Risk..Rating."
page_2_pattern = r"Sector Industry.*"
page_3_pattern = (
	r"Competitors.*?Investment Style"
	r"[A-Za-z ]+"
)
last_page_pattern = r"Analyst Notes Archive.*"

beginning_string = "Analyst Note"
end_string = "Analyst Notes Archive"


#cleaned_text = re.sub(header_pattern, '', full_text, flags=re.DOTALL)


all_text = all_text[:7]
#print(re.search(page_1_pattern, all_text[0], flags = re.DOTALL).group())


for i in range(len(all_text)):
	# print("Before")
	# print(text)
	text = all_text[i]

	#print(re.findall(footer_pattern, text))
	# matches = re.search(footer_pattern2, text, re.DOTALL)
	# matched_string = matches.group()
	# print(matched_string)
	fixed_string = re.sub(footer_pattern, "", text, flags = re.DOTALL)
	fixed_string = re.sub(header_pattern, "", fixed_string, flags = re.DOTALL)

	all_text[i] = fixed_string
	#print(fixed_string)

	# print("After")
	#print(fixed_string) 

	# matches = re.search(header_pattern, text, flags = re.DOTALL)
	# matched_string = matches.group()

	# print(matched_string)

all_text[0] = re.sub(page_1_pattern, "", all_text[0], flags = re.DOTALL)
all_text[1] = re.sub(page_2_pattern, "", all_text[1], flags = re.DOTALL)
all_text[2] = re.sub(page_3_pattern, "", all_text[2], flags = re.DOTALL)
all_text[-1] = re.sub(last_page_pattern, "", all_text[-1], flags = re.DOTALL)
for text in all_text:
	print(text)

# print(all_text[1])