from django.shortcuts import render
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from nltk.sentiment import SentimentIntensityAnalyzer
from .models import SentimentAnalysisResult

MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
sia = SentimentIntensityAnalyzer()

def sentiment_analysis(request):
    sentiment = None    
    vader_result = None

    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')

        # Perform sentiment analysis using RoBERTa
        encoded_text = tokenizer(user_input, return_tensors='pt')
        output = model(**encoded_text)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        sentiment_score = scores.tolist()
        sentiment = "Positive" if sentiment_score.index(max(sentiment_score)) == 2 else "Neutral" if sentiment_score.index(max(sentiment_score)) == 1 else "Negative"
        
        # Perform sentiment analysis using VADER
        vader_result = sia.polarity_scores(user_input)

        # Save results to the database
        result = SentimentAnalysisResult(user_input=user_input, sentiment=sentiment, sentiment_score=max(sentiment_score))
        result.save()

        return render(request, 'index.html', {
        'user_input':  user_input,
        'sentiment': sentiment,
        'vader_result': vader_result,
        })
    return render(request, 'index.html')