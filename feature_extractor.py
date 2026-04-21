"""
Feature extractor for misinformation/phishing detection.
No NLTK required — uses regex throughout so features port directly to JS.
"""

import re
import math
from typing import Dict


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sentences(text: str):
    """Split on sentence-ending punctuation."""
    raw = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in raw if len(s) > 2]


def _words(text: str):
    """Lowercase word tokens, letters only."""
    return re.findall(r"[a-z']+", text.lower())


def _safe_div(a, b, default=0.0):
    return a / b if b else default


# ---------------------------------------------------------------------------
# Feature groups
# ---------------------------------------------------------------------------

def syntactic_features(text: str) -> Dict[str, float]:
    sents = _sentences(text)
    words = _words(text)
    n_sents = max(len(sents), 1)
    n_words = max(len(words), 1)

    sent_lengths = [len(_words(s)) for s in sents]
    avg_sent_len = _safe_div(sum(sent_lengths), n_sents)
    sent_len_variance = _safe_div(
        sum((l - avg_sent_len) ** 2 for l in sent_lengths), n_sents
    )

    # Imperative verbs (command forms at sentence start)
    imperative_verbs = {
        "click", "verify", "confirm", "send", "call", "login", "log",
        "update", "provide", "submit", "enter", "download", "install",
        "act", "respond", "contact", "follow", "share", "buy", "order"
    }
    imperative_count = sum(
        1 for s in sents
        if _words(s) and _words(s)[0] in imperative_verbs
    )

    # Questions
    question_count = sum(1 for s in sents if s.strip().endswith("?"))

    # Passive voice proxy: "is/are/was/were/been + past-participle-ish word"
    passive_matches = len(re.findall(
        r'\b(is|are|was|were|been|being)\s+\w+ed\b', text, re.I
    ))

    return {
        "avg_sent_len": avg_sent_len,
        "sent_len_variance": sent_len_variance,
        "imperative_ratio": _safe_div(imperative_count, n_sents),
        "question_ratio": _safe_div(question_count, n_sents),
        "passive_ratio": _safe_div(passive_matches, n_sents),
    }


def statistical_features(text: str) -> Dict[str, float]:
    words = _words(text)
    n_words = max(len(words), 1)

    # Type-token ratio
    unique_words = set(words)
    ttr = _safe_div(len(unique_words), n_words)

    # Hapax legomena ratio (words appearing exactly once)
    from collections import Counter
    freq = Counter(words)
    hapax = sum(1 for w, c in freq.items() if c == 1)
    hapax_ratio = _safe_div(hapax, n_words)

    # ALL CAPS word ratio
    all_caps = len(re.findall(r'\b[A-Z]{3,}\b', text))
    caps_ratio = _safe_div(all_caps, n_words)

    # Exclamation density
    excl_count = text.count("!")
    excl_ratio = _safe_div(excl_count, len(_sentences(text)) or 1)

    # Readability: Flesch-Kincaid Grade Level proxy
    # FK = 0.39*(words/sentences) + 11.8*(syllables/words) - 15.59
    def count_syllables(word):
        word = word.lower()
        count = len(re.findall(r'[aeiou]+', word))
        if word.endswith('e') and count > 1:
            count -= 1
        return max(count, 1)

    syllables = sum(count_syllables(w) for w in words)
    n_sents = max(len(_sentences(text)), 1)
    fk_grade = (
        0.39 * _safe_div(n_words, n_sents)
        + 11.8 * _safe_div(syllables, n_words)
        - 15.59
    )

    return {
        "ttr": ttr,
        "hapax_ratio": hapax_ratio,
        "caps_ratio": caps_ratio,
        "exclamation_ratio": excl_ratio,
        "fk_grade": max(fk_grade, 0),
    }


