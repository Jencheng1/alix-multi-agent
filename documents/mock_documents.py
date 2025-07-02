"""
Mock documents for testing the Alix Multi-Agent System.

This module contains sample document payloads that represent different
types of estate-related documents for testing classification and compliance.
"""

# Valid Death Certificate - should pass all validations
VALID_DEATH_CERTIFICATE = {
    "document_id": "DC001",
    "content": """
    STATE OF NEW YORK
    DEPARTMENT OF HEALTH
    CERTIFICATE OF DEATH
    Certificate Number: 2023-NY-00012345
    
    1. Full Name of Deceased: Johnathan Edward Doe
    2. Date of Death: January 1, 2023
    3. Place of Death: New York-Presbyterian Hospital, New York, NY
    4. Sex: Male
    5. Age at Death: 76 years
    6. Date of Birth: March 5, 1946
    7. Social Security Number: 123-45-6789
    8. Usual Residence: 789 Elm Street, Albany, NY 12207
    9. Marital Status: Married
    10. Name of Spouse: Margaret Anne Doe
    11. Occupation: Retired Attorney
    12. Informant Name: Michael Doe
    13. Relationship to Deceased: Son
    14. Cause of Death: Acute Myocardial Infarction
    15. Certifying Physician: Dr. Linda Park, M.D.
    16. Date Signed: January 2, 2023
    
    Filed with the New York Department of Health
    Date Received: January 3, 2023
    Registrar: Helen T. Vaughn
    """,
    "metadata": {
        "source": "New York Department of Health",
        "document_type": "official",
        "received_date": "2023-01-03"
    }
}

# Invalid Death Certificate - missing required phrases
INVALID_DEATH_CERTIFICATE = {
    "document_id": "DC002",
    "content": """
    STATE OF CALIFORNIA
    VITAL RECORDS OFFICE
    DEATH RECORD
    Record Number: 2023-CA-00067890
    
    1. Full Name of Deceased: Sarah Michelle Johnson
    2. Deceased Date: February 15, 2023
    3. Location of Death: Cedars-Sinai Medical Center, Los Angeles, CA
    4. Gender: Female
    5. Age at Death: 82 years
    6. Birth Date: June 12, 1940
    7. SSN: 987-65-4321
    8. Home Address: 456 Oak Avenue, Los Angeles, CA 90210
    9. Marital Status: Widowed
    10. Occupation: Retired Teacher
    11. Next of Kin: Robert Johnson (Son)
    12. Cause of Death: Natural Causes
    13. Attending Physician: Dr. James Wilson, M.D.
    14. Date Certified: February 16, 2023
    
    Filed with the California Vital Records Office
    Processing Date: February 17, 2023
    Clerk: Maria Rodriguez
    """,
    "metadata": {
        "source": "California Vital Records Office",
        "document_type": "official",
        "received_date": "2023-02-17"
    }
}

# Valid Will or Trust - contains "Last Will and Testament"
VALID_WILL_DOCUMENT = {
    "document_id": "WT001",
    "content": """
    LAST WILL AND TESTAMENT
    OF
    ROBERT JAMES SMITH
    
    I, Robert James Smith, of 123 Main Street, Boston, Massachusetts, being of sound mind
    and disposing memory, do hereby make, publish, and declare this to be my Last Will
    and Testament, hereby revoking all former wills and codicils by me made.
    
    FIRST: I direct that all my just debts and funeral expenses be paid as soon as
    practicable after my death.
    
    SECOND: I give, devise, and bequeath all of my property, both real and personal,
    of every kind and description, and wherever situated, to my beloved wife,
    Mary Elizabeth Smith, if she survives me.
    
    THIRD: If my said wife does not survive me, then I give, devise, and bequeath
    all of my property to my children, John Smith and Jane Smith, in equal shares.
    
    FOURTH: I hereby nominate and appoint my wife, Mary Elizabeth Smith, as the
    Executor of this my Last Will and Testament.
    
    IN WITNESS WHEREOF, I have hereunto set my hand this 15th day of March, 2023.
    
    ________________________
    Robert James Smith, Testator
    
    WITNESSES:
    The foregoing instrument was signed by the said Robert James Smith as and for
    his Last Will and Testament in the presence of us, who at his request and in
    his presence, and in the presence of each other, have subscribed our names
    as witnesses thereto.
    
    ________________________    ________________________
    Witness 1                    Witness 2
    """,
    "metadata": {
        "source": "Estate Attorney Office",
        "document_type": "legal",
        "execution_date": "2023-03-15"
    }
}

