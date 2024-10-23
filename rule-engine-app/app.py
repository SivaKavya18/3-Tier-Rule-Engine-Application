from flask import Flask, request, jsonify, render_template
from abstract_st import Node
from database import connect_db, initialize_db
import json
import re

app = Flask(__name__, static_folder='static')

# Initialize the database
initialize_db()

# Serve the HTML file
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_string = request.json['rule_string']
    rule_name=request.json['rule_name']
    rule_id = store_rule_in_db(rule_name,rule_string)
    ast=parse_rule_string_to_ast(rule_string)
    return jsonify({"message": "Rule created", "rule_name": rule_name,"AST":str(ast)})

@app.route('/combine_rules', methods=['POST'])
def combine_rules():
    rule_name = request.json['rule_name']
    rule_strings = request.json['rule_strings']
    print(rule_strings)
    combined_ast = combine_ast_rules(rule_name,rule_strings)
    return jsonify({"combined_ast": str(combined_ast)})

@app.route('/update_rule', methods=['POST'])
def update_rule():
    rule_string = request.json['rule_string']
    rule_name=request.json['rule_name']
    update_rule_in_db(rule_name,rule_string)
    return jsonify({"message": "Rule updated", "rule_name": rule_name})

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule():
    rule_name = request.json['rule_name']
    data = request.json['data']
    rule_string = retrieve_ast_from_db(rule_name)
    ast_node=parse_rule_string_to_ast(rule_string)
    result = evaluate_ast(ast_node, data)
    return jsonify({"result": result})

def store_rule_in_db(rule_name,rule_string):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rules (rule_name,rule_string) VALUES (?, ?)",
                   (rule_name,rule_string))
    rule_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return rule_id

def update_rule_in_db(rule_name,rule_string):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE rules SET rule_string=? WHERE rule_name=?",(rule_string,rule_name))
    conn.commit()
    conn.close()
    return rule_name

# Helper Functions
def parse_rule_string_to_ast(rule_string):
    # Parse a basic rule into an AST.
    tokens = re.findall(r'\(|\)|AND|OR|>|<|>=|<=|!=|=|[\w\']+', rule_string)

    def parse_tokens(tokens):
        stack = []
        current_node = None

        while tokens:
            token = tokens.pop(0)

            if token == '(':
                # Recursively parse expressions in parentheses
                sub_expr = parse_tokens(tokens)
                stack.append(sub_expr)
            elif token == ')':
                break  # End of current expression
            elif token in ('AND', 'OR'):
                # Operator node
                operator_node = Node(node_type="operator", value=token)
                if stack:
                    operator_node.left = stack.pop()
                current_node = operator_node
            elif any(op in token for op in ['>', '<', '=', '!=']):
                # Operand (condition) node
                left_operand = stack.pop()  # e.g., 'age'
                operator = token  # e.g., '>'
                right_operand = tokens.pop(0)  # e.g., '30'
                condition_node = Node(node_type="operand", value={'left': left_operand, 'operator': operator, 'right': right_operand})
                stack.append(condition_node)
            else:
                stack.append(token)

        if current_node:
            current_node.right = stack.pop() if stack else None
        else:
            current_node = stack.pop() if stack else None

        return current_node

    return parse_tokens(tokens)

def combine_ast_rules(rule_name,rule_strings):
    conn = connect_db()
    cursor = conn.cursor()
    rules=list(rule_strings.split(","))
    combined_ast = None
    new_rule=""
    for rule_string in rules:
        ruleString = retrieve_ast_from_db(rule_string)
        ast=parse_rule_string_to_ast(ruleString)
        new_rule+="("
        if combined_ast is None:
            combined_ast = ast  # Set the first rule as the combined AST
        else:
            combined_ast = Node(node_type='operator', value='AND', left=combined_ast, right=ast)
        new_rule+=ruleString+") AND "
    store_rule_in_db(rule_name,new_rule)
    conn.close()
    return combined_ast

def retrieve_ast_from_db(rule_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT rule_string FROM rules WHERE rule_name=?", (rule_name,))
    rule_data = cursor.fetchone()
    conn.close()
    return rule_data[0] if rule_data else None

def evaluate_ast(ast, data):
    if ast.type == 'operand':
        # Extract operand details from the AST node
        left_value = data.get(ast.value['left'])
        right_value = ast.value['right'].strip("'")  # Handle strings and remove quotes if present

        if left_value is None:
            raise ValueError(f"Data does not contain key: {ast.value['left']}")

        # Try converting the right_value to float if possible
        try:
            right_value = float(right_value)
            left_value = float(left_value)
        except ValueError:
            pass  # If it fails, leave it as is for string comparison

        operator = ast.value['operator']

        # Perform the comparison based on the operator
        if operator == '>':
            return left_value > right_value
        elif operator == '<':
            return left_value < right_value
        elif operator == '>=':
            return left_value >= right_value
        elif operator == '<=':
            return left_value <= right_value
        elif operator == '=':
            return left_value == right_value
        elif operator == '!=':
            return left_value != right_value

    elif ast.type == 'operator':
        # Recursively evaluate the left and right children
        left_result = evaluate_ast(ast.left, data)
        right_result = evaluate_ast(ast.right, data)

        if ast.value == 'AND':
            return left_result and right_result
        elif ast.value == 'OR':
            return left_result or right_result

    return False

if __name__ == '__main__':
    app.run(debug=True)