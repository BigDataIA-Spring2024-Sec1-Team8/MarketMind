from genai.genai_handler import call_gemini_api

def test_genai_response():
    resposne = call_gemini_api("hi")
    assert len(resposne) != 0 