import os
import jieba
import math
from collections import Counter, defaultdict

class SparseRetrievalSystem:
    def __init__(self):
        self.documents = {}
        self.inverted_index = defaultdict(dict)
        self.doc_lengths = {}
        self.doc_count = 0
        self.term_doc_freq = Counter()

    def add_document(self, doc_id, content):
        self.documents[doc_id] = content
        words = list(jieba.cut(content))
        words = [word.lower().strip() for word in words if len(word.strip()) > 1]
        word_freq = Counter(words)
        self.doc_lengths[doc_id] = len(words)
        for term, tf in word_freq.items():
            self.inverted_index[term][doc_id] = tf
        unique_terms = set(words)
        for term in unique_terms:
            self.term_doc_freq[term] += 1
        self.doc_count += 1

    def calculate_tf_idf(self, term, doc_id):
        if term not in self.inverted_index or doc_id not in self.inverted_index[term]:
            return 0.0
        tf = self.inverted_index[term][doc_id]
        df = self.term_doc_freq[term]
        tf_score = tf / self.doc_lengths[doc_id]
        idf_score = math.log(self.doc_count / (df + 1))
        return tf_score * idf_score

    def calculate_bm25(self, term, doc_id, k1=1.2, b=0.75):
        if term not in self.inverted_index or doc_id not in self.inverted_index[term]:
            return 0.0
        tf = self.inverted_index[term][doc_id]
        df = self.term_doc_freq[term]
        doc_len = self.doc_lengths[doc_id]
        avg_doc_len = sum(self.doc_lengths.values()) / len(self.doc_lengths)
        idf = math.log((self.doc_count - df + 0.5) / (df + 0.5) + 1)
        tf_component = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / avg_doc_len)))
        return idf * tf_component

    def search(self, query, algorithm='tf_idf', top_k=5):
        query_terms = list(jieba.cut(query))
        query_terms = [term.lower().strip() for term in query_terms if len(term.strip()) > 1]
        if not query_terms:
            return []
        doc_scores = defaultdict(float)
        for term in query_terms:
            if term in self.inverted_index:
                for doc_id in self.inverted_index[term]:
                    if algorithm == 'tf_idf':
                        score = self.calculate_tf_idf(term, doc_id)
                    elif algorithm == 'bm25':
                        score = self.calculate_bm25(term, doc_id)
                    else:
                        score = self.inverted_index[term][doc_id]
                    doc_scores[doc_id] += score
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_docs[:top_k]

    def get_statistics(self):
        return {
            'document_count': self.doc_count,
            'vocabulary_size': len(self.inverted_index),
            'total_terms': sum(self.doc_lengths.values()),
            'avg_doc_length': sum(self.doc_lengths.values()) / len(self.doc_lengths) if self.doc_lengths else 0
        }