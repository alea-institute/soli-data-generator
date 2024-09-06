![SOLI Logo](https://openlegalstandard.org/assets/images/soli-intro-logo.png)

[![PyPI version](https://badge.fury.io/py/soli-data-generator.svg)](https://badge.fury.io/py/soli-data-generator)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/soli-data-generator.svg)](https://pypi.org/project/soli-data-generator/)

# SOLI Data Generator

SOLI Data Generator is a Python package for generating synthetic legal data using
the [SOLI (Standards for Open Legal Information)](https://openlegalstandard.org) knowledge graph. It provides both
procedural and LLM-based generation techniques to create realistic legal text and data.

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
Date: <|date|>
Document Type: <|document_artifact|>
"""

# Format the template
formatted_text = formatter(template)
print(formatted_text)
```

**Output**:

```text
Company: Griffith-Mahoney
Industry: Electric Power Generation, Transmission and Distribution Industry
Legal Issue: Privacy
Date: 2024-08-19
Document Type: Request to Take Judicial Notice
```

### Multiple Values per Type

```python
template = """
From: <|name:1|>
To: <|name:2|>, <|email:1|>, <|email:b|>
Date: <|date|>
Subject: <|company|> matter updates
"""

print(formatter(template))
```

**Output**:

```text
From: David Henry
To: Jean Vance, obryant@example.com, landrysamuel@example.com
Date: 2024-08-31
Subject: Dorsey Ltd
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

**Output with llama3.1 8B:**

```text
Be it known that White, Johnson and Morgan is in good standing, and I, the undersigned,
hereby attest to this fact. Were I to have knowledge of any reason why the said company
should not be considered in good standing, I would bring such to the attention of the
proper authorities.

Were the company not in good standing, I would not be able to issue this certificate. Were
there any outstanding matters or issues that would prevent the company from being
considered in good standing, I would be aware of them. Were this not the case, I would not
be able to provide this certification.

Were I to have knowledge of any reason why the said company should not be considered in
good standing, I would take immediate action to rectify the situation. Were this not
possible, I would report the matter to the relevant authorities. Were the company to be
found in bad standing, I would not be able to provide this certification.

It is hereby certified that White, Johnson and Morgan is in good standing as of the date
of this certificate. Were this certification to be found to be false or misleading, I
would be subject to penalties and consequences. Were I to have any knowledge that would
prevent the company from being considered in good standing, I would be obligated to report
such to the proper authorities.
```

Quality of generated text obviously varies by model and generation parameters.

## Examples

For more detailed examples, please check the `examples/` directory in this repository.

## Contributing

We welcome contributions to all SOLI libraries!

If you'd like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and write tests if applicable
4. Run the test suite to ensure everything is working
5. Submit a pull request with a clear description of your changes

## SOLI Python library

This library relies on the SOLI Python library for interacting with the SOLI knowledge graph. For more information about
the SOLI Python library, please visit
the [SOLI Python library repository](https://github.com/alea-institute/soli-python).

## SOLI API

A public, freely-accessible API is available for the SOLI ontology.

The API is hosted at [https://soli.openlegalstandard.org/](https://soli.openlegalstandard.org/).

The source code for the API is available on GitHub
at [https://github.com/alea-institute/soli-api](https://github.com/alea-institute/soli-api).

## License

The SOLI data generation library is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions about using the SOLI Python library,
please [open an issue](https://github.com/alea-institute/soli-data-generator/issues) on GitHub.

## Learn More

To learn more about SOLI, its development, and how you can get involved, visit
the [SOLI website](https://openlegalstandard.org/) or join
the [SOLI community forum](https://discourse.openlegalstandard.org/).
