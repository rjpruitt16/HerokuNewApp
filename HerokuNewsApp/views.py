from django.shortcuts import render
from os import listdir

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
    data["Text"] = data["Text"][:150]
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
    for article in data_articles:
        if article.endswith(".txt"):
          name = article.split("_")
          article_dict.update(ReadAndAddUrl(article_dict, "article_samples/"+article, name[0]))
        print(article_dict.keys())
    return render(request, "index.html", article_dict)
