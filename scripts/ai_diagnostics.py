"""
AI Diagnostics System - Main interface for Via Series diagnostic queries
Uses Claude AI with knowledge base context for intelligent diagnosis
"""

import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from knowledge_loader import KnowledgeLoader
from system_prompt import get_system_prompt


@dataclass
class DiagnosticResponse:
    """Structured response from diagnostic system"""
    query: str
    diagnosis: str
    confidence: str  # HIGH, MEDIUM, LOW
    codes_referenced: List[str]
    next_steps: List[str]
    manual_pages: List[int]
    raw_response: Optional[str] = None


class DiagnosticSystem:
    """Main diagnostic system using Claude API and knowledge base"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize diagnostic system

        Args:
            api_key: Claude API key (gets from ANTHROPIC_API_KEY env if not provided)
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Claude API key required. Set ANTHROPIC_API_KEY env variable or pass as argument.")

        self.knowledge = KnowledgeLoader()
        if not self.knowledge.load_all():
            raise RuntimeError("Failed to load knowledge base")

        # Import Anthropic client
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("anthropic library required. Install with: pip install anthropic")

        self.conversation_history = []

    def query(self, question: str, use_history: bool = True) -> DiagnosticResponse:
        """
        Process a diagnostic query

        Args:
            question: Technician's question in German or English
            use_history: Whether to use conversation history for context

        Returns:
            DiagnosticResponse with diagnosis, confidence, etc.
        """
        # Enrich context from knowledge base
        context = self._build_context(question)

        # Prepare message
        message_content = f"""WISSENSDATENBANK KONTEXT:
{context}

TECHNIKER FRAGE:
{question}

Antworte basierend auf der Wissensdatenbank."""

        # Add to history if enabled
        if use_history:
            self.conversation_history.append({
                "role": "user",
                "content": message_content
            })

            messages = self.conversation_history
        else:
            messages = [{"role": "user", "content": message_content}]

        # Call Claude API
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                system=get_system_prompt(),
                messages=messages
            )

            diagnosis_text = response.content[0].text

            # Add to history if enabled
            if use_history:
                self.conversation_history.append({
                    "role": "assistant",
                    "content": diagnosis_text
                })

            # Parse response to extract structure
            response_obj = self._parse_response(question, diagnosis_text)
            response_obj.raw_response = diagnosis_text

            return response_obj

        except Exception as e:
            raise RuntimeError(f"Claude API call failed: {e}")

    def _build_context(self, question: str) -> str:
        """
        Build relevant knowledge base context for the query

        Args:
            question: The technician's question

        Returns:
            Formatted context string with relevant data
        """
        context = "# VERFÜGBARE WISSENSDATENBANK\n\n"

        # Check for error codes
        error_matches = []
        for code in self.knowledge.error_codes:
            if (code.get('code', '').upper() in question.upper() or
                code.get('description_de', '').lower() in question.lower()):
                error_matches.append(code)

        if error_matches:
            context += "## Relevante Fehlercodes\n"
            for error in error_matches[:5]:  # Limit to 5
                context += f"\n- **{error.get('code')}**: {error.get('description_de')}\n"
                if error.get('cause_solution'):
                    context += f"  Ursache/Lösung: {error.get('cause_solution')[:200]}...\n"

        # Check for parameters
        param_matches = self.knowledge.search_parameters_by_description(question)
        if param_matches:
            context += "\n## Relevante Parameter\n"
            for param in param_matches[:5]:  # Limit to 5
                context += f"- **{param.get('code')}**: {param.get('description_de')}\n"

        # Check for components
        abbrev_matches = self.knowledge.search_abbreviations(question)
        if abbrev_matches:
            context += "\n## Relevante Komponenten\n"
            for abbrev in abbrev_matches[:5]:  # Limit to 5
                context += f"- **{abbrev.get('code')}**: {abbrev.get('description_de')}\n"

        return context

    def _parse_response(self, question: str, response: str) -> DiagnosticResponse:
        """
        Parse Claude's response to extract structured information

        Args:
            question: Original question
            response: Claude's response

        Returns:
            DiagnosticResponse object
        """
        # Extract codes referenced (simple pattern matching)
        codes = []
        import re
        # Find F-codes
        f_codes = re.findall(r'F\d{2}\s?\d{2}', response)
        codes.extend(f_codes)
        # Find P-codes
        p_codes = re.findall(r'P\d{4}', response)
        codes.extend(p_codes)

        # Determine confidence based on response content
        if 'HOCH' in response or 'Handbuch' in response or 'Seite' in response:
            confidence = 'HIGH'
        elif 'MITTEL' in response:
            confidence = 'MEDIUM'
        else:
            confidence = 'MEDIUM'

        # Extract manual pages
        pages = []
        page_matches = re.findall(r'Seite:\s*(\d+)', response)
        pages = [int(p) for p in page_matches]

        # Extract next steps (lines that start with numbers)
        next_steps = []
        lines = response.split('\n')
        for line in lines:
            if re.match(r'^\d+\.\s', line):
                next_steps.append(line.strip())

        return DiagnosticResponse(
            query=question,
            diagnosis=response,
            confidence=confidence,
            codes_referenced=codes,
            next_steps=next_steps[:5],  # Limit to 5 steps
            manual_pages=pages
        )

    def clear_history(self):
        """Clear conversation history for fresh start"""
        self.conversation_history = []

    def get_knowledge_summary(self) -> Dict:
        """Get summary of loaded knowledge base"""
        return self.knowledge.get_summary()


def main():
    """Example usage"""
    print("Via Series AI Diagnostics System")
    print("=" * 50)

    try:
        # Initialize system
        system = DiagnosticSystem()

        print(f"✅ System initialized")
        print(f"Knowledge base: {system.get_knowledge_summary()}")

        # Example queries
        test_queries = [
            "Was ist Fehlercode F01 02?",
            "Der Aufzug funktioniert nicht. Sicherheitskreis öffnet sich. Was ist falsch?",
            "Wie konfiguriere ich die Fahrtdauer (P0001)?",
        ]

        for i, query in enumerate(test_queries, 1):
            print(f"\n{'=' * 50}")
            print(f"Query {i}: {query}")
            print("=" * 50)

            response = system.query(query)

            print(f"\nDiagnosis:")
            print(response.diagnosis)

            print(f"\n\nMetadata:")
            print(f"- Confidence: {response.confidence}")
            print(f"- Codes Referenced: {', '.join(response.codes_referenced)}")
            print(f"- Manual Pages: {', '.join(map(str, response.manual_pages))}")
            if response.next_steps:
                print(f"- Next Steps: {len(response.next_steps)} identified")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
