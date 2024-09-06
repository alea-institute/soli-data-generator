"""
Generate text from a context based on SOLI or Faker entities.
"""

# imports
import random
from typing import Optional

from alea_llm_client.llms import BaseAIModel

# packages
from soli import SOLI

# project
from soli_data_generator.procedural.template import TemplateFormatter

# constants
TEXT_UNITS = ["paragraph(s)", "sentence(s)"]
MIN_TEXT_LENGTH = 1
MAX_TEXT_LENGTH = 5

# person, tense, etc.
VERB = [
    "write",
    "draft",
    "compose",
    "create",
    "generate",
    "produce",
    "author",
    "craft",
    "formulate",
    "construct",
]
PERSON_VALUES = ["first", "second", "third"]
TENSE_VALUES = [
    "past",
    "present",
    "future",
    "imperfect",
    "conditional",
    "subjunctive",
    "imperative",
]


# faker/soli graph types for combinatorics
PROCEDURAL_TYPES = [
    "actor_player",
    "address",
    "area_of_law",
    "asset_type",
    "company",
    "date",
    "document_artifact",
    "event",
    "forums_and_venues",
    "industry",
    "location",
    "name",
    "objectives",
    "services",
]

TYPE_LABEL = {
    "actor_player": "Actor/Player",
    "address": "Address",
    "area_of_law": "Area of Law",
    "asset_type": "Asset Type",
    "company": "Company",
    "date": "Date",
    "document_artifact": "Document Artifact",
    "event": "Event",
    "forums_and_venues": "Forum/Venue",
    "industry": "Industry",
    "location": "Location",
    "name": "Name",
    "objectives": "Objectives",
    "services": "Services",
}


def get_random_background(
    soli_graph: SOLI,
    min_types: int = 1,
    max_types: int = 3,
) -> str:
    """
    Sample a random subset of tags, then populate the tag template with background.

    Args:
    - soli_graph (SOLI): the SOLI graph to use for sampling

    Returns:
    - str: the populated background text
    """
    # always include the document type
    document_type = random.choice(soli_graph.get_document_artifacts(max_depth=3))

    # sample a random subset of tags
    tags = random.sample(PROCEDURAL_TYPES, k=random.randint(min_types, max_types))

    # set up template
    background_template = ""
    for tag in tags:
        background_template += f"{TYPE_LABEL[tag]}: <|{tag}|>\n"

    # add document type directly
    background_template += f"Document Type: {document_type}\n"

    # format it
    t = TemplateFormatter()
    return t(background_template)


def get_random_instructions(
    min_length: int = MIN_TEXT_LENGTH, max_length: int = MAX_TEXT_LENGTH
) -> str:
    """
    Get randomized instructions for writing.

    Returns:
    - str: the randomized instructions
    """
    # cover the following:
    # - verb
    # - length
    # - text unit
    # - person
    # - tense
    verb = random.choice(VERB)
    text_length = random.randint(min_length, max_length)
    text_unit = random.choice(TEXT_UNITS)
    person = random.choice(PERSON_VALUES)
    tense = random.choice(TENSE_VALUES)

    return f"""# Instructions
1. Carefully review the Background information above.
2. {verb.title()} {text_length} {text_unit} in the {person} person and {tense} tense that would occur in the Document Type above.
3. Do not respond with any other tokens or explanation.  Just return the realistic text from the Document Type above.
"""


class TextGenerator:
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

    def generate(self) -> str:
        """
        Generate text procedurally from SOLI or Faker entities.

        Returns:
        - str: the generated text
        """
        # combine random background information with random drafting instructions
        prompt = get_random_background(
            soli_graph=self.graph,
            min_types=self.min_types,
            max_types=self.max_types,
        )
        prompt += "\n"
        prompt += get_random_instructions(
            min_length=self.min_text_length,
            max_length=self.max_text_length,
        )

        # return text from the model generation
        return self.model.chat(prompt).text

    def __call__(self, *args, **kwargs) -> str:
        """
        Generate text procedurally from SOLI or Faker entities.

        Returns:
        - str: the generated text
        """
        return self.generate()
