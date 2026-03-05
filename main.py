from storage import init_db, is_new_job, save_job
from scrapers.myjobmag import scrape_myjobmag
from scrapers.reliefweb import scrape_reliefweb
from notifier import send_telegram_summary

def main():
    print("--- 🏁 Starting Real Job Search ---")
    init_db()
    all_jobs = []
    
    # 1. Fetch jobs from our sources
    print("Fetching from MyJobMag...")
    all_jobs.extend(scrape_myjobmag())
    
    print("Fetching from ReliefWeb...")
    all_jobs.extend(scrape_reliefweb())
    
    # 2. Filter for only the brand new ones
    new_jobs_to_notify = []
    for job in all_jobs:
     if is_new_job(job['url'])::
            save_job(job['url'], job['title'], job['company'])
            new_jobs_to_notify.append(job)
    
    # 3. Send the summary only if new jobs exist
    if new_jobs_to_notify:
        print(f"Success! Found {len(new_jobs_to_notify)} new jobs.")
        send_telegram_summary(new_jobs_to_notify)
    else:
        print("No new jobs found since the last check.")
    
    print("--- ✅ Search Finished ---")

if __name__ == "__main__":
    main()


