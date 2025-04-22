from pypdf import PdfReader
import re

#Regular Expression Patterns
footer_pattern = r"© Morningstar .*? at the end of this report." #Remove on every page
header_pattern = r"Morningstar Equity Analyst Report.*?;;;;;.*?, UTC\s*" #Remove on every page
bullet_pattern = r"^u "
apostrophe_pattern_1 = r" ’ s"
apostrophe_pattern_2 = r" ’"


page_1_pattern = r".*?Sustainalytics . ESG Risk..Rating."
page_2_pattern = r"Sector Industry.*"
page_3_pattern = (
	r"Competitors.*?Investment Style"
	r"[A-Za-z ]+"
)
page_3_supplement_pattern = r"Analysis Security 1 Security 2 Security 3 Security 4"
last_page_pattern = r"Analyst Notes Archive.*"


def find_last_page(text):
	"""Input: list of strings; Output: Integer; 
	Step 1: Find the last page"""

	last_page = -1
	current_page_check = 1
	while last_page < 0:
		if "Analyst Notes Archive" in text[current_page_check]:
			last_page = current_page_check
		else:
			current_page_check += 1

	return last_page + 1 #To avoid a slicing error


def process_each_page(text):
	"""Input: list of string; Output: list of strings; 
	Step 2: Process each page to remove header and footer"""

	fixed_text = []
	for page in text:
		fixed_string = re.sub(footer_pattern, "", page, flags = re.DOTALL)
		fixed_string = re.sub(header_pattern, "", fixed_string, flags = re.DOTALL)
		fixed_string = re.sub(bullet_pattern, "", fixed_string, flags = re.MULTILINE)

		fixed_text.append(fixed_string)

	return fixed_text


def process_special_pages(text):
	"""Input: list of string; Output: list of strings
	Step 3: Process specific pages"""

	text[0] = re.sub(page_1_pattern, "", text[0], flags = re.DOTALL)
	text[1] = re.sub(page_2_pattern, "", text[1], flags = re.DOTALL)
	text[2] = re.sub(page_3_pattern, "", text[2], flags = re.DOTALL)
	text[2] = re.sub(page_3_supplement_pattern, "", text[2])
	text[-1] = re.sub(last_page_pattern, "", text[-1], flags = re.DOTALL)

	return text


def final_process(text):
	"""Input: list of strings; Output: String
	Step 4: remove new lines and concatenate to single string"""

	fixed_text = ""
	for page in text:
		cleaned = re.sub(r'\s+', ' ', page)
		fixed_text = fixed_text + " " + cleaned
		fixed_text = re.sub(r'\s+', ' ', fixed_text)

		#fix apostrophes
	fixed_text = re.sub(apostrophe_pattern_1, "'s", fixed_text)
	fixed_text = re.sub(apostrophe_pattern_2, "'", fixed_text)

	return fixed_text

def process_input(file_string):
	"""Input: File String, Output: tuple(string, integer)
	Performs all of the steps of document processing"""

	reader = PdfReader(file_string)

	all_text = [page.extract_text() for page in reader.pages]
	label = extract_label(all_text)

	last = find_last_page(all_text) #Step 1: Find last page

	all_text = all_text[:last]
	all_text = process_each_page(all_text) #Step 2: Process all pages
	all_text = process_special_pages(all_text) #Step 3: Page specific processing
	final_text = final_process(all_text) #Step 4: remove new lines and concatenate to single string

	return final_text, label

def extract_label(all_text):
	"""Input: document, Output: Integer
	Uses Regular Expressions to extract the label from Morningstar docs"""

	label_dict = {'QQQQQ': 5, 'QQQQ': 4, 'QQQ': 3, 'QQ': 2, 'Q': 1}
	label_pattern = r" ([Q]+)."

	page_1 = all_text[0]
	text_label = re.search(label_pattern, page_1).group(1)

	return label_dict[text_label]

#print(extract_label(all_text))
#print(all_text[0], extract_label(all_text))

#processed_text = process_input(all_text)

#print(processed_text)

# current_file = r"E:\Data\NLP\Morningstar\m_adidas_addyy.pdf"
# test = process_input(current_file)
# #print(test)
# print(test[0])
# # # reader = PdfReader(current_file)
# # # all_text = [page.extract_text() for page in reader.pages]
# # # for page in all_text:
# # # 	print(page)
# # #print(extract_label(all_text))