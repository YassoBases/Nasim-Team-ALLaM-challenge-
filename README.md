# Nasim - Arabic Medical Assistant

Nasim is an AI-powered Arabic-language medical assistant built on the ALLaM model, designed to provide culturally relevant and accurate healthcare support for Arabic-speaking users. It serves as a 24/7 virtual healthcare guide, offering advice on topics ranging from initial diagnoses to mental health, pregnancy, drug interactions, and more. Nasim is built to empower users with quick, reliable, and evidence-based health information in Arabic.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [API Integration](#api-integration)
- [Testing Nasim](#testing-nasim)
- [Contributing](#contributing)
- [Contact](#contact)

---

## Features

- **Initial Diagnoses**: Provides initial assessments based on symptoms and engages in follow-up questions to increase diagnostic accuracy.
- **Drug and Food Interactions**: Offers guidance on safe drug combinations and interactions with specific foods.
- **Mental Health Support**: Offers support and resources for mental health, encouraging healthy coping strategies.
- **Pregnancy Advice**: Provides tailored guidance for expectant mothers, addressing pregnancy-safe practices and common questions.
- **Chronic Disease Management**: Assists users in managing chronic diseases, offering advice on lifestyle adjustments and medication adherence.
- **Dermatology**: Provides advice on common skin issues like acne, dryness, and sensitivity.
- **Exercise and Nutrition**: Recommends fitness and dietary practices for various health goals.
- **Emergency Procedures and Alerts**: Offers basic first aid steps and critical response guidance for urgent health issues.
- **General Medical Information**: Answers common health questions and provides educational information on various health topics.
- **Tracking Medication**: Helps users schedule and remember their medication timings.
- **Food-Drug Checker**: Identifies potential food interactions with specific medications.
- **Voice Interaction**: Provides a user-friendly, conversational interface.
- **Emergency Health Alerts**: Delivers alerts on urgent health risks or conditions.

---

## Installation

To run Nasim locally or deploy it on a server, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/username/Nasim.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd Nasim
   ```
3. **Install Dependencies**:
   Ensure you have Python 3.x installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory.
   - Add your ALLaM model API key and any other required configurations.

5. **Run the Application**:
   ```bash
   python app.py
   ```

---

## Usage

Once Nasim is running, you can interact with the AI through a web interface or directly via API calls.

1. **Web Interface**:
   - Open your browser and navigate to `http://localhost:5000` (or the specified port).
   - Use the different modules to ask Nasim health-related questions in Arabic.

2. **API Access**:
   - Endpoints are available for each module. Check the [API Documentation](#api-integration) for details on available endpoints and example requests.

---

## Project Structure

```
Nasim/
├── src/                     # Source code files
│   ├── modules/             # Individual modules for each feature
│   ├── templates/           # HTML templates for web interface
│   ├── static/              # Static files like CSS, images
│   └── app.py               # Main application file
├── tests/                   # Test cases for each module
├── requirements.txt         # Python dependencies
└── README.md                # Project README file
```

---

## Technologies Used

- **ALLaM Model**: Arabic Large Language Model for natural language processing in Arabic.
- **Python**: Main programming language.
- **Flask**: Lightweight web framework for building the web interface.
- **HTML, CSS, JavaScript**: Front-end technologies for the user interface.
- **RAG (Retrieval-Augmented Generation)**: Ensures that Nasim’s responses are based on the latest medical information.
- **Web Scraping**: Used for updating Nasim's knowledge with new medical data.

---

## API Integration

Nasim’s backend API is structured to handle requests to different modules. Below are the main endpoints:

- **/diagnosis**: Handles initial diagnoses based on symptoms.
- **/drug-interaction**: Checks for drug and food interactions.
- **/mental-health**: Provides mental health advice.
- **/pregnancy**: Offers pregnancy guidance.
- **/chronic-disease**: Manages chronic disease questions.

Example Request:
```bash
curl -X POST http://localhost:5000/diagnosis -d '{"symptoms": "صداع مستمر"}'
```

---

## Testing Nasim

To ensure Nasim’s accuracy and reliability, test it with prompts across all modules:

```bash
# Run tests using pytest
pytest tests/
```

Sample Prompts for Testing:
- **Diagnosis**: "أشعر بألم في الصدر وضيق في التنفس"
- **Drug Interaction**: "هل يمكن تناول الدواء مع القهوة؟"
- **Mental Health**: "أشعر بالاكتئاب، ماذا أفعل؟"

Refer to the `tests/` directory for additional test cases covering all modules.

---

## Contributing

We welcome contributions! To contribute to Nasim:

1. **Fork** the repository.
2. **Create a branch** for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. **Make changes** and commit them:
   ```bash
   git commit -m "Add new feature"
   ```
4. **Push to your branch**:
   ```bash
   git push origin feature-name
   ```
5. **Open a Pull Request** on GitHub.

Please ensure all new code follows the existing coding standards and includes test cases.

---

## Contact

For any questions, suggestions, or partnership inquiries, please reach out to the project maintainer:

- **Email**: yasser.taha.bases@gmail.com
- **Email**: deema6644@gmail.com
- **GitHub**: [yasso_bases](https://github.com/yasso_bases)

---
