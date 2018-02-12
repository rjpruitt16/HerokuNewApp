from django.db import models
from django.contrib.postgres.fields import ArrayField

class ArticleScheme(models.Model):
    title = models.CharField(max_length=30)
    newsoutlet = models.CharField(max_length=10)
    url = models.CharField(max_length=30)
    date_joined = models.DateField()
    text = models.CharField(max_length=100)
    polarity = models.CharField(max_length=4)
    subjectivity = models.CharField(max_length=4)
    keywords = ArrayField(models.CharField(max_length=10), blank=True)

    def __str__(self):
        return ("title:{}\nnewsoutet:{}\nurl:{}\ndate_joined:{}"
        + "\ntext:{}\npolarity:{}\nsubjectivity:{}\nkeywords:{}").format(
          self.title, self.newsoutlet, self.url, self.date_joined, self.text,
          self.polarity, self.subjectivity, str(self.keywords)
        )
