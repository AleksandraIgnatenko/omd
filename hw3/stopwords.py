from typing import Set, Dict, List, Tuple, Counter
import math

ENGLISH_STOPWORDS: Set[str] = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all',
    'am', 'an', 'and', 'any',
    'are', 'as', 'at', 'be', 'because', 'been', 'before',
    'being', 'below', 'between',
    'both', 'but', 'by', 'can', 'could', 'couldn', 'did',
    'didn', 'do', 'does', 'doesn',
    'doing', 'don', 'down', 'during', 'each', 'few', 'for',
    'from', 'further', 'had', 'hadn',
    'has', 'hasn', 'have', 'haven', 'having',
    'he', 'her', 'here', 'hers', 'herself', 'him',
    'himself', 'his', 'how', 'i', 'if', 'in',
    'into', 'is', 'isn', 'it', 'its', 'itself',
    'just', 'me', 'more', 'most', 'mustn', 'my',
    'myself', 'no', 'nor', 'not',
    'of', 'off', 'on', 'once', 'only', 'or', 'other',
    'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
    'same', 'shan', 'she', 'should', 'shouldn', 'so', 'some', 'such',
    'than', 'that', 'the', 'their', 'theirs', 'them',
    'themselves', 'then', 'there',
    'these', 'they', 'this', 'those', 'through', 'to',
    'too', 'under', 'until', 'up', 'very',
    'was', 'wasn', 'we', 'were', 'weren',
    'what', 'when', 'where', 'which', 'while', 'who', 'whom',
    'why', 'with', 'won', 'would', 'wouldn', 'you', 'your',
    'yours', 'yourself', 'yourselves',
    'concerning', 'having', 'especially', 'also',
    'well', 'made', 'made', 'based'
}


def calculate_tfdf(
    category_words_dict: Dict[str, List[str]]
) -> Dict[str, List[Tuple]]:
    """
    Рассчитывает метрику TF-IDF для слов в каждой категории премий.

    Args:
        category_words_dict: Словарь, где:
            ключ (str): название категории.
            значение (List[str]): список всех слов мотиваций в этой категории.

    Returns:
        Dict[str, List[tuple]]: Словарь, где:
            ключ (str): название категории.
            значение (List[tuple]): список кортежей.
    """
    num_categories: int = len(category_words_dict)
    tfdf_results: Dict[str, List[Tuple]] = {}

    word_doc_freq: Dict[str, int] = {}
    for cat, words in category_words_dict.items():
        unique_words_in_cat: Set[str] = set(
            w for w in words if w not in ENGLISH_STOPWORDS
        )
        for word in unique_words_in_cat:
            word_doc_freq[word] = word_doc_freq.get(word, 0) + 1

    for cat, words in category_words_dict.items():
        clean_words: List[str] = [
            w for w in words if w not in ENGLISH_STOPWORDS
        ]
        total_words_in_cat: int = len(clean_words)
        word_counts: Counter = Counter(clean_words)

        cat_tfidf: List[Tuple] = []

        for word, count in word_counts.items():
            tf: float = count / total_words_in_cat
            idf: float = math.log(num_categories / word_doc_freq[word])
            tfidf_score: float = tf * idf
            cat_tfidf.append((word, tfidf_score))

        tfdf_results[cat] = sorted(
            cat_tfidf,
            key=lambda x: x[1],
            reverse=True
        )

    return tfdf_results
