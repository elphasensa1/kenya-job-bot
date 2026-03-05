import requests
from bs4 import BeautifulSoup
from .base import HEADERS

def scrape_brightermonday():
    # This URL searches for all jobs in Kenya, newest first
    url = "https://www.brightermonday.co.ke/jobs"
    jobs = []
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # BrighterMonday uses specific classes for their job cards
        listings = soup.select('.flex-1.flex.flex-col') 
        
        for item in listings[:15]: # Look at the top 15
            title_link = item.select_one('a')
            if title_link:
                title = title_link.text.strip()
                job_url = title_link['href']
                # Try to get company name
                company_tag = item.select_one('.text-sm.font-normal')
                company = company_tag.text.strip() if company_tag else "Company Hidden"
                
                jobs.append({'title': title, 'url': job_url, 'company': company})
    except Exception as e:
        print(f"Error scraping BrighterMonday: {e}")
    return jobs
