"""
Simple procedural template method for SOLI data generation.

This method relies on a simple markup format for SOLI tag structure and Faker methods that supports
one or more sampled values for each SOLI taxonomic category or Faker method.

Examples:
 - We are representing a client in the <|industry|> industry regarding a situation involving <|area_of_law|>.
 - The company has multiple business lines, including both <|industry:1|> and <|industry:2|> operations.
 - The experts who will be working on this matter include both <|name:1|> and <|name:2|>.


Valid SOLI tags:
    actor_player
    area_of_law
    asset_type
    communication_modality
    currency
    data_format
    document_artifact
    engagement_terms
    event
    forums_and_venues
    governmental_body
    industry
    language
    soli_type
    legal_authorities
    legal_entity
    location
    matter_narrative
    matter_narrative_format
    objectives
    service
    standards_compatibility
    status
    system_identifiers
"""

import random
import re

# imports
from enum import Enum
from typing import Any, Dict, Optional, Tuple

from faker import Faker

# packages
from soli import SOLI, OWLClass, SOLITypes

# project


class FakerTag(Enum):
    """
    Faker tag enumeration for supported Faker methods.
    """

    ADDRESS = "address"
    COMPANY = "company"
    DATE = "date"
    TIME = "time"
    EMAIL = "email"
    FILENAME = "filename"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    NAME = "name"
    JOB = "job"


# TODO: decide where/how we want to set seed
# TODO: decide if we want to switch to numpy RNG

# TODO: enhanced configuration for this
FAKER_INSTANCE = Faker()


def normalize_soli_tag(tag: str) -> str:
    """
    Normalize the SOLI tag names by:
     - lowercasing
     - replacing spaces with _
     - removing any /, -, or other special characters
     - replacing 2+ _ with a single _

    Args:
    - tag (str): the SOLI tag to normalize

    Returns:
    - str: the normalized SOLI tag
    """
    return re.sub(r"[_\W]+", "_", tag.strip().lower())


def build_regex_pattern():
    """
    Combine all SOLI taxonomic categories and Faker methods into a single regex pattern for matching SOLI tags.

    Make sure to support both single and multiple values for each taxonomic category or Faker method.
     - <|tag|>
     - <|tag:1|>
     - <|tag:a|>

    Returns:
    - str: the regex pattern for matching SOLI tags
    """
    # get each tag set
    soli_tags = "|".join([normalize_soli_tag(tag.value) for tag in SOLITypes])
    faker_tags = "|".join([tag.value for tag in FakerTag])

    # create a regex that will match any of the tags, with optional index or count
    return rf"<\|(?P<tag>{soli_tags}|{faker_tags})(?::(?P<index>[0-9]+|[a-z]))?\|>"


# compiled pattern mapper
RE_PATTERN_MAP = re.compile(build_regex_pattern())


def build_pattern_map(template: str, pattern: re.Pattern = RE_PATTERN_MAP) -> dict:
    """
    Build a mapping of tags in a template to their corresponding taxonomic categories or Faker methods.

    Args:
    - template (str): the template string containing SOLI tags

    Returns:
    - dict: the mapping of SOLI tags to their corresponding taxonomic categories or Faker methods
    """
    # find all matches in the template
    matches = pattern.finditer(template)

    # build a mapping of tag to taxonomic category or Faker method
    pattern_map = {}
    for match in matches:
        tag = match.group("tag")
        index = match.group("index")
        pattern_map[(tag, index)] = None

    return pattern_map


def get_template_tag(tag: str, index: str) -> str:
    """
    Get the template tag for a SOLI taxonomic category or Faker method.

    Args:
        - tag (str): the SOLI tag
        - index (str): the index of the SOLI tag

    Returns:
        - str: the template tag for the SOLI taxonomic category or Faker method
    """
    return f"<|{tag}{f':{index}' if index else ''}|>"


