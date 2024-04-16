import csv
import urllib.request as Req
from urllib.parse import urlencode
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup

URL_OVER18 = "https://www.ptt.cc/ask/over18"
URL_LOTTERY = "https://www.ptt.cc/bbs/Lottery/index.html"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded",
}

over18_form_data = {"from": "/bbs/Lottery/index.html", "yes": "yes"}
over18_encode = urlencode(over18_form_data).encode("utf-8")

cookie = CookieJar()
opener = Req.build_opener(Req.HTTPCookieProcessor(cookie))

req_over18 = Req.Request(URL_OVER18, data=over18_encode, headers=headers)
opener.open(req_over18)


def req_and_parse(url):
    req = Req.Request(url, headers=headers)
    res = opener.open(req)
    soup = BeautifulSoup(res.read().decode("utf-8"), features="html.parser")
    return soup


page_count = 0
while page_count < 3:
    print(f"----------------Start Scraping Page{page_count + 1}----------------")
    menu = req_and_parse(URL_LOTTERY)

    with open("article.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        for article_info in menu.select(".r-ent"):
            title = article_info.select_one(".title").text.strip()
            if "本文已被刪除" in title:
                continue
            like = article_info.select_one(".nrec").text or 0

            article_url = article_info.select_one(".title a").get("href")
            article = req_and_parse("https://www.ptt.cc" + article_url)

            meta_line = article.find_all("div", class_="article-metaline")
            for meta in meta_line:
                tag = meta.find("span", class_="article-meta-tag")
                if tag and tag.get_text() != "時間":
                    continue
                time = meta.find("span", class_="article-meta-value").get_text()
                writer.writerow([title, like, time])
    print(f"----------------Finish Scraping Page{page_count + 1}----------------")
    prev_page_link = menu.select(".btn-group-paging a")[1]
    if prev_page_link.get("href"):
        URL_LOTTERY = "https://www.ptt.cc" + prev_page_link.get("href")
    else:
        break

    page_count += 1

print("----------------Scraping Finished----------------")
