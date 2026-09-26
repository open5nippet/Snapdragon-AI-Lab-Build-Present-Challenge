import re
from collections import Counter

STOP = {
    "the","and","that","this","with","from","have","will","your","you","are","for","was",
    "were","into","about","there","their","they","then","than","what","when","where","which",
    "been","also","just","very","more","some","like","only","because","would","could","should",
    "has","had","but","not","can","all","our","its","a","an","of","to","in","on","is","it"
}


def split_sentences(text: str):
    text = re.sub(r"\s+", " ", text.strip())
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def keyword_list(text: str, n=8):
    words = re.findall(r"[A-Za-z][A-Za-z0-9'-]{2,}", text.lower())
    counts = Counter(w for w in words if w not in STOP)
    return [w for w, _ in counts.most_common(n)]


def heuristic_pack(text: str):
    sents = split_sentences(text)
    keys = keyword_list(text)
    ranked = sorted(sents, key=lambda s: len(set(re.findall(r"[a-zA-Z]+", s.lower())) & set(keys)), reverse=True)
    summary = " ".join(ranked[:3]) if ranked else "No summary available."

    actions = []
    for s in sents:
        low = s.lower()
        if any(x in low for x in ["need to", "should", "must", "todo", "action", "submit", "prepare", "review", "finish"]):
            actions.append(s)
    if not actions and sents:
        actions = ["Review the main points and turn them into your next study or meeting action."]

    questions = []
    for k in keys[:5]:
        questions.append(f"What is {k} and why does it matter in this topic?")

    glossary = [
        f"{k}: a term worth reviewing in the context of this transcript." for k in keys[:5]
    ]

    return {
        "summary": summary,
        "key_points": ranked[:6],
        "action_items": actions[:5],
        "glossary": glossary,
        "questions": questions,
    }
