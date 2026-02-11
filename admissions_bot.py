import json
import re
from datetime import datetime
from eligibility_checker import EligibilityChecker

class UniversityAdmissionsBot:
    def __init__(self, knowledge_base_file='admissions_data.json'):
        """Initialize the chatbot with knowledge base"""
        self.load_knowledge_base(knowledge_base_file)
        self.eligibility_checker = EligibilityChecker()
        self.user_context = {
            'name': None,
            'interest': None,
            'previous_questions': []
        }
        self.welcome_message = """
        🎓 Welcome to the University Admissions Bot!
        
        I'm here to help you with:
        • Admission requirements and procedures
        • Required documents
        • Eligibility criteria
        • Courses and programs
        • Important deadlines
        • Fees and financial aid
        
        Type 'exit' to end the conversation.
        How can I help you today?
        """
    
    def load_knowledge_base(self, filename):
        """Load the knowledge base from JSON file"""
        try:
            with open(filename, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print("Error: Knowledge base file not found. Using default data.")
            # Fallback to hardcoded data if file not found
            self.data = self.get_default_data()
    
    def get_default_data(self):
        """Provide default data if JSON file is missing"""
        return {
            "admissions": {
                "general": {
                    "apply": "You can apply through our online portal. Complete the application form, upload documents, and pay the application fee."
                }
            }
        }
    
    def preprocess_input(self, user_input):
        """Clean and normalize user input"""
        user_input = user_input.lower().strip()
        # Remove special characters
        user_input = re.sub(r'[^\w\s]', '', user_input)
        return user_input
    
    def find_intent(self, user_input):
        """Determine user intent based on keywords"""
        processed_input = self.preprocess_input(user_input)
        words = processed_input.split()
        
        for intent, keywords in self.data['keywords'].items():
            for keyword in keywords:
                if keyword in processed_input or keyword in words:
                    return intent
        return 'unknown'
    
    def generate_response(self, intent, user_input):
        """Generate response based on intent"""
        if intent == 'greetings':
            return "Hello! I'm the University Admissions Bot. How can I assist you with your admission questions today?"
        
        elif intent == 'apply':
            return self.data['admissions']['general']['apply']
        
        elif intent == 'documents':
            # Check for specific document type
            if 'transcript' in user_input.lower():
                return self.data['admissions']['documents']['transcripts']
            elif 'recommendation' in user_input.lower():
                return self.data['admissions']['documents']['recommendation']
            else:
                return self.data['admissions']['documents']['required']
        
        elif intent == 'deadline':
            return self.data['admissions']['general']['deadlines']
        
        elif intent == 'eligibility':
            if 'international' in user_input.lower():
                return self.data['admissions']['eligibility']['international']
            elif 'graduate' in user_input.lower() or 'master' in user_input.lower():
                return self.data['admissions']['eligibility']['graduate']
            else:
                return self.data['admissions']['eligibility']['undergraduate']
        
        elif intent == 'courses':
            if 'engineering' in user_input.lower():
                return self.data['admissions']['courses']['engineering']
            elif 'graduate' in user_input.lower() or 'master' in user_input.lower():
                return self.data['admissions']['courses']['graduate']
            else:
                return self.data['admissions']['courses']['undergraduate']
        
        elif intent == 'fees':
            if 'aid' in user_input.lower() or 'scholarship' in user_input.lower():
                return self.data['admissions']['fees']['financial_aid']
            elif 'application' in user_input.lower():
                return self.data['admissions']['fees']['application']
            else:
                return self.data['admissions']['fees']['tuition']
        
        elif intent == 'international':
            return self.data['admissions']['eligibility']['international'] + "\n\n" + "Additional requirements: Valid passport, student visa, financial documentation, and evaluated transcripts."
        
        elif intent == 'thanks':
            return "You're welcome! Is there anything else I can help you with?"
        
        elif intent == 'exit':
            return "Thank you for using the University Admissions Bot. Good luck with your application! 🎓"
        
        else:
            return "I'm not sure I understand. Could you please rephrase your question? You can ask me about admissions, documents, deadlines, eligibility, courses, or fees."
    
    def check_eligibility_interactive(self):
        """Interactive eligibility checker"""
        print("\n--- Eligibility Checker ---")
        return self.eligibility_checker.check_eligibility()
    
    def run(self):
        """Main chatbot loop"""
        print(self.welcome_message)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    print("Bot: Please type a message.")
                    continue
                
                # Store in context
                self.user_context['previous_questions'].append(user_input)
                
                # Check for exit command
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    print(f"Bot: {self.generate_response('exit', user_input)}")
                    break
                
                # Check for eligibility checker command
                if 'check eligibility' in user_input.lower() or 'am i eligible' in user_input.lower():
                    result = self.check_eligibility_interactive()
                    if result:
                        print(f"Bot: {result}")
                    continue
                
                # Determine intent and generate response
                intent = self.find_intent(user_input)
                response = self.generate_response(intent, user_input)
                
                print(f"Bot: {response}")
                
            except KeyboardInterrupt:
                print("\nBot: Goodbye! Thanks for chatting with us.")
                break
            except Exception as e:
                print(f"Bot: I encountered an error. Please try again. (Error: {e})")

if __name__ == "__main__":
    bot = UniversityAdmissionsBot()
    bot.run()