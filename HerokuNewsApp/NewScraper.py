#!/usr/bin/env python3
import bs4 as bs
from urllib.request import Request, urlopen
from newspaper import Article
from textblob import TextBlob
from datetime import datetime

from . import settings
from django.core.management import setup_environ
setup_environ(settings)

from HerokuNewsApp import models

def getArticle(url):
    article = Article(url)
    article.download()
    article.parse()
    return article

def makeUrlSoup(url):
    sauce = Request(url, headers={"User-Agent": "Mozilla"})
    webpage = urlopen(sauce).read()
    soup = bs.BeautifulSoup(webpage, 'lxml')
    return soup

def writeArticleToTextFile(article, path, keywords, sentiment):
    article.download()
    with open(path, "w") as text_file:
        text_file.write('{}\n{}\n{}\n{}\n{}'.format(
            article.url, article.text.replace('\n\n', ' '),
            keywords, str(article)), sentiment)

def AddArticleToDP(article, sentimnent, newsoutlet):
    ArticlePost = ArticleScheme(
      title=article.title,
      text=article.text,
      url=article.url,
      data_joinedd=datetime.now(),
      sentiment=str(sentiment)[:4],
      newsoutlet=newsoutlet,
      keywords=article.keywords,
    )
    print(str(ArticlePost))
    #ArticlePost.save()


def getListOfArticleLinks(url, soup):
    ## A function to get Article links from front page.
    for article in soup.find_all('article'):
        return article.find_all('a', href=True)

def FindAndWriteArticle(front_page="", article_name="", addToDatabase=True):
    soup = makeUrlSoup(front_page)
    url = getListOfArticleLinks(front_page, soup)[0]["href"]
    article = getArticle(url)
    newsoutlet = article_name.split("_")[0]
    blob = TextBlob(article.text)
    writeArticleToTextFile(article, "article_samples/" + article_name, article.keywords, blob.entiment)
    if addToDatabase:
        AddArticleToDP(article, blob.sentiment, )

if __name__ == "__main__":
    ##FindAndWriteArticle("https://www.washingtonpost.com/news-opinions-sitemap.xml", 'Washington_article.txt')

    ##FindAndWriteArticle("http://www.cnn.com/sitemaps/sitemap-articles-2017-11.xml", "CNN_article.txt")

    ##FindAndWriteArticle("https://www.huffingtonpost.com/sitemap.xml", "HuffingtonPost_article.txt")

    FindAndWriteArticle(front_page="https://www.npr.org/sections/politics/", article_name="NPR_article.txt")

    ##FindAndWriteArticle("http://www.foxnews.com/sitemap.xml?idx=26", "foxnews_article.txt")

    ##FindAndWriteArticle("https://www.bloomberg.com/feeds/bpol/sitemap_news.xml", "bloomberg_article.txt")
