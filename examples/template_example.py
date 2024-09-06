# imports
from soli_data_generator.procedural.template import TemplateFormatter


if __name__ == "__main__":
    # Initialize the TemplateFormatter
    formatter = TemplateFormatter()

    # Define a template with SOLI and Faker tags
    template = """
Company: <|company|>
Industry: <|industry|>
Location: <|location|>
Legal Issue: <|area_of_law|>
Document Type: <|document_artifact|>
Date: <|date|>

On <|date|>, <|company|>, a company operating in the <|industry|> industry,
encountered a legal issue related to <|area_of_law|> at their location in <|location|>.
As a result, they have requested the preparation of a <|document_artifact|> to address
the situation.
    """.strip()

    # Format the template
    formatted_text = formatter(template)

    # Print the formatted text
    print(formatted_text)
