from django.db import models

# Create your models here.

class SentimentAnalysisResult(models.Model):
    user_input = models.TextField()
    sentiment = models.CharField(max_length=10)
    sentiment_score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Meta:
    app_label = 'sentiment'