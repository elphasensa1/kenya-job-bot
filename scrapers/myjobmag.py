import requests
from bs4 import BeautifulSoup
from .base import HEADERS

def scrape_myjobmag():
    url = "https://www.myjobmag.co.ke/jobs-location/nairobi"
    jobs = []
    print(f"🔍 Accessing: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        print(f"🌐 Website Response Code: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # We try to find the list of jobs
        job_listings = soup.select('.job-list-items li') # Updated selector for 2026
        print(f"📊 Found {len(job_listings)} raw items on the page.")

        for item in job_listings:
            h2_tag = item.find('h2')
            if h2_tag and h2_tag.find('a'):
                link_tag = h2_tag.find('a')
                title = link_tag.text.strip()
                job_url = "https://www.myjobmag.co.ke" + link_tag['href']
                jobs.append({'title': title, 'url': job_url, 'company': 'MyJobMag Listing'})
                
        print(f"✅ Successfully parsed {len(jobs)} jobs from MyJobMag.")
    except Exception as e:
        print(f"❌ Error scraping MyJobMag: {e}")
    return jobs