def discourse_features(text: str) -> Dict[str, float]:
    t = text.lower()
    sents = _sentences(text)
    n_sents = max(len(sents), 1)
    words = _words(text)
    n_words = max(len(words), 1)

    # Attribution / evidence phrases
    attribution = [
        "according to", "researchers", "study found", "published in",
        "data shows", "scientists", "university", "reported by",
        "sources say", "officials said", "spokesperson", "confirmed by",
        "evidence suggests", "peer-reviewed", "journal"
    ]
    attr_count = sum(1 for p in attribution if p in t)

    # Declarative factual claim markers (asserting without evidence)
    claim_markers = [
        "the truth is", "everyone knows", "it is a fact", "proven that",
        "100%", "always", "never", "all doctors", "all scientists",
        "the government", "they don't want", "big pharma", "mainstream media"
    ]
    claim_count = sum(1 for p in claim_markers if p in t)

    # Hedging language (legitimate journalism)
    hedges = [
        "may", "might", "could", "alleged", "reportedly", "appears to",
        "suggests", "according", "possible", "likely", "unclear",
        "unconfirmed", "sources indicate"
    ]
    hedge_count = sum(1 for p in hedges if p in t)

    # Named entity proxies: capitalized word sequences (not sentence-start)
    named_entities = re.findall(r'(?<!\.\s)(?<!\n)(?<= )[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', text)
    ne_density = _safe_div(len(named_entities), n_words)

    # Social proof manipulation: short testimonial pattern
    # e.g. "I made $X" / "— Name" / "said [Name]"
    testimonial_pattern = len(re.findall(
        r'(i made \$|i earned|paid off|changed my life|— [A-Z]|" ?- ?[A-Z])', text, re.I
    ))

    # In-group/out-group framing
    outgroup = ["they", "elites", "the establishment", "globalists", "deep state", "mainstream"]
    ingroup = ["we the people", "real americans", "true patriots", "wake up", "sheeple"]
    outgroup_count = sum(t.count(w) for w in outgroup)
    ingroup_count = sum(t.count(w) for w in ingroup)

    return {
        "attribution_density": _safe_div(attr_count, n_sents),
        "unattributed_claim_ratio": _safe_div(claim_count, n_sents),
        "hedge_density": _safe_div(hedge_count, n_sents),
        "named_entity_density": ne_density,
        "testimonial_count": float(testimonial_pattern),
        "outgroup_framing": _safe_div(outgroup_count, n_words),
        "ingroup_framing": _safe_div(ingroup_count, n_words),
    }


def structural_phishing_features(text: str) -> Dict[str, float]:
    t = text.lower()

    # Credential requests — specific, not generic urgency words
    credential_asks = [
        "credit card number", "card number", "cvv", "social security",
        "ssn", "bank account", "routing number", "password", "pin number",
        "mother's maiden", "date of birth", "full name and address"
    ]
    cred_score = sum(1 for p in credential_asks if p in t)

    # Account threat language (requires action)
    account_threats = [
        "account.*suspend", "account.*terminat", "account.*clos",
        "access.*revok", "permanently closed", "legal action",
        "your account will", "account has been"
    ]
    threat_score = sum(
        1 for p in account_threats if re.search(p, t)
    )

    # Suspicious URL patterns (structural, not domain blocklist)
    urls = re.findall(r'https?://[^\s<>"]+', text, re.I)
    suspicious_url_score = 0
    for url in urls:
        domain = re.search(r'https?://([^/\s]+)', url)
        if domain:
            d = domain.group(1).lower()
            # High subdomain depth
            if d.count('.') >= 3:
                suspicious_url_score += 1
            # Non-standard TLDs
            if re.search(r'\.(ru|xyz|top|click|tk|ml|ga|cf|gq|pw|cc|ws)$', d):
                suspicious_url_score += 2
            # Brand name + extra chars (typosquatting proxy)
            brands = ["amazon", "paypal", "microsoft", "apple", "google",
                      "facebook", "netflix", "bank", "chase", "wells"]
            for brand in brands:
                if brand in d and not d.endswith(f'{brand}.com'):
                    suspicious_url_score += 2

    # Urgency co-occurring with threat (not standalone)
    urgency_words = [
        "immediately", "urgent", "within 24 hours", "within 48 hours",
        "act now", "final notice", "last chance", "expire"
    ]
    urgency_count = sum(1 for w in urgency_words if w in t)
    # Only meaningful if threat or credential ask is also present
    urgency_structural = float(
        urgency_count > 0 and (cred_score > 0 or threat_score > 0)
    )

    # Benign context suppressors
    benign = [
        "best regards", "kind regards", "sincerely", "thank you for",
        "please find attached", "as discussed", "following up",
        "per our conversation", "hope this helps", "feel free to"
    ]
    benign_score = sum(1 for p in benign if p in t)

    return {
        "credential_ask_count": float(min(cred_score, 5)),
        "account_threat_count": float(min(threat_score, 5)),
        "suspicious_url_score": float(min(suspicious_url_score, 6)),
        "urgency_structural": urgency_structural,
        "benign_context_score": float(min(benign_score, 4)),
    }


