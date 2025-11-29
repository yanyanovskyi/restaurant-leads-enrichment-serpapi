# Restaurant Leads Enrichment via SerpAPI

This Python project automatically **enriches restaurant leads** with data from Google using the SerpAPI search engine.

Given an Excel file with restaurant **Name** and **City**, the script extracts:

- Official website / menu link  
- Google reviews count  
- Phone number  
- Facebook page  
- Instagram profile  
- Delivery platforms (Glovo, Wolt, Pyszne, Uber Eats, Bolt Food, etc.)

The final result is exported into a new Excel file with fully enriched data.

---

## ⚙️ Features

✔ Enriches restaurant leads from Google  
✔ Extracts and cleans social media links  
✔ Detects delivery platforms from all found URLs  
✔ Works with any list of restaurants  
✔ Uses SerpAPI (safe: API key loaded from environment variable)  
✔ Saves results into `leads_with_info.xlsx`  

---

## 📥 Input format

Create an Excel file **`leads.xlsx`** with at least the following columns:

| Name        | City     |
|-------------|----------|
| Pizza Roma  | Kraków   |
| Sushi House | Warszawa |

---

## 📤 Output

After running the script, you will get:

**`leads_with_info.xlsx`**

Additional columns include:

- `Website`  
- `Google Reviews`  
- `Phone`  
- `Facebook`  
- `Instagram`  
- `Order` (detected delivery platforms, e.g. `glovo, wolt, pyszne`)  

---

## 🛠 Tech Stack

- **Python 3.10+**
- **pandas** — Excel processing  
- **requests** — API requests  
- **openpyxl** — Excel writing  

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/yanyanovskyi/restaurant-leads-enrichment-serpapi.git
cd restaurant-leads-enrichment-serpapi
