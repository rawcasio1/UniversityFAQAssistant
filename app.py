from flask import Flask, render_template, request, jsonify
from utils.database import init_db, get_all_faqs, add_faq, update_faq, delete_faq
from utils.matcher import find_best_match

app = Flask(__name__)

# Initialize the database on startup
init_db()

# --- FRONTEND ROUTES ---
@app.route('/')
def home():
    """Renders the main Chatbot Interface for students."""
    return render_template('index.html')

@app.route('/admin')
def admin():
    """Renders the Admin Panel."""
    return render_template('admin.html')

# --- API ROUTES (CHATBOT) ---
@app.route('/api/chat', methods=['POST'])
def chat():
    """Handles incoming student questions and returns the best FAQ match."""
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
        
    response_data = find_best_match(user_message)
    return jsonify(response_data)

# --- API ROUTES (ADMIN CRUD) ---
@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    """Returns all FAQs as JSON."""
    faqs = get_all_faqs()
    return jsonify(faqs)

@app.route('/api/faqs', methods=['POST'])
def create_faq():
    """Adds a new FAQ."""
    data = request.get_json()
    add_faq(data['title'], data['question'], data['answer'], data['keywords'], data['policy_section'])
    return jsonify({"message": "FAQ added successfully"}), 201

@app.route('/api/faqs/<int:faq_id>', methods=['PUT'])
def edit_faq(faq_id):
    """Updates an existing FAQ."""
    data = request.get_json()
    update_faq(faq_id, data['title'], data['question'], data['answer'], data['keywords'], data['policy_section'])
    return jsonify({"message": "FAQ updated successfully"})

@app.route('/api/faqs/<int:faq_id>', methods=['DELETE'])
def remove_faq(faq_id):
    """Deletes an FAQ."""
    delete_faq(faq_id)
    return jsonify({"message": "FAQ deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
    