
# mcp_mysql_server.py
# This Flask application simulates an MCP Server for a MySQL database.

from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Mock Database Interaction ---
def execute_mysql_query_mock(sql_query):
    """
    Simulates executing a SQL query, returning mock data based on the query pattern.
    """
    print(f"MCP Server: Attempting to execute SQL (mock): '{sql_query.strip()}'")

    # Mock responses based on query patterns from ai_agent_client.py
    if "SELECT first_name, last_name FROM Customers WHERE state = 'CA'" in sql_query:
        return [
            {"first_name": "Alice", "last_name": "Smith"},
            {"first_name": "Charlie", "last_name": "Brown"}
        ]
    elif "SELECT COUNT(*) FROM Customers" in sql_query:
        return [{"count": 4}]
    elif "SELECT customer_id, first_name, last_name, city, state FROM Customers LIMIT 5" in sql_query:
        return [
            {"customer_id": 1, "first_name": "Alice", "last_name": "Smith", "city": "Los Angeles", "state": "CA"},
            {"customer_id": 2, "first_name": "Bob", "last_name": "Johnson", "city": "New York", "state": "NY"},
            {"customer_id": 3, "first_name": "Charlie", "last_name": "Brown", "city": "Los Angeles", "state": "CA"},
            {"customer_id": 4, "first_name": "Diana", "last_name": "Prince", "city": "Miami", "state": "FL"}
        ]
    # This is the default/fallback query from the agent
    elif "SELECT customer_id, first_name, last_name FROM Customers LIMIT 3" in sql_query:
        return [
            {"customer_id": 1, "first_name": "Alice", "last_name": "Smith"},
            {"customer_id": 2, "first_name": "Bob", "last_name": "Johnson"},
            {"customer_id": 3, "first_name": "Charlie", "last_name": "Brown"}
        ]
    else:
        return [{"message": "Mock query executed successfully, no specific data returned for this query pattern."}]

# --- MCP Tool Endpoint ---
@app.route('/mcp/tools/query_customer_data', methods=['POST'])
def query_customer_data_tool():
    """
    MCP Tool: `query_customer_data`
    Receives SQL queries from the AI agent.
    """
    data = request.json
    sql_query = data.get('sql_query')

    if not sql_query:
        return jsonify({"error": "Missing 'sql_query' parameter."}), 400

    try:
        results = execute_mysql_query_mock(sql_query)
        return jsonify({"status": "success", "data": results})
    except Exception as e:
        print(f"MCP Server Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- MCP Resource Endpoint ---
@app.route('/mcp/resources/customer_schema', methods=['GET'])
def get_customer_schema_resource():
    """
    MCP Resource: `customer_schema`
    Provides the database schema to the AI agent.
    """
    schema_info = {
        "tables": {
            "Customers": {
                "columns": {
                    "customer_id": "INT PRIMARY KEY", "first_name": "VARCHAR(50)", "last_name": "VARCHAR(50)",
                    "email": "VARCHAR(100) UNIQUE", "phone_number": "VARCHAR(20)", "address": "VARCHAR(255)",
                    "city": "VARCHAR(100)", "state": "VARCHAR(50)", "zip_code": "VARCHAR(10)", "registration_date": "DATE"
                },
                "description": "Contains information about individual customers."
            },
            "Orders": {
                "columns": {
                    "order_id": "INT PRIMARY KEY", "customer_id": "INT (FK to Customers)",
                    "order_date": "DATE", "total_amount": "DECIMAL(10, 2)", "status": "VARCHAR(50)"
                },
                "description": "Contains information about customer orders."
            }
        },
        "relationships": ["Customers.customer_id is a foreign key in Orders.customer_id"],
        "business_rules": ["PII such as email and phone_number should not be exposed to general queries."]
    }
    return jsonify(schema_info)

if __name__ == '__main__':
    print("Starting MCP MySQL Server on http://127.0.0.1:5000...")
    app.run(port=5000)
