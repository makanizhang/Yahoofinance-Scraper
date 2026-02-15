# Yahoofinance-Scraper

# Stock Data Scraper 📈

A lightweight, command-line Python utility to fetch historical market data from Yahoo Finance. This tool automates the process of downloading stock prices, cleaning the data, and exporting it to a structured CSV format (Also relational databases).

## Features

* **Multi-Interval Support:** Fetch data in various timeframes (1m, 2m, 5m, 1h, 1d, etc.).
* **Data Standardization:** Automatically renames and formats columns for consistency.
* **Robust Error Handling:** Skips missing tickers without crashing and logs warnings.
* **Rate Limiting:** Built-in sleep timers to stay within API usage limits.
* **CLI Ready:** Easy to use via terminal arguments.

---

## Getting Started

### Prerequisites

Ensure you have Python 3.x installed. You will need the following libraries:

```bash
pip install yfinance pandas

```


---

## 🛠 Usage

Run the script from your terminal using the following arguments:

| Argument | Description | Example |
| --- | --- | --- |
| `--ticker` | The stock symbol (Required) | `AAPL` |
| `--start` | Start date (YYYY-MM-DD) | `2023-01-01` |
| `--end` | End date (YYYY-MM-DD) | `2024-01-01` |
| `--interval` | Data frequency (Default: 1d) | `1h` |

### Example Command

```bash
python scraper.py --ticker TSLA --start 2023-01-01 --end 2023-12-31 --interval 1d

```

---

## 📊 Output Format

The script generates a `stock_data.csv` file with the following structure:

| symbol | date | interval | open | close | high | low | volume | dividends |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TSLA | 2023-01-03 | 1d | 118.47 | 108.10 | 118.80 | 104.64 | 231402800 | 0.0 |

---
