"""Daily best-effort investor dashboard data collector; unofficial sources, personal research."""
import datetime as dt
import json
import math
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote as urlquote
import feedparser
import yfinance as yf

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data"/"dashboard.json"
COMPANIES=json.loads((ROOT/"companies.json").read_text())
OLD=json.loads(DATA.read_text()) if DATA.exists() else {"companies":{}}
NOW=dt.datetime.now(dt.timezone.utc).isoformat()

def numeric(x):
    try:
        v=float(x)
        return v if math.isfinite(v) else None
    except (TypeError,ValueError,OverflowError): return None

def first_row(df,labels):
    if df is None or df.empty: return None
    for label in labels:
        if label in df.index:
            for item in df.loc[label].values:
                n=numeric(item)
                if n is not None:return n
    return None

def iso_date(x):
    if isinstance(x,(list,tuple)): return iso_date(x[0]) if x else None
    if isinstance(x,(dt.datetime,dt.date)):return x.strftime("%Y-%m-%d")
    if isinstance(x,str):
        try:return dt.date.fromisoformat(x[:10]).isoformat()
        except ValueError: pass
    return None

def fetch(item):
    symbol=item["ticker"]
    prior=OLD.get("companies",{}).get(symbol,{})
    out={**prior,**item,"error":None,"last_attempt_at":NOW}
    try:
        obj=yf.Ticker(symbol)
        meta=obj.get_info() or {}
        hist=obj.history(period="3mo",auto_adjust=False)
        series=hist["Close"].dropna() if hist is not None and not hist.empty else None
        q={}
        if series is not None and len(series):
            q={"price":numeric(series.iloc[-1]),
               "date":series.index[-1].strftime("%Y-%m-%d"),
               "previous_close":numeric(series.iloc[-2]) if len(series)>1 else None,
               "history":[{"date":d.strftime("%Y-%m-%d"),"price":numeric(p)} for d,p in series.tail(65).items()]}
            if len(series)>21:q["month_change_pct"]=numeric((series.iloc[-1]/series.iloc[-22]-1)*100)
        for field,key in [("market_cap","marketCap"),("pe","trailingPE"),("forward_pe","forwardPE"),("ps","priceToSalesTrailing12Months"),("fifty_two_week_high","fiftyTwoWeekHigh"),("fifty_two_week_low","fiftyTwoWeekLow")]:
            q[field]=numeric(meta.get(key))
        if q.get("price") is not None:out["quote"]=q
        out["quote_checked_at"]=NOW
        f={}
        for field,key in [("revenue_ttm","totalRevenue"),("revenue_growth","revenueGrowth"),("gross_margin","grossMargins"),("operating_margin","operatingMargins"),("profit_margin","profitMargins"),("free_cash_flow","freeCashflow"),("total_cash","totalCash"),("total_debt","totalDebt"),("operating_cash_flow","operatingCashflow"),("ebitda","ebitda"),("forward_eps","forwardEps")]:
            f[field]=numeric(meta.get(key))
            if f[field] is None:f[field]=prior.get("fundamentals",{}).get(field)
        try:
            stmt=obj.quarterly_income_stmt
            f["latest_quarter_revenue"]=first_row(stmt,["Total Revenue","Operating Revenue"])
            f["latest_quarter_net_income"]=first_row(stmt,["Net Income","Net Income Common Stockholders"])
            if stmt is not None and not stmt.empty:f["financial_period_end"]=str(stmt.columns[0].date())
        except Exception:pass
        out["fundamentals"]=f
        out["fundamentals_checked_at"]=NOW
        try:
            cal=obj.calendar
            if hasattr(cal,"to_dict"):cal=cal.to_dict()
            if isinstance(cal,dict):
                date=iso_date(cal.get("Earnings Date"))
                if date:out["earnings_date"]=date
        except Exception:pass
    except Exception as e:
        out["error"]="Market-data fetch failed: "+type(e).__name__
    try:
        query=urlquote('"' + item["name"] + '" ' + symbol + ' stock earnings when:7d')
        url="https://news.google.com/rss/search?q="+query+"&hl=en-US&gl=US&ceid=US:en"
        feed=feedparser.parse(url,request_headers={"User-Agent":"Mozilla/5.0"})
        articles=[]
        for x in feed.entries[:8]:
            source=x.get("source") or {}
            articles.append({"title":x.get("title",""),"url":x.get("link",""),"published":x.get("published",""),"source":source.get("title","") if isinstance(source,dict) else ""})
        if articles:
            out["news"]=articles
            out["news_checked_at"]=NOW
    except Exception:pass
    return symbol,out

def main():
    collected={}
    with ThreadPoolExecutor(max_workers=3) as pool:
        for future in as_completed([pool.submit(fetch,item) for item in COMPANIES]):
            symbol,value=future.result()
            collected[symbol]=value
            print(symbol,"quote",bool(value.get("quote",{}).get("price")),"news",len(value.get("news",[])),value.get("error"))
    DATA.parent.mkdir(parents=True,exist_ok=True)
    DATA.write_text(json.dumps({"updated_at":NOW,"data_provider":"Yahoo Finance (unofficial yfinance), Google News RSS","companies":collected},indent=2,ensure_ascii=False,allow_nan=False)+"\n")

if __name__=="__main__":main()
