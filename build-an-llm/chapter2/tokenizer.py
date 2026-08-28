import re
import tiktoken


class SimpleTokenizerV1:
    def __init__(self, vocab: dict[str:int]) -> None:
        self.str2int = vocab
        self.int2str = {id: token for token, id in vocab.items()}

    def encode(self, text: str) -> list[int]:
        preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', text)
        preprocessed = [item.strip() for item in preprocessed if item.strip()]
        preprocessed = [
            item if item in self.str2int else "<|unk|>" for item in preprocessed
        ]
        ids = [self.str_to_int[s] for s in preprocessed]
        return ids

    def decode(self, ids: list[int]) -> str:
        text = " ".join([self.int2str[id] for id in ids])
        text = re.sub(r'\s+(,.?!"()\)', r"\1", text)
        return text


tokenizer = tiktoken.get_encoding("gpt2")
text = "Akwirw ier"
ids = tokenizer.encode(text)
encoded_decoded_text = tokenizer.decode(ids)
print(encoded_decoded_text)
