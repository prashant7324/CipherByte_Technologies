import requests
from bs4 import BeautifulSoup
import json
import csv
import logging
import time
import random

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class DataMiner:
    def __init__(
        self,
        urls,
        container_selector,
        field_selectors,
        output_format="json",
        output_file="output"
    ):
        """
        :param urls: List of URLs to scrape
        :param container_selector: CSS selector for item containers on the page
        :param field_selectors: Dict mapping field names to dicts with keys:
            - selector: CSS selector for the field relative to container
            - attribute: attribute to extract (e.g., 'text', 'href', 'src')
        :param output_format: 'json' or 'csv'
        :param output_file: file name without extension
        """
        self.urls = urls
        self.container_selector = container_selector
        self.field_selectors = field_selectors
        self.output_format = output_format.lower()
        self.output_file = f"{output_file}.{self.output_format}"
        self.data = []

    def fetch(self, url):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110"
            )
        }
        try:
            logging.info(f"Fetching URL: {url}")
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            # random sleep to avoid rate limiting
            time.sleep(random.uniform(1, 3))
            return resp.text
        except requests.RequestException as e:
            logging.error(f"Request failed for {url}: {e}")
            return None

    def parse(self, html):
        return BeautifulSoup(html, "html.parser")

    def extract(self, soup):
        items = []
        containers = soup.select(self.container_selector)
        logging.info(f"Found {len(containers)} item containers.")

        for container in containers:
            record = {}
            for field, cfg in self.field_selectors.items():
                sel = cfg.get("selector")
                attr = cfg.get("attribute", "text")
                element = container.select_one(sel)
                if element:
                    if attr == "text":
                        record[field] = element.get_text(strip=True)
                    else:
                        record[field] = element.get(attr)
                else:
                    record[field] = None
            items.append(record)
        return items

    def run(self):
        for url in self.urls:
            html = self.fetch(url)
            if not html:
                continue
            soup = self.parse(html)
            extracted = self.extract(soup)
            self.data.extend(extracted)
        self.store()

    def store(self):
        if self.output_format == "json":
            with open(self.output_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            logging.info(f"Data saved to {self.output_file}")

        elif self.output_format == "csv":
            if not self.data:
                logging.warning("No data to write.")
                return
            with open(self.output_file, "w", newline='', encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.data[0].keys())
                writer.writeheader()
                writer.writerows(self.data)
            logging.info(f"Data saved to {self.output_file}")

        else:
            logging.error(f"Unsupported format: {self.output_format}")


if __name__ == "__main__":
    # Example usage
    urls = [
        "https://example.com/products/page1",
        "https://example.com/products/page2",
    ]
    container_selector = ".product-item"
    field_selectors = {
        "title": {"selector": ".product-title", "attribute": "text"},
        "price": {"selector": ".price", "attribute": "text"},
        "detail_url": {"selector": "a.detail-link", "attribute": "href"},
        "image_url": {"selector": "img.product-image", "attribute": "src"},
    }

    miner = DataMiner(
        urls,
        container_selector,
        field_selectors,
        output_format="csv",
        output_file="products"
    )
    miner.run()