from django.shortcuts import render
from newsapi import NewsApiClient
import datetime
import requests
from gensim.summarization import summarize
import nlp
from goose3 import Goose
from nltk.tokenize import sent_tokenize


def home(request):
    return render(request, "home.html")


def feed(request):
    articles = []
    if request.method == "POST":
        query = request.POST.get("query")
        sort_by = request.POST.get("sort_by")

        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=14)
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        today_str = now.strftime("%Y-%m-%d")

        newsapi = NewsApiClient(api_key="5df0230b73754bb4a4454b1980ca0486")
        response = newsapi.get_everything(
            q=query,
            language="en",
            sort_by=sort_by,
            from_param=yesterday_str,
            to=today_str,
        )
        raw_articles = response.get("articles")
        if raw_articles:
            article_id = 1
            for article in raw_articles:
                article["publishedAt"] = article["publishedAt"].split("T")[0]
                if (
                    (
                        query.lower() in article.get("title", "").lower()
                        or query.lower() in article.get("description", "").lower()
                    )
                    and article.get("title") != "[Removed]"
                    and article.get("description") is not None
                ):
                    article["id"] = article_id
                    articles.append(article)
                    article_id += 1

        if not articles:
            message = "error"
            return render(request, "feed.html", {"articles": message})

        return render(request, "feed.html", {"articles": articles})
    else:
        return render(request, "feed.html")
