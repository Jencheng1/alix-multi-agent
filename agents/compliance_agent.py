"""
Compliance Agent for the Alix Multi-Agent System.

This agent enforces strict validation rules based on the classified document type
to ensure documents meet required standards for estate settlement processing.
"""

import re
from typing import Dict, Any, List


class ComplianceAgent:
    """
    Agent responsible for validating documents based on their classified category.
    
    Enforces specific validation rules for certain document types and bypasses
    validation for others, returning compliance status and reasons.
    """
    
    def __init__(self):
        """Initialize the Compliance Agent with validation rules."""
        self._setup_validation_rules()
    
    def _setup_validation_rules(self):
        """
        Set up validation rules for different document categories.
        
        Each category has specific requirements that must be met for the
        document to be considered compliant.
        """
        self.validation_rules = {
            "Death Certificate": {
                "required_phrases": [
                    "certificate of death",
                    "date of death"
                ],
                "description": "Must contain 'Certificate of Death' and 'Date of Death'"
            },
            "Will or Trust": {
                "required_phrases_any": [
                    "last will and testament",
                    "trust agreement"
                ],
                "description": "Must contain 'Last Will and Testament' or 'Trust Agreement'"
            }
        }
    
    def validate_document(self, document: Dict[str, Any], classification_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a document based on its classification and content.
        
        Args:
            document (Dict[str, Any]): Original document payload containing:
                - document_id: Unique identifier for the document
                - content: Text content of the document
                - metadata: Additional document metadata (optional)
            classification_result (Dict[str, Any]): Result from Classification Agent containing:
                - document_id: Document identifier
                - category: Classified category name
                - categoryCode: Corresponding taxonomy code
        
        Returns:
            Dict[str, Any]: Validation result containing:
                - document_id: Original document identifier
                - valid: Boolean indicating if document is compliant
                - reason: Explanation of validation result
                - category: Document category that was validated
                - validation_details: Additional validation information
        """
        document_id = document.get("document_id", "unknown")
        content = document.get("content", "").lower()
        category = classification_result.get("category", "Miscellaneous")
        
        # Check if this category requires validation
        if category not in self.validation_rules:
            # Bypass validation for categories not in validation rules
            return {
                "document_id": document_id,
                "valid": True,
                "reason": f"Document category '{category}' bypasses validation",
                "category": category,
                "validation_details": {
                    "bypassed": True,
                    "required_validation": False
                }
            }
        
        # Perform category-specific validation
        if category == "Death Certificate":
            return self._validate_death_certificate(document_id, content, category)
        elif category == "Will or Trust":
            return self._validate_will_or_trust(document_id, content, category)
        else:
            # This shouldn't happen given the check above, but handle gracefully
            return {
                "document_id": document_id,
                "valid": True,
                "reason": f"No specific validation rules for category '{category}'",
                "category": category,
                "validation_details": {
                    "bypassed": True,
                    "required_validation": False
                }
            }
    
    def _validate_death_certificate(self, document_id: str, content: str, category: str) -> Dict[str, Any]:
        """
        Validate a Death Certificate document.
        
        Args:
            document_id (str): Document identifier
            content (str): Document content (lowercase)
            category (str): Document category
        
        Returns:
            Dict[str, Any]: Validation result for Death Certificate
        """
        rules = self.validation_rules["Death Certificate"]
        required_phrases = rules["required_phrases"]
        
        missing_phrases = []
        found_phrases = []
        
        for phrase in required_phrases:
            # Use word boundaries to ensure exact phrase matching
            pattern = r'\b' + re.escape(phrase.lower()) + r'\b'
            if re.search(pattern, content):
                found_phrases.append(phrase)
            else:
                missing_phrases.append(phrase)
        
        is_valid = len(missing_phrases) == 0
        
        if is_valid:
            reason = f"Death Certificate validation passed: all required phrases found ({', '.join(found_phrases)})"
        else:
            reason = f"Death Certificate validation failed: missing required phrases ({', '.join(missing_phrases)})"
        
        return {
            "document_id": document_id,
            "valid": is_valid,
            "reason": reason,
            "category": category,
            "validation_details": {
                "bypassed": False,
                "required_validation": True,
                "required_phrases": required_phrases,
                "found_phrases": found_phrases,
                "missing_phrases": missing_phrases
            }
        }
    
    def _validate_will_or_trust(self, document_id: str, content: str, category: str) -> Dict[str, Any]:
        """
        Validate a Will or Trust document.
        
        Args:
            document_id (str): Document identifier
            content (str): Document content (lowercase)
            category (str): Document category
        
        Returns:
            Dict[str, Any]: Validation result for Will or Trust
        """
        rules = self.validation_rules["Will or Trust"]
        required_phrases_any = rules["required_phrases_any"]
        
        found_phrases = []
        
        for phrase in required_phrases_any:
            # Use word boundaries to ensure exact phrase matching
            pattern = r'\b' + re.escape(phrase.lower()) + r'\b'
            if re.search(pattern, content):
                found_phrases.append(phrase)
        
        is_valid = len(found_phrases) > 0
        
        if is_valid:
            reason = f"Will or Trust validation passed: found required phrase(s) ({', '.join(found_phrases)})"
        else:
            reason = f"Will or Trust validation failed: must contain '{required_phrases_any[0]}' or '{required_phrases_any[1]}'"
        
        return {
            "document_id": document_id,
            "valid": is_valid,
            "reason": reason,
            "category": category,
            "validation_details": {
                "bypassed": False,
                "required_validation": True,
                "required_phrases_any": required_phrases_any,
                "found_phrases": found_phrases,
                "requires_any_phrase": True
            }
        }
    
    def get_validation_rules(self) -> Dict[str, Dict]:
        """
        Get the current validation rules for debugging/inspection.
        
        Returns:
            Dict[str, Dict]: Mapping of categories to their validation rules
        """
        return self.validation_rules.copy()
    
    def get_categories_requiring_validation(self) -> List[str]:
        """
        Get list of document categories that require validation.
        
        Returns:
            List[str]: List of category names that have validation rules
        """
        return list(self.validation_rules.keys())

