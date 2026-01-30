import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from threading import Thread, current_thread
import time

start_date = input("Enter Start Date: YYYY-MM-DD: ")
end_date = input("Enter End Date: YYYY-MM-DD: ")

base_url = "https://arraf.app/gold/price/egypt/"
all_data = []
lock = Thread().lock = None  # for thread-safe append

# Prepare dates list
start_dt = datetime.strptime(start_date, "%Y-%m-%d")
end_dt = datetime.strptime(end_date, "%Y-%m-%d")
delta = timedelta(days=1)
dates_list = []
current_dt = start_dt
while current_dt <= end_dt:
    dates_list.append(current_dt.strftime("%Y-%m-%d"))
    current_dt += delta

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Connection": "keep-alive"
})

def safe_get(url, thread_name, date_str, tries=5, timeout=15):
    for attempt in range(1, tries + 1):
        try:
            return session.get(url, timeout=timeout)
        except requests.exceptions.Timeout:
            print(f"[{thread_name}] Timeout on {date_str} (attempt {attempt}/{tries}), retrying in 1s")
            time.sleep(1)
        except Exception as e:
            print(f"[{thread_name}] Error on {date_str} (attempt {attempt}/{tries}): {e}, retrying in 1s")
            time.sleep(1)
    print(f"[{thread_name}] Failed to fetch {date_str} after {tries} attempts")
    return None

def fetch_dates(thread_index, dates):
    global all_data
    thread_name = f"T{thread_index+1}"
    for date_str in dates:
        print(f"[{thread_name}] Processing {date_str} ...")
        response = safe_get(base_url + date_str, thread_name, date_str)
        if response is None or response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        try:
            ons = soup.select_one(".columns.is-flex-tablet-p .column:nth-child(1) .flight-price").text.strip()
            g_gold = soup.select_one(".columns.is-flex-tablet-p .column:nth-child(3) .flight-price").text.strip()
        except:
            ons = g_gold = ""

        cards = soup.select(".flight-card")
        prices = {}
        for card in cards:
            label = card.select_one(".start span").text.strip()
            ends = card.select(".end")
            buy = ends[0].select_one("span").text.strip() if len(ends) > 0 else ""
            sell = ends[1].select_one("span").text.strip() if len(ends) > 1 else ""
            prices[label] = {"buy": buy, "sell": sell}

        record = {
            "التاريخ": date_str,
            "سعر الأونصة": ons,
            "سعر جنيه الذهب": g_gold,
            "سعر عيار 24 شراء": prices.get("سعر عيار ٢٤", {}).get("buy", ""),
            "سعر عيار 24 بيع": prices.get("سعر عيار ٢٤", {}).get("sell", ""),
            "سعر عيار 22 شراء": prices.get("سعر عيار ٢٢", {}).get("buy", ""),
            "سعر عيار 22 بيع": prices.get("سعر عيار ٢٢", {}).get("sell", ""),
            "سعر عيار 21 شراء": prices.get("سعر عيار ٢١", {}).get("buy", ""),
            "سعر عيار 21 بيع": prices.get("سعر عيار ٢١", {}).get("sell", ""),
            "سعر عيار 18 شراء": prices.get("سعر عيار ١٨", {}).get("buy", ""),
            "سعر عيار 18 بيع": prices.get("سعر عيار ١٨", {}).get("sell", ""),
            "سعر الأونصة بالدولار": prices.get("سعر الاونصة بالدولار", {}).get("buy", ""),
            "سعر دولار الصاغة": prices.get("سعر دولار الصاغة", {}).get("buy", ""),
        }

        # Append thread-safely
        all_data.append(record)
        time.sleep(0.1)  # slight delay to reduce overload

# Split dates in round-robin style
threads_count = 15
thread_dates = [[] for _ in range(threads_count)]
for i, date_str in enumerate(dates_list):
    thread_dates[i % threads_count].append(date_str)

threads = []
for i in range(threads_count):
    t = Thread(target=fetch_dates, args=(i, thread_dates[i]))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# Sort by date and renumber
df = pd.DataFrame(all_data)
df['التاريخ'] = pd.to_datetime(df['التاريخ']).dt.date
df = df.sort_values(by='التاريخ').reset_index(drop=True)
df.insert(0, "م", range(1, len(df)+1))

df.to_excel("gold_prices_multithread.xlsx", index=False)
print("\nData Saved at gold_prices.xlsx")
