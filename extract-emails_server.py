import csv
import aiohttp
import asyncio

async def extract_emails(session, url):
    api_url = "https://www.uxlive.me/api/website-info-extractor/"
    payload = {"web_url": url, "info_request": {"emails": True}}
    
    try:
        async with session.post(api_url, json=payload) as response:
            data = await response.json()
            emails = data.get("meta_data", {}).get("emails", [])
            return emails
    except aiohttp.ClientError as e:
        print(f"Error extracting emails for {url}: {e}")
        return None

async def process_csv(input_csv_path, output_csv_path):
    async with aiohttp.ClientSession() as session:
        with open(input_csv_path, 'r') as input_file:
            csv_reader = csv.reader(input_file)
            header = next(csv_reader)
            website_link_index = header.index("Website Link")
            website_links = [row[website_link_index] for row in csv_reader]

        tasks = [extract_emails(session, link) for link in website_links]
        result_data = await asyncio.gather(*tasks)

    flattened_result_data = [', '.join(emails) if emails else "" for emails in result_data]

    with open(input_csv_path, 'r') as input_file:
        csv_reader = csv.reader(input_file)
        header = next(csv_reader)
        data = list(csv_reader)

    for row, emails in zip(data, flattened_result_data):
        row.append(emails)

    with open(output_csv_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(header + ["Extracted Emails"])
        csv_writer.writerows(data)

# Specify the paths for input and output CSV files
input_csv_path = 'Crawler - Sheet1.csv'
output_csv_path = 'result.csv'

# Process the CSV file and extract emails
asyncio.run(process_csv(input_csv_path, output_csv_path))