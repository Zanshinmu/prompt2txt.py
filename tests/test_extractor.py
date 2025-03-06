from prompt2txt.extractor import PromptExtractor

def test_clean_prompt_string():
    extractor = PromptExtractor()
    
    test_cases = [
        ("<tag>prompt</tag>", "prompt"),
        ("BREAK prompt BREAK", " prompt "),
        (",, prompt", "prompt"),
        ("prompt\nmore text", "prompt"),
    ]
    
    for input_str, expected in test_cases:
        assert extractor.clean_prompt_string(input_str) == expected
