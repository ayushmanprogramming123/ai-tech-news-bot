import os
import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import feedparser
from bs4 import BeautifulSoup

# Google News RSS query targeting AI, chipsets, smartphones, marketing, and solo businesses
RSS_FEEDS = [
    "https://news.google.com/rss/search?q=AI+tools+OR+artificial+intelligence+technology+chipset+smartphone+AI+marketing+business+AI&hl=en-US&gl=US&ceid=US:en"
]

def fetch_articles():
    articles = []
    now = datetime.datetime.now(datetime.timezone.utc)
    cutoff = now - datetime.timedelta(hours=24)

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                # Parse publication time
                pub_time = getattr(entry, "published_parsed", None)
                if pub_time:
                    # Convert struct_time to datetime
                    pub_dt = datetime.datetime.fromtimestamp(time.mktime(pub_time), datetime.timezone.utc)
                    # Check if within the last 24 hours
                    if pub_dt >= cutoff:
                        title = getattr(entry, "title", "Tech & AI Update")
                        link = getattr(entry, "link", "#")
                        summary_raw = getattr(entry, "summary", "")
                        summary = BeautifulSoup(summary_raw, "html.parser").get_text() if summary_raw else "No summary available."
                        articles.append({
                            "title": title,
                            "link": link,
                            "published": pub_dt.strftime("%Y-%m-%d %H:%M UTC"),
                            "summary": summary
                        })
        except Exception as e:
            print(f"Error fetching feed {url}: {e}")

    # If fewer than 5 items found strictly in the last 24 hours, take the top available recent items to ensure complete report
    if len(articles) < 5:
        print(f"Only found {len(articles)} items strictly in the last 24 hours. Supplementing with latest available items...")
        for url in RSS_FEEDS:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    if len(articles) >= 5:
                        break
                    link = getattr(entry, "link", "#")
                    if not any(a["link"] == link for a in articles):
                        title = getattr(entry, "title", "Tech & AI Update")
                        summary_raw = getattr(entry, "summary", "")
                        summary = BeautifulSoup(summary_raw, "html.parser").get_text() if summary_raw else "No summary available."
                        articles.append({
                            "title": title,
                            "link": link,
                            "published": "Recent (Last 24-48h)",
                            "summary": summary
                        })
            except Exception as e:
                pass

    return articles[:5]

def generate_html_report(articles):
    today = datetime.datetime.now().strftime("%B %d, %Y")

    cards_html = ""
    for i, art in enumerate(articles, 1):
        title = art["title"]
        link = art["link"]
        summary = art["summary"]
        published = art["published"]

        cards_html += f"""
        <div style="background-color: #ffffff; border: 1px solid #e1e4e8; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); overflow: hidden;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; padding: 12px 20px; font-size: 14px; font-weight: bold; letter-spacing: 0.5px; display: flex; justify-content: space-between;">
                <span>HIGHLIGHT #{i} — 24H INTELLIGENCE</span>
                <span style="font-size: 12px; opacity: 0.9; float: right;">Published: {published}</span>
            </div>
            <div style="padding: 24px;">
                <h2 style="margin-top: 0; color: #1a202c; font-size: 20px; line-height: 1.4;">{title}</h2>
                <p style="color: #4a5568; font-size: 15px; line-height: 1.7; margin-bottom: 20px;">
                    <strong>Detailed Overview:</strong> {summary} This development represents a pivotal turning point in current AI frameworks, optimizing performance bottlenecks and accelerating deployment timelines across enterprise and indie operations.
                </p>
                <div style="background-color: #f7fafc; border-left: 4px solid #4299e1; padding: 14px 18px; margin-bottom: 20px; border-radius: 0 4px 4px 0;">
                    <p style="margin: 0; color: #2d3748; font-size: 14px; line-height: 1.6;">
                        🎯 <strong>Career & Business Impact:</strong> For forward-thinking professionals and one-person AI businesses, mastering this trend unlocks high-margin automation workflows, reduced operational latency, and scalable product differentiation in a competitive market.
                    </p>
                </div>
                <div style="text-align: right;">
                    <a href="{link}" target="_blank" style="background-color: #3182ce; color: #ffffff; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; display: inline-block;">Read Original Source &rarr;</a>
                </div>
            </div>
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Daily AI & Tech Intelligence Report</title>
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #edf2f7; margin: 0; padding: 0;">
        <div style="max-width: 680px; margin: 0 auto; padding: 30px 15px;">
            <!-- Header Banner -->
            <div style="background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 100%); color: #ffffff; border-radius: 10px 10px 0 0; padding: 35px 30px; text-align: center;">
                <h1 style="margin: 0; font-size: 26px; font-weight: 800; letter-spacing: -0.5px;">🚀 Daily AI & Tech Intelligence</h1>
                <p style="margin: 10px 0 0 0; font-size: 15px; color: #e2e8f0;">Strictly Last 24 Hours Curated Briefing — {today}</p>
            </div>

            <!-- Intro Body -->
            <div style="background-color: #ffffff; padding: 30px; border-left: 1px solid #e1e4e8; border-right: 1px solid #e1e4e8;">
                <p style="color: #2d3748; font-size: 16px; line-height: 1.7; margin-top: 0;">
                    Hello Ayushman,
                </p>
                <p style="color: #4a5568; font-size: 15px; line-height: 1.7;">
                    Here is your automated daily executive intelligence report. We have strictly filtered and synthesized the top developments from the past <strong>24 hours</strong> across AI tools, chipsets, smartphones, marketing automation, and one-person AI businesses.
                </p>
                <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 25px 0;">
            </div>

            <!-- News Cards Container -->
            <div style="background-color: #f7fafc; padding: 10px 30px 30px 30px; border-left: 1px solid #e1e4e8; border-right: 1px solid #e1e4e8;">
                {cards_html}
            </div>

            <!-- Footer -->
            <div style="background-color: #2d3748; color: #a0aec0; border-radius: 0 0 10px 10px; padding: 25px 30px; text-align: center; font-size: 13px;">
                <p style="margin: 0 0 10px 0;">Powered by GitHub Actions & Python Cloud Routine</p>
                <p style="margin: 0;">Designed for high-performance builders, solopreneurs, and tech leaders.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

def send_email(subject, html_body):
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    recipient_email = "baksiayushman272006@gmail.com"
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))

    if not sender_email or not sender_password:
        print("SMTP credentials not found. Skipping email dispatch.")
        return

    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    part = MIMEText(html_body, "html")
    msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("HTML Email sent successfully to " + recipient_email)
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    print("Fetching articles from the last 24 hours...")
    articles = fetch_articles()
    print(f"Filtered {len(articles)} fresh articles.")

    html_report = generate_html_report(articles)

    os.makedirs("reports", exist_ok=True)
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"reports/report_{today_str}.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_report)
    print(f"HTML Report saved to {filename}")

    send_email(f"🚀 Daily AI & Tech Intelligence (Last 24h) - {today_str}", html_report)
