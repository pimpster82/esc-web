#!/usr/bin/env python3
"""
CLI Validation Tool - Interactive validation of AI responses
Allows quick testing and feedback collection from command line
"""

import json
from ai_diagnostics import DiagnosticSystem
from validation_manager import ValidationManager


class CLIValidator:
    """Interactive CLI validator"""

    def __init__(self):
        """Initialize validator"""
        print("\n🛗 ESC Validation Tool (CLI)")
        print("=" * 70)
        print("Interactive testing and feedback collection")
        print("=" * 70 + "\n")

        try:
            self.diagnostic_system = DiagnosticSystem()
            print("✅ Diagnostic system loaded")
        except Exception as e:
            print(f"❌ Error loading diagnostic system: {e}")
            exit(1)

        try:
            self.validation_manager = ValidationManager()
            print("✅ Validation manager initialized")
        except Exception as e:
            print(f"❌ Error initializing validation manager: {e}")
            exit(1)

        self.session_count = 0

    def run(self):
        """Run interactive validation loop"""
        print("\nCommands:")
        print("  'q' or 'quit' - Exit")
        print("  'stats'      - Show validation statistics")
        print("  'clear'      - Clear history\n")

        while True:
            try:
                # Get query
                query = input("📋 Query: ").strip()

                if not query:
                    continue

                if query.lower() in ['q', 'quit']:
                    self._show_session_summary()
                    print("\n👋 Goodbye!")
                    break

                if query.lower() == 'stats':
                    self._show_stats()
                    continue

                if query.lower() == 'clear':
                    self.diagnostic_system.clear_history()
                    print("✅ History cleared\n")
                    continue

                # Get response
                print("\n⏳ Processing...\n")
                response = self.diagnostic_system.query(query)

                # Display response
                print("─" * 70)
                print(f"Confidence: {response.confidence}")
                print("─" * 70)
                print(response.diagnosis)
                print("─" * 70)

                # Get feedback
                while True:
                    feedback_input = input(
                        "\n✓ Correct / ✗ Incorrect / ? Unsure / s Skip: "
                    ).strip().lower()

                    if feedback_input == 's':
                        print()
                        break

                    if feedback_input in ['j', '✓', 'c', 'correct']:
                        feedback = 'correct'
                    elif feedback_input in ['n', '✗', 'i', 'incorrect']:
                        feedback = 'incorrect'
                    elif feedback_input in ['?', 'u', 'unsure']:
                        feedback = 'unsure'
                    else:
                        print("Invalid input. Please try again.")
                        continue

                    # Optional notes
                    notes = input("📝 Notes (optional): ").strip()

                    # Store feedback
                    self.validation_manager.add_feedback(
                        query=query,
                        response=response.diagnosis,
                        feedback=feedback,
                        confidence=response.confidence,
                        notes=notes
                    )

                    self.session_count += 1
                    print(f"✅ Feedback recorded (#{self.session_count})\n")
                    break

            except KeyboardInterrupt:
                self._show_session_summary()
                print("\n👋 Interrupted!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")

    def _show_stats(self):
        """Show validation statistics"""
        stats = self.validation_manager.get_stats()

        print("\n" + "=" * 70)
        print("📊 VALIDATION STATISTICS")
        print("=" * 70)
        print(f"Total validations:  {stats['total_validations']}")
        print(f"  ✓ Correct:       {stats['correct']}")
        print(f"  ✗ Incorrect:     {stats['incorrect']}")
        print(f"  ? Unsure:        {stats['unsure']}")
        print(f"Accuracy:          {stats['accuracy']}%")
        print(f"Last updated:      {stats['last_updated']}")
        print("=" * 70 + "\n")

    def _show_session_summary(self):
        """Show session summary"""
        if self.session_count == 0:
            return

        print("\n" + "=" * 70)
        print("📈 SESSION SUMMARY")
        print("=" * 70)
        print(f"Queries validated: {self.session_count}")

        # Get recent feedback
        recent = self.validation_manager.get_feedback(limit=self.session_count)

        # Count by type
        correct = len([f for f in recent if f['feedback'] == 'correct'])
        incorrect = len([f for f in recent if f['feedback'] == 'incorrect'])
        unsure = len([f for f in recent if f['feedback'] == 'unsure'])

        print(f"\nSession results:")
        print(f"  ✓ Correct:   {correct}")
        print(f"  ✗ Incorrect: {incorrect}")
        print(f"  ? Unsure:    {unsure}")

        if correct + incorrect > 0:
            accuracy = correct / (correct + incorrect) * 100
            print(f"  Accuracy:    {accuracy:.1f}%")

        print("=" * 70 + "\n")


def main():
    """Main entry point"""
    validator = CLIValidator()
    validator.run()


if __name__ == "__main__":
    main()
