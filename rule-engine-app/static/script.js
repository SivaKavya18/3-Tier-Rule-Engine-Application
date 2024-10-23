// static/script.js

// Handle Create Rule Form Submission
document.getElementById('createRuleForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const ruleString = document.getElementById('ruleString').value;
    const CreateRuleName=document.getElementById('CreateRuleName').value;
  
    const response = await fetch('/create_rule', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rule_string:ruleString, rule_name: CreateRuleName })
    });
  
    const result = await response.json();
    document.getElementById('createRuleResponse').innerText = `Rule created with name: ${result.rule_name}`;
  });
  
  // Handle Evaluate Rule Form Submission
  document.getElementById('evaluateRuleForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const ruleName = document.getElementById('ruleName').value;
    const ruleData = JSON.parse(document.getElementById('ruleData').value);
  
    const response = await fetch('./evaluate_rule', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rule_name: ruleName, data: ruleData })
    });
  
    const result = await response.json();
    document.getElementById('evaluateRuleResponse').innerText = `Evaluation result: ${result.result}`;
  });

  // Handle Combine Rule Form Submission
  document.getElementById('CombineRuleForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const ruleNameForCombined = document.getElementById('RuleNameForCombined').value;
    const ruleStrings = document.getElementById('ruleStrings').value;
  
    const response = await fetch('./combine_rules', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rule_name: ruleNameForCombined, rule_strings: ruleStrings })
    });
    document.getElementById('CombineRuleResponse').innerText = `Rules are Combined`;
  });

  // Handle Update Rule Form Submission
  document.getElementById('updateRuleForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const ruleNameToUpdate = document.getElementById('ruleNameToUpdate').value;
    const ruleStringUpdate = document.getElementById('ruleStringUpdate').value;
  
    const response = await fetch('./update_rule', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rule_name: ruleNameToUpdate, rule_string: ruleStringUpdate })
    });
  
    const result = await response.json();
    document.getElementById('UpdateRuleResponse').innerText = `Updated ${result.rule_name}`;
  });
  