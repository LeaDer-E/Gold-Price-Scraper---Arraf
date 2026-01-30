# Gold Price Scraper - Arraf.app

A Python script to scrape gold prices in Egypt from [Arraf.app](https://arraf.app/gold/price/egypt/) for a specified date range, featuring multithreading for high-speed data collection and automatic Excel export.

## ✨ Features

- **⚡ High Speed**: Uses 15 concurrent threads to fetch data simultaneously
- **📊 Excel Export**: Automatically saves data to a clean, formatted Excel file
- **🔄 Auto-Retry**: Built-in retry mechanism (5 attempts) for timeouts and connection errors
- **🛡️ Thread-Safe**: Handles concurrent data writing safely
- **📅 Flexible Date Range**: Select any start and end date (YYYY-MM-DD format)
- **🧹 Sorted Output**: Automatically sorts data by date before saving

## 📋 Requirements

- Python 3.6+
- Libraries: `requests`, `beautifulsoup4`, `pandas`, `openpyxl`

## 🚀 Installation & Usage

### 1. Install Dependencies

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

### 2. Run the Script

```bash
python gold_scraper.py
```

### 3. Enter Date Range

When prompted, enter the dates in YYYY-MM-DD format:

```
Enter Start Date: YYYY-MM-DD: 2024-01-01
Enter End Date: YYYY-MM-DD: 2024-01-31
```

### 4. Output

The script will create a file named `gold_prices_multithread.xlsx` in the same directory, containing all scraped data sorted by date with an index column.

## 📊 Data Structure

The Excel file includes the following columns:

| Column (Arabic) | Description |
|----------------|-------------|
| م | Index (Serial Number) |
| التاريخ | Date |
| سعر الأونصة | Ounce Price |
| سعر جنيه الذهب | Gold Pound Price |
| سعر عيار 24 شراء | 24K - Buy Price |
| سعر عيار 24 بيع | 24K - Sell Price |
| سعر عيار 22 شراء | 22K - Buy Price |
| سعر عيار 22 بيع | 22K - Sell Price |
| سعر عيار 21 شراء | 21K - Buy Price |
| سعر عيار 21 بيع | 21K - Sell Price |
| سعر عيار 18 شراء | 18K - Buy Price |
| سعر عيار 18 بيع | 18K - Sell Price |
| سعر الأونصة بالدولار | Ounce Price in USD |
| سعر دولار الصاغة | Jewelers' Dollar Rate |

## ⚙️ Configuration

You can tweak the following settings in the script:

- **Thread Count**: Change `threads_count = 15` (line 58) to adjust parallel requests
- **Retry Attempts**: Modify `tries=5` in `safe_get()` function for more/less retries
- **Timeout**: Adjust `timeout=15` in `safe_get()` for slower connections
- **Delay**: Change `time.sleep(0.1)` in `fetch_dates()` to reduce server load

## 📝 Sample Output

| م | التاريخ | سعر الأونصة | سعر عيار 24 شراء | سعر عيار 24 بيع |
|---|---------|-------------|------------------|-----------------|
| 1 | 2024-01-01 | 2,050 EGP | 2,460 EGP | 2,480 EGP |
| 2 | 2024-01-02 | 2,055 EGP | 2,465 EGP | 2,485 EGP |

## ⚠️ Disclaimer

- Use responsibly and avoid overwhelming the server with excessive requests
- The script includes built-in delays and retry mechanisms to be respectful to the host server
- Data accuracy depends on the source website (Arraf.app)

## 🛠️ How It Works

1. **Date Generation**: Creates a list of dates between start and end date
2. **Thread Distribution**: Splits dates evenly across 15 threads (round-robin)
3. **Data Fetching**: Each thread fetches HTML pages using `requests.Session()` for connection pooling
4. **Parsing**: Uses BeautifulSoup to extract gold prices from HTML elements
5. **Storage**: Thread-safe appending to a shared list
6. **Export**: Converts to pandas DataFrame, sorts by date, and exports to Excel

---

**Developed for educational purposes. Please respect the website's terms of service.**
