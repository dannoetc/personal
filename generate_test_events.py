import time
from datetime import datetime
import requests

BASE_URL = "http://127.0.0.1:8000"
HEADERS = {
    "Content-Type": "application/json",
    "X-Fake-User": "melissa@example.com",
}


def send_event(event_type: str):
    payload = {
        "type": event_type,
        # You can omit timestamp and let the server default it,
        # but we'll send it explicitly for clarity:
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    resp = requests.post(f"{BASE_URL}/events", json=payload, headers=HEADERS)
    print(f"[{event_type}] status={resp.status_code} -> {resp.json()}")
    return resp.json()


def simulate_session_1():
    print("\n=== Simulating Session 1 (4 questions, some pauses) ===")
    # Q1: 3s active
    send_event("NEXT")   # Start session + question 1
    time.sleep(1)
    time.sleep(2)
    send_event("NEXT")   # Close Q1, start Q2

    # Q2: 2s active, 2s paused
    time.sleep(1)
    send_event("PAUSE")  # pause
    time.sleep(2)
    send_event("PAUSE")  # resume
    time.sleep(1)
    send_event("NEXT")   # Close Q2, start Q3

    # Q3: quick
    time.sleep(1)
    send_event("NEXT")   # Close Q3, start Q4

    # Q4: 2s active then exit
    time.sleep(2)
    send_event("EXIT")   # Close Q4 + end session


def simulate_session_2():
    print("\n=== Simulating Session 2 (2 longer questions) ===")
    # Start new session automatically with NEXT
    send_event("NEXT")   # Q1
    time.sleep(3)
    send_event("NEXT")   # Close Q1, start Q2

    # Q2 with a pause in middle
    time.sleep(2)
    send_event("PAUSE")
    time.sleep(3)
    send_event("PAUSE")  # resume
    time.sleep(2)
    send_event("EXIT")   # Close Q2 + end session


if __name__ == "__main__":
    print("Generating test events against FastAPI at", BASE_URL)
    simulate_session_1()
    simulate_session_2()
    print("\nDone. Now try:")
    print(" - GET /sessions/today")
    print(" - Check one session_id via GET /sessions/{session_id}/summary")
