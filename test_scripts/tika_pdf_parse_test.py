from tika import parser

#text = parser.from_file("TrentRiversResume.pdf")
#print(text['content'])

text = parser.from_file("9a1e0e4d-7f23-4afd-9698-0ab93c74d4e4.pdf")
print(text['content'])