import bs4 as bs
from urllib.request import Request, urlopen
from newspaper import Article
from textblob import TextBlob
from datetime import datetime
from django.core.management.base import BaseCommand
from HerokuNewsApp.models import ArticleScheme
import logging

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'link and file name arg required. Optional boolean to add to DB'

    def getArticle(self, url):
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        return article

    def makeUrlSoup(self, url):
        sauce = Request(url, headers={"User-Agent": "Mozilla"})
        webpage = urlopen(sauce).read()
        soup = bs.BeautifulSoup(webpage, 'lxml')
        return soup

    def writeArticleToTextFile(self, article, path, keywords, sentiment):
        with open(path, "w") as text_file:
            text_file.write('{}\n{}\n{}\n{}\n{}'.format(
                article.url, article.text.replace('\n\n', ' '),
                keywords, str(article), sentiment))

    def AddArticleToDB(self, article, sentiment, newsoutlet):
        article.download()
        ArticlePost = ArticleScheme(
          title=article.title,
          text=article.text.replace('\n\n', ' '),
          url=article.url,
          date_joined=datetime.now(),
          polarity=str(sentiment.polarity)[:4],
          subjectivity=str(sentiment.subjectivity)[:4],
          newsoutlet=newsoutlet,
          keywords=article.keywords[:10]
        )
        print(str(ArticlePost))
        #ArticlePost.save()

    def getListOfArticleLinks(self, soup, newsoutlet=""):
        ## A function to get Article links from front page.
        tag="article"
        classNameDict = {}

        infotofindarticledict = {
          "WashingtonPost": ["div", {"class": "headline"}],
          "FoxNews": ["article", {"class": "article"}],
        }

        if newsoutlet in infotofindarticledict.keys():
            tag, clasNameDict = infotofindarticledict[newsoutlet]

        if classNameDict:
            for article in soup.find_all(tag, clasNameDict):
                return article.find_all('a', href=True)
        else:
            for article in soup.find_all(tag):
                return article.find_all('a', href=True)

    def FindAndWriteArticle(self, front_page="", newsoutlet="", addToDatabase=True):
        soup = self.makeUrlSoup(front_page)
        url = ""
        try:
            links = self.getListOfArticleLinks(soup, newsoutlet)[0]["href"]
            url = links[0]["href"
        except IndexError:
            print("No Articles found")
            return
        logging.info("Url ", url)
        article = self.getArticle(url)
        article_name = newsoutlet+"_article.txt"
        blob = TextBlob(article.text)
        self.writeArticleToTextFile(article, "article_samples/" + article_name, article.keywords, blob.sentiment)
        if addToDatabase:
            self.AddArticleToDB(article, blob.sentiment, newsoutlet)

    def add_arguments(self, parser):
        parser.add_argument(
            '--url', dest='url', required=True,
            help='the url to process',
        )
        parser.add_argument(
            '--news', dest='news', required=True,
            help='The name of the newsoutlet.',
        )

    def handle(self, *args, **options):
        self.FindAndWriteArticle(options['url'], options["news"])
