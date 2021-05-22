from src.module.preprocessor import PreProcessor
from src.module.postprocessor import PostProccesor
from src.data.word_db import WordDatabase

class Replacer:
    def __init__(self):
        self.db = WordDatabase()
        self.processor = {
            'ko': self.Processor(),
            'en': self.Processor()
        }
        self.load()

    class Processor:
        def __init__(self):
            self.pre = PreProcessor()
            self.post = PostProccesor()

    def preprocess(self, text, target):
        return self.processor[target].pre.process(text)

    def postprocess(self, text, target):
        return self.processor[target].post.process(text)

    def load(self):
        self.db.load()
        for target in self.db.data:
            preprocessor_data, postprocessor_data = self.db.data[target]

            self.processor[target].pre.set_keyword_data(preprocessor_data)
            self.processor[target].post.set_keyword_data(postprocessor_data)









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
