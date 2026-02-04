# 🎓 Graduation Project Checker (PDF/DOCX)

Graduation Project Checker is a web-based application designed to help students verify whether their graduation project documentation meets the official university template and requirements.

The system allows users to upload their project file in **PDF or Word (DOCX)** format and automatically performs structural and technical checks, providing clear feedback and improvement suggestions.

---

## 🚀 Features

- Upload graduation project files (PDF / DOCX)
- Automatic compliance checking based on the official template
- Clear compliance score
- Project idea summary extraction
- Detection of missing or incomplete chapters
- Practical fix suggestions for each issue
- DOCX formatting checks
- Downloadable evaluation report (JSON)
- Simple and user-friendly web interface

---

## 🧠 System Overview

The application uses a **rule-based evaluation engine** to ensure stable and reproducible results.  
An AI-based feedback module is designed as an optional extension and can be enabled in future versions when API access is guaranteed.

---

## 🛠️ Technologies Used

- Python 3.10+
- Streamlit
- PDF & DOCX processing libraries
- Rule-based validation logic

---

## ▶️ How to Run Locally

1. Clone the repository:
```bash
git clone https://github.com/alzoubitoqa/Graduation-Project-Checker---stable-version.git
cd grad-checker-chatbot
Create and activate virtual environment:

python -m venv .venv
.venv\Scripts\activate
Install dependencies:

pip install -r requirements.txt
Run the application:

streamlit run app.py
🌐 Deployment
The application can be deployed publicly using Streamlit Community Cloud, allowing evaluators to access the system through a public link without any local setup.
⚠️ Limitations

The current version uses rule-based evaluation only.

AI-based feedback is disabled in the stable version to ensure reliability.

Formatting checks are available for DOCX files only.

📄 License

This project is licensed under the MIT License.

👩‍💻 Author

Toqa Alzoubi
Graduation Project – Stable Version


