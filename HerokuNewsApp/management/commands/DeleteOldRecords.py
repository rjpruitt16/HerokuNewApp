from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from HerokuNewsApp.models import ArticleScheme

class Command(BaseCommand):
    def DeleteRecords():
        past_thirty_days = datetime.today() - timedelta(days=29)
        ArticleScheme.objects.filter(date_joined_lte=past_thirty_days).delete()
