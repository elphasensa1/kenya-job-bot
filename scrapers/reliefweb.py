import feedparser

def scrape_reliefweb():
    # RSS feed for jobs in Kenya
    feed_url = "https://reliefweb.int/jobs/rss?country=131"
    jobs = []
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:10]:
            jobs.append({
                'title': entry.title,
                'url': entry.link,
                'company': 'NGO/Humanitarian'
            })
    except Exception as e:
        print(f"Error scraping ReliefWeb: {e}")
    return jobs