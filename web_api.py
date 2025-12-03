#!/usr/bin/env python3
"""
ESC (Elevator Service Companion) - Backend API
Flask server with Claude AI integration for intelligent elevator diagnostics
"""

import os
import json
import anthropic
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__, static_folder='.')
CORS(app)

# Load knowledge base
KNOWLEDGE_BASE = None
FEEDBACK_FILE = 'feedback.json'

def load_knowledge_base():
    """Load the knowledge base from JSON file"""
    import sys
    global KNOWLEDGE_BASE
    try:
        # Use absolute path based on script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        knowledge_path = os.path.join(script_dir, 'knowledge.json')
        print(f"[LOADING] Attempting to load from: {knowledge_path}", file=sys.stderr, flush=True)
        with open(knowledge_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            KNOWLEDGE_BASE = data

            # Count actual entries
            total = 0
            if isinstance(data, dict):
                total = (len(data.get('error_codes', [])) +
                        len(data.get('parameters', [])) +
                        len(data.get('abbreviations', [])))
            else:
                total = len(data)

            print(f"✓ Knowledge base loaded: {total} entries", file=sys.stderr, flush=True)
            return data
    except Exception as e:
        print(f"✗ Error loading knowledge base: {e}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {}

def get_knowledge_summary():
    """Get a summary of the knowledge base"""
    if not KNOWLEDGE_BASE:
        return {"total": 0, "error_codes": 0, "parameters": 0, "components": 0}

    # Handle nested structure
    if isinstance(KNOWLEDGE_BASE, dict):
        error_codes = len(KNOWLEDGE_BASE.get('error_codes', []))
        parameters = len(KNOWLEDGE_BASE.get('parameters', []))
        components = len(KNOWLEDGE_BASE.get('abbreviations', []))

        return {
            "total": error_codes + parameters + components,
            "error_codes": error_codes,
            "parameters": parameters,
            "components": components
        }

    # Fallback for flat structure
    error_codes = sum(1 for item in KNOWLEDGE_BASE if item.get('type') == 'error')
    parameters = sum(1 for item in KNOWLEDGE_BASE if item.get('type') == 'parameter')
    components = sum(1 for item in KNOWLEDGE_BASE if item.get('type') == 'component')

    return {
        "total": len(KNOWLEDGE_BASE),
        "error_codes": error_codes,
        "parameters": parameters,
        "components": components
    }

def format_knowledge_for_claude():
    """Format the knowledge base for Claude's context - COMPACT VERSION"""
    if not KNOWLEDGE_BASE:
        return "Knowledge base not loaded."

    formatted = "# Via Series Elevator Knowledge Base (Summary)\n\n"

    # Handle nested structure
    if isinstance(KNOWLEDGE_BASE, dict):
        errors = KNOWLEDGE_BASE.get('error_codes', [])
        params = KNOWLEDGE_BASE.get('parameters', [])
        components = KNOWLEDGE_BASE.get('abbreviations', [])
    else:
        # Fallback for flat structure
        errors = [item for item in KNOWLEDGE_BASE if item.get('type') == 'error']
        params = [item for item in KNOWLEDGE_BASE if item.get('type') == 'parameter']
        components = [item for item in KNOWLEDGE_BASE if item.get('type') == 'component']

    # Only include summary counts and sample entries to avoid stack overflow
    formatted += f"## Available Data\n"
    formatted += f"- {len(errors)} Error Codes (F01 02 to F11 13)\n"
    formatted += f"- {len(params)} Parameters (P0001 to P0015)\n"
    formatted += f"- {len(components)} Hardware Components/Abbreviations\n\n"

    formatted += "## Sample Error Codes\n"
    for item in errors[:5]:  # Only first 5
        formatted += f"- {item.get('code')}: {item.get('description_de', '')[:80]}...\n"

    formatted += "\n## Sample Components\n"
    for item in components[:10]:  # Only first 10
        formatted += f"- {item.get('code')}: {item.get('description_de', '')[:60]}...\n"

    formatted += "\n**Note**: Search the full knowledge base for specific codes when needed."

    return formatted

def query_claude(question):
    """Query Claude AI with the user's question"""
    api_key = os.environ.get('ANTHROPIC_API_KEY')

    if not api_key:
        return {
            "success": False,
            "error": "ANTHROPIC_API_KEY not configured. Please set it in Railway environment variables."
        }

    try:
        # Initialize Anthropic client with explicit parameters only
        import sys
        print(f"[CLAUDE] Initializing Anthropic client...", file=sys.stderr, flush=True)
        print(f"[CLAUDE] API Key present: {bool(api_key)}, Length: {len(api_key) if api_key else 0}, Starts with: {api_key[:15] if api_key else 'N/A'}...", file=sys.stderr, flush=True)

        try:
            client = anthropic.Anthropic(api_key=api_key)
            print(f"[CLAUDE] Client initialized successfully", file=sys.stderr, flush=True)
        except TypeError as te:
            print(f"[CLAUDE] TypeError during client init: {te}", file=sys.stderr, flush=True)
            # Fallback: try without any proxy settings
            import os as _os
            # Remove proxy env vars if they exist
            for key in list(_os.environ.keys()):
                if 'PROXY' in key.upper():
                    print(f"[CLAUDE] Removing env var: {key}", file=sys.stderr, flush=True)
                    del _os.environ[key]
            client = anthropic.Anthropic(api_key=api_key)
            print(f"[CLAUDE] Client initialized after removing proxy vars", file=sys.stderr, flush=True)

        # Search for relevant entries in knowledge base based on question
        relevant_entries = []
        question_upper = question.upper()

        if isinstance(KNOWLEDGE_BASE, dict):
            all_items = (KNOWLEDGE_BASE.get('error_codes', []) +
                        KNOWLEDGE_BASE.get('parameters', []) +
                        KNOWLEDGE_BASE.get('abbreviations', []))
        else:
            all_items = KNOWLEDGE_BASE

        # Find relevant entries
        for item in all_items:
            code = item.get('code', '')
            desc = item.get('description_de', item.get('description', ''))
            if code.upper() in question_upper or any(word in desc.upper() for word in question_upper.split() if len(word) > 3):
                relevant_entries.append(item)
                if len(relevant_entries) >= 10:  # Limit to 10 most relevant
                    break

        # Format relevant entries
        knowledge_context = "# Relevant Knowledge Base Entries\n\n"
        for item in relevant_entries:
            knowledge_context += f"**{item.get('code')}**: {item.get('description_de', item.get('description', ''))}\n"
            if item.get('cause_solution'):
                knowledge_context += f"  Ursache/Lösung: {item['cause_solution']}\n"
            if item.get('manual_page'):
                knowledge_context += f"  Handbuchseite: {item['manual_page']}\n"
            knowledge_context += "\n"

        if not relevant_entries:
            knowledge_context = format_knowledge_for_claude()

        system_prompt = """You are an expert elevator service technician assistant for Via Series elevators.

Your role is to:
1. Provide accurate technical diagnostics based on the provided knowledge base entries
2. Reference specific error codes, parameters, or components when relevant
3. Respond in GERMAN language
4. Be concise but thorough

Confidence level:
- HIGH: Information directly from knowledge base
- MEDIUM: Inferred from related knowledge
- LOW: General elevator knowledge"""

        user_prompt = f"""Frage: {question}

Wissensbasis:
{knowledge_context}

Bitte antworte auf Deutsch mit:
1. Direkte Antwort
2. Referenzierte Codes
3. Handbuchseiten (falls vorhanden)
4. Konfidenz-Level"""

        # Use the latest Sonnet 4.5 model
        model_to_use = "claude-sonnet-4-5-20250929"  # Latest Sonnet 4.5

        message = client.messages.create(
            model=model_to_use,
            max_tokens=2000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )

        response_text = message.content[0].text

        # Parse confidence level from response
        confidence = "MEDIUM"
        if "HIGH" in response_text.upper() or "hoch" in response_text.lower():
            confidence = "HIGH"
        elif "LOW" in response_text.upper() or "niedrig" in response_text.lower():
            confidence = "LOW"

        # Extract referenced codes (simple heuristic)
        codes_referenced = []
        if isinstance(KNOWLEDGE_BASE, dict):
            # Handle nested structure
            all_items = (KNOWLEDGE_BASE.get('error_codes', []) +
                        KNOWLEDGE_BASE.get('parameters', []) +
                        KNOWLEDGE_BASE.get('abbreviations', []))
        else:
            all_items = KNOWLEDGE_BASE

        for item in all_items:
            if item.get('code', '').upper() in response_text.upper():
                codes_referenced.append(item['code'])

        # Extract manual pages
        manual_pages = []
        import re
        page_matches = re.findall(r'Seite\s+(\d+)', response_text, re.IGNORECASE)
        page_matches += re.findall(r'page\s+(\d+)', response_text, re.IGNORECASE)
        manual_pages = list(set(page_matches))

        return {
            "success": True,
            "diagnosis": response_text,
            "confidence": confidence,
            "codes_referenced": codes_referenced[:5],  # Limit to 5
            "manual_pages": manual_pages[:5]  # Limit to 5
        }

    except anthropic.APIError as e:
        return {
            "success": False,
            "error": f"Claude API error: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }

def save_feedback(feedback_data):
    """Save user feedback to a JSON file"""
    try:
        # Load existing feedback
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
                feedback_list = json.load(f)
        else:
            feedback_list = []

        # Add timestamp
        feedback_data['timestamp'] = datetime.utcnow().isoformat()

        # Append new feedback
        feedback_list.append(feedback_data)

        # Save back to file
        with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
            json.dump(feedback_list, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"Error saving feedback: {e}")
        return False

# API Routes (defined first for priority)
@app.route('/api/knowledge-summary', methods=['GET'])
def api_knowledge_summary():
    """Get knowledge base summary"""
    summary = get_knowledge_summary()
    return jsonify({
        "success": True,
        "summary": summary
    })

@app.route('/api/query', methods=['POST'])
def api_query():
    """Process a diagnostic query using Claude AI"""
    data = request.get_json()

    if not data or 'question' not in data:
        return jsonify({
            "success": False,
            "error": "Missing 'question' parameter"
        }), 400

    question = data['question']

    # Query Claude
    result = query_claude(question)

    return jsonify(result)

@app.route('/api/feedback', methods=['POST'])
def api_feedback():
    """Save user feedback"""
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400

    required_fields = ['query', 'response', 'feedback', 'confidence']
    for field in required_fields:
        if field not in data:
            return jsonify({
                "success": False,
                "error": f"Missing required field: {field}"
            }), 400

    success = save_feedback(data)

    if success:
        return jsonify({"success": True})
    else:
        return jsonify({
            "success": False,
            "error": "Failed to save feedback"
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    # Calculate total entries for nested structure
    entries = 0
    if KNOWLEDGE_BASE:
        if isinstance(KNOWLEDGE_BASE, dict):
            entries = (len(KNOWLEDGE_BASE.get('error_codes', [])) +
                      len(KNOWLEDGE_BASE.get('parameters', [])) +
                      len(KNOWLEDGE_BASE.get('abbreviations', [])))
        else:
            entries = len(KNOWLEDGE_BASE)

    return jsonify({
        "status": "healthy",
        "knowledge_loaded": KNOWLEDGE_BASE is not None,
        "entries": entries
    })

# Static file routes
@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/knowledge.json')
def knowledge_json():
    """Serve the knowledge base JSON"""
    return send_from_directory('.', 'knowledge.json')

# Initialize - Load knowledge base on startup (works with gunicorn)
import sys
print("=" * 60, file=sys.stderr, flush=True)
print("ESC - Elevator Service Companion API Server", file=sys.stderr, flush=True)
print("=" * 60, file=sys.stderr, flush=True)
load_knowledge_base()

if not os.environ.get('ANTHROPIC_API_KEY'):
    print("\n⚠️  WARNING: ANTHROPIC_API_KEY not set!", file=sys.stderr, flush=True)
    print("   Set it with: export ANTHROPIC_API_KEY='your-key-here'", file=sys.stderr, flush=True)
else:
    print("✓ ANTHROPIC_API_KEY configured", file=sys.stderr, flush=True)

print("🚀 Server ready", file=sys.stderr, flush=True)
print("=" * 60 + "\n", file=sys.stderr, flush=True)

# Development server (only when run directly with python)
if __name__ == '__main__':
    print("\n🚀 Starting development server...")
    print("   Local: http://localhost:8080")
    print("   Railway: Will use $PORT environment variable")
    print("=" * 60 + "\n")

    # Use PORT from environment (Railway sets this automatically)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
