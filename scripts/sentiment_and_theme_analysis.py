import pandas as pd
import spacy
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict

# Load data
df = pd.read_csv('data/bank_reviews.csv')

# Sentiment Analysis
classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')
def get_sentiment(text):
    if not text or len(text.strip()) == 0:
        return 'NEUTRAL', 0.5
    result = classifier(text[:512])[0]  # Truncate to 512 tokens
    label = result['label'].upper()
    score = result['score']
    return label, score

df['sentiment_label'], df['sentiment_score'] = zip(*df['review'].apply(get_sentiment))

# Thematic Analysis
nlp = spacy.load('en_core_web_sm')

# Preprocessing for thematic analysis
def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return ' '.join(tokens)

df['processed_text'] = df['review'].apply(preprocess_text)

# Extract keywords using TF-IDF
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=100)
tfidf_matrix = vectorizer.fit_transform(df['processed_text'])
feature_names = vectorizer.get_feature_names_out()

# Manual theme clustering
themes = {
    'CBE': {
        'Account Access Issues': ['login error', 'authentication fail', 'pin issue'],
        'Transaction Performance': ['slow transfer', 'transfer fail', 'loading delay'],
        'User Interface': ['intuitive ui', 'poor summary', 'ui change'],
        'Customer Support': ['support unresponsive', 'contact issue'],
        'Feature Requests': ['fingerprint login', 'qr code', 'budget tool']
    },
    'BOA': {
        'Account Access Issues': ['login fail', 'zero balance', 'authentication bug'],
        'Transaction Performance': ['slow load', 'transfer error', 'et-switch fail'],
        'User Interface': ['poor design', 'logo issue', 'unresponsive ui'],
        'Customer Support': ['support delay', 'unresolved issue'],
        'Feature Requests': ['fingerprint login', 'faster transfer']
    },
    'Dashen': {
        'Account Access Issues': ['login issue', 'account access'],
        'Transaction Performance': ['transfer speed', 'payment delay'],
        'User Interface': ['clean ui', 'navigation ease'],
        'Customer Support': ['support response', 'helpdesk'],
        'Feature Requests': ['biometric login', 'transaction limit']
    }
}

# Assign themes to reviews
def assign_themes(text, bank):
    doc = nlp(text.lower())
    review_themes = []
    for theme, keywords in themes[bank].items():
        if any(keyword in text.lower() for keyword in keywords):
            review_themes.append(theme)
    return ', '.join(review_themes) if review_themes else 'Other'

df['theme'] = df.apply(lambda x: assign_themes(x['review'], x['bank']), axis=1)


# Save results in the 'data' folder
output_df = df[['review_id', 'review', 'sentiment_label', 'sentiment_score', 'theme']]
output_df.to_csv('data/sentiment_themes.csv', index=False)
print("Saved sentiment and theme analysis to data/sentiment_themes.csv")


# Aggregate sentiment by bank and rating
print(df.groupby(['bank', 'rating'])['sentiment_score'].mean())