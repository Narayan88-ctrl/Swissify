# ~/Swissify/swissify_engine/rules/numbers_swiss.py
# Convert German-style numbers to Swiss style:
#  - thousands '.' -> apostrophe ’
#  - decimal ','   -> '.'
#  - DO NOT touch dates like 31.12.2025 or IPs etc.

from __future__ import annotations
import re

APO = "’"  # Swiss thousands separator

# --- Protect patterns we must not touch ---------------------------------------
_DATE = re.compile(r"\b\d{1,2}\.\d{1,2}\.\d{2,4}\b")
_IP   = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_VERSION = re.compile(r"\bv?\d+\.\d+(?:\.\d+)?\b")

_PROTECT_TOKEN_OPEN  = "\uE000"
_PROTECT_TOKEN_CLOSE = "\uE001"

def _protect(text: str) -> str:
    def wrap(m): return f"{_PROTECT_TOKEN_OPEN}{m.group(0)}{_PROTECT_TOKEN_CLOSE}"
    text = _DATE.sub(wrap, text)
    text = _IP.sub(wrap, text)
    text = _VERSION.sub(wrap, text)
    return text

def _unprotect(text: str) -> str:
    return text.replace(_PROTECT_TOKEN_OPEN, "").replace(_PROTECT_TOKEN_CLOSE, "")

# --- Core converters -----------------------------------------------------------
# 1) Decimal numbers with thousands groups:  1.234,56  ->  1’234.56
_DECIMAL_DE = re.compile(r"\b(\d{1,3}(?:\.\d{3})*),(\d+)\b")

# 2) Integers with thousands groups only:    12.345.678 -> 12’345’678
_INTEGER_DE = re.compile(r"\b\d{1,3}(?:\.\d{3})+\b")

def _repl_decimal(m: re.Match) -> str:
    int_part = m.group(1).replace(".", APO)
    frac_part = m.group(2)
    return f"{int_part}.{frac_part}"

def _repl_integer(m: re.Match) -> str:
    return m.group(0).replace(".", APO)

# Optional cleanup for any legacy ${n} placeholders (from old rules)
_PLACEHOLDER = re.compile(r"\$\{\d+\}")

def apply(text: str) -> str:
    if not text:
        return text
    original = text

    # Protect things we should not change
    text = _protect(text)

    # Decimals first (so we don't break integer-only pattern)
    text = _DECIMAL_DE.sub(_repl_decimal, text)

    # Then integers with thousands groups
    text = _INTEGER_DE.sub(_repl_integer, text)

    # Unprotect
    text = _unprotect(text)

    # Cleanup legacy placeholders if any slipped through
    text = _PLACEHOLDER.sub("", text)

    return text

# Minimal registry hook if your engine auto-loads packs/rules
def register():
    return {
        "name": "numbers_swiss",
        "fn": apply,
        "description": "Convert German number formatting to Swiss style (’ thousands, . decimal), safely ignoring dates/IPs.",
    }
