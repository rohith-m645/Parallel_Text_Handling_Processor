"""
============================================================
 MODULE 2 — Rule Checker and Scorer
------------------------------------------------------------
 Responsibilities:
   - Score text using positive/negative word lists
   - Classify into 10 sentiment/issue categories
   - Process batches in parallel (used by ProcessPoolExecutor)
============================================================
"""

from .loader import tokenize, clean_text

# ── Word Lists ──
# Using set() for O(1) instant lookup speed (faster than list)
positive_words = set(["good", "great", "excellent", "happy", "amazing", "love"])
negative_words = set(["bad", "poor", "terrible", "hate", "worst"])

refund_words   = ["refund", "money back", "return"]
delivery_words = ["late", "delayed", "not delivered", "missing"]
damage_words   = ["broken", "damaged", "defective"]
service_words  = ["no response", "rude"]
price_words    = ["expensive", "overpriced"]
sarcasm_words  = ["yeah right", "as if"]
spam_words     = ["spam", "junk", "promotion"]
scam_words     = ["scam", "fraud", "fake"]


def calculate_score(text):
    """
    Rule-based sentiment scoring:
      +1 for each positive word found
      -1 for each negative word found
    Example: "great product but bad delivery" → score = 0
    """
    words = tokenize(text)
    score = 0
    for w in words:
        if w in positive_words:
            score += 1
        elif w in negative_words:
            score -= 1
    return score


def classify(text, score):
    """
    Classifies text into one of 10 categories (priority order):
      1. Scam Risk        6. Customer Service
      2. Spam             7. Price Complaint
      3. Refund Issue     8. Sarcasm
      4. Delivery Issue   9. Positive / Negative / Neutral
      5. Product Damage
    """
    text = text.lower()
    if any(w in text for w in scam_words):     return "Scam Risk"
    if any(w in text for w in spam_words):     return "Spam"
    if any(w in text for w in refund_words):   return "Refund Issue"
    if any(w in text for w in delivery_words): return "Delivery Issue"
    if any(w in text for w in damage_words):   return "Product Damage"
    if any(w in text for w in service_words):  return "Customer Service"
    if any(w in text for w in price_words):    return "Price Complaint"
    if any(w in text for w in sarcasm_words):  return "Sarcasm"
    if score > 0:   return "Positive"
    elif score < 0: return "Negative"
    else:           return "Neutral"


def process_batch(batch):
    """
    Processes a batch of text lines inside a separate CPU process.
    Must be module-level for multiprocessing pickling to work.

    Returns:
        list of tuples: (clean_text, score, sentiment)
    """
    results = []
    for line in batch:
        if line.strip():
            score     = calculate_score(line)
            sentiment = classify(line, score)
            results.append((clean_text(line), score, sentiment))
    return results
