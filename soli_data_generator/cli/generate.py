"""
Generation CLI script to wrap the TextGenerator or AnnotatedTextGenerator classes.
"""

# imports
import argparse
import json

# packages
import tqdm
from alea_llm_client import AnthropicModel, OpenAIModel, VLLMModel
from soli import OWLClass

# project
from soli_data_generator.llm import AnnotatedTextGenerator, TextGenerator


def main():
    """
    pipx-runnable main function for generating text from an AI model.
    """
    # parse arguments
    parser = argparse.ArgumentParser(description="Generate text from an AI model.")
    parser.add_argument(
        "--model",
        type=str,
        default="vllm",
        help="the AI model to use for text generation (vllm:name, openai:name, or anthropic:name)",
    )
    parser.add_argument(
        "--type",
        type=str,
        default="annotated",
        help="the type of generation (text or annotated)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output.jsonl",
        help="the output JSON file for the generated text",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=10,
        help="the number of samples to generate",
    )
    args = parser.parse_args()

    # create the model
    if args.model.startswith("vllm"):
        if ":" in args.model:
            _, model_name = args.model.split(":")
            model = VLLMModel(model=model_name)
        else:
            model = VLLMModel()
    elif args.model == "openai":
        if ":" in args.model:
            _, model_name = args.model.split(":")
            model = OpenAIModel(model=model_name)
        else:
            model = OpenAIModel()
    elif args.model == "anthropic":
        if ":" in args.model:
            _, model_name = args.model.split(":")
            model = AnthropicModel(model=model_name)
        else:
            model = AnthropicModel()
    else:
        raise ValueError(f"Invalid model: {args.model}")

    # create the generator
    if args.type == "text":
        generator = TextGenerator(model)
    elif args.type == "annotated":
        generator = AnnotatedTextGenerator(model)
    else:
        raise ValueError(
            f"Invalid generation type: {args.type}; must be 'text' or 'annotated'"
        )

    # generate samples
    with open(args.output, "at+", encoding="utf-8") as output_file:
        for _ in tqdm.tqdm(range(args.samples)):
            try:
                sample = generator()
                if args.type == "annotated":
                    for span in sample["spans"]:
                        if isinstance(span["owl_class"], OWLClass):
                            span["owl_class"] = span["owl_class"].iri
            except Exception as e:
                print(f"Error generating sample: {str(e)}")
                continue

            output_file.write(json.dumps(sample) + "\n")
            output_file.flush()


if __name__ == "__main__":
    main()
