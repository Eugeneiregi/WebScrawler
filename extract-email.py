import csv
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
import requests
from googlesearch import search
from urllib.parse import urljoin

import time

async def fetch_url(session, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    async with session.get(url, headers=headers) as response:
        response.raise_for_status()
        return await response.text()

async def extract_emails_from_page(session, url):
    try:
        html_content = await fetch_url(session, url)
        soup = BeautifulSoup(html_content, 'html.parser')
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.get_text())
        return emails if emails else None
    except Exception as e:
        return None

async def process_url(session, url):
    try:
        main_page_emails = await extract_emails_from_page(session, url)
        if main_page_emails:
            return url, main_page_emails
        
        # Potential paths for the contact page
        contact_page_paths = ['contact-us', 'contact', 'get-in-touch', 'about-us/contact']
        
        for contact_path in contact_page_paths:
            contact_page_url = urljoin(url, contact_path)
            contact_page_emails = await extract_emails_from_page(session, contact_page_url)
            if contact_page_emails:
                return contact_page_url, contact_page_emails
        
        return url, None
    except Exception as e:
        return url, None

async def scrape_emails_from_urls(input_csv_path, output_csv_path):
    tasks = []

    async with aiohttp.ClientSession() as session:
        with open(input_csv_path, 'r') as input_file:
            csv_reader = csv.reader(input_file)
            header = next(csv_reader)
            try:
                url_column_index = header.index("Website Link")
            except ValueError:
                print("Column 'Website Link' not found in CSV.")
                return

            for row in csv_reader:
                if len(row) <= url_column_index or not row[url_column_index]:
                    print(f"Skipping empty row at line {csv_reader.line_num}")
                    continue
                url = row[url_column_index]
                tasks.append(process_url(session, url))

        results = await asyncio.gather(*tasks)

    with open(output_csv_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(["Website Link", "Extracted Emails"])

        for url, emails_or_error in results:
            csv_writer.writerow([url, ', '.join(emails_or_error) if emails_or_error else ""])

if __name__ == "__main__":
    # Specify the paths for input and output CSV files
    input_csv_path = 'Crawler - Sheet1.csv'
    output_csv_path = 'output.csv'

    # Scrape emails from URLs and store in output CSV
    asyncio.run(scrape_emails_from_urls(input_csv_path, output_csv_path))



# async def fetch_url(session, url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#     }

#     async with session.get(url, headers=headers) as response:
#         response.raise_for_status()
#         return await response.text()

# async def process_url(session, url):
#     try:
#         html_content = await fetch_url(session, url)
#         soup = BeautifulSoup(html_content, 'html.parser')
#         emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.get_text())
#         return url, emails if emails else None
#     except Exception as e:
#         return url, str(e)

# async def scrape_emails_from_urls(input_csv_path, output_csv_path):
#     tasks = []

#     async with aiohttp.ClientSession() as session:
#         with open(input_csv_path, 'r') as input_file:
#             csv_reader = csv.reader(input_file)
#             header = next(csv_reader)
#             url_column_index = header.index("Website Link")
#             urls_to_scrape = [row[url_column_index] for row in csv_reader]

#         for url in urls_to_scrape:
#             tasks.append(process_url(session, url))

#         results = await asyncio.gather(*tasks)

#     with open(output_csv_path, 'w', newline='') as output_file:
#         csv_writer = csv.writer(output_file)
#         csv_writer.writerow(["Website Link", "Extracted Emails"])

#         for url, emails_or_error in results:
#             csv_writer.writerow([url, ', '.join(emails_or_error) if emails_or_error else ""])

# if __name__ == "__main__":
#     # Specify the paths for input and output CSV files
#     input_csv_path = 'Crawler - Sheet1.csv'
#     output_csv_path = 'output.csv'

#     # Scrape emails from URLs and store in output CSV
#     asyncio.run(scrape_emails_from_urls(input_csv_path, output_csv_path))











