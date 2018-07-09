import csv
from goose3 import Goose
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import concurrent.futures
import threading
import traceback

csv_writer_lock = threading.Lock()
f = csv.reader(open(r"links.csv"), delimiter=',')
w = csv.writer(open(r"sentiment.csv", "w+", newline=''))
w.writerow(["Negative", "Neutral", "Positive", "Compound", "Name", "Source", "Title", "Publish Date", "URL"])

def worker(row):

    with csv_writer_lock:
        ticker = row[0]
        # name = row [1]
        date = row[1][2:-11]
        source = row[2][2:-1]
        title = row[3][2:-1]
        link = row[4][2:-1]
        val = URLValidator()
        try:
            val(link)
            article = g.extract(url=link)
            if "keyword" in article.cleaned_text:
                vs = analyzer.polarity_scores(article.cleaned_text)
                w.writerow([vs["neg"], vs["neu"], vs["pos"], vs["compound"],
                            ticker, source, article.title.encode("cp437", "ignore"), date, link])
                print(link)

        except ValidationError:
            print(traceback.format_exc())
        except Exception:
            print(traceback.format_exc())
    return


g = Goose()
analyzer = SentimentIntensityAnalyzer()

executor = concurrent.futures.ThreadPoolExecutor(20)
futures = [executor.submit(worker, row) for row in f]
concurrent.futures.wait(futures)