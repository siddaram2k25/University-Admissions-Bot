import unittest
from admissions_bot import UniversityAdmissionsBot
from eligibility_checker import EligibilityChecker

class TestAdmissionsBot(unittest.TestCase):
    def setUp(self):
        self.bot = UniversityAdmissionsBot('admissions_data.json')
    
    def test_intent_recognition(self):
        self.assertEqual(self.bot.find_intent("How do I apply?"), 'apply')
        self.assertEqual(self.bot.find_intent("What documents do I need?"), 'documents')
        self.assertEqual(self.bot.find_intent("When is the deadline?"), 'deadline')
    
    def test_response_generation(self):
        response = self.bot.generate_response('apply', '')
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)

if __name__ == '__main__':
    unittest.main()