def get_random_owl_label(owl_class: OWLClass) -> str:
    """
    Get a random label for an OWL class.

    Args:
    - owl_class (OWLClass): the OWL class to get a label for

    Returns:
    - str: a random label for the OWL class
    """
    # store label set
    label_choices = []
    if owl_class.label:
        label_choices.append(owl_class.label)

    if owl_class.preferred_label:
        label_choices.append(owl_class.preferred_label)

    if owl_class.alternative_labels:
        label_choices.extend(owl_class.alternative_labels)

    return random.choice(label_choices)


# pylint: disable=too-many-branches,too-many-statements
def sample_values(
    pattern_map: Dict[Tuple[str, str], Any],
    soli_graph: SOLI,
) -> Dict[Tuple[str, str], int | float | str]:
    """
    Sample values for each SOLI taxonomic category or Faker method in the pattern map.

    Args:
    - pattern_map (dict): the mapping of SOLI tags to their corresponding taxonomic categories or Faker methods

    Returns:
    - dict: the mapping of SOLI tags to their corresponding sampled values
    """
    # sample values for each tag
    value_map = {}
    for tag, index in pattern_map.keys():
        # Faker sampling
        if tag == "address":
            value_map[(tag, index)] = FAKER_INSTANCE.address()
        elif tag == "company":
            value_map[(tag, index)] = FAKER_INSTANCE.company()
        elif tag == "date":
            date_type = random.choice(["past", "future", "decade"])
            if date_type == "past":
                value_map[(tag, index)] = FAKER_INSTANCE.past_date()
            elif date_type == "future":
                value_map[(tag, index)] = FAKER_INSTANCE.future_date()
            elif date_type == "decade":
                value_map[(tag, index)] = FAKER_INSTANCE.date_this_decade()
        elif tag == "time":
            value_map[(tag, index)] = FAKER_INSTANCE.time()
        elif tag == "email":
            value_map[(tag, index)] = FAKER_INSTANCE.email()
        elif tag == "filename":
            value_map[(tag, index)] = FAKER_INSTANCE.file_name()
        elif tag == "first_name":
            value_map[(tag, index)] = FAKER_INSTANCE.first_name()
        elif tag == "last_name":
            value_map[(tag, index)] = FAKER_INSTANCE.last_name()
        elif tag == "name":
            value_map[(tag, index)] = FAKER_INSTANCE.name()
        elif tag == "job":
            value_map[(tag, index)] = FAKER_INSTANCE.job()
        # SOLI sampling
        elif tag == "actor_player":
            sampled_class: OWLClass = random.choice(soli_graph.get_player_actors())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "area_of_law":
            sampled_class: OWLClass = random.choice(soli_graph.get_areas_of_law())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "asset_type":
            sampled_class: OWLClass = random.choice(soli_graph.get_asset_types())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "communication_modality":
            sampled_class: OWLClass = random.choice(
                soli_graph.get_communication_modalities()
            )
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "currency":
            sampled_class: OWLClass = random.choice(soli_graph.get_currencies())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "data_format":
            sampled_class: OWLClass = random.choice(soli_graph.get_data_formats())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "document_artifact":
            sampled_class: OWLClass = random.choice(soli_graph.get_document_artifacts())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "engagement_terms":
            sampled_class: OWLClass = random.choice(soli_graph.get_engagement_terms())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "event":
            sampled_class: OWLClass = random.choice(soli_graph.get_events())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "forums_and_venues":
            sampled_class: OWLClass = random.choice(soli_graph.get_forum_venues())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "governmental_body":
            sampled_class: OWLClass = random.choice(
                soli_graph.get_governmental_bodies()
            )
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "industry":
            sampled_class: OWLClass = random.choice(soli_graph.get_industries())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "language":
            sampled_class: OWLClass = random.choice(soli_graph.get_languages())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "soli_type":
            sampled_class: OWLClass = random.choice(soli_graph.get_soli_types())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "legal_authorities":
            sampled_class: OWLClass = random.choice(soli_graph.get_legal_authorities())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "legal_entity":
            sampled_class: OWLClass = random.choice(soli_graph.get_legal_entities())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "location":
            sampled_class: OWLClass = random.choice(soli_graph.get_locations())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "matter_narrative":
            sampled_class: OWLClass = random.choice(soli_graph.get_matter_narratives())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "matter_narrative_format":
            sampled_class: OWLClass = random.choice(
                soli_graph.get_matter_narrative_formats()
            )
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "objectives":
            sampled_class: OWLClass = random.choice(soli_graph.get_objectives())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "service":
            sampled_class: OWLClass = random.choice(soli_graph.get_services())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "standards_compatibility":
            sampled_class: OWLClass = random.choice(
                soli_graph.get_standards_compatibilities()
            )
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "status":
            sampled_class: OWLClass = random.choice(soli_graph.get_statuses())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)
        elif tag == "system_identifiers":
            sampled_class: OWLClass = random.choice(soli_graph.get_system_identifiers())
            value_map[(tag, index)] = get_random_owl_label(sampled_class)

    return value_map


