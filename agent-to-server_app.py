# simulated_app.py
# This script simulates a user application interacting with the AI Agent.

from ai_agent_client import AIAgent

def run_simulated_application():
    print("--- Welcome to the AI-Powered Customer Data Query Application ---")
    print("Ensure 'mcp_mysql_server.py' is running in a separate terminal.")
    print("Type 'exit' to stop.")

    agent = AIAgent()
    if not agent.schema:
        print("\nApplication could not initialize. Exiting.")
        return

    while True:
        user_query = input("\nEnter your query about customer data: ")
        if user_query.lower() in ['exit', 'quit']:
            break

        response = agent.query_customer_data(user_query)

        if response.get("status") == "success":
            print("\n--- Query Results ---")
            data = response.get("data", [])
            if data:
                for row in data:
                    print(row)
            else:
                print("No data returned.")
        else:
            print(f"\n--- Error ---")
            print(f"Application encountered an error: {response.get('message', 'Unknown error')}")

if __name__ == "__main__":
    run_simulated_application()
