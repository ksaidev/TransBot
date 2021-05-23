import re

# url = re.compile(r"(?:[a-zA-Z]|[0-9]+)(?:[a-zA-Z]|[0-9]|[$\-@.&+:/?=]|[!*(),])+")
url = re.compile(r"(?:(?:[a-zA-Z]|[0-9])+(?:[$\-@.&+:/?=]|[!*(),])+)+(?:[a-zA-Z]|[0-9]|/)+")

text = '제가 만든 사이트는 https://ksadensity.com/입니다. ' \
       '제 이메일은 percy3368@ksa.hs.kr입니다. ' \
       'the url for the students site is students.ksa.hs.kr.'

matches = url.finditer(text)

replaced_text = ''
start = 0
for match in matches:
    end = match.start()
    replaced_text += text[start:end]
    start = match.end()
    replaced_text += 'url'
replaced_text += text[start:]

print(text)
print(replaced_text)
# matches = url.findall()
# print(matches)
# # ['https://ksadensity.com/', 'percy3368@ksa.hs.kr', 'students.ksa.hs.kr']
