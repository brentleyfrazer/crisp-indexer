"""
MS Crisp - Semantic & E-Prime Text Indexer
Based on research by Dr. Brentley Frazer (Griffith University)
DOI: 10.25904/1912/527
"""

import re
from typing import Dict, List, Any


class CrispIndexer:
    # Explicit copula forms (tenses of the verb 'to be')
    BASE_COPULAS = {
        "am", "is", "isn't", "are", "aren't", 
        "was", "wasn't", "were", "weren't", 
        "be", "been", "being"
    }

    # Contractions where the apostrophe represents an elided copula ('s = is, 're = are, 'm = am)
    COPULA_CONTRACTIONS = {
        "i'm", "you're", "we're", "they're", 
        "he's", "she's", "it's", "there's", 
        "here's", "where's", "how's", "what's", 
        "who's", "that's"
    }

    def __init__(self):
        self.forbidden_tokens = self.BASE_COPULAS.union(self.COPULA_CONTRACTIONS)
        # Regex to segment sentences on [.?!;:] while preserving integrity
        self.sentence_regex = re.compile(r'[^.?!;:]+[.?!;:]?', re.MULTILINE)
        # Word boundary tokenizer preserving apostrophes inside contractions
        self.word_regex = re.compile(r"\b[a-zA-Z]+(?:'[a-zA-Z]+)?\b")

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyzes text for E-Prime compliance.
        Computes the Bourland Crispiness Index (sentence-level) and Copula Density (token-level).
        """
        if not text or not text.strip():
            return {
                "total_words": 0,
                "total_sentences": 0,
                "copula_occurrences": 0,
                "copula_density_pct": 0.0,
                "crispy_sentences": 0,
                "non_crispy_sentences": 0,
                "crispiness_index": 1.0,
                "is_100_percent_eprime": True,
                "violations": []
            }

        # 1. Token-level analysis
        words_with_spans = [
            {"word": m.group(0), "lower": m.group(0).lower(), "start": m.start(), "end": m.end()}
            for m in self.word_regex.finditer(text)
        ]
        
        total_words = len(words_with_spans)
        violations = []
        for token in words_with_spans:
            if token["lower"] in self.forbidden_tokens:
                violations.append({
                    "word": token["word"],
                    "start": token["start"],
                    "end": token["end"],
                    "type": "copula" if token["lower"] in self.BASE_COPULAS else "copula_contraction"
                })

        copula_count = len(violations)
        copula_density = (copula_count / total_words * 100.0) if total_words > 0 else 0.0

        # 2. Sentence-level analysis (Bourland Crispiness Index)
        raw_sentences = [s.strip() for s in self.sentence_regex.findall(text) if s.strip()]
        total_sentences = len(raw_sentences)
        non_crispy_sentence_count = 0

        for sent in raw_sentences:
            sent_words = {w.lower() for w in self.word_regex.findall(sent)}
            if not sent_words.isdisjoint(self.forbidden_tokens):
                non_crispy_sentence_count += 1

        crispy_sentence_count = max(0, total_sentences - non_crispy_sentence_count)
        crispiness_index = (crispy_sentence_count / total_sentences) if total_sentences > 0 else 1.0

        return {
            "total_words": total_words,
            "total_sentences": total_sentences,
            "copula_occurrences": copula_count,
            "copula_density_pct": round(copula_density, 2),
            "crispy_sentences": crispy_sentence_count,
            "non_crispy_sentences": non_crispy_sentence_count,
            "crispiness_index": round(crispiness_index, 4),
            "is_100_percent_eprime": (copula_count == 0),
            "violations": violations
        }
