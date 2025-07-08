# ai_agent_client.py
# This script simulates an AI Agent (MCP Client) interacting with the MCP Server.

import requests
import json

class AIAgent:
    def __init__(self, mcp_server_url="http://127.0.0.1:5000"):
        self.mcp_server_url = mcp_server_url
        self.schema = self._get_schema()

    def _get_schema(self):
        """Fetches the database schema (MCP Resource) from the MCP server."""
        schema_url = f"{self.mcp_server_url}/mcp/resources/customer_schema"
        try:
            print(f"AI Agent: Fetching schema from {schema_url}...")
            response = requests.get(schema_url)
            response.raise_for_status()
            schema = response.json()
            print("AI Agent: Schema fetched successfully.")
            return schema
        except requests.exceptions.RequestException as e:
            print(f"AI Agent Error: Could not fetch schema from MCP server: {e}")
            return None

    def _natural_language_to_sql(self, natural_language_query):
        """Conceptual Natural Language to SQL (NL2SQL) generation."""
        print(f"\nAI Agent: Translating natural language query: '{natural_language_query}' to SQL...")
        
        query_lower = natural_language_query.lower()
        if "customers from california" in query_lower:
            return "SELECT first_name, last_name FROM Customers WHERE state = 'CA';"
        elif "total number of customers" in query_lower:
            return "SELECT COUNT(*) FROM Customers;"
        elif "list some customer details" in query_lower:
            return "SELECT customer_id, first_name, last_name, city, state FROM Customers LIMIT 5;"
        else:
            print("AI Agent: Could not generate specific SQL. Returning a default query.")
            return "SELECT customer_id, first_name, last_name FROM Customers LIMIT 3;"

    def query_customer_data(self, natural_language_query):
        """Processes a natural language query and interacts with the MCP server."""
        if not self.schema:
            return {"status": "error", "message": "Database schema is not available."}

        sql_query = self._natural_language_to_sql(natural_language_query)
        print(f"AI Agent: Generated SQL: '{sql_query.strip()}'")

        tool_url = f"{self.mcp_server_url}/mcp/tools/query_customer_data"
        headers = {'Content-Type': 'application/json'}
        payload = {'sql_query': sql_query}

        try:
            print(f"AI Agent: Sending SQL query to MCP Server at {tool_url}...")
            response = requests.post(tool_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Failed to communicate with MCP server: {e}"}
