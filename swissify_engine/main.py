from __future__ import annotations
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Set
from pathlib import Path
import re
import yaml

# ---------- Paths ----------
HERE = Path(__file__).resolve().parent
RULES_PATH = HERE / "swissify_rules.yaml"

# ---------- Config load ----------
def load_cfg() -> Dict[str, Any]:
    """
    Load YAML config. If missing, provide a safe minimal fallback so the engine still works.
    """
    if not RULES_PATH.exists():
        return {
            "packs": {
                "all": ["orthography_core", "swiss_lexicon", "numbers_swiss", "quotes_punct"],
                "default_enabled": ["orthography_core", "swiss_lexicon", "numbers_swiss", "quotes_punct"],
            },
            "rules": [
                {"pack": "orthography_core", "kind": "regex", "find": "ß", "replace": "ss"},
                {"pack": "orthography_core", "kind": "replace", "find": "ä", "replace": "ae"},
                {"pack": "orthography_core", "kind": "replace", "find": "ö", "replace": "oe"},
                {"pack": "orthography_core", "kind": "replace", "find": "ü", "replace": "ue"},
                {"pack": "orthography_core", "kind": "replace", "find": "Ä", "replace": "Ae"},
                {"pack": "orthography_core", "kind": "replace", "find": "Ö", "replace": "Oe"},
                {"pack": "orthography_core", "kind": "replace", "find": "Ü", "replace": "Ue"},
                {"pack": "orthography_core", "kind": "replace", "find": "Straße", "replace": "Strasse"},
                {"pack": "orthography_core", "kind": "replace", "find": "groß", "replace": "gross"},
                {"pack": "swiss_lexicon", "kind": "regex", "find": r"\bFahrrad\b", "replace": "Velo"},
                {"pack": "swiss_lexicon", "kind": "regex", "find": r"\bFahrräder\b", "replace": "Velos"},
                {"pack": "swiss_lexicon", "kind": "regex", "find": r"\bBürgersteig\b", "replace": "Trottoir"},
                {"pack": "swiss_lexicon", "kind": "regex", "find": r"\bKrankenhaus\b", "replace": "Spital"},
                {"pack": "swiss_lexicon", "kind": "regex", "find": r"\bErdgeschoss\b", "replace": "Parterre"},
                {"pack": "swiss_lexicon", "kind": "regex", "find": r"\bZugbegleiter\b", "replace": "Kondukteur"},
                {"pack": "swiss_lexicon", "kind": "regex", "find": r"\bSchaffner\b", "replace": "Kondukteur"},
                # Numbers & quotes fallback examples (real ones come from YAML)
            ],
        }

    data = yaml.safe_load(RULES_PATH.read_text(encoding="utf-8")) or {}

    # Normalize packs section (support both list and dict forms)
    packs = data.get("packs") or {}
    if isinstance(packs, list):
        packs = {"all": packs, "default_enabled": packs}
    packs.setdefault("all", [])
    default_enabled = packs.get("enable") or packs.get("default_enabled") or packs.get("all", [])
    packs["default_enabled"] = default_enabled
    data["packs"] = packs

    # Validate regex patterns
    rules = list(data.get("rules") or [])
    for i, r in enumerate(rules, 1):
        if (r.get("kind") or "replace").lower() == "regex":
            re.compile(r.get("find", ""))
    data["rules"] = rules
    return data

CFG = load_cfg()
ALL_PACKS: Set[str] = set(CFG["packs"]["all"])
DEFAULT_ENABLED: Set[str] = set(CFG["packs"]["default_enabled"])
RULES: List[Dict[str, Any]] = CFG["rules"]

# ---------- Engine core ----------
def apply_rules(text: str, enabled: Optional[Set[str]]) -> str:
    """
    Apply rules in order. If 'enabled' is None, use DEFAULT_ENABLED.
    - kind == 'regex'  -> re.sub
    - any other kind (replace/literal/missing) -> str.replace (literal)
    """
    active = enabled if enabled is not None else DEFAULT_ENABLED
    out = text
    for r in RULES:
        pack = r.get("pack") or ""
        if pack and active and pack not in active:
            continue
        kind = (r.get("kind") or "replace").lower()
        find = r.get("find", "")
        repl = r.get("replace", "")
        if not find:
            continue
        if kind == "regex":
            out = re.sub(find, repl, out)
        else:
            out = out.replace(find, repl)
    return out

def parse_enable_param(enable: Optional[str]) -> Optional[Set[str]]:
    """
    Parse ?enable=... query:
      - None  -> use DEFAULT_ENABLED
      - ""    -> empty set (disable all packs)
      - "a,b" -> set("a","b")
    """
    if enable is None:
        return None
    s = enable.strip()
    if s == "":
        return set()
    return {x.strip() for x in s.split(",") if x.strip()}

# ---------- FastAPI app ----------
app = FastAPI(title="Swissify Engine", version="1.2.0")

class ConvertIn(BaseModel):
    text: str

class ConvertOut(BaseModel):
    input: str
    output: str

@app.get("/health")
def health():
    return {
        "status": "ok",
        "rules": len(RULES),
        "packs_all": sorted(ALL_PACKS),
        "enabled_packs_default": sorted(DEFAULT_ENABLED),
    }

@app.get("/packs")
def packs():
    return {
        "all": sorted(ALL_PACKS),
        "default_enabled": sorted(DEFAULT_ENABLED),
        "count_rules": len(RULES),
    }

@app.post("/convert", response_model=ConvertOut)
def convert(payload: ConvertIn, enable: Optional[str] = Query(None, description="Comma-separated pack names")):
    enabled = parse_enable_param(enable)
    output = apply_rules(payload.text, enabled)
    return {"input": payload.text, "output": output}
