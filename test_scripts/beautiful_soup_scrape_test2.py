import requests
from bs4 import BeautifulSoup

#url = 'https://www.cnbc.com/2025/04/14/airlines-bet-on-rich-travelers-in-first-class-despite-economic-concerns.html'
url = "https://www.cnbc.com/2025/04/15/nvidia-says-it-will-record-5point5-billion-quarterly-charge-tied-to-h20-processors-exported-to-china.html"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

paragraphs = soup.find_all('p')
article_text = '\n'.join([para.get_text() for para in paragraphs])

print(article_text)

# all_text = soup.get_text()
# print(all_text)

# lines = (line.strip() for line in all_text.splitlines())
# chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
# text = "\n".join(chunk for chunk in chunks if chunk)
# print(text)