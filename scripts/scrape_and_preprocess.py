import pandas as pd
from google_play_scraper import reviews, Sort
from datetime import datetime
import uuid
import os

# Define app IDs for the banks (replace with actual Google Play Store IDs)
app_ids = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking',
    'Dashen': 'com.dashen.dashensuperapp'
}

# Function to scrape reviews
def scrape_reviews(app_id, bank_name, count=400):
    result, _ = reviews(
        app_id,
        lang='en',
        country='et',
        sort=Sort.NEWEST,
        count=count
    )
    data = []
    for review in result:
        data.append({
            'review_id': str(uuid.uuid4()),
            'review': review['content'],
            'rating': review['score'],
            'date': review['at'].strftime('%Y-%m-%d'),
            'bank': bank_name,
            'source': 'Google Play'
        })
    return data

output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(output_dir, exist_ok=True)
# Collect reviews for all banks
all_reviews = []
for bank, app_id in app_ids.items():
    print(f"Scraping reviews for {bank}...")
    reviews_data = scrape_reviews(app_id, bank)
    all_reviews.extend(reviews_data)

# Create DataFrame
df = pd.DataFrame(all_reviews)

# Preprocessing
# Remove duplicates based on review_id and review text
df.drop_duplicates(subset=['review_id', 'review'], keep='first', inplace=True)

# Handle missing data
df['review'].fillna('', inplace=True)
df['rating'].fillna(df['rating'].median(), inplace=True)

# Ensure date is in YYYY-MM-DD format
df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

# Save to CSV
df.to_csv('../data/bank_reviews.csv', index=False)
print("Saved cleaned reviews to ../data/bank_reviews.csv")

# Summary
print(f"Total reviews collected: {len(df)}")
print(f"Missing data: {df.isnull().sum()}")