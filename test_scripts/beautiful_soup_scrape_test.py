import requests
from bs4 import BeautifulSoup

url = 'https://apnews.com/article/jpmorgan-bank-earnings-economy-tariffs-profit-be31f6305b847f5f555edb2f251e36c2'
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