# Sales Trend Dashboard

An interactive sales and profit dashboard for a retail store (2015–2018). It shows how sales and profit grow over time, which season drives the business, which regions and customer segments earn the most, and which products lose money.

**Live demo:** `https://<your-username>.github.io/sales-trend-dashboard/`

![Dashboard preview](preview.png)

## Key insights

- **$2.26M in sales and $401.96K in profit**, a **17.8% profit margin** over four years.
- **Q4 is the peak season**: it brings roughly 39% of yearly sales, driven by Technology and Furniture.
- **2018 was the strongest year**, with sales up about 32% on 2017.
- **The Consumer segment earns about half of all profit**, Corporate about 28%, Home Office about 20%.
- **West and East lead the regions**; Central has the lowest margin.
- **Tables lose money** despite strong sales, mostly because of heavy discounts.

## Features

- KPI cards: total sales, total profit, profit margin, QoQ and MoM profit growth, and year-on-year change
- Year and region filters that update every chart (you can also click a region bar)
- Sales and profit trend: by quarter, or by month when a year is selected
- Quarterly performance, profit by segment (donut) and seasonal profit (treemap)
- Sortable sub-category profitability table that highlights loss-making products
- Light and dark mode, responsive layout and hover tooltips

## Project structure

```
index.html               ← the full dashboard (one self-contained file, open it in any browser)
data/sales_orders.csv    ← raw order-level data (10,169 rows), for Power BI, Excel or Python
data/sales_monthly.csv   ← monthly summary the dashboard reads
src/index.html           ← dashboard source (HTML, CSS, D3.js)
src/build.js             ← rebuilds index.html from src/ and data/  (node src/build.js)
powerbi/SalesTrend.pbip  ← Power BI project (open in Power BI Desktop, save as .pbix)
src/build_pbip.py        ← regenerates the Power BI project
```

## Dataset

`sales_orders.csv` is in the style of the retail "Superstore" dataset: Order ID, Order Date, Ship Date, Ship Mode, Customer ID, Segment, Region, State, Category, Sub-Category, Quantity, Discount, Sales and Profit.

> Note: this is a **sample dataset** generated to recreate my original Power BI project, whose source files were lost. Its totals and patterns match the original dashboard.

## Power BI version

`powerbi/SalesTrend.pbip` is the Power BI project: data model, Calendar table, DAX measures and the report page. The order data is embedded in the model, so it needs no external file.

1. Open `powerbi/SalesTrend.pbip` in Power BI Desktop. If it asks, turn on **File → Options → Preview features → Power BI Project (.pbip) save option** and **Store reports using enhanced metadata format (PBIR)**, then restart.
2. Click **Refresh** to load the data.
3. Use **File → Save as → Power BI file (*.pbix)** to get a single `.pbix`.

`src/build_pbip.py` regenerates the project from `data/sales_orders.csv`.

Main measures:

```DAX
Total Sales   = SUM ( Orders[Sales] )
Total Profit  = SUM ( Orders[Profit] )
Profit Margin = DIVIDE ( [Total Profit], [Total Sales] )

QoQ Profit Growth =
VAR Prev = CALCULATE ( [Total Profit], DATEADD ( 'Date'[Date], -1, QUARTER ) )
RETURN DIVIDE ( [Total Profit] - Prev, Prev )

MoM Profit Growth =
VAR Prev = CALCULATE ( [Total Profit], DATEADD ( 'Date'[Date], -1, MONTH ) )
RETURN DIVIDE ( [Total Profit] - Prev, Prev )

YoY Sales Growth =
VAR Prev = CALCULATE ( [Total Sales], SAMEPERIODLASTYEAR ( 'Date'[Date] ) )
RETURN DIVIDE ( [Total Sales] - Prev, Prev )
```

## Publishing to GitHub Pages

1. Create a new public repository, for example `sales-trend-dashboard`.
2. Upload every file in this folder (drag and drop on github.com works).
3. Go to **Settings → Pages**, set **Source** to *Deploy from a branch*, choose `main` and `/ (root)`, and save.
4. After about a minute the dashboard is live at `https://<your-username>.github.io/sales-trend-dashboard/`.

## Tools

Power BI (original design) · D3.js · HTML/CSS/JavaScript · Python (data generation)
