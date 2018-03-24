from django.db import models
from django.contrib.postgres.fields import ArrayField

class TruncatingCharField(models.CharField):
    def get_prep_value(self, value):
        value = super(TruncatingCharField, self).get_prep_value(value)
        if value:
            return value[:self.max_length]
        return value

class ArticleScheme(models.Model):
    title = TruncatingCharField(max_length=200)
    newsoutlet = TruncatingCharField(max_length=10)
    url = TruncatingCharField(max_length=200)
    date_joined = models.DateField()
    text = TruncatingCharField(max_length=100)
    polarity = TruncatingCharField(max_length=4)
    subjectivity = TruncatingCharField(max_length=4)
    keywords = ArrayField(TruncatingCharField(max_length=10), blank=True)

    def __str__(self):
        return ("title:{}\nnewsoutet:{}\nurl:{}\ndate_joined:{}"
        + "\ntext:{}\npolarity:{}\nsubjectivity:{}\nkeywords:{}").format(
          self.title, self.newsoutlet, self.url, self.date_joined, self.text,
          self.polarity, self.subjectivity, str(self.keywords)
        )
