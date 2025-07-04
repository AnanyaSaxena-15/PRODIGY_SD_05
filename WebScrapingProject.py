import requests
from bs4 import BeautifulSoup
import csv
from tabulate import tabulate  # <-- For table output

# Base URL of the site
base_url = 'http://books.toscrape.com/catalogue/page-{}.html'

# Empty list to hold all book data
book_data = []

# Loop through the first 5 pages
for page in range(1, 6):
    print(f"Scraping Page {page}...")
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    books = soup.find_all('article', class_='product_pod')

    for book in books:
        # Extract book title
        title = book.h3.a['title']

        # Extract and clean price, then convert to INR
        raw_price = book.find('p', class_='price_color').text.strip()
        clean_price = ''.join(c for c in raw_price if c.isdigit() or c == '.')
        inr_price = round(float(clean_price) * 105, 2)  # 1 GBP = ₹105

        # Extract rating (e.g., 'Three')
        rating = book.p['class'][1]

        # Add to list
        book_data.append([title, f"₹{inr_price}", rating])

# Save data to CSV
filename = 'books_data.csv'
with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Price (₹)', 'Rating'])
    writer.writerows(book_data)

# Print to terminal in table format
print("\n--- Scraped Books ---\n")
print(tabulate(book_data, headers=["Title", "Price (₹)", "Rating"], tablefmt="grid"))

print(f"\n✅ Done! {len(book_data)} books saved to {filename}")
