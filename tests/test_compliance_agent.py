"""
Unit tests for the Compliance Agent.

This module contains test cases to verify the correct functionality
of the ComplianceAgent class and its document validation capabilities.
"""

import unittest
import sys
import os

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.compliance_agent import ComplianceAgent


class TestComplianceAgent(unittest.TestCase):
    """Test cases for the ComplianceAgent class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.agent = ComplianceAgent()
    
    def test_initialization(self):
        """Test that the agent initializes correctly."""
        self.assertIsInstance(self.agent, ComplianceAgent)
        self.assertIsInstance(self.agent.validation_rules, dict)
        self.assertIn("Death Certificate", self.agent.validation_rules)
        self.assertIn("Will or Trust", self.agent.validation_rules)
    
    def test_valid_death_certificate(self):
        """Test validation of a valid death certificate."""
        document = {
            "document_id": "TEST_DC_VALID",
            "content": """
            STATE OF NEW YORK
            CERTIFICATE OF DEATH
            Certificate Number: 2023-NY-12345
            
            Full Name of Deceased: John Doe
            Date of Death: January 1, 2023
            Place of Death: New York Hospital
            Cause of Death: Natural Causes
            """
        }
        
        classification_result = {
            "document_id": "TEST_DC_VALID",
            "category": "Death Certificate",
            "categoryCode": "01.0000-50"
        }
        
        result = self.agent.validate_document(document, classification_result)
        
        self.assertEqual(result["document_id"], "TEST_DC_VALID")
        self.assertTrue(result["valid"])
        self.assertEqual(result["category"], "Death Certificate")
        self.assertIn("validation passed", result["reason"].lower())
        self.assertFalse(result["validation_details"]["bypassed"])
        self.assertTrue(result["validation_details"]["required_validation"])
    
    def test_invalid_death_certificate_missing_certificate_phrase(self):
        """Test validation of death certificate missing 'Certificate of Death'."""
        document = {
            "document_id": "TEST_DC_INVALID_1",
            "content": """
            STATE OF CALIFORNIA
            DEATH RECORD
            Record Number: 2023-CA-67890
            
            Full Name of Deceased: Jane Smith
            Date of Death: February 15, 2023
            Place of Death: Los Angeles Hospital
            """
        }
        
        classification_result = {
            "document_id": "TEST_DC_INVALID_1",
            "category": "Death Certificate",
            "categoryCode": "01.0000-50"
        }
        
        result = self.agent.validate_document(document, classification_result)
        
        self.assertEqual(result["document_id"], "TEST_DC_INVALID_1")
        self.assertFalse(result["valid"])
        self.assertEqual(result["category"], "Death Certificate")
        self.assertIn("validation failed", result["reason"].lower())
        self.assertIn("certificate of death", result["validation_details"]["missing_phrases"])
    
    def test_invalid_death_certificate_missing_date_phrase(self):
        """Test validation of death certificate missing 'Date of Death'."""
        document = {
            "document_id": "TEST_DC_INVALID_2",
            "content": """
            STATE OF TEXAS
            CERTIFICATE OF DEATH
            Certificate Number: 2023-TX-11111
            
            Full Name of Deceased: Bob Johnson
            Deceased Date: March 10, 2023
            Place of Death: Houston Medical Center
            """
        }
        
        classification_result = {
            "document_id": "TEST_DC_INVALID_2",
            "category": "Death Certificate",
            "categoryCode": "01.0000-50"
        }
        
        result = self.agent.validate_document(document, classification_result)
        
        self.assertEqual(result["document_id"], "TEST_DC_INVALID_2")
        self.assertFalse(result["valid"])
        self.assertIn("date of death", result["validation_details"]["missing_phrases"])
    
    def test_valid_will_document(self):
        """Test validation of a valid will document."""
        document = {
            "document_id": "TEST_WILL_VALID",
            "content": """
            LAST WILL AND TESTAMENT
            OF
            ROBERT SMITH
            
            I, Robert Smith, being of sound mind, do hereby make this
            my Last Will and Testament, revoking all prior wills.
            
            I give all my property to my spouse and children.
            """
        }
        
        classification_result = {
            "document_id": "TEST_WILL_VALID",
            "category": "Will or Trust",
            "categoryCode": "02.0300-50"
        }
        
        result = self.agent.validate_document(document, classification_result)
        
        self.assertEqual(result["document_id"], "TEST_WILL_VALID")
        self.assertTrue(result["valid"])
        self.assertEqual(result["category"], "Will or Trust")
        self.assertIn("validation passed", result["reason"].lower())
        self.assertIn("last will and testament", result["validation_details"]["found_phrases"])
    
    def test_valid_trust_document(self):
        """Test validation of a valid trust document."""
        document = {
            "document_id": "TEST_TRUST_VALID",
            "content": """
            THE JOHNSON FAMILY TRUST AGREEMENT
            
            This Trust Agreement is made between John Johnson and Mary Johnson
            as Settlors and Trustees for the benefit of their family.
            
            The Settlors transfer property to be held in trust.
            """
        }
        
        classification_result = {
            "document_id": "TEST_TRUST_VALID",
            "category": "Will or Trust",
            "categoryCode": "02.0300-50"
        }
        
        result = self.agent.validate_document(document, classification_result)
        
        self.assertEqual(result["document_id"], "TEST_TRUST_VALID")
        self.assertTrue(result["valid"])
        self.assertEqual(result["category"], "Will or Trust")
        self.assertIn("validation passed", result["reason"].lower())
        self.assertIn("trust agreement", result["validation_details"]["found_phrases"])
    
    def test_invalid_will_or_trust_document(self):
        """Test validation of invalid will/trust document missing required phrases."""
        document = {
            "document_id": "TEST_WILL_INVALID",
            "content": """
            ESTATE PLANNING DOCUMENT
            OF
            MARGARET WILSON
            
            I, Margaret Wilson, hereby distribute my assets as follows:
            All property goes to my children equally.
            
            This represents my final wishes for asset distribution.
            """
        }
        
        classification_result = {
            "document_id": "TEST_WILL_INVALID",
            "category": "Will or Trust",
            "categoryCode": "02.0300-50"
        }
        
        result = self.agent.validate_document(document, classification_result)
        
        self.assertEqual(result["document_id"], "TEST_WILL_INVALID")
        self.assertFalse(result["valid"])
        self.assertEqual(result["category"], "Will or Trust")
        self.assertIn("validation failed", result["reason"].lower())
        self.assertEqual(len(result["validation_details"]["found_phrases"]), 0)
    
    def test_bypass_financial_statement(self):
        """Test that financial statements bypass validation."""
        document = {
            "document_id": "TEST_FS_BYPASS",
            "content": """
            BANK STATEMENT
            Account Holder: Test User
            Account Balance: $10,000.00
            """
        }
        
        classification_result = {
            "document_id": "TEST_FS_BYPASS",
            "category": "Financial Statement",
            "categoryCode": "04.5000-00"
        }
        
        result = self.agent.validate_document(document, classification_result)
        
        self.assertEqual(result["document_id"], "TEST_FS_BYPASS")
        self.assertTrue(result["valid"])
        self.assertEqual(result["category"], "Financial Statement")
        self.assertIn("bypasses validation", result["reason"])
        self.assertTrue(result["validation_details"]["bypassed"])
        self.assertFalse(result["validation_details"]["required_validation"])
    
    def test_bypass_property_deed(self):
        """Test that property deeds bypass validation."""
        document = {
            "document_id": "TEST_DEED_BYPASS",
            "content": """
            WARRANTY DEED
            Grantor: John Smith
            Grantee: Jane Smith
            Property: 123 Main Street
            """
        }
        
        classification_result = {
            "document_id": "TEST_DEED_BYPASS",
            "category": "Property Deed",
            "categoryCode": "03.0090-00"
        }
        
        result = self.agent.validate_document(document, classification_result)
        
        self.assertEqual(result["document_id"], "TEST_DEED_BYPASS")
        self.assertTrue(result["valid"])
        self.assertEqual(result["category"], "Property Deed")
        self.assertIn("bypasses validation", result["reason"])
        self.assertTrue(result["validation_details"]["bypassed"])
    
    def test_bypass_miscellaneous_document(self):
        """Test that miscellaneous documents bypass validation."""
        document = {
            "document_id": "TEST_MISC_BYPASS",
            "content": "This is a random document with no specific category."
        }
        
        classification_result = {
            "document_id": "TEST_MISC_BYPASS",
            "category": "Miscellaneous",
            "categoryCode": "00.0000-00"
        }
        
        result = self.agent.validate_document(document, classification_result)
        
        self.assertEqual(result["document_id"], "TEST_MISC_BYPASS")
        self.assertTrue(result["valid"])
        self.assertEqual(result["category"], "Miscellaneous")
        self.assertIn("bypasses validation", result["reason"])
        self.assertTrue(result["validation_details"]["bypassed"])
    
    def test_get_validation_rules(self):
        """Test getting validation rules."""
        rules = self.agent.get_validation_rules()
        
        self.assertIsInstance(rules, dict)
        self.assertIn("Death Certificate", rules)
        self.assertIn("Will or Trust", rules)
        self.assertIn("required_phrases", rules["Death Certificate"])
        self.assertIn("required_phrases_any", rules["Will or Trust"])
    
    def test_get_categories_requiring_validation(self):
        """Test getting categories that require validation."""
        categories = self.agent.get_categories_requiring_validation()
        
        self.assertIsInstance(categories, list)
        self.assertIn("Death Certificate", categories)
        self.assertIn("Will or Trust", categories)
        self.assertEqual(len(categories), 2)
    
    def test_case_insensitive_validation(self):
        """Test that validation is case-insensitive."""
        document = {
            "document_id": "TEST_CASE_INSENSITIVE",
            "content": """
            CERTIFICATE OF DEATH
            DATE OF DEATH: JANUARY 1, 2023
            """
        }
        
        classification_result = {
            "document_id": "TEST_CASE_INSENSITIVE",
            "category": "Death Certificate",
            "categoryCode": "01.0000-50"
        }
        
        result = self.agent.validate_document(document, classification_result)
        
        self.assertTrue(result["valid"])
        self.assertIn("certificate of death", result["validation_details"]["found_phrases"])
        self.assertIn("date of death", result["validation_details"]["found_phrases"])
    
    def test_document_without_id(self):
        """Test validation of document without ID."""
        document = {
            "content": "Certificate of Death and Date of Death are present."
        }
        
        classification_result = {
            "category": "Death Certificate",
            "categoryCode": "01.0000-50"
        }
        
        result = self.agent.validate_document(document, classification_result)
        
        self.assertEqual(result["document_id"], "unknown")
        self.assertTrue(result["valid"])


if __name__ == "__main__":
    unittest.main()

