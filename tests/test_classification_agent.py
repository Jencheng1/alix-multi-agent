"""
Unit tests for the Classification Agent.

This module contains test cases to verify the correct functionality
of the ClassificationAgent class and its document classification capabilities.
"""

import unittest
import sys
import os

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.classification_agent import ClassificationAgent
from data.taxonomy import DOCUMENT_TAXONOMY


class TestClassificationAgent(unittest.TestCase):
    """Test cases for the ClassificationAgent class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.agent = ClassificationAgent()
    
    def test_initialization(self):
        """Test that the agent initializes correctly."""
        self.assertIsInstance(self.agent, ClassificationAgent)
        self.assertEqual(self.agent.taxonomy, DOCUMENT_TAXONOMY)
        self.assertIsInstance(self.agent.classification_rules, dict)
        self.assertGreater(len(self.agent.classification_rules), 0)
    
    def test_classify_death_certificate(self):
        """Test classification of a valid death certificate."""
        document = {
            "document_id": "TEST_DC_001",
            "content": """
            STATE OF NEW YORK
            DEPARTMENT OF HEALTH
            CERTIFICATE OF DEATH
            Certificate Number: 2023-NY-00012345
            
            Full Name of Deceased: John Doe
            Date of Death: January 1, 2023
            Place of Death: New York Hospital
            Cause of Death: Natural Causes
            Certifying Physician: Dr. Smith
            """
        }
        
        result = self.agent.classify_document(document)
        
        self.assertEqual(result["document_id"], "TEST_DC_001")
        self.assertEqual(result["category"], "Death Certificate")
        self.assertEqual(result["categoryCode"], "01.0000-50")
        self.assertGreater(result["confidence"], 0.0)
        self.assertLessEqual(result["confidence"], 1.0)
    
    def test_classify_will_document(self):
        """Test classification of a will document."""
        document = {
            "document_id": "TEST_WILL_001",
            "content": """
            LAST WILL AND TESTAMENT
            OF
            JANE SMITH
            
            I, Jane Smith, being of sound mind and disposing memory,
            do hereby make, publish, and declare this to be my Last Will
            and Testament, hereby revoking all former wills and codicils.
            
            I give, devise, and bequeath all of my property to my children.
            I hereby nominate my spouse as the Executor of this will.
            """
        }
        
        result = self.agent.classify_document(document)
        
        self.assertEqual(result["document_id"], "TEST_WILL_001")
        self.assertEqual(result["category"], "Will or Trust")
        self.assertEqual(result["categoryCode"], "02.0300-50")
        self.assertGreater(result["confidence"], 0.0)
    
    def test_classify_trust_document(self):
        """Test classification of a trust document."""
        document = {
            "document_id": "TEST_TRUST_001",
            "content": """
            THE JOHNSON FAMILY TRUST AGREEMENT
            
            This Trust Agreement is made between John Johnson and Mary Johnson
            as Settlors and Trustees.
            
            The Settlors hereby transfer property to the Trustees to be held
            and administered according to this Trust Agreement.
            
            This trust is created for the benefit of the Settlors and their
            descendants as beneficiaries.
            """
        }
        
        result = self.agent.classify_document(document)
        
        self.assertEqual(result["document_id"], "TEST_TRUST_001")
        self.assertEqual(result["category"], "Will or Trust")
        self.assertEqual(result["categoryCode"], "02.0300-50")
        self.assertGreater(result["confidence"], 0.0)
    
    def test_classify_financial_statement(self):
        """Test classification of a financial statement."""
        document = {
            "document_id": "TEST_FS_001",
            "content": """
            FIRST NATIONAL BANK
            ACCOUNT STATEMENT
            
            Account Holder: Robert Wilson
            Account Number: 1234567890
            Statement Period: January 2023
            
            Beginning Balance: $10,000.00
            Total Deposits: $5,000.00
            Total Withdrawals: $2,000.00
            Ending Balance: $13,000.00
            
            Assets and Liabilities Summary:
            Total Assets: $50,000.00
            Total Liabilities: $20,000.00
            """
        }
        
        result = self.agent.classify_document(document)
        
        self.assertEqual(result["document_id"], "TEST_FS_001")
        self.assertEqual(result["category"], "Financial Statement")
        self.assertEqual(result["categoryCode"], "04.5000-00")
        self.assertGreater(result["confidence"], 0.0)
    
    def test_classify_property_deed(self):
        """Test classification of a property deed."""
        document = {
            "document_id": "TEST_DEED_001",
            "content": """
            WARRANTY DEED
            
            KNOW ALL MEN BY THESE PRESENTS, that John Davis and Mary Davis,
            husband and wife (the Grantors), do hereby grant, bargain, sell,
            and convey unto Robert Thompson (the Grantee), the following
            described real estate property:
            
            Lot 15 in Block 3 of Oakwood Subdivision
            
            This property deed transfers ownership of the real estate
            from the Grantor to the Grantee.
            """
        }
        
        result = self.agent.classify_document(document)
        
        self.assertEqual(result["document_id"], "TEST_DEED_001")
        self.assertEqual(result["category"], "Property Deed")
        self.assertEqual(result["categoryCode"], "03.0090-00")
        self.assertGreater(result["confidence"], 0.0)
    
    def test_classify_miscellaneous_document(self):
        """Test classification of a document that doesn't match any category."""
        document = {
            "document_id": "TEST_MISC_001",
            "content": """
            RANDOM DOCUMENT
            
            This is just a random document that doesn't contain any
            specific keywords related to estate planning, death certificates,
            wills, trusts, financial statements, or property deeds.
            
            It should be classified as miscellaneous.
            """
        }
        
        result = self.agent.classify_document(document)
        
        self.assertEqual(result["document_id"], "TEST_MISC_001")
        self.assertEqual(result["category"], "Miscellaneous")
        self.assertEqual(result["categoryCode"], "00.0000-00")
        self.assertEqual(result["confidence"], 0.0)
    
    def test_classify_empty_document(self):
        """Test classification of an empty document."""
        document = {
            "document_id": "TEST_EMPTY_001",
            "content": ""
        }
        
        result = self.agent.classify_document(document)
        
        self.assertEqual(result["document_id"], "TEST_EMPTY_001")
        self.assertEqual(result["category"], "Miscellaneous")
        self.assertEqual(result["categoryCode"], "00.0000-00")
        self.assertEqual(result["confidence"], 0.0)
    
    def test_classify_document_without_id(self):
        """Test classification of a document without an ID."""
        document = {
            "content": "This is a test document with some content."
        }
        
        result = self.agent.classify_document(document)
        
        self.assertEqual(result["document_id"], "unknown")
        self.assertEqual(result["category"], "Miscellaneous")
    
    def test_get_supported_categories(self):
        """Test getting supported categories."""
        categories = self.agent.get_supported_categories()
        
        self.assertIsInstance(categories, dict)
        self.assertEqual(categories, DOCUMENT_TAXONOMY)
        self.assertIn("Death Certificate", categories)
        self.assertIn("Will or Trust", categories)
        self.assertIn("Miscellaneous", categories)
    
    def test_get_classification_rules(self):
        """Test getting classification rules."""
        rules = self.agent.get_classification_rules()
        
        self.assertIsInstance(rules, dict)
        self.assertIn("Death Certificate", rules)
        self.assertIn("Will or Trust", rules)
        self.assertIsInstance(rules["Death Certificate"], list)
        self.assertGreater(len(rules["Death Certificate"]), 0)
    
    def test_case_insensitive_classification(self):
        """Test that classification is case-insensitive."""
        document = {
            "document_id": "TEST_CASE_001",
            "content": """
            CERTIFICATE OF DEATH
            DATE OF DEATH: JANUARY 1, 2023
            """
        }
        
        result = self.agent.classify_document(document)
        
        self.assertEqual(result["category"], "Death Certificate")
        self.assertGreater(result["confidence"], 0.0)


if __name__ == "__main__":
    unittest.main()

