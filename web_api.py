#!/usr/bin/env python3
"""
Web API Server for ESC AI Diagnostics
Provides Claude-based diagnostic queries via REST API
"""

import json
import os
import sys
from pathlib import Path
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

# Add scripts to path and change to scripts directory
script_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(script_dir))
import os
os.chdir(script_dir)

from ai_diagnostics import DiagnosticSystem
from validation_manager import ValidationManager

# Initialize Flask app - use correct static folder path
static_folder = str(Path(__file__).parent / "web")
app = Flask(__name__, static_folder=static_folder, static_url_path='')
CORS(app)

# Initialize diagnostic system
try:
    diagnostic_system = DiagnosticSystem()
    print("✅ Diagnostic system initialized")
except Exception as e:
    print(f"❌ Failed to initialize diagnostic system: {e}")
    diagnostic_system = None

# Initialize validation manager
try:
    validation_manager = ValidationManager()
    print("✅ Validation manager initialized")
except Exception as e:
    print(f"❌ Failed to initialize validation manager: {e}")
    validation_manager = None


@app.route('/')
def index():
    """Serve the web interface"""
    return app.send_static_file('index.html')


@app.route('/api/query', methods=['POST'])
def query():
    """
    Process a diagnostic query

    Request body:
    {
        "question": "string",
        "use_history": true/false (optional)
    }

    Response:
    {
        "success": true/false,
        "diagnosis": "string",
        "confidence": "HIGH/MEDIUM/LOW",
        "codes_referenced": ["code1", "code2"],
        "manual_pages": [1, 2, 3],
        "next_steps": ["step1", "step2"],
        "error": "error message (if failed)"
    }
    """
    if not diagnostic_system:
        return jsonify({
            "success": False,
            "error": "Diagnostic system not initialized"
        }), 500

    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        use_history = data.get('use_history', True)

        if not question:
            return jsonify({
                "success": False,
                "error": "No question provided"
            }), 400

        # Process query
        response = diagnostic_system.query(question, use_history=use_history)

        return jsonify({
            "success": True,
            "diagnosis": response.diagnosis,
            "confidence": response.confidence,
            "codes_referenced": response.codes_referenced,
            "manual_pages": response.manual_pages,
            "next_steps": response.next_steps
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear conversation history for fresh start"""
    if not diagnostic_system:
        return jsonify({
            "success": False,
            "error": "Diagnostic system not initialized"
        }), 500

    try:
        diagnostic_system.clear_history()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/knowledge-summary', methods=['GET'])
def knowledge_summary():
    """Get summary of loaded knowledge base"""
    if not diagnostic_system:
        return jsonify({
            "success": False,
            "error": "Diagnostic system not initialized"
        }), 500

    try:
        summary = diagnostic_system.get_knowledge_summary()
        return jsonify({
            "success": True,
            "summary": summary
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==================== VALIDATION ENDPOINTS ====================

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit validation feedback for a query/response

    Request body:
    {
        "query": "string",
        "response": "string",
        "feedback": "correct|incorrect|unsure",
        "confidence": "HIGH|MEDIUM|LOW",
        "notes": "optional notes"
    }
    """
    if not validation_manager:
        return jsonify({
            "success": False,
            "error": "Validation manager not initialized"
        }), 500

    try:
        data = request.get_json()
        query = data.get('query', '')
        response = data.get('response', '')
        feedback = data.get('feedback', '').lower()
        confidence = data.get('confidence', 'MEDIUM')
        notes = data.get('notes', '')

        # Validate feedback value
        if feedback not in ['correct', 'incorrect', 'unsure']:
            return jsonify({
                "success": False,
                "error": "Invalid feedback value. Must be one of: correct, incorrect, unsure"
            }), 400

        # Add feedback
        record = validation_manager.add_feedback(
            query=query,
            response=response,
            feedback=feedback,
            confidence=confidence,
            notes=notes
        )

        return jsonify({
            "success": True,
            "record": record
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/validation/summary', methods=['GET'])
def validation_summary():
    """Get validation summary and statistics"""
    if not validation_manager:
        return jsonify({
            "success": False,
            "error": "Validation manager not initialized"
        }), 500

    try:
        summary = validation_manager.get_summary()
        return jsonify({
            "success": True,
            "summary": summary
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/validation/feedback', methods=['GET'])
def get_validation_feedback():
    """Get all validation feedback

    Query parameters:
    - limit: Maximum number of records (default: all)
    - type: Filter by type (correct, incorrect, unsure)
    """
    if not validation_manager:
        return jsonify({
            "success": False,
            "error": "Validation manager not initialized"
        }), 500

    try:
        limit = request.args.get('limit', type=int)
        feedback_type = request.args.get('type', type=str)

        feedback = validation_manager.get_feedback(
            limit=limit,
            feedback_type=feedback_type
        )

        return jsonify({
            "success": True,
            "feedback": feedback,
            "count": len(feedback)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/validation/export', methods=['GET'])
def export_validation():
    """Export validation data as CSV"""
    if not validation_manager:
        return jsonify({
            "success": False,
            "error": "Validation manager not initialized"
        }), 500

    try:
        csv_data = validation_manager.export_csv()
        return csv_data, 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=validation_feedback.csv'
        }
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


def main():
    """Run the web API server"""
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'

    print(f"\n🛗 ESC Web API Server")
    print(f"{'='*50}")
    print(f"Starting on http://localhost:{port}")
    print(f"Open http://localhost:{port} in your browser")
    print(f"{'='*50}\n")

    app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == '__main__':
    main()
