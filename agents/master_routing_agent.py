"""
Master Routing Agent for the Alix Multi-Agent System.

This agent serves as the orchestrator for the document processing pipeline,
routing documents through the Classification Agent and then the Compliance Agent
to produce final processing results.
"""

import time
from typing import Dict, Any, Optional
from datetime import datetime

from agents.classification_agent import ClassificationAgent
from agents.compliance_agent import ComplianceAgent


class MasterRoutingAgent:
    """
    Master agent that orchestrates the document processing pipeline.
    
    Accepts document payloads, routes them through classification and compliance
    agents, and returns comprehensive processing results.
    """
    
    def __init__(self):
        """Initialize the Master Routing Agent with sub-agents."""
        self.classification_agent = ClassificationAgent()
        self.compliance_agent = ComplianceAgent()
        self.processing_history = []
    
    def process_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a document through the complete pipeline.
        
        Args:
            document (Dict[str, Any]): Document payload containing:
                - document_id: Unique identifier for the document
                - content: Text content of the document
                - metadata: Additional document metadata (optional)
        
        Returns:
            Dict[str, Any]: Complete processing result containing:
                - document_id: Original document identifier
                - processing_status: Overall processing status
                - classification_result: Results from Classification Agent
                - compliance_result: Results from Compliance Agent
                - final_status: Final document status (APPROVED/REJECTED/ERROR)
                - processing_timestamp: When processing completed
                - processing_duration: Time taken to process (seconds)
        """
        start_time = time.time()
        processing_timestamp = datetime.now().isoformat()
        
        document_id = document.get("document_id", "unknown")
        
        try:
            # Step 1: Classify the document
            print(f"[MASTER] Processing document {document_id}: Starting classification...")
            classification_result = self.classification_agent.classify_document(document)
            
            if not classification_result:
                raise Exception("Classification agent returned empty result")
            
            print(f"[MASTER] Document {document_id} classified as: {classification_result.get('category', 'Unknown')}")
            
            # Step 2: Validate compliance
            print(f"[MASTER] Processing document {document_id}: Starting compliance validation...")
            compliance_result = self.compliance_agent.validate_document(document, classification_result)
            
            if not compliance_result:
                raise Exception("Compliance agent returned empty result")
            
            print(f"[MASTER] Document {document_id} compliance check: {'PASSED' if compliance_result.get('valid') else 'FAILED'}")
            
            # Step 3: Determine final status
            final_status = self._determine_final_status(classification_result, compliance_result)
            processing_status = "SUCCESS"
            
            processing_duration = time.time() - start_time
            
            # Create comprehensive result
            result = {
                "document_id": document_id,
                "processing_status": processing_status,
                "classification_result": classification_result,
                "compliance_result": compliance_result,
                "final_status": final_status,
                "processing_timestamp": processing_timestamp,
                "processing_duration": round(processing_duration, 4),
                "pipeline_steps": [
                    {
                        "step": "classification",
                        "status": "completed",
                        "agent": "ClassificationAgent",
                        "result": classification_result
                    },
                    {
                        "step": "compliance",
                        "status": "completed",
                        "agent": "ComplianceAgent",
                        "result": compliance_result
                    }
                ]
            }
            
            print(f"[MASTER] Document {document_id} processing completed: {final_status}")
            
        except Exception as e:
            processing_duration = time.time() - start_time
            error_message = str(e)
            
            print(f"[MASTER] Error processing document {document_id}: {error_message}")
            
            result = {
                "document_id": document_id,
                "processing_status": "ERROR",
                "classification_result": None,
                "compliance_result": None,
                "final_status": "ERROR",
                "error_message": error_message,
                "processing_timestamp": processing_timestamp,
                "processing_duration": round(processing_duration, 4),
                "pipeline_steps": []
            }
        
        # Store in processing history
        self.processing_history.append(result)
        
        return result
    
    def _determine_final_status(self, classification_result: Dict[str, Any], 
                              compliance_result: Dict[str, Any]) -> str:
        """
        Determine the final processing status based on classification and compliance results.
        
        Args:
            classification_result (Dict[str, Any]): Classification agent result
            compliance_result (Dict[str, Any]): Compliance agent result
        
        Returns:
            str: Final status (APPROVED, REJECTED, or ERROR)
        """
        # Check if classification was successful
        if not classification_result or not classification_result.get("category"):
            return "ERROR"
        
        # Check if compliance validation passed
        if not compliance_result:
            return "ERROR"
        
        # If compliance check passed, document is approved
        if compliance_result.get("valid", False):
            return "APPROVED"
        else:
            return "REJECTED"
    
    def process_batch(self, documents: list) -> Dict[str, Any]:
        """
        Process multiple documents in batch.
        
        Args:
            documents (list): List of document payloads
        
        Returns:
            Dict[str, Any]: Batch processing results containing:
                - total_documents: Number of documents processed
                - successful_processing: Number of successfully processed documents
                - approved_documents: Number of approved documents
                - rejected_documents: Number of rejected documents
                - error_documents: Number of documents with errors
                - results: List of individual processing results
                - batch_timestamp: When batch processing completed
        """
        print(f"[MASTER] Starting batch processing of {len(documents)} documents...")
        
        batch_start_time = time.time()
        results = []
        
        for document in documents:
            result = self.process_document(document)
            results.append(result)
        
        # Calculate batch statistics
        successful_processing = len([r for r in results if r["processing_status"] == "SUCCESS"])
        approved_documents = len([r for r in results if r["final_status"] == "APPROVED"])
        rejected_documents = len([r for r in results if r["final_status"] == "REJECTED"])
        error_documents = len([r for r in results if r["final_status"] == "ERROR"])
        
        batch_duration = time.time() - batch_start_time
        
        batch_result = {
            "total_documents": len(documents),
            "successful_processing": successful_processing,
            "approved_documents": approved_documents,
            "rejected_documents": rejected_documents,
            "error_documents": error_documents,
            "results": results,
            "batch_timestamp": datetime.now().isoformat(),
            "batch_duration": round(batch_duration, 4)
        }
        
        print(f"[MASTER] Batch processing completed:")
        print(f"  - Total: {batch_result['total_documents']}")
        print(f"  - Approved: {batch_result['approved_documents']}")
        print(f"  - Rejected: {batch_result['rejected_documents']}")
        print(f"  - Errors: {batch_result['error_documents']}")
        print(f"  - Duration: {batch_result['batch_duration']}s")
        
        return batch_result
    
    def get_processing_history(self) -> list:
        """
        Get the complete processing history.
        
        Returns:
            list: List of all processed document results
        """
        return self.processing_history.copy()
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get information about the configured agents.
        
        Returns:
            Dict[str, Any]: Information about sub-agents and their capabilities
        """
        return {
            "master_agent": {
                "class": self.__class__.__name__,
                "description": "Orchestrates document processing pipeline"
            },
            "classification_agent": {
                "class": self.classification_agent.__class__.__name__,
                "supported_categories": self.classification_agent.get_supported_categories(),
                "classification_rules": list(self.classification_agent.get_classification_rules().keys())
            },
            "compliance_agent": {
                "class": self.compliance_agent.__class__.__name__,
                "categories_requiring_validation": self.compliance_agent.get_categories_requiring_validation(),
                "validation_rules": list(self.compliance_agent.get_validation_rules().keys())
            }
        }
    
    def reset_history(self):
        """Reset the processing history."""
        self.processing_history = []
        print("[MASTER] Processing history reset")

