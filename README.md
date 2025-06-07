# B5W2: Customer Experience Analytics for Fintech Apps

## Project Overview
This project focuses on analyzing customer satisfaction with mobile banking apps by collecting and processing user reviews from the Google Play Store for three Ethiopian banks:
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

The goal is to scrape app reviews, analyze sentiments and themes, and visualize insights to simulate the role of a Data Analyst at Omega Consultancy, a firm advising banks.

## Business Objective
Omega Consultancy is supporting banks to improve their mobile apps to enhance customer retention and satisfaction. As a Data Analyst, the role involves:
- Scraping user reviews from the Google Play Store
- Analyzing sentiment (positive/negative/neutral) and extracting themes (e.g., "bugs", "UI")
- Identifying satisfaction drivers (e.g., speed) and pain points (e.g., crashes)
- Storing cleaned review data in an Oracle database
- Delivering a report with visualizations and actionable recommendations

## Project Structure
```
fintech_app_analytics/
├── data/
│   ├── raw/         # Raw scraped data
│   └── processed/   # Cleaned and processed data
├── scripts/         # Python scripts for scraping, analysis, and database operations
├── notebooks/       # Jupyter notebooks for analysis and visualization
├── database/        # Database schema and SQL scripts
├── visualizations/  # Generated plots and visualizations
├── reports/         # Final reports and presentations
└── README.md        # Project documentation
```

## Tasks
1. **Data Collection and Preprocessing**
   - Scrape reviews from Google Play Store
   - Preprocess them for analysis
   - Manage code via GitHub

2. **Sentiment and Thematic Analysis**
   - Quantify review sentiment
   - Identify themes to uncover satisfaction drivers and pain points

3. **Store Cleaned Data in Oracle**
   - Design and implement a relational database
   - Store the cleaned and processed review data

4. **Insights and Recommendations**
   - Derive insights from sentiment and themes
   - Visualize results and recommend app improvements

## Scenarios
The project simulates real consulting tasks faced by product, marketing, and engineering teams:

1. **Scenario 1: Retaining Users**
   - Analyze slow loading issues during transfers across banks

2. **Scenario 2: Enhancing Features**
   - Extract desired features through keyword and theme extraction

3. **Scenario 3: Managing Complaints**
   - Analyze and track complaints to guide AI chatbot integration

## Key Performance Indicators (KPIs)
- **Proactivity**: Sharing scraping/NLP references
- **Data Quality**: 1,200+ clean reviews with <5% errors
- **Insights**: 3+ drivers/pain points per bank
- **Clarity**: Stakeholder-friendly visualizations

## Technologies Used
- Python for scraping, data processing, and analysis
- NLP libraries for sentiment analysis and theme extraction
- Oracle XE for database storage
- Data visualization libraries for creating insights
- Git for version control

## Timeline
- **Introduction**: June 4, 2024
- **Interim Submission**: June 9, 2024
- **Final Submission**: June 10, 2024

