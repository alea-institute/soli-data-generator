# imports


# packages
import pytest
from soli import SOLI

# project
from soli_data_generator.procedural.template import format_template, TemplateFormatter


@pytest.fixture
def soli():
    return SOLI()


def test_single_soli_entity(soli):
    text = "The company operates in the <|industry|> industry."
    template = format_template(text, soli)
    assert "<|industry|>" not in template
    assert (
        text[0 : len("The company operates in the ")] == "The company operates in the "
    )


def test_multiple_soli_entities(soli):
    text = "The company operates in the <|industry|> industry and has its corporate headquarters in <|location|>."
    template = format_template(text, soli)
    assert "<|industry|>" not in template
    assert "<|location|>" not in template
    assert (
        text[0 : len("The company operates in the ")] == "The company operates in the "
    )
    assert (
        text[
            len("The company operates in the ") : len("The company operates in the ")
            + len("<|industry|>")
        ]
        == "<|industry|>"
    )


# test the class version
def test_single_soli_entity_class(soli):
    t = TemplateFormatter()
    text = "The company operates in the <|industry|> industry."
    print(t(text))


def test_faker_entities(soli):
    template = """
    <|address|> is where <|name|> lives.
    They work at <|company|> as a <|job|>.
    Their email is <|email|>.
    They were born on <|date|> at <|time|>.
    Their first name is <|first_name|> and their last name is <|last_name|>.
    They recently created a file named <|filename|>.
    """

    # multiple paths through stochastic generation
    for _ in range(10):
        formatted = format_template(template, soli)

    # Check that all Faker tags have been replaced
    assert "<|address|>" not in formatted
    assert "<|name|>" not in formatted
    assert "<|company|>" not in formatted
    assert "<|job|>" not in formatted
    assert "<|email|>" not in formatted
    assert "<|date|>" not in formatted
    assert "<|time|>" not in formatted
    assert "<|first_name|>" not in formatted
    assert "<|last_name|>" not in formatted
    assert "<|filename|>" not in formatted

    # Check that the basic structure of the text is maintained
    assert "is where" in formatted
    assert "lives." in formatted
    assert "They work at" in formatted
    assert "as a" in formatted
    assert "Their email is" in formatted
    assert "They were born on" in formatted
    assert "at" in formatted
    assert "Their first name is" in formatted
    assert "and their last name is" in formatted
    assert "They recently created a file named" in formatted

    # Additional checks to ensure the replaced values are of the expected type
    assert "@" in formatted  # Check for a valid email format
    assert (
        "." in formatted.split("They recently created a file named")[-1]
    )  # Check for a file extension


def test_soli_entities(soli):
    template = """
    The <|actor_player|> is involved in a case related to <|area_of_law|>.
    They are dealing with <|asset_type|> assets using <|communication_modality|> for communication.
    The transaction involves <|currency|> and requires handling <|data_format|> data.
    Key <|document_artifact|> have been prepared under <|engagement_terms|>.
    An important <|event|> is scheduled at <|forums_and_venues|>.
    The <|governmental_body|> oversees activities in the <|industry|> sector.
    Documentation is provided in <|language|> following <|soli_type|> standards.
    <|legal_authorities|> are consulted, and <|legal_entity|> is representing the client.
    The matter takes place in <|location|> and involves a <|matter_narrative|>.
    The <|matter_narrative_format|> outlines <|objectives|> for the <|service|> provided.
    We ensure <|standards_compatibility|> and track the <|status|> using <|system_identifiers|>.
    """

    # multiple paths through stochastic generation
    for _ in range(10):
        formatted = format_template(template, soli)

    soli_tags = [
        "actor_player",
        "area_of_law",
        "asset_type",
        "communication_modality",
        "currency",
        "data_format",
        "document_artifact",
        "engagement_terms",
        "event",
        "forums_and_venues",
        "governmental_body",
        "industry",
        "language",
        "soli_type",
        "legal_authorities",
        "legal_entity",
        "location",
        "matter_narrative",
        "matter_narrative_format",
        "objectives",
        "service",
        "standards_compatibility",
        "status",
        "system_identifiers",
    ]

    # Check that all SOLI tags have been replaced
    for tag in soli_tags:
        assert f"<|{tag}|>" not in formatted

    # Check that the basic structure of the text is maintained
    assert "is involved in a case related to" in formatted
    assert "They are dealing with" in formatted
    assert "assets using" in formatted
    assert "for communication" in formatted
    assert "The transaction involves" in formatted
    assert "and requires handling" in formatted
    assert "Key" in formatted
    assert "have been prepared under" in formatted
    assert "An important" in formatted
    assert "is scheduled at" in formatted
    assert "The" in formatted
    assert "oversees activities in the" in formatted
    assert "sector" in formatted
    assert "Documentation is provided in" in formatted
    assert "following" in formatted
    assert "standards" in formatted
    assert "are consulted, and" in formatted
    assert "is representing the client" in formatted
    assert "The matter takes place in" in formatted
    assert "and involves a" in formatted
    assert "The" in formatted
    assert "outlines" in formatted
    assert "for the" in formatted
    assert "provided" in formatted
    assert "We ensure" in formatted
    assert "and track the" in formatted
    assert "using" in formatted
