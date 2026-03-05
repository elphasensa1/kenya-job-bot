
from notifier import send_telegram_summary

def main():
    print("--- 🏁 Starting Emergency Connection Test ---")
    send_telegram_summary([{"title": "test"}])
    print("--- ✅ Test Complete ---")

if __name__ == "__main__":
    main()
