# 🎓 University Admissions Bot — Project Documentation

## 📌 1. Introduction
The University Admissions Bot is a rule-based chatbot designed to help students get quick and clear information about university admissions, eligibility, and application procedures.

---

## ❓ 2. Problem Statement
Students often struggle to find accurate admission information. University websites can be confusing and time-consuming to navigate. This chatbot provides instant answers in a conversational format.

---

## 🎯 3. Objectives
- Provide admission guidance through chat interaction
- Explain eligibility criteria and required documents
- Help students understand the application process
- Offer important deadline information

---

## 🛠 4. Technologies Used
- Python
- Rule-based Natural Language Processing (keyword matching)
- JSON for knowledge base storage

---

## ⚙️ 5. System Architecture

**User → Chatbot → Keyword Matching → Response from Knowledge Base**

The chatbot reads the user’s question, finds matching keywords, and provides the most relevant admission-related response.

---

## 🧠 6. Modules

### 6.1 Knowledge Base
Stores admission FAQs, requirements, and guidelines in a structured format (`admissions_data.json`).

### 6.2 Chatbot Engine
Processes user input and matches keywords to the correct responses.

### 6.3 Eligibility Checker (Creative Feature)
Allows students to enter their academic percentage and suggests suitable programs.

---

## 💡 7. Key Features
- Admission FAQs
- Document requirement guidance
- Course eligibility information
- Application steps explanation
- Deadline information
- Eligibility suggestion feature

---

## 🚧 8. Limitations
- Not connected to real university databases
- Uses static data
- Does not process real applications

---

## 🔮 9. Future Enhancements
- Web-based interface
- Multi-language support
- Integration with real admission portals
- Voice interaction

---

## 📊 10. Conclusion
The University Admissions Bot simplifies the admission process by providing quick and structured information. It demonstrates how rule-based chatbots can solve real-world information challenges efficiently.

