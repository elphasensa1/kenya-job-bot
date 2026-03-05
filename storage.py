import sqlite3

def init_db():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs 
                 (url TEXT PRIMARY KEY, title TEXT, company TEXT, date_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def is_new_job(url):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("SELECT url FROM jobs WHERE url=?", (url,))
    result = c.fetchone()
    conn.close()
    return result is None

def save_job(url, title, company):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO jobs (url, title, company) VALUES (?, ?, ?)", (url, title, company))
        conn.commit()
    except sqlite3.IntegrityError:
        pass 
    conn.close()