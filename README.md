# Signal Desk — Daily Investment Dashboard

A deployable personal-research HTML dashboard tracking GLW, SPCX, MU, AMD, ETSY, SNDK, BE, and PATH. Features: stock prices and changes, three-month price plots, market caps, valuation, quarterly/trailing fundamentals, earnings-date field, recent news, search, sorting, and investor-relations links. The research upgrade adds a cross-watchlist headlines feed, upcoming earnings watch, side-by-side financial comparison table, quote coverage and freshness indicators, and GitHub shortcuts to add symbols or trigger updates.

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
## Research dashboard upgrade

- The **Add a stock** button links directly to `companies.json` in GitHub for editing. Commit a correctly formatted JSON entry to trigger a fresh deployment; there is no database or HTML edit necessary.
- The **Run data update** button opens the GitHub Actions workflow. Choose **Run workflow** and run it once. A green check indicates workflow completion, not necessarily fresh quotes for every ticker.
- The cross-company news feed orders provider articles by publication date and presents direct links. Earnings dates are supplied by the provider and must be verified independently.
- The comparison table exposes prices, revenue, growth, market capitalization, P/S and free cash flow side by side. Financial periods and accounting conventions may differ.
- The latest quote date and fetch counts help distinguish fresh data from failed retrievals. A browser refresh merely reloads the most recent published data; it does not execute the collector.
- Stock symbols must be recognized by the financial data source. Unsupported tickers can appear with blank quotes rather than invented values.

## Research Laboratory (new)

Open `research.html` (linked from the main dashboard) after the next successful deployment.

### Research data coverage
- **Historical financials:** up to eight reported quarterly and annual periods for available income statement, balance sheet, and cash-flow lines. Source is unofficial Yahoo Finance via `yfinance`. A missing field shows an em dash, not a made-up number; some quarterly cash flows may be cumulative, so verify filings before comparing quarters.
- **Earnings intelligence:** reported/estimated EPS and a calculated beat/miss percentage, when the source provides both; upcoming dates from the existing provider calendar. Verify all earnings events against company investor relations.
- **Valuation laboratory:** manually controlled revenue growth, terminal free-cash-flow margin, exit EV/FCF multiple, time horizon, required return and net cash. The tool uses a constant share count inferred from market capitalization / price, and does not account for dilution, dividends, interim cash flows, or changes in net cash. The result is an illustrative scenario, **not a price target**.
- **Catalyst alerts:** informational rules for >=5% closing-price moves, earnings dates within 14 days, comparable year-over-year quarterly revenue declines >=10% when enough history exists, and data retrieval failures. These are **snapshot alerts**, not push notifications or real-time monitoring.
- **AI news intelligence:** optional OpenAI model interpretation of sourced headlines only; OFF by default. When OFF, the page still provides source-linked news. Models do not receive full article text, and interpretations are not factual verification.

### Optional AI headline summaries
To enable, open **Settings → Secrets and variables → Actions → New repository secret** in GitHub, name the secret `OPENAI_API_KEY`, paste an OpenAI API key, then run the workflow once. Do not paste API keys into tracked repository files or public HTML. The workflow uses `gpt-4.1-mini` by default and can incur API charges for each company, each refresh. You can remove the secret to disable AI generation; the news links will continue to work. AI errors are shown as unavailable rather than invented summaries.

### Research workflow troubleshooting
Go to **Actions → Refresh and publish investment dashboard → latest run**, and inspect **Refresh research intelligence** and **deploy-pages** steps. A green workflow check means the process finished; it is not proof that each financial field was retrieved. Check the Research Lab's source and period fields. GitHub Pages can take time to update after the workflow completes.

### Adding a ticker
Continue editing `companies.json` and committing valid JSON. The same configuration automatically drives the main dashboard, research collector, and research company selector. The data source must recognize the exchange ticker. No HTML code changes needed.

### Security and limitations
GitHub Pages publishes all JSON datasets publicly. Do not add personal balances, API credentials, or private notes to the data files. For production-grade research, use licensed market data, SEC-source reconciliation, more stringent data-quality checks, and explicit rate-limit/retry handling.

## Current hosting: public GitHub Pages (restored)

The regular `.github/workflows/daily.yml` workflow is restored. It fetches quotes/news and research intelligence and deploys directly to GitHub Pages on pushes, scheduled runs, or manual dispatch. The private Cloudflare migration workflows have been removed.

**Account action needed:** Set repository visibility back to **Public** in GitHub Settings → Danger Zone → Change repository visibility, because ChatGPT's connected GitHub actions cannot change repo visibility. Then confirm Settings → Pages → Build and deployment → GitHub Actions, and run the regular dashboard workflow from Actions.

**Cost safeguard:** Optional AI analysis is off unless Actions variable `SIGNAL_DESK_ENABLE_PAID_AI=true` and `OPENAI_API_KEY` is provided. No credentials belong in the repo or published JSON. Free-tier eligibility depends on current GitHub limits and account usage.

**Public data warning:** The GitHub Pages HTML, JavaScript and published `data/*.json` are publicly accessible and should contain no portfolio balances, account details, credentials, or private investment notes.

## News links (November 2026 fix)

The news collector now uses provider article URLs from Yahoo Finance news metadata instead of Google News RSS redirect tokens, which could lead visitors to Google automated-query error pages. The **More coverage** link opens the ticker's Yahoo Finance news page. The research collector reuses the cleaned headline data. If the news API does not provide a direct HTTPS link, the entry is omitted; missing news is not backfilled with stale redirect links. Publisher websites can still require a subscription or deny access independently. After any change to this collector, run the GitHub Actions deploy workflow to refresh the published JSON; a browser-only refresh will not repair old cached link data.
