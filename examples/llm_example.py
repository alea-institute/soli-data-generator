# imports
from alea_llm_client import VLLMModel
from soli_data_generator import TextGenerator


if __name__ == "__main__":
    # Initialize the VLLM model
    # Can also use OpenAIModel or AnthropicModel.
    model = VLLMModel()

    # Initialize the TextGenerator
    generator = TextGenerator(model)

    # Generate text
    for i in range(3):
        print("Sample", i + 1)
        text = generator()
        print(text)
