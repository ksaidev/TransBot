import string
import re
import random

class Replacer:
    _keyword = '_keyword_'
    _white_space_chars = {'.', '\t', '\n', '\a', ' ', ','}
    non_word_boundaries = set(string.digits + string.ascii_letters + '_')
    # keyword_trie_dict = {}
    keyword_data = {'ko': {}, 'en': {}}
    case_sensitive = False
    _terms_in_trie = 0
    replace_protector = re.compile(
        r"(?:(?:[a-zA-Z]|[0-9])+(?:[$\-@.&+:/?=]|[!*(),])+)+(?:[a-zA-Z]|[0-9]|/)+"
    )

    @classmethod
    def __len__(cls):
        return cls._terms_in_trie


    @classmethod
    def __setitem__(cls, keyword, clean_name, target):
        status = False

        if keyword and clean_name:
            if not cls.case_sensitive:
                keyword = keyword.lower()
            current_dict = cls.keyword_data[target]
            for letter in keyword:
                current_dict = current_dict.setdefault(letter, {})
            if cls._keyword not in current_dict:
                status = True
                cls._terms_in_trie += 1
            current_dict[cls._keyword] = clean_name
        return status

    @classmethod
    def set_keyword_data(cls, keyword_data):
        cls.keyword_data = keyword_data

    @classmethod
    def get_keyword_data(cls):
        return cls.keyword_data

    @classmethod
    def add_keyword(cls, pair, target):
        keyword, clean_name = pair
        return cls.__setitem__(keyword, clean_name, target)


    class KeyGenerator:
        MID_TRAILER, END_TRAILER = 'a', 'n'

        def __init__(self):
            self.index = self.index_generator()

        def generate(self, word):
            return f'{next(self.index)}{self.trailer(word)}'

        @staticmethod
        def index_generator():
            generated = set()
            while True:
                index = random.randrange(10**2, 10**3)
                if index not in generated:
                    yield index
                    generated.add(index)

        @classmethod
        def trailer(cls, word):
            letter = word[-1]
            return cls.END_TRAILER if (ord(letter) - ord('가')) % 28 != 0 else cls.MID_TRAILER


    def __init__(self, target):
        self.replaced = {}
        # self.keyword_trie_dict = self.keyword_data[target]
        self.target = target
        self.key_generator = self.KeyGenerator()


    def replace_keywords(self, sentence, max_cost=0):
        if not sentence:
            # if sentence is empty or none just return the same.
            return sentence
        new_sentence = []
        orig_sentence = sentence
        if not self.case_sensitive:
            sentence = sentence.lower()
        current_word = ''
        current_dict = self.keyword_data[self.target]

        sequence_end_pos = 0
        idx = 0
        sentence_len = len(sentence)
        curr_cost = max_cost
        while idx < sentence_len:
            char = sentence[idx]
            # when we reach whitespace
            if char not in self.non_word_boundaries:
                current_word += orig_sentence[idx]
                current_white_space = char
                # if end is present in current_dict
                if self._keyword in current_dict or char in current_dict:
                    # update longest sequence found

                    longest_sequence_found = None
                    is_longer_seq_found = False
                    if self._keyword in current_dict:

                        longest_sequence_found = current_dict[self._keyword]
                        sequence_end_pos = idx

                    # re look for longest_sequence from this position
                    if char in current_dict:
                        current_dict_continued = current_dict[char]
                        current_word_continued = current_word
                        idy = idx + 1
                        while idy < sentence_len:
                            inner_char = sentence[idy]
                            if inner_char not in self.non_word_boundaries and self._keyword in current_dict_continued:
                                current_word_continued += orig_sentence[idy]
                                # update longest sequence found
                                current_white_space = inner_char
                                longest_sequence_found = current_dict_continued[self._keyword]
                                sequence_end_pos = idy
                                is_longer_seq_found = True
                            if inner_char in current_dict_continued:
                                current_word_continued += orig_sentence[idy]
                                current_dict_continued = current_dict_continued[inner_char]
                            elif curr_cost > 0:
                                next_word = self.get_next_word(sentence[idy:])
                                current_dict_continued, cost, _ = next(
                                    self.levensthein(next_word, max_cost=curr_cost, start_node=current_dict_continued),
                                    ({}, 0, 0)
                                )
                                idy += len(next_word) - 1
                                curr_cost -= cost
                                current_word_continued += next_word  # just in case of a no match at the end
                                if not current_dict_continued:
                                    break
                            else:
                                break
                            idy += 1
                        else:
                            # end of sentence reached.
                            if self._keyword in current_dict_continued:
                                # update longest sequence found
                                current_white_space = ''
                                longest_sequence_found = current_dict_continued[self._keyword]
                                sequence_end_pos = idy
                                is_longer_seq_found = True
                        if is_longer_seq_found:
                            idx = sequence_end_pos
                            current_word = current_word_continued
                    current_dict = self.keyword_data[self.target]
                    if longest_sequence_found:
                        curr_cost = max_cost

                        key = self.key_generator.generate(longest_sequence_found)
                        new_sentence.append(key + current_white_space)
                        self.replaced[key] = longest_sequence_found
                        current_word = ''

                    else:
                        new_sentence.append(current_word)
                        current_word = ''

                else:
                    # we reset current_dict
                    current_dict = self.keyword_data[self.target]
                    new_sentence.append(current_word)
                    current_word = ''

            elif char in current_dict:
                # we can continue from this char
                current_word += orig_sentence[idx]
                current_dict = current_dict[char]
            elif curr_cost > 0:
                next_orig_word = self.get_next_word(orig_sentence[idx:])
                next_word = next_orig_word if self.case_sensitive else str.lower(next_orig_word)
                current_dict, cost, _ = next(
                    self.levensthein(next_word, max_cost=curr_cost, start_node=current_dict),
                    (self.keyword_data[self.target], 0, 0)
                )
                idx += len(next_word) - 1
                curr_cost -= cost
                current_word += next_orig_word  # just in case of a no match at the end
            else:
                current_word += orig_sentence[idx]
                # we reset current_dict
                current_dict = self.keyword_data[self.target]
                # skip to end of word
                idy = idx + 1
                while idy < sentence_len:
                    char = sentence[idy]
                    current_word += orig_sentence[idy]
                    if char not in self.non_word_boundaries:
                        break
                    idy += 1
                idx = idy
                new_sentence.append(current_word)
                current_word = ''

            # if we are end of sentence and have a sequence discovered
            if idx + 1 >= sentence_len:
                if self._keyword in current_dict:
                    sequence_found = current_dict[self._keyword]

                    key = self.key_generator.generate(sequence_found)
                    new_sentence.append(key)
                    self.replaced[key] = sequence_found
                else:
                    new_sentence.append(current_word)
            idx += 1
        return "".join(new_sentence)


    def levensthein(self, word, max_cost=2, start_node=None):
        start_node = start_node or self.keyword_data[self.target]
        rows = range(len(word) + 1)

        for char, node in start_node.items():
            yield from self._levenshtein_rec(char, node, word, rows, max_cost, depth=1)

    def _levenshtein_rec(self, char, node, word, rows, max_cost, depth=0):
        n_columns = len(word) + 1
        new_rows = [rows[0] + 1]
        cost = 0

        for col in range(1, n_columns):
            insert_cost = new_rows[col - 1] + 1
            delete_cost = rows[col] + 1
            replace_cost = rows[col - 1] + int(word[col - 1] != char)
            cost = min((insert_cost, delete_cost, replace_cost))
            new_rows.append(cost)

        stop_crit = isinstance(node, dict) and node.keys() & (self._white_space_chars | {self._keyword})
        if new_rows[-1] <= max_cost and stop_crit:
            yield node, cost, depth

        elif isinstance(node, dict) and min(new_rows) <= max_cost:
            for new_char, new_node in node.items():
                yield from self._levenshtein_rec(new_char, new_node, word, new_rows, max_cost, depth=depth + 1)

    def get_next_word(self, sentence):

        next_word = str()
        for char in sentence:
            if char not in self.non_word_boundaries:
                break
            next_word += char
        return next_word


    def preprocess(self, text):
        """
        Keyword replacement before translation
        Doesn't replace keywords in an url or an email.
        """
        matches = self.replace_protector.finditer(text)

        replaced_text = ''
        start = 0
        for match in matches:
            end = match.start()

            replaced_text += self.replace_keywords(text[start:end])

            start = match.end()
            replaced_text += text[end:start]
        replaced_text += self.replace_keywords(text[start:])

        return replaced_text

    def postprocess(self, text):
        """
        Keyword replacement after translation
        """
        replaced_text = text

        for key in self.replaced:
            if key in replaced_text:
                replaced_text = replaced_text.replace(key, self.replaced[key], 1)
            elif key[:-1] in replaced_text:
                replaced_text = replaced_text.replace(key[:-1], self.replaced[key], 1)
            else:
                raise IndexError
        return replaced_text




if __name__ == '__main__':
    replacer = Replacer('ko')
    # replacer.add_keywords_from_dict({'ksa': ['한과 영', 'korea']})
    # print(replacer.replace_keywords('한과 영은 좋은 학교이다'))

    Replacer.add_keyword(('사과', 'apple'), 'ko')
    pre = replacer.preprocess('사과는 맛있다')
    print(pre)
    print(replacer.replaced)
    print(replacer.postprocess(pre))

