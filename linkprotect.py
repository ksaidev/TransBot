import re

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

a = re.findall(regex, 'percy3368@gmail.com')
print(a)
