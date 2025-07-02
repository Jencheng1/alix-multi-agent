#!/usr/bin/env python3
"""
Main CLI entry point for the Alix Multi-Agent System.

This script serves as the command-line interface to demonstrate the
multi-agent document processing system by processing mock documents
and displaying the results.
"""

import sys
import json
from typing import Dict, Any

from agents.master_routing_agent import MasterRoutingAgent
from documents.mock_documents import get_all_documents, get_document_by_id


def print_separator(title: str = "", width: int = 80):
    """Print a formatted separator line."""
    if title:
        title_formatted = f" {title} "
        padding = (width - len(title_formatted)) // 2
        separator = "=" * padding + title_formatted + "=" * padding
        if len(separator) < width:
            separator += "="
    else:
        separator = "=" * width
    print(separator)


def print_document_summary(document: Dict[str, Any]):
    """Print a summary of the document being processed."""
    doc_id = document.get("document_id", "Unknown")
    content_preview = document.get("content", "")[:100].replace("\n", " ").strip()
    if len(document.get("content", "")) > 100:
        content_preview += "..."
    
    print(f"Document ID: {doc_id}")
    print(f"Content Preview: {content_preview}")
    print(f"Metadata: {document.get('metadata', {})}")


def print_processing_result(result: Dict[str, Any]):
    """Print the processing result in a formatted way."""
    doc_id = result.get("document_id", "Unknown")
    final_status = result.get("final_status", "Unknown")
    processing_status = result.get("processing_status", "Unknown")
    
    # Status color coding (for terminals that support ANSI colors)
    status_colors = {
        "APPROVED": "\033[92m",  # Green
        "REJECTED": "\033[91m",  # Red
        "ERROR": "\033[93m",     # Yellow
    }
    reset_color = "\033[0m"
    
    status_color = status_colors.get(final_status, "")
    
    print(f"Processing Status: {processing_status}")
    print(f"Final Status: {status_color}{final_status}{reset_color}")
    print(f"Processing Duration: {result.get('processing_duration', 0):.4f} seconds")
    
    # Classification details
    classification = result.get("classification_result", {})
    if classification:
        print(f"Classified Category: {classification.get('category', 'Unknown')}")
        print(f"Category Code: {classification.get('categoryCode', 'Unknown')}")
        print(f"Classification Confidence: {classification.get('confidence', 0):.2f}")
    
    # Compliance details
    compliance = result.get("compliance_result", {})
    if compliance:
        print(f"Compliance Valid: {compliance.get('valid', False)}")
        print(f"Compliance Reason: {compliance.get('reason', 'No reason provided')}")
    
    # Error details if any
    if result.get("error_message"):
        print(f"Error: {result.get('error_message')}")


def print_batch_summary(batch_result: Dict[str, Any]):
    """Print a summary of batch processing results."""
    print_separator("BATCH PROCESSING SUMMARY")
    print(f"Total Documents Processed: {batch_result.get('total_documents', 0)}")
    print(f"Successfully Processed: {batch_result.get('successful_processing', 0)}")
    print(f"Approved Documents: {batch_result.get('approved_documents', 0)}")
    print(f"Rejected Documents: {batch_result.get('rejected_documents', 0)}")
    print(f"Error Documents: {batch_result.get('error_documents', 0)}")
    print(f"Total Processing Time: {batch_result.get('batch_duration', 0):.4f} seconds")
    print(f"Batch Timestamp: {batch_result.get('batch_timestamp', 'Unknown')}")


