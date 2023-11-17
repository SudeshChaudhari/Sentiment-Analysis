from django.contrib import admin
from .models import SentimentAnalysisResult

# # Register your models here.
@admin.register(SentimentAnalysisResult)
class SentimentAnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('user_input', 'sentiment', 'sentiment_score', 'timestamp')