def apply_template_map(
    template: str, value_map: Dict[Tuple[str, str], int | float | str]
) -> str:
    """
    Apply a mapping of SOLI tags to their corresponding taxonomic categories or Faker methods to a template.

    Args:
    - template (str): the template string containing SOLI tags
    - value_map (dict): the mapping of SOLI tags to their corresponding taxonomic categories or Faker methods

    Returns:
    - str: the template with the SOLI tags replaced by their corresponding taxonomic categories or Faker methods
    """
    # make a copy of the template
    template_output = template

    # apply the value map to the template
    for (tag, index), value in value_map.items():
        template_tag = get_template_tag(tag, index)
        template_output = template_output.replace(template_tag, str(value))

    return template_output


def format_template(
    template: str,
    soli_graph: SOLI,
) -> str:
    """
    Format a template string by sampling values for each SOLI taxonomic category or Faker method.

    Args:
    - template (str): the template string containing SOLI tags

    Returns:
    - str: the formatted template with the SOLI tags replaced by their corresponding taxonomic categories or Faker methods
    """
    # build a pattern map from the template
    pattern_map = build_pattern_map(template)

    # sample values for each tag
    value_map = sample_values(pattern_map, soli_graph)

    # apply the value map to the template
    return apply_template_map(template, value_map)


# class-based version for easier SOLI graph setup
class TemplateFormatter:
    """
    Class-based version of the template formatter for easier SOLI graph setup and re-use.
    """

    def __init__(
        self,
        pattern_mapper: re.Pattern = RE_PATTERN_MAP,
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
        - pattern_mapper (re.Pattern): the compiled regex pattern for matching SOLI tags
        - source_type (str): the source type for the SOLI knowledge graph
        - github_repo_owner (str): the owner of the GitHub repository
        - github_repo_name (str): the name of the GitHub repository
        - github_repo_branch (str): the branch of the GitHub repository
        - use_cache (bool): whether to use the cache for the SOLI knowledge graph
        """
        # store the pattern mapper
        self.pattern = pattern_mapper

        # create the SOLI graph
        self.graph = SOLI(
            source_type=source_type,
            http_url=http_url,
            github_repo_owner=github_repo_owner,
            github_repo_name=github_repo_name,
            github_repo_branch=github_repo_branch,
            use_cache=use_cache,
        )

    def format(self, template: str) -> str:
        """
        Format a template string by sampling values for each SOLI taxonomic category or Faker method.

        Args:
        - template (str): the template string containing SOLI tags

        Returns:
        - str: the formatted template with the SOLI tags replaced by their corresponding taxonomic categories or Faker methods
        """
        # build a pattern map from the template
        pattern_map = build_pattern_map(template=template, pattern=self.pattern)

        # sample values for each tag
        value_map = sample_values(pattern_map=pattern_map, soli_graph=self.graph)

        # apply the value map to the template
        return apply_template_map(template=template, value_map=value_map)

    def __call__(self, *args, **kwargs):
        """
        Call the format method on the template string.

        Args:
        - *args: Variable length argument list.
        - **kwargs: Arbitrary keyword arguments.

        Returns:
        - str: the formatted template with the SOLI tags replaced by their corresponding taxonomic categories or Faker methods
        """
        return self.format(*args, **kwargs)
