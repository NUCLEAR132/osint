# pip install flask
# pip install playwright
# playwright install
import os
os.system("playwright install")
from flask import Flask, render_template, request, jsonify
from playwright.sync_api import sync_playwright
app = Flask(__name__)
def classify_site(link,title):
    link_lower = link.lower() if link else ""
    title_lower = title.lower() if title else ""
    social_sites = {
        "Facebook" :["facebook.com","facebook","fb","messenger","Facebook","Face_book"]
        "Youtube" :["youtube.com","youtube","Youtube","youtu.be","youtube.kid"]
        "Telegram" :["telegram.org","t.me","telegram","Telegram"]
    }
    for site, keyword in social_sites.items():
        if any(k in link_lower or k in title_lower for k in keyword):
            return site
    education_sites = {
        "Udemy" :["udemy.com","udemy","Udemy"]
        "Coursera" :["coursera.org","coursera","Coursera"]
    }
    for site, keyword in social_sites.items():
        if any(k in link_lower or k in title_lower for k in keyword):
            return site
    news_sites = ["cnn.com","bbc.com","aljazeera.com","News.com"]
    if any(k in link_lower or k in title_lower for k in news_sites):
            return "News Site"
    if any(Email_words in title_lower for Email_words in ["@", "mail", "gmail.com", "بريد"]):
            return "Emails"
    if any(phone_words in title_lower for phone_words in ["phone", "mobile", "رقم", "هاتف"]):
            return "Phone Number"
    official_sites = [".edu",".org","gov",".gov","site","website"]
    if any(k in link_lower or k in title_lower for k in official_sites):
            return "Official Sites"
    general_sites = ["github.com","gitlab.com","arcivhe.org"]
    if any(k in link_lower or k in title_lower for k in general_sites):
            return "General Sites"
    return "Websites"
def osint_ex(query):
    try:
        with sync_playwright as pr :
            browser = pr.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            search_link = f"https://duckduckgo.com/?q={query}&t=h_&ia=web"
            page.goto(search_link,timeout=60000,wait_until="load")
            num_pages = 10
            all_results = []
            for _ in range(num_pages):
                page.wait_for_selector("article[data-testid='result']",timeout=20000)
                results = page.query.selector_all("article[data-testid='result']")
                for result in results:
                    try:
                        title_element = query.selector("h2 a")
                        link_element = query.selector("h2 a")
                        image_element = query.selector("img")
                        if title_element and link_element:
                            title = title_element.inner_text()
                            link = link_element.get_attribute("href")
                            image = image_element.get_attribute("src") if image_element else None
                            site_type = classify_site(link,title)
                            all_results.append(
                                {
                                    "Title" : title, 
                                    "Link" : link, 
                                    "Image": image, 
                                    "Type" : site_type
                                }
                            )
                    except Exception:
                        continue      
                next_btn = query.selector("button#more-results")
                if next_btn:
                    next_btn.click()
                    page.wait_for_timeout(4000)
                else:
                    break
            browser.close()
    except Exception:
        print(f"Error found {e}")
        return[]
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/search',method=["POST"])
def search():
    query = request.form.get("query")
    results = osint_ex(query)
    return jsonify(results)
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000, threaded=True)