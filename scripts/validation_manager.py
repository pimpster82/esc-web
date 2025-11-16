"""
Validation Manager - Handle feedback collection and validation tracking
Stores all validation data for quality analysis
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class ValidationManager:
    """Manage validation feedback and quality metrics"""

    def __init__(self, feedback_dir: str = "../data/validation"):
        """Initialize validation manager

        Args:
            feedback_dir: Directory to store validation data
        """
        self.feedback_dir = Path(feedback_dir)
        self.feedback_dir.mkdir(parents=True, exist_ok=True)

        self.feedback_file = self.feedback_dir / "feedback.json"
        self.stats_file = self.feedback_dir / "stats.json"

        # Initialize files if they don't exist
        if not self.feedback_file.exists():
            self._save_feedback([])
        if not self.stats_file.exists():
            self._save_stats(self._init_stats())

    def _init_stats(self) -> Dict:
        """Initialize stats structure"""
        return {
            "total_validations": 0,
            "correct": 0,
            "incorrect": 0,
            "unsure": 0,
            "accuracy": 0.0,
            "last_updated": None
        }

    def _load_feedback(self) -> List[Dict]:
        """Load feedback from file"""
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def _save_feedback(self, feedback: List[Dict]):
        """Save feedback to file"""
        with open(self.feedback_file, 'w', encoding='utf-8') as f:
            json.dump(feedback, f, indent=2, ensure_ascii=False)

    def _load_stats(self) -> Dict:
        """Load statistics from file"""
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self._init_stats()

    def _save_stats(self, stats: Dict):
        """Save statistics to file"""
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

    def add_feedback(self, query: str, response: str, feedback: str,
                    confidence: str = "MEDIUM", notes: str = "") -> Dict:
        """Add validation feedback

        Args:
            query: The original question/query
            response: The AI's response
            feedback: One of: "correct", "incorrect", "unsure"
            confidence: AI confidence level
            notes: Optional user notes

        Returns:
            Feedback record
        """
        feedback_data = self._load_feedback()

        record = {
            "id": len(feedback_data) + 1,
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response[:500],  # Truncate long responses
            "feedback": feedback,  # correct, incorrect, unsure
            "confidence": confidence,
            "notes": notes
        }

        feedback_data.append(record)
        self._save_feedback(feedback_data)

        # Update statistics
        self._update_stats(feedback)

        return record

    def _update_stats(self, feedback: str):
        """Update statistics based on feedback"""
        stats = self._load_stats()

        stats["total_validations"] += 1

        if feedback == "correct":
            stats["correct"] += 1
        elif feedback == "incorrect":
            stats["incorrect"] += 1
        elif feedback == "unsure":
            stats["unsure"] += 1

        # Calculate accuracy (only from correct/incorrect, ignore unsure)
        total = stats["correct"] + stats["incorrect"]
        if total > 0:
            stats["accuracy"] = round(stats["correct"] / total * 100, 1)

        stats["last_updated"] = datetime.now().isoformat()

        self._save_stats(stats)

    def get_feedback(self, limit: int = None, feedback_type: str = None) -> List[Dict]:
        """Get feedback records

        Args:
            limit: Maximum number of records to return
            feedback_type: Filter by feedback type (correct, incorrect, unsure)

        Returns:
            List of feedback records
        """
        feedback = self._load_feedback()

        # Filter by type if specified
        if feedback_type:
            feedback = [f for f in feedback if f["feedback"] == feedback_type]

        # Sort by timestamp (newest first)
        feedback.sort(key=lambda x: x["timestamp"], reverse=True)

        # Apply limit
        if limit:
            feedback = feedback[:limit]

        return feedback

    def get_stats(self) -> Dict:
        """Get current statistics"""
        return self._load_stats()

    def get_summary(self) -> Dict:
        """Get validation summary with breakdown"""
        feedback = self._load_feedback()
        stats = self._load_stats()

        return {
            "total_validations": stats["total_validations"],
            "breakdown": {
                "correct": stats["correct"],
                "incorrect": stats["incorrect"],
                "unsure": stats["unsure"]
            },
            "accuracy": f"{stats['accuracy']}%",
            "last_updated": stats["last_updated"],
            "recent_feedback": self.get_feedback(limit=10)
        }

    def export_csv(self) -> str:
        """Export feedback as CSV"""
        import csv
        from io import StringIO

        feedback = self._load_feedback()

        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            "id", "timestamp", "query", "feedback", "confidence", "notes"
        ])

        writer.writeheader()
        for record in feedback:
            writer.writerow({
                "id": record["id"],
                "timestamp": record["timestamp"],
                "query": record["query"],
                "feedback": record["feedback"],
                "confidence": record["confidence"],
                "notes": record["notes"]
            })

        return output.getvalue()


if __name__ == "__main__":
    # Test the manager
    manager = ValidationManager()

    print("Validation Manager Test\n")
    print("=" * 60)

    # Add sample feedback
    print("Adding sample feedback...")
    manager.add_feedback(
        query="F01 02",
        response="Sicherheitskreis geöffnet",
        feedback="correct",
        confidence="HIGH",
        notes="Correct description and causes"
    )

    manager.add_feedback(
        query="SMQ",
        response="Safety Monitoring and Control Board",
        feedback="correct",
        confidence="HIGH"
    )

    print("✅ Feedback added\n")

    # Get summary
    print("=" * 60)
    print("Validation Summary")
    print("=" * 60)
    summary = manager.get_summary()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
