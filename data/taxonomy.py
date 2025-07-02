"""
Document taxonomy definitions for the Alix Multi-Agent System.

This module defines the DOCUMENT_TAXONOMY dictionary that maps document categories
to their corresponding classification codes used in estate settlement processing.
"""

DOCUMENT_TAXONOMY = {
    "Death Certificate": "01.0000-50",
    "Will or Trust": "02.0300-50",
    "Property Deed": "03.0090-00",
    "Financial Statement": "04.5000-00",
    "Tax Document": "05.5000-70",
    "Miscellaneous": "00.0000-00"
}

# Reverse mapping for code to category lookup
CODE_TO_CATEGORY = {code: category for category, code in DOCUMENT_TAXONOMY.items()}

