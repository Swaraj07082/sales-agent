tools = [{
  "type": "function",
  "function": {
    "name": "get_deals",
    "description": "Retrieve available deals for a specific company from the CRM system.",
    "parameters": {
      "type": "object",
      "properties": {
        "company": {
          "type": "string",
          "description": "The name of the company for which to retrieve deals"
        }
      },
      "required": ["company"]
    }
  }
}, 
{
  "type": "function",
  "function": {
    "name": "update_deal_stage",
    "description": "Update the stage of a deal for a specific company in the CRM system.",
    "parameters": {
      "type": "object",
      "properties": {
        "company": {
          "type": "string",
          "description": "The name of the company for which to update the deal stage"
        },
        "new_stage": {
          "type": "string",
          "description": "The new stage to set for the deal"
        }
      },
      "required": ["company", "new_stage"]
    }
  }
},
{
  "type": "function",
  "function": {
    "name": "schedule_meeting",
    "description": "Schedule a meeting for a specific company in the CRM system.",
    "parameters": {
      "type": "object",
      "properties": {
        "company": {
          "type": "string",
          "description": "The name of the company for which to schedule a meeting"
        },
        "date": {
          "type": "string",
          "description": "The date to schedule the meeting (in YYYY-MM-DD format)"
        }
      },
      "required": ["company", "date"]
    }
  }
},
{
  "type": "function",
  "function": {
    "name": "send_email",
    "description": "Send an email with a specific subject and body.",
    "parameters": {
      "type": "object",
      "properties": {
        "subject": {
          "type": "string",
          "description": "The subject of the email"
        },
        "body": {
          "type": "string",
          "description": "The body content of the email"
        }
      },
      "required": ["subject", "body"]
    }
  }
}]