# Valid Trust Document - contains "Trust Agreement"
VALID_TRUST_DOCUMENT = {
    "document_id": "WT002",
    "content": """
    THE JOHNSON FAMILY REVOCABLE LIVING TRUST AGREEMENT
    
    This Trust Agreement is made this 10th day of April, 2023, between
    William Johnson and Patricia Johnson, husband and wife (the "Settlors"),
    and William Johnson and Patricia Johnson, as Trustees (the "Trustees").
    
    ARTICLE I - CREATION OF TRUST
    The Settlors hereby transfer and assign to the Trustees the property
    described in Schedule A attached hereto and incorporated herein by reference,
    to be held, administered, and distributed in accordance with the terms
    of this Trust Agreement.
    
    ARTICLE II - TRUST PURPOSES
    This trust is created for the benefit of the Settlors during their lifetimes,
    and thereafter for the benefit of their descendants and such other persons
    as may be designated as beneficiaries under this Trust Agreement.
    
    ARTICLE III - DISTRIBUTIONS DURING SETTLORS' LIFETIMES
    During the lifetimes of both Settlors, the Trustees shall distribute to or
    for the benefit of the Settlors such amounts of the net income and principal
    of the trust as the Trustees, in their sole discretion, deem necessary or
    advisable for the health, education, maintenance, and support of the Settlors.
    
    ARTICLE IV - SUCCESSOR TRUSTEES
    Upon the death or incapacity of both original Trustees, their son,
    Michael Johnson, shall serve as successor Trustee.
    
    IN WITNESS WHEREOF, the parties have executed this Trust Agreement
    on the date first written above.
    
    ________________________    ________________________
    William Johnson, Settlor     Patricia Johnson, Settlor
    
    ________________________    ________________________
    William Johnson, Trustee     Patricia Johnson, Trustee
    """,
    "metadata": {
        "source": "Trust Attorney Office",
        "document_type": "legal",
        "execution_date": "2023-04-10"
    }
}

# Invalid Will or Trust - missing required phrases
INVALID_WILL_DOCUMENT = {
    "document_id": "WT003",
    "content": """
    ESTATE PLANNING DOCUMENT
    OF
    MARGARET ANNE WILSON
    
    I, Margaret Anne Wilson, of 789 Elm Street, Chicago, Illinois, being of sound mind,
    do hereby make this estate planning document to distribute my assets upon my death.
    
    FIRST: I direct that all my debts and expenses be paid from my estate.
    
    SECOND: I leave all my real estate property located at 789 Elm Street, Chicago,
    Illinois, to my daughter, Susan Wilson.
    
    THIRD: I leave all my personal property, including bank accounts, investments,
    and personal belongings, to be divided equally between my children,
    Susan Wilson and David Wilson.
    
    FOURTH: I appoint my daughter, Susan Wilson, as the administrator of my estate.
    
    This document represents my final wishes regarding the distribution of my assets.
    
    Signed this 20th day of May, 2023.
    
    ________________________
    Margaret Anne Wilson
    
    WITNESSED BY:
    ________________________    ________________________
    Witness 1                    Witness 2
    """,
    "metadata": {
        "source": "Self-prepared document",
        "document_type": "informal",
        "execution_date": "2023-05-20"
    }
}

# Financial Statement - should bypass validation
FINANCIAL_STATEMENT_DOCUMENT = {
    "document_id": "FS001",
    "content": """
    FIRST NATIONAL BANK
    ACCOUNT STATEMENT
    
    Account Holder: Thomas Anderson
    Account Number: ****-****-****-1234
    Statement Period: January 1, 2023 - January 31, 2023
    
    ACCOUNT SUMMARY
    Beginning Balance (01/01/2023): $45,678.90
    Total Deposits: $8,500.00
    Total Withdrawals: $3,200.45
    Ending Balance (01/31/2023): $50,978.45
    
    TRANSACTION DETAILS
    01/03/2023  Direct Deposit - Salary           +$4,250.00
    01/05/2023  ATM Withdrawal                    -$200.00
    01/10/2023  Check #1234 - Mortgage Payment    -$1,850.00
    01/15/2023  Direct Deposit - Salary           +$4,250.00
    01/18/2023  Online Transfer - Savings         -$500.00
    01/22/2023  Grocery Store Purchase            -$125.45
    01/25/2023  Utility Payment                   -$275.00
    01/28/2023  Gas Station Purchase              -$50.00
    01/30/2023  Restaurant Purchase               -$200.00
    
    ACCOUNT INFORMATION
    Account Type: Checking Account
    Interest Rate: 0.05% APY
    Monthly Service Fee: $0.00 (waived with minimum balance)
    
    For questions about your account, please contact us at 1-800-BANK-123
    or visit our website at www.firstnationalbank.com
    """,
    "metadata": {
        "source": "First National Bank",
        "document_type": "financial",
        "statement_date": "2023-01-31"
    }
}

