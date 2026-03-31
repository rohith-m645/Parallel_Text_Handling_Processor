"""
============================================================
 MODULE 2 — Rule Checker and Scorer
------------------------------------------------------------
 Responsibilities:
   - Score text using positive/negative word lists
   - Classify into 20+ sentiment/issue categories
   - Process batches in parallel (used by ProcessPoolExecutor)
============================================================
"""

from .loader import tokenize, clean_text

# ── Sentiment Word Lists ──
# Using set() for O(1) instant lookup speed (faster than list)
positive_words = set(["good", "great", "excellent", "happy", "amazing", "love",
                      "perfect", "awesome", "fantastic", "wonderful", "best",
                      "superb", "outstanding", "brilliant", "satisfied", "pleased"])

negative_words = set(["bad", "poor", "terrible", "hate", "worst",
                      "awful", "horrible", "useless", "pathetic", "disgusting",
                      "disappointed", "frustrating", "annoying", "waste", "regret"])

# ── Original Issue Categories ──
refund_words   = ["refund", "money back", "return", "cashback", "reimburse", "chargeback"]
delivery_words = ["late", "delayed", "not delivered", "missing", "never arrived",
                  "wrong address", "lost package", "tracking", "out for delivery"]
damage_words   = ["broken", "damaged", "defective", "cracked", "shattered",
                  "not working", "stopped working", "malfunction", "faulty"]
service_words  = ["no response", "rude", "unhelpful", "ignored", "bad support",
                  "poor service", "no help", "customer care", "not responding"]
price_words    = ["expensive", "overpriced", "costly", "too much", "not worth",
                  "cheap quality", "ripoff", "rip off", "waste of money"]
sarcasm_words  = ["yeah right", "as if", "sure it does", "totally works",
                  "oh great", "just what i needed"]
spam_words     = ["spam", "junk", "promotion", "advertisement", "unsolicited"]
scam_words     = ["scam", "fraud", "fake", "counterfeit", "duplicate",
                  "not original", "knockoff", "cheated", "deceived"]

# ── NEW Issue Categories ──

# Packaging issues
packaging_words = ["packaging", "poorly packed", "bad packaging", "box damaged",
                   "package torn", "no bubble wrap", "loose packaging",
                   "arrived open", "package broken", "wrapping"]

# Size / Fit issues
size_words      = ["wrong size", "too small", "too big", "size issue",
                   "doesnt fit", "doesn't fit", "size chart", "small fit",
                   "large fit", "incorrect size", "not my size", "tight fit",
                   "loose fit", "size mismatch"]

# Quality issues
quality_words   = ["poor quality", "low quality", "bad quality", "cheap material",
                   "not durable", "fell apart", "broke easily", "bad build",
                   "flimsy", "not sturdy", "bad finish", "peeling", "fading",
                   "quality issue", "not as described"]

# Wrong item issues
wrong_item_words = ["wrong item", "wrong product", "not what i ordered",
                    "different product", "incorrect item", "sent wrong",
                    "received wrong", "not matching", "different color",
                    "different model"]

# Warranty / Support issues
warranty_words  = ["warranty", "guarantee", "no warranty", "warranty expired",
                   "service center", "repair", "replacement", "after sales",
                   "not covered", "warranty claim"]

# Authenticity issues
authentic_words = ["not authentic", "not genuine", "original", "fake brand",
                   "not branded", "imitation", "replica", "not real",
                   "authenticity", "genuine product"]

# Stock / Availability issues
stock_words     = ["out of stock", "not available", "back order", "unavailable",
                   "sold out", "waitlist", "pre order", "stock issue"]

# App / Website issues
app_words       = ["app crash", "website down", "not loading", "error page",
                   "cant login", "can't login", "login issue", "app issue",
                   "website issue", "payment failed", "checkout error"]

# Health / Safety issues
safety_words    = ["unsafe", "dangerous", "health risk", "chemical smell",
                   "burning smell", "caught fire", "electric shock",
                   "safety issue", "hazardous", "toxic"]

# Quantity issues
quantity_words  = ["less quantity", "wrong quantity", "missing items",
                   "incomplete", "partial delivery", "not enough",
                   "quantity issue", "short quantity", "missing piece"]


# ── Score Function ──
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


# ── Classify Function ──
def classify(text, score):
    """
    Classifies text into one of 20 categories (priority order):

    HIGH PRIORITY (checked first):
      1. Scam Risk        6. Safety Issue
      2. Fraud/Fake       7. Health Risk

    ISSUE CATEGORIES:
      8.  Refund Issue       14. Wrong Item
      9.  Delivery Issue     15. Warranty Issue
      10. Product Damage     16. Stock Issue
      11. Customer Service   17. App/Website Issue
      12. Price Complaint    18. Quantity Issue
      13. Packaging Issue    19. Size/Fit Issue
                             20. Quality Issue

    SENTIMENT (fallback):
      21. Positive / Negative / Neutral
    """
    t = text.lower()

    # ── High Priority ──
    if any(w in t for w in scam_words):      return "Scam Risk"
    if any(w in t for w in spam_words):      return "Spam"
    if any(w in t for w in safety_words):    return "Safety Issue"
    if any(w in t for w in authentic_words): return "Authenticity Issue"

    # ── Issue Categories ──
    if any(w in t for w in refund_words):    return "Refund Issue"
    if any(w in t for w in delivery_words):  return "Delivery Issue"
    if any(w in t for w in damage_words):    return "Product Damage"
    if any(w in t for w in service_words):   return "Customer Service"
    if any(w in t for w in price_words):     return "Price Complaint"
    if any(w in t for w in packaging_words): return "Packaging Issue"
    if any(w in t for w in size_words):      return "Size/Fit Issue"
    if any(w in t for w in quality_words):   return "Quality Issue"
    if any(w in t for w in wrong_item_words):return "Wrong Item"
    if any(w in t for w in warranty_words):  return "Warranty Issue"
    if any(w in t for w in stock_words):     return "Stock Issue"
    if any(w in t for w in app_words):       return "App/Website Issue"
    if any(w in t for w in quantity_words):  return "Quantity Issue"
    if any(w in t for w in sarcasm_words):   return "Sarcasm"

    # ── Sentiment Fallback ──
    if score > 0:   return "Positive"
    elif score < 0: return "Negative"
    else:           return "Neutral"


# ── Batch Processor ──
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