def ai_generated_features(text: str) -> Dict[str, float]:
    """
    Features that distinguish AI-generated text from human writing.
    Based on HC3 and RAID benchmark research findings.
    """
    words = _words(text)
    sents = _sentences(text)
    n_words = max(len(words), 1)
    n_sents = max(len(sents), 1)

    # AI text has unnaturally uniform sentence length
    sent_lengths = [len(_words(s)) for s in sents]
    if len(sent_lengths) > 2:
        mean_len = sum(sent_lengths) / len(sent_lengths)
        variance = sum((l - mean_len)**2 for l in sent_lengths) / len(sent_lengths)
        # Low variance relative to mean = suspiciously uniform
        uniformity = 1.0 - min(_safe_div(math.sqrt(variance), mean_len + 1), 1.0)
    else:
        uniformity = 0.0

    # Transition phrase density (AI overuses these)
    transitions = [
        "furthermore", "moreover", "additionally", "in conclusion",
        "it is important to note", "it should be noted", "as mentioned",
        "in summary", "to summarize", "notably", "significantly",
        "it is worth", "one must consider", "it is essential"
    ]
    t = text.lower()
    transition_count = sum(1 for p in transitions if p in t)
    transition_density = _safe_div(transition_count, n_sents)

    # Superlative/absolute claim density (AI spam hallmark)
    absolutes = [
        "best", "greatest", "most powerful", "revolutionary", "breakthrough",
        "guaranteed", "100%", "proven", "scientifically proven",
        "you will", "you'll never", "secret", "hidden truth"
    ]
    absolute_count = sum(1 for p in absolutes if p in t)

    # Lexical richness — AI text slightly more repetitive than human journalism
    from collections import Counter
    freq = Counter(words)
    top10_coverage = sum(sorted(freq.values(), reverse=True)[:10]) / n_words

    return {
        "sentence_uniformity": uniformity,
        "transition_density": transition_density,
        "absolute_claim_density": _safe_div(absolute_count, n_sents),
        "top10_word_coverage": top10_coverage,
    }


# ---------------------------------------------------------------------------
# Main extractor
# ---------------------------------------------------------------------------

FEATURE_NAMES = None  # set on first call


def extract_features(text: str) -> Dict[str, float]:
    """Extract all features. Returns an ordered flat dict."""
    feats = {}
    feats.update(syntactic_features(text))
    feats.update(statistical_features(text))
    feats.update(discourse_features(text))
    feats.update(structural_phishing_features(text))
    feats.update(ai_generated_features(text))
    return feats


def feature_vector(text: str):
    """Return features as an ordered list (for sklearn)."""
    d = extract_features(text)
    return list(d.values()), list(d.keys())


if __name__ == "__main__":
    sample = "Your Amazon account has been suspended. Verify your credit card number immediately at amaz0n-secure.ru or your account will be permanently closed."
    feats, names = feature_vector(sample)
    for n, v in zip(names, feats):
        print(f"  {n:<35} {v:.4f}")
