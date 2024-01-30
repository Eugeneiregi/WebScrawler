import csv
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re

async def fetch_url(session, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    async with session.get(url, headers=headers) as response:
        response.raise_for_status()
        return await response.text()

async def process_url(session, url):
    try:
        html_content = await fetch_url(session, url)
        soup = BeautifulSoup(html_content, 'html.parser')
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.get_text())
        return url, emails if emails else None
    except Exception as e:
        return url, str(e)

async def scrape_emails_from_urls(input_csv_path, output_csv_path):
    tasks = []

    async with aiohttp.ClientSession() as session:
        with open(input_csv_path, 'r') as input_file:
            csv_reader = csv.reader(input_file)
            header = next(csv_reader)
            url_column_index = header.index("Website Link")
            urls_to_scrape = [row[url_column_index] for row in csv_reader]

        for url in urls_to_scrape:
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






# import csv
# import requests

# def extract_emails(url):
#     api_url = "https://www.uxlive.me/api/website-info-extractor/"
#     payload = {"web_url": url, "info_request": {"emails": True}}

#     try:
#         response = requests.post(api_url, json=payload)
#         response.raise_for_status()
        
#         if response.status_code == 200:
#             data = response.json()
#             emails = data.get("meta_data", {}).get("emails", [])
#             return emails
#     except requests.RequestException as e:
#         print(f"Error extracting emails for {url}: {e}")
    
#     return None

# def process_csv(input_csv_path, output_csv_path):
#     with open(input_csv_path, 'r') as input_file:
#         csv_reader = csv.reader(input_file)
#         header = next(csv_reader)
#         website_link_index = header.index("Website Link")
#         website_links = [row[website_link_index] for row in csv_reader]

#     result_data = [extract_emails(link) for link in website_links if extract_emails(link) is not None]
#     flattened_result_data = [', '.join(emails) if emails else "" for emails in result_data]

#     with open(input_csv_path, 'r') as input_file:
#         csv_reader = csv.reader(input_file)
#         header = next(csv_reader)
#         data = list(csv_reader)

#     for row, emails in zip(data, flattened_result_data):
#         row.append(emails)

#     with open(output_csv_path, 'w', newline='') as output_file:
#         csv_writer = csv.writer(output_file)
#         csv_writer.writerow(header + ["Extracted Emails"])
#         csv_writer.writerows(data)

# # Specify the paths for input and output CSV files
# input_csv_path = 'Crawler - Sheet1.csv'
# output_csv_path = 'result.csv'

# # Process the CSV file and extract emails
# process_csv(input_csv_path, output_csv_path)


