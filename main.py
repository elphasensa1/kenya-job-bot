import os
from storage import init_db, is_new_job, save_job
from scrapers.myjobmag import scrape_myjobmag
from scrapers.reliefweb import scrape_reliefweb
from notifier import send_telegram_summary

def main():
    print("--- 🏁 Bot Started ---")
    init_db()
    
    # FORCED TEST: This ensures you get a message NO MATTER WHAT 
    # (We will remove this once we know Telegram is working)
    test_job = {
        'title': '🚀 Connection Successful!',
        'url': 'https://github.com',
        'company': 'Your Kenya Job Bot'
    }
    print("Sending a test message to verify Telegram...")
    send_telegram_summary([test_job])
    
    all_jobs = []
    
    print("Checking MyJobMag...")
    all_jobs.extend(scrape_myjobmag())
    
    print("Checking ReliefWeb...")
    all_jobs.extend(scrape_reliefweb())
    
    print(f"Found {len(all_jobs)} jobs total. Checking for new ones...")
    
    new_jobs_to_notify = []
    for job in all_jobs:
        if is_new_job(job['url']):
            save_job(job['url'], job['title'], job['company'])
            new_jobs_to_notify.append(job)
    
    if new_jobs_to_notify:
        print(f"Found {len(new_jobs_to_notify)} brand new jobs! Sending summary...")
        send_telegram_summary(new_jobs_to_notify)
    else:
        print("No new jobs found in this run.")
        
    print("--- ✅ Bot Finished Successfully ---")

if __name__ == "__main__":
    main()
