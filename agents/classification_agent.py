"""
Classification Agent for the Alix Multi-Agent System.

This agent analyzes document content and classifies it into categories
based on the estate-related taxonomy using keyword-based classification.
"""

import re
from typing import Dict, Any
from data.taxonomy import DOCUMENT_TAXONOMY


class ClassificationAgent:
    """
    Agent responsible for classifying documents into predefined categories.
    
    Uses keyword-based classification to determine document type based on
    content analysis and returns the appropriate category code.
    """
    
    def __init__(self):
        """Initialize the Classification Agent with taxonomy data."""
        self.taxonomy = DOCUMENT_TAXONOMY
        self._setup_classification_rules()
    
    def _setup_classification_rules(self):
        """
        Set up keyword-based classification rules for each document category.
        
        Each category has a set of keywords that, if found in the document content,
        indicate that the document belongs to that category.
        """
        self.classification_rules = {
            "Death Certificate": [
                "certificate of death",
                "death certificate",
                "department of health",
                "deceased",
                "date of death",
                "cause of death",
                "certifying physician"
            ],
            "Will or Trust": [
                "last will and testament",
                "will and testament",
                "trust agreement",
                "trust document",
                "executor",
                "beneficiary",
                "testator",
                "trustee"
            ],
            "Property Deed": [
                "deed",
                "property deed",
                "warranty deed",
                "quitclaim deed",
                "real estate",
                "property transfer",
                "grantor",
                "grantee"
            ],
            "Financial Statement": [
                "financial statement",
                "bank statement",
                "account statement",
                "balance sheet",
                "income statement",
                "assets",
                "liabilities",
                "account balance"
            ],
            "Tax Document": [
                "tax return",
                "tax document",
                "irs",
                "internal revenue service",
                "form 1040",
                "tax year",
                "taxable income",
                "tax liability"
            ]
        }
    
    def classify_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify a document based on its content.
        
        Args:
            document (Dict[str, Any]): Document payload containing:
                - document_id: Unique identifier for the document
                - content: Text content of the document
                - metadata: Additional document metadata (optional)
        
        Returns:
            Dict[str, Any]: Classification result containing:
                - document_id: Original document identifier
                - category: Classified category name
                - categoryCode: Corresponding taxonomy code
                - confidence: Classification confidence score (0.0-1.0)
        """
        document_id = document.get("document_id", "unknown")
        content = document.get("content", "").lower()
        
        if not content.strip():
            return {
                "document_id": document_id,
                "category": "Miscellaneous",
                "categoryCode": self.taxonomy["Miscellaneous"],
                "confidence": 0.0
            }
        
        # Score each category based on keyword matches
        category_scores = {}
        
        for category, keywords in self.classification_rules.items():
            score = 0
            matched_keywords = []
            
            for keyword in keywords:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                matches = len(re.findall(pattern, content))
                if matches > 0:
                    score += matches
                    matched_keywords.append(keyword)
            
            if score > 0:
                category_scores[category] = {
                    "score": score,
                    "matched_keywords": matched_keywords
                }
        
        # Determine best category
        if not category_scores:
            classified_category = "Miscellaneous"
            confidence = 0.0
        else:
            # Select category with highest score
            best_category = max(category_scores.keys(), 
                              key=lambda cat: category_scores[cat]["score"])
            classified_category = best_category
            
            # Calculate confidence based on number of matched keywords
            max_score = category_scores[best_category]["score"]
            total_keywords = len(self.classification_rules[best_category])
            confidence = min(max_score / total_keywords, 1.0)
        
        return {
            "document_id": document_id,
            "category": classified_category,
            "categoryCode": self.taxonomy[classified_category],
            "confidence": confidence
        }
    
    def get_supported_categories(self) -> Dict[str, str]:
        """
        Get all supported document categories and their codes.
        
        Returns:
            Dict[str, str]: Mapping of category names to taxonomy codes
        """
        return self.taxonomy.copy()
    
    def get_classification_rules(self) -> Dict[str, list]:
        """
        Get the current classification rules for debugging/inspection.
        
        Returns:
            Dict[str, list]: Mapping of categories to their keyword lists
        """
        return self.classification_rules.copy()

