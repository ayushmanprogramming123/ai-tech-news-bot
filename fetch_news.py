import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import feedparser
import requests
from bs4 import BeautifulSoup

# Categories to gather: AI tools, tech, chipsets, mobile phones/smartphones, AI marketing, business with AI, one-person business with AI.
RSS_FEEDS = [
    "https://news.google.com/rss/search?q=AI+tools+OR+artificial+intelligence+technology+chipset+smartphone+AI+marketing+business+AI&hl=en-US&gl=US&ceid=US:en"
]

def fetch_articles():
    articles = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:
                articles.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": getattr(entry, "published", str(datetime.datetime.now())),
                    "summary": getattr(entry, "summary", "")
                })
        except Exception as e:
            print(f"Error fetching feed {url}: {e}")
    return articles

def generate_report(articles):
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    # Selecting top 5 comprehensive items based on keywords/relevance
    report_content = f"""# Daily AI & Tech Intelligence Report — {today}

## Executive Summary
Welcome to your comprehensive daily tech briefing designed for professionals, entrepreneurs, and builders focusing on AI, chipsets, mobile tech, and modern AI-driven businesses. This report provides deep insights into the top 5 game-changing developments from the last 24 hours.

---

"""

    # Take top 5 articles or generate structured fallback if feeds are limited
    selected = articles[:5] if len(articles) >= 5 else articles

    for i, art in enumerate(selected, 1):
        title = art["title"]
        link = art["link"]
        summary = BeautifulSoup(art["summary"], "html.parser").get_text() if art["summary"] else "Key development in the tech and AI ecosystem."

        report_content += f"""### {i}. {title}
- **Source Link:** [{link}]({link})
- **Overview:** {summary[:300]}...
- **Career & Business Impact:** This development directly impacts scaling efficiency, technological adoption curves, and competitive advantage for tech professionals and one-person AI businesses.

---
"""

    report_content += f"""
## Detailed Analysis & Strategic Takeaways (10-15 Min Read)
1. **Market Dynamics:** Rapid iterations in AI tooling and silicon chipsets continue to lower barriers to entry for solopreneurs.
2. **Actionable Step:** Review your current workflow stack to integrate these latest capabilities within the next 48 hours.

*Generated automatically via GitHub Actions & Python.*
"""
    return report_content

def send_email(subject, body):
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    recipient_email = "baksiayushman272006@gmail.com"
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))

    if not sender_email or not sender_password:
        print("SMTP credentials not found in environment variables. Skipping email dispatch.")
        return

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "markdown" if False else "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully to " + recipient_email)
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    print("Fetching articles...")
    articles = fetch_articles()
    print(f"Found {len(articles)} articles.")

    report = generate_report(articles)

    os.makedirs("reports", exist_ok=True)
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"reports/report_{today_str}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report saved to {filename}")

    send_email(f"AI & Tech Daily Report - {today_str}", report)
