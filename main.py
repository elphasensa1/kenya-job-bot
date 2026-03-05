from storage import init_db, is_new_job, save_job
from scrapers.myjobmag import scrape_myjobmag
from scrapers.reliefweb import scrape_reliefweb
from notifier import send_telegram_summary

def main():
    init_db()
    all_jobs = []
    
    # Run the scrapers
    all_jobs.extend(scrape_myjobmag())
    all_jobs.extend(scrape_reliefweb())
    
    new_jobs_to_notify = []
    for job in all_jobs:
        if is_new_job(job['url']):
            save_job(job['url'], job['title'], job['company'])
            new_jobs_to_notify.append(job)
    
    # Only send if there's actually something new!
    if new_jobs_to_notify:
        send_telegram_summary(new_jobs_to_notify)
    else:
        print("Everything is up to date. No new jobs found.")

if __name__ == "__main__":
    main()
