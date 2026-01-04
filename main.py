import json
from intent_extractor import extract_intent
from query_generator import generate_sql
from db_executor import execute_query

def main():
    print("🧠 Schema-aware DB Agent\nType 'exit' to quit\n")

    while True:
        user_input = input("Ask: ")
        if user_input.lower() == "exit":
            break

        intent = extract_intent(user_input)
        print("\nIntent:", intent)

        sql = generate_sql(intent, user_input)
        print("\nGenerated SQL:\n", sql)

        try:
            result = execute_query(sql)
            print("\nResult:")
            print(json.dumps(result, indent=2))
        except Exception as e:
            print("\nDB Error:", e)

if __name__ == "__main__":
    main()
