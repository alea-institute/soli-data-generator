# import

# packages
from alea_llm_client import VLLMModel, AnthropicModel, OpenAIModel

# project
from soli_data_generator import TextGenerator


def test_vllm():
    model = VLLMModel()
    generator = TextGenerator(model)
    for _ in range(5):
        text = generator()
        assert isinstance(text, str)
        assert "<|" not in text
        assert len(text) > 0


def test_openai():
    model = OpenAIModel(model="gpt-4o-mini")
    generator = TextGenerator(model)
    for _ in range(5):
        text = generator()
        assert isinstance(text, str)
        assert "<|" not in text
        assert len(text) > 0


def test_anthropic():
    model = AnthropicModel()
    generator = TextGenerator(model)
    for _ in range(5):
        text = generator()
        assert isinstance(text, str)
        assert "<|" not in text
        assert len(text) > 0
