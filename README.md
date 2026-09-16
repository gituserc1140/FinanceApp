# MoneyOS UK

MoneyOS UK is a modular personal finance dashboard for UK users, built as a lightweight MVP for Streamlit Community Cloud free-tier deployment.

## Features

- Dashboard: assets, liabilities, net worth, savings rate, monthly summary, and rule-based financial insights
- Net Worth Tracker: add/edit assets and liabilities, save historical snapshots, net worth trend and allocation charts
- Financial Goal Planner: create goals, update progress, and forecast completion
- Financial Health Score: score out of 100 with personalised recommendations
- FIRE Calculator: FIRE number, estimated retirement age, and wealth projection chart
- Subscription Audit Tool: upload CSV statements, detect recurring transactions, annual subscription cost, and largest recurring expense
- Cash Flow Forecast: historical cash flow plus 3/6/12 month projections
- Side Hustle Profit Tracker: monthly revenue/cost tracking, profit margin, and break-even analysis

## Tech Stack

- Python 3.12
- Streamlit
- Pandas
- Plotly
- SQLite

## Project Structure

```text
project/
├── app.py
├── pages/
├── services/
├── database/
├── models/
├── utils/
├── assets/
├── requirements.txt
└── README.md
```

## Run Locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the app:

```bash
streamlit run app.py
```

## Demo Data

- The app auto-initialises an SQLite database (`moneyos_uk.db`) with demo records on first run.
- An example bank statement CSV is provided at `/home/runner/work/FinanceApp/FinanceApp/assets/demo_bank_statement.csv` for Subscription Audit testing.

## Deployment Notes (Streamlit Community Cloud)

- No paid APIs required.
- Lightweight local SQLite usage.
- Cached data reads reduce rerender/database overhead.
- Rule-based insights engine avoids external AI API usage.

## Portfolio Positioning

MoneyOS UK is built as a professional SaaS-style portfolio project with clean architecture and clear separation between UI and business logic, while remaining scalable for future AI integrations.
