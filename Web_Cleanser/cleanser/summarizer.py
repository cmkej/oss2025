# cleanser/summarizer.py

import re
import numpy as np
from collections import Counter


# -------------------------
# 문단 분리
# -------------------------
def split_paragraphs(text):
    paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 30]
    return paragraphs


# -------------------------
# 문장 분리
# -------------------------
def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 15]
    return sentences


# -------------------------
# 문장 전처리
# -------------------------
def preprocess(sentence):
    return re.findall(r"[가-힣a-zA-Z]+", sentence.lower())


# -------------------------
# 벡터 변환
# -------------------------
def sentence_to_vector(words, vocab):
    counter = Counter(words)
    return np.array([counter.get(word, 0) for word in vocab], dtype=float)


# -------------------------
# 코사인 유사도
# -------------------------
def cosine_sim(a, b):
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# -------------------------
# 문단 기반 + TextRank 혼합 요약 (문장 자르지 않음!)
# -------------------------
def summarize_text(text, summary_count=3):
    # 문단 나누기
    paragraphs = split_paragraphs(text)
    if len(paragraphs) == 0:
        return "요약할 문단이 없습니다."

    # 문단 중요도 (길이 기반)
    paragraph_scores = [(i, len(p)) for i, p in enumerate(paragraphs)]
    paragraph_scores.sort(key=lambda x: x[1], reverse=True)

    # 상위 문단 선택 (최대 3개)
    selected_paragraphs = [paragraphs[i] for i, _ in paragraph_scores[:3]]

    # 문단 내 문장 추출
    all_sentences = []
    for p in selected_paragraphs:
        all_sentences.extend(split_sentences(p))

    if len(all_sentences) == 0:
        return "요약할 문장이 없습니다."

    # TextRank: 문장 간 유사도 기반 점수 계산
    processed = [preprocess(s) for s in all_sentences]
    vocab = list(set(word for words in processed for word in words))
    vectors = np.array([sentence_to_vector(words, vocab) for words in processed])

    n = len(vectors)
    sim_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                sim_matrix[i][j] = cosine_sim(vectors[i], vectors[j])

    scores = np.sum(sim_matrix, axis=1)

    # 점수 높은 문장 선택
    top_idx = np.argsort(scores)[::-1][:summary_count]
    top_idx.sort()

    # 🔥 핵심 문장 그대로 출력 (절대 자르지 않음)
    selected = [all_sentences[i] for i in top_idx]

    return " ".join(selected)
