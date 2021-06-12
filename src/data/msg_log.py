import json

class MessageLogger:
    def __init__(self, log_dir='data/message.json'):
        self.dir = log_dir
        self.data = {}

    def load(self):
        try:
            with open(self.dir, 'r') as f:
                data = json.load(f)
            # Replacer.set_keyword_data(data)
        except json.decoder.JSONDecodeError:
            pass

    def save(self):
        data = Replacer.get_keyword_data()
        with open(self.dir, 'w') as f:
            json.dump(data, f, indent=None)