import re
from random import choice
from datetime import datetime

def _collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def _cap_length(text: str, limit: int = 420) -> str:
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + " …"

# Remove last sentence if they are questions (helps avoid interrogating tone)
def strip_trailing_question(reply: str, max_remove: int = 1) -> str:
    text = reply.strip()
    for _ in range(max_remove):
        parts = re.split(r'(?<=[.!?])\s+', text)
        if parts and parts[-1].endswith("?") and len(parts) > 1:
            parts = parts[:-1]
            text = " ".join(parts)
        else:
            break
    return text

_GREETING_PATTERNS = [
    r"^\s*hi+\b", r"^\s*hello\b", r"^\s*hey+\b", r"^\s*y[o0]\b",
    r"^\s*good\s+morning\b", r"^\s*good\s+afternoon\b", r"^\s*good\s+evening\b",
    r"^\s*hi(?:\s*there)?\b", r"^\s*hello(?:\s*there)?\b", r"^\s*hey(?:\s*there)?\b"
]

def is_greeting(user_input: str) -> bool:
    lowered = user_input.lower().strip()
    lowered = re.sub(r"[!.\-~]+$", "", lowered)  # tolerate punctuation at end
    return any(re.search(p, lowered) for p in _GREETING_PATTERNS)

def greeting_reply() -> str:
    hour = datetime.now().hour
    if 5 <= hour < 12:
        sal = "Good morning"
    elif 12 <= hour < 18:
        sal = "Good afternoon"
    else:
        sal = "Good evening"
    return f"{sal}! I’m really glad you reached out. How are you feeling today?"

def add_encouragement(reply: str, emotion: str) -> str:
    bank = {
        "negative": [
            "You're not alone — we can take this one small step at a time.",
            "It's okay to feel like this; it says nothing about your worth.",
            "I’m here with you. You’ve handled hard days before."
        ],
        "neutral": [
            "I’m here if you want to talk things through.",
            "Taking a moment to check in with yourself can help.",
            "One step at a time is still progress."
        ],
        "positive": [
            "That’s great — keep leaning into what’s working for you!",
            "Lovely to hear — celebrate the small wins.",
            "Hold on to that good momentum."
        ]
    }
    choices = bank.get(emotion, [])
    return _collapse_ws(f"{reply} {choice(choices) if choices else ''}")

def coping_suggestion(emotion: str) -> str:
    suggestions = {
        "negative": [
            "If it helps, try a 4-7-8 breath: inhale 4, hold 7, exhale 8.",
            "You could jot down one thing that feels manageable today.",
            "A short walk or stretch might ease the intensity a bit."
        ],
        "neutral": [
            "A brief pause to notice your body and breath can be grounding.",
            "Setting a tiny, doable goal can create momentum."
        ],
        "positive": [
            "Maybe note what helped today so future-you can reuse it.",
            "Sharing your good moment with someone can reinforce it."
        ]
    }
    opts = suggestions.get(emotion, [])
    return choice(opts) if opts else ""

_CRISIS_PATTERNS = [
    r"\bkill myself\b", r"\bsuicid(e|al)\b", r"\bend it all\b",
    r"\bself[-\s]?harm\b", r"\bcut(ting)? myself\b", r"\bI don'?t want to live\b"
]

def _matches_any(text: str, patterns) -> bool:
    return any(re.search(p, text, flags=re.IGNORECASE) for p in patterns)

def crisis_message() -> str:
    return (
        "I’m really sorry you’re feeling this overwhelmed. You matter, and you deserve support. "
        "If you feel in immediate danger, please contact local emergency services now. "
        "If you can, consider reaching out to someone you trust or a local crisis line for immediate help."
    )

SENSITIVE_MAP = {
    ("useless", "worthless", "no value", "hate myself"): [
        "You’re not your thoughts — feeling low doesn’t make you less worthy.",
        "Please be gentle with yourself; your worth isn’t measured by today’s feelings."
    ],
    ("failed", "i failed", "fail", "flunk", "did badly", "bad grade"): [
        "A result is feedback, not a final verdict on you.",
        "One setback doesn’t define you — skills grow with practice and support."
    ],
    ("disappoint", "let down my parents", "not good enough for my parents"): [
        "Feeling pressure from expectations is heavy — your effort still matters.",
        "Your value isn’t defined by meeting every expectation; you’re allowed to learn at your pace."
    ],
    ("anxious", "panic", "overwhelmed", "stressed", "can’t cope"): [
        "That sounds intense. Let’s slow the moment: name 5 things you can see, 4 you can feel.",
        "Your body is signaling overload — small grounding steps can help."
    ],
    ("alone", "lonely", "no one cares"): [
        "I’m here with you right now. Reaching out is a strong step.",
        "It can feel isolating — is there one person you might text today?"
    ],
}

def override_for_sensitive_inputs(user_input: str) -> str | None:
    lowered = user_input.lower()

    if _matches_any(lowered, _CRISIS_PATTERNS):
        return crisis_message()

    for triggers, responses in SENSITIVE_MAP.items():
        if any(t in lowered for t in triggers):
            return choice(responses)
    return None

# Remove irrelevant persona lines from open-domain models
_PERSONA_PATTERNS = [
    r"\bI am at home\b.*", r"\bI (just|recently) got back\b.*",
    r"\bI am (watching|playing)\b.*", r"\bmy (boyfriend|girlfriend|dog|cat)\b.*"
]

def sanitize_model_reply(text: str) -> str:
    cleaned = text.strip()
    sentences = re.split(r'(?<=[.!?])\s+', cleaned)
    kept = []
    for s in sentences:
        if any(re.search(p, s, flags=re.IGNORECASE) for p in _PERSONA_PATTERNS):
            continue
        kept.append(s)
    cleaned = " ".join(kept).strip()
    return _collapse_ws(cleaned)

def build_final_reply(user_input: str, model_reply: str, emotion: str) -> str:
    if is_greeting(user_input):
        base = greeting_reply()
        out = add_encouragement(base, emotion)
        tip = coping_suggestion(emotion)
        if tip:
            out = f"{out} {tip}"
        return _cap_length(_collapse_ws(out))

    sensitive = override_for_sensitive_inputs(user_input)
    if sensitive:
        out = add_encouragement(sensitive, emotion)
        tip = coping_suggestion(emotion)
        if tip:
            out = f"{out} {tip}"
        return _cap_length(_collapse_ws(out))

    reply = sanitize_model_reply(model_reply)
    reply = strip_trailing_question(reply, max_remove=2 if emotion == "negative" else 1)
    out = add_encouragement(reply, emotion)
    tip = coping_suggestion(emotion)
    if tip and emotion != "positive":
        out = f"{out} {tip}"
    return _cap_length(_collapse_ws(out))
