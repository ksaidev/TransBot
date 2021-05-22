import re

url = re.compile(r"(?:[a-zA-Z]|[0-9]|[$\-@.&+:/?=]|[!*(),])+")

a = re.findall(url, '제가 만든 사이트는 하입니다')
print(a)
