import requests

API = "http://127.0.0.1:5000/query"


def run_demo():
    print("Farmer Query Chatbot Demo (type 'quit' to exit)")
    while True:
        q = input("You: ")
        if not q or q.strip().lower() in ("quit", "exit"):
            break
        r = requests.post(API, json={"query": q})
        try:
            print("Bot:", r.json().get("advice"))
        except Exception:
            print("Error: could not reach API. Make sure app.py is running.")


if __name__ == "__main__":
    run_demo()
