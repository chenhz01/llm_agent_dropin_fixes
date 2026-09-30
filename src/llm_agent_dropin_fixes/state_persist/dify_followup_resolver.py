# dify_followup_resolver.py
# Source issue: https://github.com/langgenius/dify/issues/43289
# Upstream repo: langgenius/dify #43289
# Category: state_persist
# Root cause / claim: Resolves anaphoric follow-ups to the anchor turn's slot so memory can seed the resolved query instead of raw sys.query.
# Verifier note: py rewrites 'And for 220 guests?' into 'And for 220 guests? (may, saturday)', exactly recovering the lost context in #43289.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

import re

# Plug in your own conversation turns (from the chat-messages API or backend state).
# The LLM node binds memory to raw sys.query, so a follow-up like 'And for 220 guests?'
# loses the 'Saturday in May' anchor from an earlier turn. This resolves the follow-up
# against the turn that carries the missing slot, so memory seeds the resolved query.

ENTITY_RE = re.compile(
    r'(?:\b\d{1,4}\b|monday|tuesday|wednesday|thursday|friday|saturday|sunday|'
    r'january|february|march|april|may|june|july|august|september|october|november|december)',
    re.I,
)

def slots(text):
    return set(m.group(0).lower() for m in ENTITY_RE.finditer(text))

def resolve_followup(turns):
    followup = next(t['text'] for t in reversed(turns) if t['role'] == 'user')
    anchor = None
    for t in reversed(turns):
        if t['role'] == 'user' and t['text'] != followup:
            anchor = t['text']; break
    missing = slots(anchor or '') - slots(followup)
    if not missing:
        return followup
    return followup.rstrip('?. ') + ' (' + ', '.join(sorted(missing)) + ')?'

if __name__ == '__main__':
    turns = [
        {'role': 'user', 'text': 'What is the price for a wedding on a Saturday in May?'},
        {'role': 'assistant', 'text': '120 per person.'},
        {'role': 'user', 'text': 'And for 220 guests?'},
    ]
    print(resolve_followup(turns))  # -> 'And for 220 guests? (may, saturday)'
