#!/usr/bin/env python3
"""
Simple test script for ESC AI Diagnostic System
Run this to test natural language queries with Claude

Usage:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python test_ai_simple.py
"""

import os
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from ai_diagnostics import DiagnosticSystem


def main():
    """Interactive diagnostic system"""

    # Check API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nTo use this, set your API key:")
        print("  export ANTHROPIC_API_KEY='sk-ant-...'")
        print("\nGet your API key from: https://console.anthropic.com/account/keys")
        return 1

    print("🛗 ESC AI Diagnostics - Interactive Test")
    print("=" * 60)

    try:
        # Initialize system
        system = DiagnosticSystem()
        print("✅ System initialized")
        print(f"📚 Knowledge Base: {system.get_knowledge_summary()}")
        print("\n" + "=" * 60)

        # Example queries to try
        example_queries = [
            "Was ist Fehlercode F01 02?",
            "Der Aufzug funktioniert nicht, Sicherheitskreis ist offen. Was ist falsch?",
            "Wie konfiguriere ich die Fahrtdauer?",
            "Was ist die Komponente XTSS?",
        ]

        print("\n📝 Example queries you can try:")
        for i, q in enumerate(example_queries, 1):
            print(f"  {i}. {q}")

        print("\n" + "=" * 60)
        print("Type your question (or 'quit' to exit):\n")

        # Interactive loop
        while True:
            try:
                query = input("❓ Your question: ").strip()

                if query.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break

                if not query:
                    continue

                print("\n⏳ Analyzing...")
                response = system.query(query)

                print("\n" + "=" * 60)
                print("📋 DIAGNOSIS:\n")
                print(response.diagnosis)

                print("\n" + "-" * 60)
                print("📊 METADATA:")
                print(f"  Confidence: {response.confidence}")
                if response.codes_referenced:
                    print(f"  Codes Referenced: {', '.join(response.codes_referenced)}")
                if response.manual_pages:
                    print(f"  Manual Pages: {', '.join(map(str, response.manual_pages))}")
                if response.next_steps:
                    print(f"  Next Steps: {len(response.next_steps)}")
                    for step in response.next_steps:
                        print(f"    • {step}")

                print("\n" + "=" * 60 + "\n")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Try a different question.\n")

    except Exception as e:
        print(f"❌ Failed to initialize system: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
