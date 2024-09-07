# import

# packages
from alea_llm_client import VLLMModel, AnthropicModel, OpenAIModel

# project
from soli_data_generator import AnnotatedTextGenerator

# model fixture


def test_vllm():
    model = VLLMModel()
    generator = AnnotatedTextGenerator(model)
    for _ in range(3):
        sample = generator()
        assert isinstance(sample, dict)
        assert len(sample["spans"]) > 0


def test_openai():
    model = OpenAIModel(model="gpt-4o")
    generator = AnnotatedTextGenerator(model)
    for _ in range(3):
        sample = generator()
        assert isinstance(sample, dict)
        assert len(sample["spans"]) > 0


def test_anthropic():
    model = AnthropicModel()
    generator = AnnotatedTextGenerator(model)
    for _ in range(3):
        sample = generator()
        assert isinstance(sample, dict)
        assert len(sample["spans"]) > 0
