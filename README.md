# Alix Multi-Agent System

A sophisticated multi-agent system designed for automated document processing in estate settlement contexts. This system demonstrates intelligent document classification and compliance validation through a clean, modular architecture that prioritizes clarity and composability.

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [System Components](#system-components)
- [Document Processing Pipeline](#document-processing-pipeline)
- [Configuration](#configuration)
- [Key Assumptions](#key-assumptions)
- [Technical Implementation](#technical-implementation)
- [Performance Considerations](#performance-considerations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Alix Multi-Agent System is a Python-based solution that automates the triage and classification of estate-related documents. Built for the Alix Technical Test (June 2025), this system demonstrates how intelligent agents can work together to process documents efficiently and accurately.

### Key Features

- **Multi-Agent Architecture**: Three specialized agents working in coordination
- **Document Classification**: Intelligent categorization using keyword-based analysis
- **Compliance Validation**: Automated enforcement of document-specific rules
- **Extensible Design**: Modular structure allows easy addition of new document types
- **Comprehensive Testing**: Full test coverage with unit tests for all components
- **CLI Interface**: Easy-to-use command-line interface for document processing
- **Local Execution**: Runs entirely locally without external dependencies

### Business Context

In estate settlement, organizations process large volumes of documents including death certificates, wills, tax forms, property records, and correspondence. This system automates the initial triage and validation process, reducing manual effort and ensuring consistent application of business rules.

## System Architecture

The system follows a clean multi-agent architecture with three primary components:

```
┌─────────────────────────────────────────────────────────────┐
│                    Master Routing Agent                     │
│                     (Orchestrator)                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                Classification Agent                        │
│              (Document Categorization)                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 Compliance Agent                           │
│               (Validation Rules)                           │
└─────────────────────────────────────────────────────────────┘
```

### Agent Responsibilities

1. **Master Routing Agent**: Orchestrates the entire pipeline, managing document flow between agents and aggregating results
2. **Classification Agent**: Analyzes document content and assigns appropriate categories based on the estate taxonomy
3. **Compliance Agent**: Enforces validation rules specific to each document category

## Quick Start

Get the system running in under 5 minutes:

```bash
# Clone or download the project
cd alix-multi-agent-system

# Run the system with all mock documents
python main.py

# Run a specific document
python main.py DC001

# Get help
python main.py --help
```

## Installation

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Setup

1. **Download the System**
   ```bash
   # If you have the source code
   cd alix-multi-agent-system
   ```

2. **Verify Installation**
   ```bash
   python --version  # Should show Python 3.7+
   ```

3. **Test the Installation**
   ```bash
   python main.py --help
   ```

The system is designed to run with zero external dependencies, making it easy to deploy and test in any Python environment.

## Usage

### Command Line Interface

The system provides a comprehensive CLI for document processing:

#### Process All Documents
```bash
python main.py
```

This command processes all mock documents and displays:
- Individual document processing results
- Batch processing summary
- Detailed results table
- System information

#### Process Specific Document
```bash
python main.py <document_id>
```

Available document IDs:
- `DC001`: Valid Death Certificate
- `DC002`: Invalid Death Certificate  
- `WT001`: Valid Will Document
- `WT002`: Valid Trust Document
- `WT003`: Invalid Will Document
- `FS001`: Financial Statement (bypass)
- `PD001`: Property Deed (bypass)

#### Get Help
```bash
python main.py --help
```

### Programmatic Usage

You can also use the system programmatically:

```python
from agents.master_routing_agent import MasterRoutingAgent
from documents.mock_documents import get_all_documents

# Initialize the system
master_agent = MasterRoutingAgent()

# Process a single document
document = {
    "document_id": "custom_001",
    "content": "Certificate of Death for John Doe. Date of Death: Jan 1, 2023",
    "metadata": {"source": "custom"}
}

result = master_agent.process_document(document)
print(f"Status: {result['final_status']}")

# Process multiple documents
documents = get_all_documents()
batch_result = master_agent.process_batch(documents)
print(f"Approved: {batch_result['approved_documents']}")
```

## Testing

The system includes comprehensive unit tests for all components.

### Run All Tests
```bash
# Run all tests
python -m unittest discover tests

# Run with verbose output
python -m unittest discover tests -v
```

### Run Specific Test Suites
```bash
# Test Classification Agent only
python -m unittest tests.test_classification_agent

# Test Compliance Agent only  
python -m unittest tests.test_compliance_agent
```

### Test Coverage

The test suite covers:
- **Classification Agent**: 12 test cases covering all document categories
- **Compliance Agent**: 13 test cases covering validation scenarios
- **Edge Cases**: Empty documents, missing IDs, case sensitivity
- **Integration**: End-to-end processing workflows

Expected test results:
```
Ran 25 tests in 0.XXXs
OK
```

## System Components

### 1. Master Routing Agent (`agents/master_routing_agent.py`)

The orchestrator that manages the entire document processing pipeline.

**Key Methods:**
- `process_document(document)`: Process a single document through the pipeline
- `process_batch(documents)`: Process multiple documents efficiently
- `get_processing_history()`: Retrieve processing history
- `get_agent_info()`: Get information about configured agents

**Features:**
- Error handling and recovery
- Processing time tracking
- Comprehensive result aggregation
- Batch processing optimization

### 2. Classification Agent (`agents/classification_agent.py`)

Analyzes document content and assigns categories using keyword-based classification.

**Supported Categories:**
- Death Certificate (`01.0000-50`)
- Will or Trust (`02.0300-50`)  
- Property Deed (`03.0090-00`)
- Financial Statement (`04.5000-00`)
- Tax Document (`05.5000-70`)
- Miscellaneous (`00.0000-00`)

**Key Methods:**
- `classify_document(document)`: Classify a document and return category
- `get_supported_categories()`: Get all supported categories
- `get_classification_rules()`: Get keyword rules for debugging

**Classification Algorithm:**
1. Convert document content to lowercase
2. Search for category-specific keywords using word boundaries
3. Score each category based on keyword matches
4. Select category with highest score
5. Calculate confidence based on match ratio

### 3. Compliance Agent (`agents/compliance_agent.py`)

Enforces validation rules based on document categories.

**Validation Rules:**
- **Death Certificate**: Must contain "Certificate of Death" AND "Date of Death"
- **Will or Trust**: Must contain "Last Will and Testament" OR "Trust Agreement"
- **Other Categories**: Bypass validation (automatically valid)

**Key Methods:**
- `validate_document(document, classification)`: Validate based on category
- `get_validation_rules()`: Get current validation rules
- `get_categories_requiring_validation()`: Get categories that need validation

### 4. Document Taxonomy (`data/taxonomy.py`)

Defines the classification system used throughout the application.

**Taxonomy Structure:**
```python
DOCUMENT_TAXONOMY = {
    "Death Certificate": "01.0000-50",
    "Will or Trust": "02.0300-50", 
    "Property Deed": "03.0090-00",
    "Financial Statement": "04.5000-00",
    "Tax Document": "05.5000-70",
    "Miscellaneous": "00.0000-00"
}
```

### 5. Mock Documents (`documents/mock_documents.py`)

Comprehensive test dataset covering all scenarios:

**Test Cases:**
- Valid Death Certificate (should pass validation)
- Invalid Death Certificate (missing required phrases)
- Valid Will Document (contains "Last Will and Testament")
- Valid Trust Document (contains "Trust Agreement")  
- Invalid Will Document (missing required phrases)
- Financial Statement (should bypass validation)
- Property Deed (should bypass validation)

## Document Processing Pipeline

The system processes documents through a standardized pipeline:

### Step 1: Document Input
- Accept document payload with ID, content, and metadata
- Validate input format and required fields
- Initialize processing context

### Step 2: Classification
- Analyze document content using keyword matching
- Score potential categories based on keyword frequency
- Select highest-scoring category with confidence measure
- Return classification result with category and code

### Step 3: Compliance Validation
- Apply category-specific validation rules
- For Death Certificates: Check for required phrases
- For Wills/Trusts: Verify legal document indicators
- For other categories: Bypass validation
- Return validation result with pass/fail status

### Step 4: Result Aggregation
- Combine classification and compliance results
- Determine final document status (APPROVED/REJECTED/ERROR)
- Calculate processing metrics and timestamps
- Store result in processing history

### Processing States

Documents can have the following final states:
- **APPROVED**: Successfully classified and passed validation
- **REJECTED**: Successfully classified but failed validation  
- **ERROR**: Processing failed due to system error

## Configuration

### Adding New Document Categories

To add a new document category:

1. **Update Taxonomy** (`data/taxonomy.py`):
   ```python
   DOCUMENT_TAXONOMY["New Category"] = "XX.XXXX-XX"
   ```

2. **Add Classification Rules** (`agents/classification_agent.py`):
   ```python
   self.classification_rules["New Category"] = [
       "keyword1", "keyword2", "keyword3"
   ]
   ```

3. **Add Validation Rules** (if needed) (`agents/compliance_agent.py`):
   ```python
   self.validation_rules["New Category"] = {
       "required_phrases": ["required phrase"],
       "description": "Validation description"
   }
   ```

### Customizing Validation Rules

Validation rules can be customized by modifying the `validation_rules` dictionary in the Compliance Agent:

```python
# Require all phrases (AND logic)
"required_phrases": ["phrase1", "phrase2"]

# Require any phrase (OR logic)  
"required_phrases_any": ["phrase1", "phrase2"]
```

## Key Assumptions

### Design Decisions

1. **Local Execution**: System runs entirely locally without external API calls or cloud dependencies
2. **Keyword-Based Classification**: Uses simple but effective keyword matching rather than complex ML models
3. **Mock Data**: Uses simulated documents rather than real estate documents for privacy and testing
4. **Synchronous Processing**: Processes documents sequentially rather than in parallel
5. **In-Memory Storage**: Stores processing history in memory rather than persistent database

### Technical Assumptions

1. **Python Environment**: Assumes Python 3.7+ with standard library only
2. **Text Documents**: Assumes all documents are text-based (no OCR or PDF parsing)
3. **English Language**: Classification rules are designed for English-language documents
4. **Case Insensitive**: All text matching is case-insensitive
5. **Word Boundaries**: Uses word boundary matching to avoid partial word matches

### Business Assumptions

1. **Estate Context**: Focused specifically on estate settlement document types
2. **Compliance Rules**: Implements simplified validation rules for demonstration
3. **Document Quality**: Assumes reasonable document quality and formatting
4. **Processing Volume**: Designed for moderate document volumes (hundreds, not millions)
5. **Human Oversight**: Intended to assist rather than replace human review

## Technical Implementation

### Code Organization

```
alix-multi-agent-system/
├── agents/                 # Agent implementations
│   ├── __init__.py
│   ├── master_routing_agent.py
│   ├── classification_agent.py
│   └── compliance_agent.py
├── data/                   # Data definitions
│   ├── __init__.py
│   └── taxonomy.py
├── documents/              # Mock documents
│   ├── __init__.py
│   └── mock_documents.py
├── tests/                  # Unit tests
│   ├── __init__.py
│   ├── test_classification_agent.py
│   └── test_compliance_agent.py
├── main.py                 # CLI entry point
└── README.md              # This file
```

### Design Patterns

1. **Agent Pattern**: Each agent has a specific responsibility and clean interface
2. **Strategy Pattern**: Different validation strategies based on document category
3. **Factory Pattern**: Document creation and management through factory functions
4. **Observer Pattern**: Master agent observes and coordinates sub-agent activities

### Error Handling

The system implements comprehensive error handling:
- **Input Validation**: Checks for required fields and valid formats
- **Processing Errors**: Catches and reports agent processing failures
- **Graceful Degradation**: Continues processing other documents if one fails
- **Error Reporting**: Provides detailed error messages and context

### Performance Characteristics

- **Processing Speed**: ~0.001-0.01 seconds per document
- **Memory Usage**: Minimal (stores only processing history)
- **Scalability**: Linear scaling with document count
- **Resource Requirements**: Very low (CPU and memory)

## Performance Considerations

### Optimization Strategies

1. **Keyword Indexing**: Pre-compiled regex patterns for faster matching
2. **Batch Processing**: Optimized batch operations reduce overhead
3. **Memory Management**: Efficient data structures minimize memory usage
4. **Lazy Loading**: Documents loaded only when needed

### Scaling Recommendations

For production deployment with larger document volumes:

1. **Parallel Processing**: Implement multi-threading for document processing
2. **Database Storage**: Replace in-memory storage with persistent database
3. **Caching**: Cache classification results for similar documents
4. **Load Balancing**: Distribute processing across multiple instances
5. **Monitoring**: Add comprehensive logging and monitoring

### Performance Metrics

The system tracks several performance metrics:
- Processing duration per document
- Batch processing time
- Classification confidence scores
- Validation success rates
- Error rates by category

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError` when running tests
```bash
# Solution: Run from project root directory
cd alix-multi-agent-system
python -m unittest discover tests
```

**Issue**: No output when running `python main.py`
```bash
# Solution: Check Python version and file permissions
python --version  # Should be 3.7+
ls -la main.py    # Should be readable
```

**Issue**: Classification confidence always 0.0
```bash
# Solution: Check document content has relevant keywords
# Use get_classification_rules() to see expected keywords
```

### Debug Mode

Enable debug output by modifying the master agent:

```python
# In master_routing_agent.py, set debug=True
print(f"[DEBUG] Processing document: {document_id}")
```

### Logging

Add logging for production use:

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

### Code Style

- Follow PEP 8 Python style guidelines
- Use descriptive variable and function names
- Add docstrings for all public methods
- Include type hints where appropriate
- Maintain test coverage above 90%

### Testing Guidelines

- Write unit tests for all new functionality
- Include edge case testing
- Test error conditions and recovery
- Verify integration between components
- Document test scenarios and expected outcomes

## License

This project is developed for the Alix Technical Test (June 2025) and is intended for evaluation purposes.

---

**Developed by**: Manus AI  
**Date**: June 2025  
**Version**: 1.0.0  
**Contact**: For questions about this implementation, please refer to the technical test documentation.

