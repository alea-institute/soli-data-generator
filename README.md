# SOLI Data Generator

SOLI Data Generator is a Python package for generating synthetic legal data using the SOLI (Standards for Open Legal Information) knowledge graph. It provides both procedural and LLM-based generation techniques to create realistic legal text and data.

## Features

- Procedural generation using templates with SOLI and Faker tags
- LLM-based text generation using various AI models
- Easy integration with the SOLI knowledge graph
- Flexible and extensible architecture

## Installation

You can install SOLI Data Generator using pip:

```bash
pip install soli-data-generator
```

## Usage

### Procedural Template Generation

```python
from soli import SOLI
from soli_data_generator.procedural.template import TemplateFormatter

# Initialize the SOLI graph
soli_graph = SOLI()

# Initialize the TemplateFormatter
formatter = TemplateFormatter()

# Define a template with SOLI and Faker tags
template = """
Company: <|company|>
Industry: <|industry|>
Legal Issue: <|area_of_law|>
Document Type: <|document_artifact|>
"""

# Format the template
formatted_text = formatter.format(template)

print(formatted_text)
```

### LLM-based Text Generation

```python
from alea_llm_client import VLLMModel
from soli_data_generator.llm.text import TextGenerator

# Initialize the VLLM model
model = VLLMModel()

# Initialize the TextGenerator
generator = TextGenerator(model)

# Generate text
generated_text = generator()

print(generated_text)
```

## Examples

For more detailed examples, please check the `examples/` directory in this repository.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Contact

For any questions or concerns, please open an issue on the GitHub repository.
