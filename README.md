# Signal Desk — Daily Investment Dashboard

A deployable personal-research HTML dashboard tracking GLW, SPCX, MU, AMD, ETSY, SNDK, BE, and PATH. Features: stock prices and changes, three-month price plots, market caps, valuation, quarterly/trailing fundamentals, earnings-date field, recent news, search, sorting, and investor-relations links.

## Publish a permanent public URL (GitHub Pages)

1. Create a **public** GitHub repository named `signal-desk` (or another name). Upload the **contents** of this folder, including `.github/workflows/daily.yml` (uploading a ZIP as one file will NOT work). You can also clone and push this folder with Git.
2. Open repository **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Open **Actions → Refresh and publish investment dashboard → Run workflow**. Allow Actions to run if prompted.
4. Once deployment finishes successfully, your link is `https://YOUR-USERNAME.github.io/signal-desk/` (substitute your GitHub username and repository name). To verify, open the site and check the last fetch timestamp. A successful workflow run does not necessarily mean all providers supplied data.
5. The workflow automatically attempts updates every day at 12:15 UTC and at 22:15 UTC on weekdays. GitHub schedule execution may be delayed or skipped and market data may not update on market holidays.

## Add a new company

Edit `companies.json`, appending an object:

```json
{"ticker":"MSFT","name":"Microsoft","theme":"AI software","thesis":"Cloud and enterprise AI demand","ir":"https://www.microsoft.com/en-us/Investor"}
```

Commit the change. The workflow automatically reruns, fetches data, and publishes the new company card. `companies.json` is the source of truth, so no HTML editing is needed.

## Data and important constraints

- Market data/fundamentals/earnings-date field: `yfinance` (unofficial Yahoo Finance access, intended for **personal use only** and subject to provider terms, limits, blocking, coverage and potential data delays). No API key required for the prototype.
- News: Google News RSS search. Articles may be irrelevant or duplicates. External links open the source; news is not independently verified.
- A successful fetch is **not** guaranteed. The UI reports the latest check, latest close date, and missing fields. Existing data is retained on transient fetch failure. Confirm specific earnings dates via company investor-relations pages.
- Revenue and financial fields can use distinct fiscal period endpoints. yfinance's `revenueGrowth` is an annualized year-over-year quarterly ratio when available; validate against SEC filings before investment decisions.
- The original build intentionally leaves all prices **blank** until the first successful live update; no invented prices are embedded.
- For a private dashboard, commercial use, higher reliability, more financial history, earnings transcripts, SEC filing parsing, alerts, and licensed market feeds: replace collector calls with an authenticated commercial provider and move data collection to a private server / scheduler. Do not place API keys in public HTML or GitHub repository files; use encrypted GitHub Actions secrets.
- Do not regard GitHub Pages as a secure home for private portfolio balances; published static files are public.

## Local preview

From the folder run `python3 -m http.server 8000`, then visit `http://localhost:8000`. Initial sample data is empty, pending a refresh. To populate locally, run `pip install -r requirements.txt && python update_data.py` with a working Internet connection.