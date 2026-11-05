"""Pin the answer language.

Multilingual models such as Qwen sometimes drift into Chinese when the question
is in a lower-resource language like Thai. Telling the model the exact language
(instead of "reply in the same language") fixes most of these cases.
"""

import re

_THAI = re.compile(r"[฀-๿]")
_CJK = re.compile(r"[一-鿿㐀-䶿]")


def detect_language(text: str) -> str:
    return "Thai" if _THAI.search(text) else "English"


def language_instruction(text: str) -> str:
    lang = detect_language(text)
    return f"Answer in {lang} only. Do not use Chinese or any other language."


def strict_language_instruction(text: str) -> str:
    """A firmer reminder written in the target language itself, used when retrying."""
    if detect_language(text) == "Thai":
        return "สำคัญมาก: ตอบเป็นภาษาไทยเท่านั้น ห้ามใช้ภาษาจีนเด็ดขาด ถ้าข้อมูลเป็นภาษาอังกฤษ ให้แปลเป็นภาษาไทย"
    return "IMPORTANT: answer in English only. Never use Chinese."


def contains_chinese(text: str) -> bool:
    return bool(_CJK.search(text))
