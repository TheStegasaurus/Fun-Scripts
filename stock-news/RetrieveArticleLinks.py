import urllib.error
import urllib.request
import json
import csv
import math
from pprint import pprint

#sys.stdout = codecs.getwriter("iso-8859-1")(sys.stdout, 'xmlcharrefreplace')

n=type(None)
f = csv.writer(open(r"links.csv", "w+", newline=''))

# dummy api key - insert newsapi key here
apikey = "4915b30ca65743c5a087a47a01845ead5"

tickers = {
    'CFG': 'CITIZENS+FINANCIAL+GROUP+INC',
    'ZION': 'ZIONS+BANCORPORATION',
    'KEY': 'KEYCORP'
}

sources = \
    "abc-news," \
    "abc-news-au," \
    "al-jazeera-english," \
    "associated-press," \
    "australian-financial-review," \
    "bbc-news," \
    "bloomberg," \
    "business-insider," \
    "business-insider-uk," \
    "cbc-news," \
    "cnbc," \
    "cnn," \
    "daily-mail," \
    "financial-post," \
    "financial-times," \
    "fortune," \
    "fox-news," \
    "google-news," \
    "google-news-ar," \
    "google-news-au," \
    "google-news-br," \
    "google-news-ca," \
    "google-news-fr," \
    "google-news-in," \
    "google-news-is," \
    "google-news-it," \
    "google-news-ru," \
    "google-news-sa," \
    "google-news-uk," \
    "independent," \
    "msnbc," \
    "national-review," \
    "nbc-news," \
    "news24," \
    "newsweek," \
    "new-york-magazine," \
    "politico," \
    "reuters," \
    "rt," \
    "the-american-conservative," \
    "the-globe-and-mail," \
    "the-guardian-au," \
    "the-guardian-uk," \
    "the-huffington-post," \
    "the-jerusalem-post," \
    "the-new-york-times," \
    "the-telegraph," \
    "the-wall-street-journal," \
    "the-washington-post," \
    "the-washington-times," \
    "time," \
    "usa-today," \
    "vice-news," \
    "wired"

f.writerow(["Ticker", "Company", "PublishDate", "Source", "Title", "URL"])
for key, value in tickers.items():
    try:
        apicall = "https://newsapi.org/v2/everything?sources="+sources+"&q=%22" + value + "%22&from=2018-01-01&sort_by=relevancy&language=en&pageSize=20&page=1&apiKey=" + apikey
        contents = urllib.request.urlopen(apicall).read()
        data = json.loads(contents)
        totalarticles = data["totalResults"]
        print("TICKER: " + key)
        print("Articles: "+str(totalarticles))
        numpages = math.ceil(totalarticles/100)
        print("Pages: "+str(numpages))
        print("")

        for x in range(1, numpages+1):
            apicall = "https://newsapi.org/v2/everything?sources=" + sources + "&q=%22" + value + "%22&sort_by=relevancy&language=en&pageSize=100&page="+str(x)+"&apiKey=" + apikey
            contents = urllib.request.urlopen(apicall).read()
            data = json.loads(contents)
            #pprint(contents)
            for article in data["articles"]:
                if type(article["publishedAt"])!=n and type(article["source"]["name"]) != n and type(article["title"])!=n and type(article["url"])!= n:
                    f.writerow([
                        key, value.replace("+", " "), article["publishedAt"].encode("cp437", "ignore"), article["source"]["name"].encode("cp437", "ignore"),article["title"].encode("cp437", "ignore"), article["url"].encode("cp437", "ignore")])

    except TimeoutError:
        print("Timeout. Resuming...")
    except urllib.error.HTTPError:
        print("Offending api call: " + apicall)
    except Exception as e:
        print("Exception Occurred")
