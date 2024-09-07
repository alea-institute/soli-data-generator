"""
Generate annotated text from a context based on SOLI or Faker entities.
"""

# imports
import random
from typing import Optional

# packages
from alea_llm_client.llms import BaseAIModel
from alea_llm_client.llms.prompts.sections import format_instructions, format_prompt
from soli import SOLI, SOLI_TYPE_IRIS

from soli_data_generator.llm.text import MAX_TEXT_LENGTH, MIN_TEXT_LENGTH

# project
from soli_data_generator.procedural.template import (
    TemplateFormatter,
    get_all_tags,
    get_random_owl_label,
    normalize_soli_tag,
)

ANNOTATED_EXAMPLES = [
    "This <|document_artifact|> was filed on <|date|> by <|player_actor|> before the <|governmental_body|>.",
    "On or about <|date|>, <|player_actor|> filed a <|document_artifact|> with the <|forums_and_venues|>.",
    "<|company|>, a <|industry|> leader, is located in <|location|>.",
]


class AnnotatedTextGenerator:
    """
    Generate text procedurally from SOLI or Faker entities.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        model: BaseAIModel,
        min_types: int = 1,
        max_types: int = 3,
        min_text_length: int = MIN_TEXT_LENGTH,
        max_text_length: int = MAX_TEXT_LENGTH,
        source_type: str = "github",
        http_url: Optional[str] = None,
        github_repo_owner: Optional[str] = "alea-institute",
        github_repo_name: Optional[str] = "soli",
        github_repo_branch: Optional[str] = "1.0.0",
        use_cache: bool = True,
    ):
        """
        Initialize the TemplateFormatter from the SOLI knowledge graph.

        Args:
        - model (BaseAIModel): the AI model to use for text generation
        - source_type (str): the source type for the SOLI knowledge graph
        - github_repo_owner (str): the owner of the GitHub repository
        - github_repo_name (str): the name of the GitHub repository
        - github_repo_branch (str): the branch of the GitHub repository
        - use_cache (bool): whether to use the cache for the SOLI knowledge graph
        """
        # set the model
        self.model = model

        # set params
        self.min_types = min_types
        self.max_types = max_types
        self.min_text_length = min_text_length
        self.max_text_length = max_text_length

        # create the SOLI graph
        self.graph = SOLI(
            source_type=source_type,
            http_url=http_url,
            github_repo_owner=github_repo_owner,
            github_repo_name=github_repo_name,
            github_repo_branch=github_repo_branch,
            use_cache=use_cache,
        )

    def get_soli_examples(self, max_depth: int = 3, num_examples: int = 5) -> dict:
        """
        Get a random sample of SOLI class examples by tag.

        Args:
        - max_depth (int): the maximum depth to search for examples
        - num_examples (int): the number of examples to return

        Returns:
        - dict: the examples by tag
        """
        examples = {}
        for tag, tag_iri in SOLI_TYPE_IRIS.items():
            tag_name = normalize_soli_tag(tag.value)
            examples[tag_name] = []
            tag_examples = self.graph.get_children(tag_iri, max_depth=max_depth)
            for owl_class in random.sample(
                tag_examples, k=min(num_examples, len(tag_examples))
            ):
                examples[tag_name].append(
                    {
                        "label": get_random_owl_label(owl_class),
                        "definition": owl_class.definition,
                    }
                )

        return examples

    def generate(self) -> dict:
        """
        Generate text procedurally from SOLI or Faker entities.

        Returns:
        - str: the generated text
        """
        # get the document type
        document_type = random.choice(self.graph.get_document_artifacts(max_depth=3))

        # generate the prompt
        prompt = format_prompt(
            {
                "examples": "\n".join(ANNOTATED_EXAMPLES),
                "tag_examples": self.get_soli_examples(),
                "tags": get_all_tags(),
                "instructions": format_instructions(
                    [
                        "Carefully review the Tags and Tag Examples above.",
                        f"Draft realistic legal text from a {document_type}.",
                        "Use the Tags above as placeholders in the text.",
                        "Only use the Tags listed above.  Do not make up your own tags.",
                        "Do not respond with any other text or explanation.",
                    ]
                ),
            }
        )

        # get the template
        template = self.model.chat(prompt).text
        template_formatter = TemplateFormatter()

        return template_formatter.format_spans(template)

    def __call__(self, *args, **kwargs) -> dict:
        """
        Generate text procedurally from SOLI or Faker entities.

        Returns:
        - str: the generated text
        """
        return self.generate()
