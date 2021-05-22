from flashtext.keyword import KeywordProcessor

replacer = KeywordProcessor()
replacer.add_keywords_from_dict({'ksa': ['한과영', 'korea']})


print(replacer.process('한과영은 좋은 학교이다'))
print(replacer.keyword_trie_dict)

