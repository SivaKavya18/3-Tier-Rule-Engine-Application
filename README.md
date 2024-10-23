# 3-Tier Rule Engine Application
This project is a simple 3-tier application consisting of a web-based UI, a Flask API, and a SQLite database backend. The system allows for dynamic creation, combination, and evaluation of rules to determine user eligibility based on attributes like age, department, salary, etc. The rules are represented using an Abstract Syntax Tree (AST) structure to evaluate.

## Features
Dynamic Rule Creation: Create conditional rules like (age > 30 AND department = 'Sales').
AST Representation: Rules are represented as Abstract Syntax Trees (ASTs) for flexibility and evaluation.
Rule Combination: Multiple rules can be combined using logical operator AND.
Eligibility Evaluation: Evaluate rules against user data to determine eligibility.
Update Rules: Rule strings can be updated by thier corresponding names

## Prerequisites
Before running the application, ensure you have the following dependencies installed:
Python 3.x
Flask: For building the web API.
SQLite3: For storing rules and metadata.

## Dependencies
The requirements.txt file lists all Python dependencies for this project.
Flask
sqlite3

## Installation
#### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/rule-engine-app.git
cd rule-engine-app
```

#### Step 2: Set Up Virtual Environment (Optional but recommended)
```bash
python3 -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Running the Application
Option 1: Locally
Start the Flask application:
```bash
python app.py
```
Open your browser and navigate to http://127.0.0.1:5000/.

Option 2: Using Docker
Build the Docker image:
```bash
docker build -t rule-engine-app .
```
Run the container:
```bash
docker run -p 5000:5000 rule-engine-app
```
Access the application at http://localhost:5000.

## Database Design
You can use SQLite to store the rules and their metadata.
To create or use rules.db:
```sql
sqlite3 rules.db
```
Table Schema:
```sql
CREATE TABLE rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name TEXT UNIQUE,   -- Name or identifier for the rule
    rule_string TEXT NOT NULL, -- The rule in string format (like age > 30)
);
```

## API Endpoints
#### 1. POST /create_rule
**Description:** Create a rule and store it in the database.

**Request Body:**
```json
{
    "rule_name": "Rule1",
    "rule_string": "(age > 30 AND department = 'Sales')"
}
```
**Response:**
```json
{
    "message": "Rule created",
    "rule_name": "Rule1"
}
```
#### 2. POST /combine_rules
**Description:** Combine multiple rules into a single rule using logical operators.

**Request Body:**
```json
{
    "rule_name": "CombinedRule",
    "rule_strings": "Rule1,Rule2"
}
```
**Response:**
```json
{
    "combined_ast": "<combined AST here>"
}
```
#### 3. POST /evaluate_rule
**Description:** Evaluate user data against a specific rule.

**Request Body:**
```json
{
    "rule_name": "Rule1",
    "data": {
        "age": 35,
        "department": "Sales",
        "salary": 60000
    }
}
```
**Response:**
```json
{
    "result": true
}
```
#### 4. POST /update_rule
**Description:** Update the rule for a specific rule name.

Request Body:
```json
{
    "rule_name": "Rule1",
    "rule_string": "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
}
```
**Response:**
```json
{
    "message": "Rule updated", 
    "rule_name": "rule_name"
}
```
## Project Structure
rule-engine-app/
│
├── app.py                     # Main Flask app and API endpoints
├── abstract_st.py             # AST structure and parsing logic
├── database.py                # Database connection and initialization
├── requirements.txt           # Python dependencies
├── static/
|   ├── index.html             # Basic frontend
|   ├── styles.css
|   ├── script.js
└── README.md                  # Project documentation
