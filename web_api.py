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
    global KNOWLEDGE_BASE
    try:
        with open('knowledge.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            KNOWLEDGE_BASE = data
            print(f"✓ Knowledge base loaded: {len(data)} entries")
            return data
    except Exception as e:
        print(f"✗ Error loading knowledge base: {e}")
        return []

def get_knowledge_summary():
    """Get a summary of the knowledge base"""
    if not KNOWLEDGE_BASE:
        return {"total": 0, "error_codes": 0, "parameters": 0, "components": 0}

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
    """Format the knowledge base for Claude's context"""
    if not KNOWLEDGE_BASE:
        return "Knowledge base not loaded."

    formatted = "# Via Series Elevator Knowledge Base\n\n"

    # Group by type
    errors = [item for item in KNOWLEDGE_BASE if item.get('type') == 'error']
    params = [item for item in KNOWLEDGE_BASE if item.get('type') == 'parameter']
    components = [item for item in KNOWLEDGE_BASE if item.get('type') == 'component']

    if errors:
        formatted += "## Error Codes\n"
        for item in errors:
            formatted += f"\n### {item['code']}\n"
            formatted += f"- Description: {item['description']}\n"
            if item.get('manual_page'):
                formatted += f"- Manual Page: {item['manual_page']}\n"

    if params:
        formatted += "\n## Parameters\n"
        for item in params:
            formatted += f"\n### {item['code']}\n"
            formatted += f"- Description: {item['description']}\n"
            if item.get('manual_page'):
                formatted += f"- Manual Page: {item['manual_page']}\n"

    if components:
        formatted += "\n## Hardware Components\n"
        for item in components:
            formatted += f"\n### {item['code']}\n"
            formatted += f"- Description: {item['description']}\n"

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
        client = anthropic.Anthropic(api_key=api_key)

        knowledge_context = format_knowledge_for_claude()

        system_prompt = """You are an expert elevator service technician assistant for Via Series elevators.
You have access to a comprehensive knowledge base with error codes, parameters, and hardware components.

Your role is to:
1. Provide accurate technical diagnostics based on the knowledge base
2. Reference specific error codes, parameters, or components when relevant
3. Suggest manual page numbers for detailed information
4. Respond in GERMAN language
5. Be concise but thorough

When answering:
- If asked about an error code, explain what it means and possible causes
- If asked about a component, explain its function and location
- If asked about a parameter, explain its purpose and typical values
- Always reference the relevant manual pages when available

Respond with a confidence level:
- HIGH: Information directly from knowledge base
- MEDIUM: Inferred from related knowledge
- LOW: General elevator knowledge, not specific to this system
"""

        user_prompt = f"""User Question: {question}

Available Knowledge Base:
{knowledge_context}

Please provide a helpful diagnostic response in German. Include:
1. Direct answer to the question
2. Referenced codes (if any)
3. Relevant manual pages (if any)
4. Your confidence level"""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
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
        for item in KNOWLEDGE_BASE:
            if item['code'].upper() in response_text.upper():
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

# Routes
@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/knowledge.json')
def knowledge_json():
    """Serve the knowledge base JSON"""
    return send_from_directory('.', 'knowledge.json')

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
    return jsonify({
        "status": "healthy",
        "knowledge_loaded": KNOWLEDGE_BASE is not None,
        "entries": len(KNOWLEDGE_BASE) if KNOWLEDGE_BASE else 0
    })

# Initialize
if __name__ == '__main__':
    print("=" * 60)
    print("ESC - Elevator Service Companion API Server")
    print("=" * 60)

    # Load knowledge base
    load_knowledge_base()

    # Check for API key
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("\n⚠️  WARNING: ANTHROPIC_API_KEY not set!")
        print("   Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        print("   Or configure it in Railway environment variables\n")
    else:
        print("✓ ANTHROPIC_API_KEY configured")

    print("\n🚀 Server starting...")
    print("   Local: http://localhost:8080")
    print("   Railway: Will use $PORT environment variable")
    print("=" * 60 + "\n")

    # Use PORT from environment (Railway sets this automatically)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
