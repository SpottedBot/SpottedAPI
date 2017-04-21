from django.core.management.base import BaseCommand
from processing.learning import SpottedAnalyzer


class Command(BaseCommand):
    help = 'Re-builds the classifier'

    def handle(self, *args, **options):

        SpottedAnalyzer(classifier='nb').fit(reload=False)
        SpottedAnalyzer(classifier='nb', detailed=True).fit(reload=False)
        SpottedAnalyzer(classifier='svm').fit(reload=False)
        SpottedAnalyzer(classifier='svm', detailed=True).fit(reload=False)

        return "Success"
