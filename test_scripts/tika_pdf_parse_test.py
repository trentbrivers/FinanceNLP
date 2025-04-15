from tika import parser

text = parser.from_file("TrentRiversResume.pdf")
print(text['content'])