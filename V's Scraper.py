import csv
import requests
from bs4 import BeautifulSoup

URL = "http://quotes.toscrape.com/"
OUTPUT_FILE = "quotes.csv"

def scrape_quotes():
    """Scrape quotes, authors, and tags from the target website and save to CSV."""
    print(f"Fetching data from {URL}...")
    
    try:
        response = requests.get(URL, timeout=10)
        # Raise an exception for HTTP error codes (like 404 or 500)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"\n[!] Network or HTTP error occurred: {e}\n")
        return

    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all quote elements on the page
    quote_elements = soup.find_all("div", class_="quote")
    
    if not quote_elements:
        print("\n[!] No quotes found on the page. The website structure may have changed.\n")
        return

    scraped_data = []
    for element in quote_elements:
        text = element.find("span", class_="text").get_text(strip=True)
        author = element.find("small", class_="author").get_text(strip=True)
        
        # Extract tags associated with the quote
        tags = [tag.get_text(strip=True) for tag in element.find_all("a", class_="tag")]
        tags_str = ", ".join(tags)
        
        scraped_data.append({
            "Quote": text,
            "Author": author,
            "Tags": tags_str
        })

    # Save the extracted data into a CSV file
    try:
        with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["Quote", "Author", "Tags"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            for item in scraped_data:
                writer.writerow(item)
                
        print(f"\n[+] Success! Scraped {len(scraped_data)} quotes and saved them to '{OUTPUT_FILE}'.\n")
        
    except IOError as e:
        print(f"\n[!] Error saving to CSV file: {e}\n")

if __name__ == "__main__":
    scrape_quotes()
