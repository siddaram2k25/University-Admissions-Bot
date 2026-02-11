from flask import Flask, render_template, request, jsonify, session
import json
import re
from datetime import datetime
from eligibility_checker import EligibilityChecker
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # For session management

class UniversityAdmissionsBot:
    def __init__(self, knowledge_base_file='admissions_data.json'):
        self.load_knowledge_base(knowledge_base_file)
        self.eligibility_checker = EligibilityChecker()
    
    def load_knowledge_base(self, filename):
        try:
            with open(filename, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = self.get_default_data()
    
    def get_default_data(self):
        return {
            "admissions": {
                "general": {
                    "apply": "You can apply through our online portal. Complete the application form, upload documents, and pay the application fee.",
                    "deadlines": "Fall 2024: Early Decision - Nov 1, 2023, Regular Decision - Jan 15, 2024. Spring 2024: Nov 15, 2023."
                },
                "documents": {
                    "required": "Required documents: Application form, Official transcripts, Test scores (SAT/ACT), English proficiency scores, 2-3 letters of recommendation, Personal statement, Resume, Passport copy (international)."
                },
                "eligibility": {
                    "undergraduate": "Undergraduate: High school graduate, 2.5+ GPA, SAT 1000+ or ACT 20+, TOEFL 80+ or IELTS 6.5+."
                },
                "courses": {
                    "undergraduate": "Undergraduate programs: Computer Science, Business, Psychology, Biology, Engineering, English, Economics."
                }
            },
            "keywords": {
                "apply": ["apply", "application", "admission", "how to"],
                "documents": ["document", "transcript", "letter", "certificate"],
                "deadline": ["deadline", "date", "last date", "when"],
                "eligibility": ["eligible", "eligibility", "qualify", "requirements"],
                "courses": ["course", "program", "major", "degree"],
                "greetings": ["hello", "hi", "hey"],
                "thanks": ["thank", "thanks"],
                "exit": ["bye", "goodbye"]
            }
        }
    
    def preprocess_input(self, user_input):
        user_input = user_input.lower().strip()
        user_input = re.sub(r'[^\w\s]', '', user_input)
        return user_input
    
    def find_intent(self, user_input):
        processed_input = self.preprocess_input(user_input)
        words = processed_input.split()
        
        for intent, keywords in self.data['keywords'].items():
            for keyword in keywords:
                if keyword in processed_input or keyword in words:
                    return intent
        return 'unknown'
    
    def generate_response(self, intent, user_input):
        if intent == 'greetings':
            return "Hello! I'm the University Admissions Bot. How can I help you with your admission questions today?"
        
        elif intent == 'apply':
            return self.data['admissions']['general']['apply']
        
        elif intent == 'documents':
            return self.data['admissions']['documents']['required']
        
        elif intent == 'deadline':
            return self.data['admissions']['general']['deadlines']
        
        elif intent == 'eligibility':
            return self.data['admissions']['eligibility']['undergraduate']
        
        elif intent == 'courses':
            return self.data['admissions']['courses']['undergraduate']
        
        elif intent == 'thanks':
            return "You're welcome! Is there anything else I can help you with?"
        
        elif intent == 'exit':
            return "Thank you for using the University Admissions Bot. Good luck with your application! 🎓"
        
        else:
            return "I'm not sure I understand. You can ask me about admissions, documents, deadlines, eligibility, courses, or try our eligibility checker!"
    
    def check_eligibility_api(self, data):
        """API endpoint for eligibility checking"""
        try:
            education_level = data.get('level', '').lower()
            
            if education_level in ['ug', 'undergraduate']:
                return self.check_undergraduate_eligibility_api(data)
            elif education_level in ['g', 'graduate']:
                return self.check_graduate_eligibility_api(data)
            else:
                return {"status": "error", "message": "Please specify undergraduate or graduate."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def check_undergraduate_eligibility_api(self, data):
        try:
            gpa = float(data.get('gpa', 0))
            test_type = data.get('test_type', '').lower()
            test_score = int(data.get('test_score', 0))
            
            if gpa > 4.0 or gpa < 0:
                return {"status": "error", "message": "Invalid GPA. Please enter a value between 0.0 and 4.0."}
            
            eligible_programs = []
            programs = {
                'Computer Science': {'gpa': 3.0, 'sat': 1200, 'act': 25},
                'Business Administration': {'gpa': 2.8, 'sat': 1100, 'act': 23},
                'Engineering': {'gpa': 3.2, 'sat': 1250, 'act': 26},
                'Psychology': {'gpa': 2.7, 'sat': 1050, 'act': 22}
            }
            
            for prog_name, requirements in programs.items():
                if gpa >= requirements['gpa']:
                    if test_type == 'sat' and test_score >= requirements['sat']:
                        eligible_programs.append(prog_name)
                    elif test_type == 'act' and test_score >= requirements['act']:
                        eligible_programs.append(prog_name)
            
            if eligible_programs:
                return {
                    "status": "success", 
                    "eligible": True,
                    "programs": eligible_programs,
                    "message": f"✅ You are eligible for: {', '.join(eligible_programs)}"
                }
            else:
                return {
                    "status": "success",
                    "eligible": False,
                    "message": "📝 Based on your current scores, you may need to improve your GPA or test scores."
                }
                
        except ValueError:
            return {"status": "error", "message": "Please enter valid numerical values."}
    
    def check_graduate_eligibility_api(self, data):
        try:
            gpa = float(data.get('gpa', 0))
            test_type = data.get('test_type', '').lower()
            test_score = int(data.get('test_score', 0))
            
            if gpa > 4.0 or gpa < 0:
                return {"status": "error", "message": "Invalid GPA. Please enter a value between 0.0 and 4.0."}
            
            eligible_programs = []
            programs = {
                'MBA': {'gpa': 3.0, 'gmat': 600, 'gre': 310},
                'MS in Computer Science': {'gpa': 3.2, 'gre': 315},
                'MS in Engineering': {'gpa': 3.1, 'gre': 310}
            }
            
            for prog_name, requirements in programs.items():
                if gpa >= requirements['gpa']:
                    if test_type == 'gre' and test_score >= requirements.get('gre', 0):
                        eligible_programs.append(prog_name)
                    elif test_type == 'gmat' and test_score >= requirements.get('gmat', 0):
                        eligible_programs.append(prog_name)
            
            if eligible_programs:
                return {
                    "status": "success",
                    "eligible": True,
                    "programs": eligible_programs,
                    "message": f"✅ You are eligible for: {', '.join(eligible_programs)}"
                }
            else:
                return {
                    "status": "success",
                    "eligible": False,
                    "message": "📝 Your scores don't meet the minimum requirements for our graduate programs."
                }
                
        except ValueError:
            return {"status": "error", "message": "Please enter valid numerical values."}

# Initialize the bot
bot = UniversityAdmissionsBot()

@app.route('/')
def home():
    """Render the chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        # Store conversation in session
        if 'conversation' not in session:
            session['conversation'] = []
        
        session['conversation'].append({'user': user_message, 'timestamp': datetime.now().isoformat()})
        
        # Check if user wants to check eligibility
        if 'check eligibility' in user_message.lower() or 'am i eligible' in user_message.lower():
            return jsonify({
                'response': "Let's check your eligibility! Please fill out the eligibility checker form below.",
                'show_eligibility_form': True
            })
        
        # Generate bot response
        intent = bot.find_intent(user_message)
        response = bot.generate_response(intent, user_message)
        
        session['conversation'].append({'bot': response, 'timestamp': datetime.now().isoformat()})
        
        return jsonify({
            'response': response,
            'show_eligibility_form': False
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/check-eligibility', methods=['POST'])
def check_eligibility():
    """Handle eligibility check requests"""
    try:
        data = request.json
        result = bot.check_eligibility_api(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset_conversation():
    """Reset the conversation"""
    session.clear()
    return jsonify({'status': 'success', 'message': 'Conversation reset'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)