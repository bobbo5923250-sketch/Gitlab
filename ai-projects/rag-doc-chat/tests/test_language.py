from rag.language import contains_chinese, detect_language, language_instruction, strict_language_instruction


def test_detect_language():
    assert detect_language("ลาพักร้อนได้กี่วัน") == "Thai"
    assert detect_language("How many days of leave?") == "English"
    assert detect_language("ใช้ API ยังไง") == "Thai"  # mixed Thai + English counts as Thai


def test_instructions_name_the_language():
    assert "Thai" in language_instruction("สวัสดี")
    assert "ภาษาไทย" in strict_language_instruction("สวัสดี")


def test_contains_chinese():
    assert contains_chinese("ลาคลอดได้ 98 วัน 其中有")
    assert not contains_chinese("ลาคลอดได้ 98 วัน [1]")
