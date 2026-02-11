class EligibilityChecker:
    """Enhanced eligibility checker for web interface"""
    
    def __init__(self):
        self.programs = {
            'undergraduate': {
                'Computer Science': {'gpa': 3.0, 'sat': 1200, 'act': 25},
                'Business Administration': {'gpa': 2.8, 'sat': 1100, 'act': 23},
                'Engineering': {'gpa': 3.2, 'sat': 1250, 'act': 26},
                'Psychology': {'gpa': 2.7, 'sat': 1050, 'act': 22},
                'Biology': {'gpa': 3.0, 'sat': 1150, 'act': 24},
                'Economics': {'gpa': 2.9, 'sat': 1120, 'act': 23}
            },
            'graduate': {
                'MBA': {'gpa': 3.0, 'gmat': 600, 'gre': 310},
                'MS in Computer Science': {'gpa': 3.2, 'gre': 315},
                'MS in Engineering': {'gpa': 3.1, 'gre': 310},
                'MA in Psychology': {'gpa': 3.0, 'gre': 305},
                'MPH': {'gpa': 3.0, 'gre': 300}
            }
        }
    
    def check_eligibility_api(self, data):
        """API endpoint for eligibility checking"""
        try:
            level = data.get('level', '').lower()
            gpa = float(data.get('gpa', 0))
            test_type = data.get('test_type', '').lower()
            test_score = int(data.get('test_score', 0))
            
            # Validate inputs
            if gpa < 0 or gpa > 4.0:
                return {'error': 'GPA must be between 0.0 and 4.0'}
            
            if level in ['ug', 'undergraduate']:
                return self.check_undergraduate(gpa, test_type, test_score)
            elif level in ['g', 'graduate']:
                return self.check_graduate(gpa, test_type, test_score)
            else:
                return {'error': 'Please select undergraduate or graduate'}
                
        except ValueError:
            return {'error': 'Please enter valid numbers'}
        except Exception as e:
            return {'error': str(e)}
    
    def check_undergraduate(self, gpa, test_type, test_score):
        """Check undergraduate eligibility"""
        eligible = []
        not_eligible = []
        
        for program, req in self.programs['undergraduate'].items():
            if gpa >= req['gpa']:
                if test_type == 'sat' and test_score >= req['sat']:
                    eligible.append(program)
                elif test_type == 'act' and test_score >= req['act']:
                    eligible.append(program)
                else:
                    not_eligible.append(program)
            else:
                not_eligible.append(program)
        
        return self.format_results(eligible, not_eligible, 'undergraduate')
    
    def check_graduate(self, gpa, test_type, test_score):
        """Check graduate eligibility"""
        eligible = []
        not_eligible = []
        
        for program, req in self.programs['graduate'].items():
            if gpa >= req['gpa']:
                if test_type == 'gre' and test_score >= req.get('gre', 0):
                    eligible.append(program)
                elif test_type == 'gmat' and test_score >= req.get('gmat', 0):
                    eligible.append(program)
                else:
                    not_eligible.append(program)
            else:
                not_eligible.append(program)
        
        return self.format_results(eligible, not_eligible, 'graduate')
    
    def format_results(self, eligible, not_eligible, level):
        """Format eligibility results"""
        if eligible:
            message = f"✅ You are eligible for: {', '.join(eligible)}"
            if not_eligible:
                message += f"\n\n❌ Not eligible for: {', '.join(not_eligible[:3])}"
                if len(not_eligible) > 3:
                    message += f" and {len(not_eligible)-3} more"
        else:
            message = "📝 Based on your current scores, you are not eligible for our programs. Consider retaking exams or improving your GPA."
            
            # Add suggestions
            suggestions = []
            if gpa_improvement_needed:
                suggestions.append("improve your GPA")
            if test_improvement_needed:
                suggestions.append(f"retake the {test_type.upper()} exam")
            
            if suggestions:
                message += f"\n\n💡 Suggestions: {', '.join(suggestions)}."
        
        return {'message': message, 'eligible': eligible, 'not_eligible': not_eligible}