def main():
    """Main entry point for the CLI application."""
    print_separator("ALIX MULTI-AGENT SYSTEM")
    print("Estate Document Processing Pipeline")
    print("Developed for Alix Technical Test - June 2025")
    print()
    
    # Initialize the Master Routing Agent
    print("Initializing Multi-Agent System...")
    master_agent = MasterRoutingAgent()
    
    # Display agent information
    agent_info = master_agent.get_agent_info()
    print(f"✓ {agent_info['master_agent']['class']} initialized")
    print(f"✓ {agent_info['classification_agent']['class']} initialized")
    print(f"✓ {agent_info['compliance_agent']['class']} initialized")
    print()
    
    # Load mock documents
    print("Loading mock documents...")
    documents = get_all_documents()
    print(f"✓ Loaded {len(documents)} mock documents")
    print()
    
    # Process documents individually with detailed output
    print_separator("INDIVIDUAL DOCUMENT PROCESSING")
    
    for i, document in enumerate(documents, 1):
        print_separator(f"DOCUMENT {i} OF {len(documents)}")
        print_document_summary(document)
        print()
        
        # Process the document
        result = master_agent.process_document(document)
        
        print()
        print_processing_result(result)
        print()
    
    # Process all documents in batch and show summary
    print_separator("BATCH PROCESSING")
    print("Processing all documents in batch mode...")
    print()
    
    # Reset history to avoid duplication
    master_agent.reset_history()
    
    # Process batch
    batch_result = master_agent.process_batch(documents)
    
    print()
    print_batch_summary(batch_result)
    
    # Detailed results table
    print()
    print_separator("DETAILED RESULTS TABLE")
    print(f"{'Doc ID':<8} {'Category':<18} {'Code':<12} {'Valid':<6} {'Status':<10} {'Duration':<10}")
    print("-" * 80)
    
    for result in batch_result.get('results', []):
        doc_id = result.get('document_id', 'Unknown')[:7]
        classification = result.get('classification_result', {})
        compliance = result.get('compliance_result', {})
        category = classification.get('category', 'Unknown')[:17]
        code = classification.get('categoryCode', 'Unknown')[:11]
        valid = str(compliance.get('valid', False))[:5]
        status = result.get('final_status', 'Unknown')[:9]
        duration = f"{result.get('processing_duration', 0):.3f}s"[:9]
        
        print(f"{doc_id:<8} {category:<18} {code:<12} {valid:<6} {status:<10} {duration:<10}")
    
    print()
    print_separator("SYSTEM INFORMATION")
    
    # Display system capabilities
    classification_agent_info = agent_info['classification_agent']
    compliance_agent_info = agent_info['compliance_agent']
    
    print("Classification Agent:")
    print(f"  - Supported Categories: {len(classification_agent_info['supported_categories'])}")
    for category, code in classification_agent_info['supported_categories'].items():
        print(f"    • {category}: {code}")
    
    print()
    print("Compliance Agent:")
    print(f"  - Categories Requiring Validation: {len(compliance_agent_info['categories_requiring_validation'])}")
    for category in compliance_agent_info['categories_requiring_validation']:
        print(f"    • {category}")
    
    print()
    print_separator("PROCESSING COMPLETE")
    print("All documents have been processed successfully!")
    print("Thank you for using the Alix Multi-Agent System.")


def run_single_document(document_id: str):
    """Process a single document by ID."""
    print_separator(f"PROCESSING DOCUMENT: {document_id}")
    
    document = get_document_by_id(document_id)
    if not document:
        print(f"Error: Document with ID '{document_id}' not found.")
        return
    
    master_agent = MasterRoutingAgent()
    print_document_summary(document)
    print()
    
    result = master_agent.process_document(document)
    print()
    print_processing_result(result)


def show_help():
    """Display help information."""
    print("Alix Multi-Agent System - CLI Help")
    print()
    print("Usage:")
    print("  python main.py                    # Process all mock documents")
    print("  python main.py <document_id>      # Process a specific document")
    print("  python main.py --help             # Show this help message")
    print()
    print("Available Document IDs:")
    documents = get_all_documents()
    for doc in documents:
        doc_id = doc.get('document_id', 'Unknown')
        content_preview = doc.get('content', '')[:50].replace('\n', ' ').strip()
        print(f"  {doc_id:<8} - {content_preview}...")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ["--help", "-h", "help"]:
            show_help()
        else:
            run_single_document(arg)
    else:
        main()

