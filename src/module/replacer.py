from src.module.flashtext import KeywordProcessor

class Replacer:
    def __init__(self):
        db_dir = '../data/words.json'
        self.preprocessor = {
            'ko': KeywordProcessor(),
            'en': KeywordProcessor()
        }








# from old flashtext

# def load_from_database(self):
#     try:
#         with open(self.db_dir, 'r') as fp:
#             data = json.load(fp)
#     except json.decoder.JSONDecodeError:
#         data = {}
#     self.keyword_trie_dict = data
#
# def save_to_database(self):
#     with open(self.db_dir, 'w') as fp:
#         json.dump(self.keyword_trie_dict, fp, indent='\t')
