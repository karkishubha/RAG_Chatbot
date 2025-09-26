from typing import List
from dataclasses import dataclass
import nltk
nltk.download('punkt', quiet=True)

@dataclass
class Chunk:
    text: str
    start: int
    end: int

def chunk_by_sentences(text: str, max_sentences: int = 8, overlap: int = 2) -> List[Chunk]:
    sents = nltk.sent_tokenize(text)
    chunks = []
    i = 0
    while i < len(sents):
        seg = sents[i:i+max_sentences]
        chunks.append(Chunk(text=" ".join(seg), start=i, end=i+len(seg)-1))
        i += max_sentences - overlap
    return chunks

def chunk_by_tokens(text: str, max_tokens: int = 500, overlap: int = 50) -> List[Chunk]:
    tokens = text.split()
    chunks = []
    i = 0
    while i < len(tokens):
        seg = tokens[i:i+max_tokens]
        chunks.append(Chunk(text=" ".join(seg), start=i, end=i+len(seg)-1))
        i += max_tokens - overlap
    return chunks
