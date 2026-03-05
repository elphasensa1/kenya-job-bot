import requests
from bs4 import BeautifulSoup
from .base import HEADERS

def scrape_myjobmag():
    url = "https://www.myjobmag.co.ke/jobs-location/nairobi"
    jobs = []
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # We look for job items in the list
        job_listings = soup.select('.job-info') # This is a common CSS selector for them
        for item in job_listings[:10]: # Check last 10
            link_tag = item.find('a')
            if link_tag:
                title = link_tag.text.strip()
                job_url = "https://www.myjobmag.co.ke" + link_tag['href']
                company = item.find_previous('li').select_one('.job-details').text.strip() if item.find_previous('li') else "N/A"
                jobs.append({'title': title, 'url': job_url, 'company': company})
    except Exception as e:
        print(f"Error scraping MyJobMag: {e}")
    return jobs