# Property Deed - should bypass validation
PROPERTY_DEED_DOCUMENT = {
    "document_id": "PD001",
    "content": """
    WARRANTY DEED
    
    KNOW ALL MEN BY THESE PRESENTS, that John Michael Davis and Mary Elizabeth Davis,
    husband and wife, of Cook County, Illinois (the "Grantors"), for and in consideration
    of the sum of Three Hundred Fifty Thousand Dollars ($350,000.00) and other good and
    valuable consideration, the receipt and sufficiency of which are hereby acknowledged,
    do hereby grant, bargain, sell, and convey unto Robert William Thompson and
    Linda Susan Thompson, husband and wife, of Cook County, Illinois (the "Grantees"),
    the following described real estate situated in Cook County, Illinois:
    
    LEGAL DESCRIPTION:
    Lot 15 in Block 3 of Oakwood Subdivision, being a subdivision of part of the
    Southeast Quarter of Section 12, Township 39 North, Range 13 East of the
    Third Principal Meridian, according to the plat thereof recorded in the
    Recorder's Office of Cook County, Illinois.
    
    Commonly known as: 456 Maple Avenue, Oak Park, Illinois 60302
    
    Property Identification Number: 16-12-345-678-0000
    
    TO HAVE AND TO HOLD the same, together with all and singular the appurtenances
    thereunto belonging or in anywise appertaining, unto the said Grantees,
    their heirs and assigns forever.
    
    AND the said Grantors, for themselves, their heirs, executors, and administrators,
    do covenant with the said Grantees, their heirs and assigns, that they are
    lawfully seized of said premises in fee simple; that they have good right
    and lawful authority to sell and convey the same; that the same are free
    and clear of all encumbrances except as herein stated; and that they will
    warrant and defend the title to said premises against the lawful claims
    of all persons whomsoever.
    
    IN WITNESS WHEREOF, the said Grantors have hereunto set their hands and seals
    this 25th day of June, 2023.
    
    ________________________    ________________________
    John Michael Davis          Mary Elizabeth Davis
    
    STATE OF ILLINOIS    )
                        ) ss.
    COUNTY OF COOK      )
    
    On this 25th day of June, 2023, before me personally appeared John Michael Davis
    and Mary Elizabeth Davis, who proved to me on the basis of satisfactory evidence
    to be the persons whose names are subscribed to the within instrument and
    acknowledged to me that they executed the same in their authorized capacities.
    
    ________________________
    Notary Public
    """,
    "metadata": {
        "source": "Cook County Recorder's Office",
        "document_type": "legal",
        "recording_date": "2023-06-25"
    }
}

# Collection of all mock documents for easy access
MOCK_DOCUMENTS = [
    VALID_DEATH_CERTIFICATE,
    INVALID_DEATH_CERTIFICATE,
    VALID_WILL_DOCUMENT,
    VALID_TRUST_DOCUMENT,
    INVALID_WILL_DOCUMENT,
    FINANCIAL_STATEMENT_DOCUMENT,
    PROPERTY_DEED_DOCUMENT
]

# Categorized collections for specific testing scenarios
DEATH_CERTIFICATES = [VALID_DEATH_CERTIFICATE, INVALID_DEATH_CERTIFICATE]
WILL_AND_TRUST_DOCUMENTS = [VALID_WILL_DOCUMENT, VALID_TRUST_DOCUMENT, INVALID_WILL_DOCUMENT]
BYPASS_DOCUMENTS = [FINANCIAL_STATEMENT_DOCUMENT, PROPERTY_DEED_DOCUMENT]

def get_all_documents():
    """Get all mock documents."""
    return MOCK_DOCUMENTS.copy()

def get_documents_by_category(category):
    """Get documents by category for targeted testing."""
    category_map = {
        "death_certificates": DEATH_CERTIFICATES,
        "will_and_trust": WILL_AND_TRUST_DOCUMENTS,
        "bypass": BYPASS_DOCUMENTS
    }
    return category_map.get(category, []).copy()

def get_document_by_id(document_id):
    """Get a specific document by its ID."""
    for doc in MOCK_DOCUMENTS:
        if doc["document_id"] == document_id:
            return doc.copy()
    return None

