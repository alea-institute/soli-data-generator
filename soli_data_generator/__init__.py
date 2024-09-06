"""
soli_data_generator is a Python package for generating synthetic data with the SOLI knowledge graph.
"""

# SPDX-License-Identifier: MIT
__version__ = "0.1.0"
__author__ = "ALEA Institute (https://aleainstitute.ai)"
__license__ = "MIT"
__copyright__ = "Copyright 2024, ALEA Institute"

from .llm import TextGenerator
from .procedural import TemplateFormatter

__all__ = ["TextGenerator", "TemplateFormatter"]
