# Ehtical_medical_chatbot
# CuraAI - Ethical AI-Powered Medical Chatbot

## 👨‍⚕️ Project Title  
**CuraAI: Ethical Challenges and Responsible AI Practices in Medical Chatbots**

## 👤 Developed by  
**K. Mohana Kumar**  
 

---

## 📌 Problem Statement

AI-powered medical chatbots provide symptom-based health guidance. However, without physical or clinical examination, AI conclusions can be misleading and ethically risky. Issues such as **misdiagnosis**, **bias**, **misinformation**, and **psychological impact** raise significant concerns.

This project addresses these challenges by integrating **ethical design principles** and **human-AI collaboration** into a secure, responsible chatbot system.

---

## 📄 Abstract

CuraAI is a responsible AI chatbot designed to assist in medical symptom analysis while respecting ethical boundaries. It uses the **GROQ API** for NLP responses, implements **session-based data privacy**, and ensures **accountability** through disclaimers, bias mitigation, and escalation to human doctors when needed.

---

## 🎯 Objectives

- Ensure session-based, privacy-compliant data handling.  
- Implement disclaimers clarifying the chatbot’s advisory role.  
- Introduce human escalation for high-risk or unsatisfied cases.  
- Reduce algorithmic bias by training on diverse datasets.  
- Support continuous learning via real-time feedback loops.

---

## 🔍 Methodology

1. **Research:** Analyze existing AI medical systems and identify ethical shortcomings.  
2. **Framework Development:** Design ethical and transparent AI flow.  
3. **Implementation:** Integrate GROQ API, FastAPI backend, and session-based security.  
4. **Evaluation:** Collect feedback from experts and users for iterative improvement.  
5. **Deployment:** Document and present results alongside ethical compliance guidelines.

---

## 🧰 Technologies Used

| Component            | Technology                             |
|----------------------|--------------------------------------|
| Frontend (UI)        | React / HTML-CSS                     |
| Backend/API          | Python with FastAPI                   |
| NLP Engine           | GROQ API                            |
| Data Privacy         | Session-based temporary storage       |
| Deployment           | Uvicorn, GitHub                      |
| Feedback Analysis    | Custom logic + logging                |
| Human Escalation     | FastAPI-based routing to doctor module|

---

## 🧱 System Architecture (Simplified Flow)

```text
User Interface --> Session Manager --> Chatbot Interaction -->
AI Processing (GROQ API + Ethical Rules) --> Response Generator
                |                                    |
                v                                    v
     Human Escalation Module <--- User Not Satisfied/Low Confidence
                |
                v
     Doctor Connect (Secure Channel)
🧩 Modules Overview
User Interaction Module

AI Processing Module (GROQ NLP)

Session-Based Security Module

Human Escalation Module

Feedback and Learning Module

✅ Key Ethical Design Elements
🔒 Session-only data retention (no long-term storage)

🧠 Bias-aware AI training

⚠️ Transparent disclaimers and limitations

🤝 Doctor fallback for critical/sensitive queries

📈 Continuous learning via real-time feedback

🧪 Results and Discussion
Improved user trust through transparency

Effective human-AI collaboration in escalated cases

Reduced bias across gender and ethnicity

Ensured accountability through clear disclaimers

Prevented premature diagnosis via symptom thresholding

🔮 Future Scope
Add multilingual support for rural accessibility

Introduce emotion detection and sentiment analysis

Integrate securely with hospital EMRs

Enable self-assessment history tracking

Adopt federated learning for privacy-preserving AI training

📅 Timeline
Refer to the final project report for detailed timeline.

📸 Screenshots
Included in the project PDF.

📂 Project Structure
arduino
Copy
Edit
CuraAI/
├── main.py
├── modules/
│   ├── chatbot.py
│   ├── escalation.py
│   └── ethics.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── .env
├── requirements.txt
└── README.md
🚀 How to Clone and Run the Project
📦 Prerequisites
Python 3.8 or higher

Git

A code editor (e.g., VS Code)

Internet connection to access GROQ API

🔁 Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/CuraAI.git
cd CuraAI
(Replace your-username with your GitHub username if applicable)

⚙️ Set Up the Environment
Create and activate a virtual environment (recommended):

bash
Copy
Edit
python -m venv venv
source venv/bin/activate       # On Linux/macOS
venv\Scripts\activate.bat      # On Windows
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
🔑 Add GROQ API Key
Create a .env file in the project root with:

ini
Copy
Edit
GROQ_API_KEY=your_actual_api_key_here
▶️ Run the Application
bash
Copy
Edit
uvicorn main:app --reload
Open your browser and navigate to:
http://127.0.0.1:8000

💬 Test the Chatbot
Use the /chat route or the frontend UI to interact with the chatbot. Alternatively, test via Postman or similar tools.

🧾 License
This project is for academic and educational purposes only.


