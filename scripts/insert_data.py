import pandas as pd
import psycopg2
from psycopg2 import sql

def get_db_connection():
    return psycopg2.connect(
        host='localhost',
        port='5432',
        dbname='week_2',
        user='postgres',
        password='1993minte'
    )

def insert_combined_reviews():
    try:
        # Connect to database
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Load both CSV files
        sentiment_df = pd.read_csv('../data/sentiment_themes.csv')
        reviews_df = pd.read_csv('../data/bank_reviews.csv')
        
        # Merge data on review_id
        combined_df = pd.merge(
            reviews_df,
            sentiment_df[['review_id', 'sentiment_label', 'sentiment_score', 'theme']],
            on='review_id',
            how='left'
        )
        
        # Get or create bank_id mapping
        cur.execute("SELECT bank_name, bank_id FROM banks")
        bank_map = {name: id for name, id in cur.fetchall()}
        
        # Insert any missing banks
        missing_banks = set(combined_df['bank']) - set(bank_map.keys())
        for bank in missing_banks:
            cur.execute(
                "INSERT INTO banks (bank_name) VALUES (%s) RETURNING bank_id",
                (bank,)
            )
            bank_map[bank] = cur.fetchone()[0]
        conn.commit()
        
        # Prepare data for insertion
        data = []
        for _, row in combined_df.iterrows():
            data.append((
                row['review_id'],
                bank_map[row['bank']],
                row['review'],
                row['rating'],
                row['date'],
                row['source'],
                row['sentiment_label'],
                row['sentiment_score'],
                row['theme']
            ))
        
        # Execute batch insert
        cur.executemany("""
            INSERT INTO reviews 
            (review_id, bank_id, review_text, rating, review_date, 
             source, sentiment_label, sentiment_score, theme)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (review_id) DO NOTHING
        """, data)
        
        conn.commit()
        print(f"Successfully inserted {cur.rowcount} reviews")
        
    except Exception as e:
        print(f"Error: {e}")
        if conn: conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()

if __name__ == "__main__":
    insert_combined_reviews()