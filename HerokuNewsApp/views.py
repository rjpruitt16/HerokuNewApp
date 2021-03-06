from django.shortcuts import render
from os import listdir
from HerokuNewsApp.models import ArticleScheme

def GetArticleSchemeDict(newsoutlets):
    articleSchemeDict = {}
    for newsoutlet in newsoutlets:
        articleSet = ArticleScheme.objects.filter(newsoutlet=newsoutlet)
        articleSchemeDict[newsoutlet + "_PolarityArray"] = []
        articleSchemeDict[newsoutlet + "_SubjectivityArray"] = []
        articleSchemeDict[newsoutlet + "_TitleArray"] = []
        for article in articleSet:
            articleSchemeDict[newsoutlet + "_PolarityArray"].append(float(article.polarity))
            articleSchemeDict[newsoutlet + "_SubjectivityArray"].append(float(article.subjectivity))
            articleSchemeDict[newsoutlet + "_TitleArray"].append(article.title)
    return articleSchemeDict

def getWords(article, number_of_words):
    if number_of_words > len(article):
        return article
    words = article.split(" ")
    summary = ""
    for word in words[:number_of_words]:
        summary += word + " "
    return summary

def ReadAndAddUrl(article_dict, path, name):
    data = ParseArticleData(path)
    data["Text"] = data["Text"][:175]
    article_dict = {}
    for key in data.keys():
         article_dict[name+"_"+key] = data[key]
    return article_dict

def ParseArticleData(path):
  data = {}
  data_order = ["Title", "Url", "Text", "Keywords", "Polarity", "Subjectivity"]
  with open(path, "r") as textfile:
     for key in data_order:
         if key == "Polarity" or key == "Subjectivity":
             data[key] = float(textfile.readline())
         else:
             data[key] = textfile.readline()
  return data

def index(request):
    data_articles = listdir("article_samples/")
    article_dict = {}
    newsoutlets = []
    for article in data_articles:
        if article.endswith(".txt"):
          newsoutlet = article.split("_")[0]
          article_dict.update(ReadAndAddUrl(article_dict,
                                            "article_samples/"+article,
                                            newsoutlet))
          if newsoutlet not in newsoutlets:
              newsoutlets.append(newsoutlet)
    db_article_dict = GetArticleSchemeDict(newsoutlets)
    article_dict.update(db_article_dict)
    return render(request, "index.html", article_dict)
