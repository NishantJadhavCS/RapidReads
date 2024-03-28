from django.shortcuts import render
from newsapi import NewsApiClient
import datetime
import requests
from gensim.summarization import summarize
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


def topheadline(request):
    if request.method == "POST":
        category = request.POST.get("category")
        api_key = "5df0230b73754bb4a4454b1980ca0486"

        url = f"https://newsapi.org/v2/top-headlines?category={category}&language=en&apiKey={api_key}"

        if request.POST.get("countryCheckbox"):
            country = "in"
            url += f"&country={country}"

        response = requests.get(url)
        raw_headlines = response.json().get("articles", [])
        headlines = []
        for headline in raw_headlines:
            if (
                headline.get("title") != "[Removed]"
                and headline.get("description") is not None
            ):
                headlines.append(headline)

        if not headlines:
            message = "error"
            return render(request, "topheadline.html", {"articles": message})

        return render(request, "topheadline.html", {"headlines": headlines})
    else:
        return render(request, "topheadline.html")


def inshorts(request):
    if request.method == "POST":
        article_url = request.POST.get("article_url")
        extractor = Goose()

        try:
            article = extractor.extract(article_url)
        except:
            return render(
                request,
                "inshorts.html",
                {"error_message": "url-error"},
            )

        if article is None:
            return render(
                request,
                "inshorts.html",
                {"error_message": "url-error"},
            )

        if not article.cleaned_text:
            return render(
                request,
                "inshorts.html",
                {"error_message": "no-text"},
            )

        sentences = sent_tokenize(article.cleaned_text)
        if len(sentences) < 2:
            return render(
                request,
                "inshorts.html",
                {"error_message": "less-sentence"},
            )

        summarized_text = summarize(article.cleaned_text)

        return render(request, "inshorts.html", {"summarized_text": summarized_text})
    else:
        return render(request, "inshorts.html")


def summarizeurl(request):
    if request.method == "GET":
        article_url = request.GET.get("article_url")
        extractor = Goose()
        try:
            article = extractor.extract(article_url)
        except:
            return render(
                request,
                "summarize.html",
                {"error_message": "url-error"},
            )

        if article is None:
            return render(
                request,
                "summarize.html",
                {"error_message": "url-error"},
            )

        if not article.cleaned_text:
            return render(
                request,
                "summarize.html",
                {"error_message": "no-text"},
            )

        sentences = sent_tokenize(article.cleaned_text)
        if len(sentences) < 2:
            return render(
                request,
                "summarize.html",
                {"error_message": "less-sentence"},
            )
        summarized_text = summarize(article.cleaned_text)
        return render(request, "summarize.html", {"summarized_text": summarized_text})

    return render(request, "summarize.html")
