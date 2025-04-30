import requests
from bs4 import BeautifulSoup
import time
import os


url = 'https://www.crummy.com/software/BeautifulSoup/bs4/doc/'

res = requests.get(url)
time.sleep(2) 

# Parse the HTML content
soup = BeautifulSoup(res.text, 'html.parser')

# Debugging: Print all <h1> and <h3> headings to verify their text
print("Available <h1> headings:")
for h1 in soup.find_all('h1'):
    print(h1.get_text(strip=True))

print("Available <h3> headings:")
for h3 in soup.find_all('h3'):
    print(h3.get_text(strip=True))

# Extract content for all <h1> and <h3> headings
headings = soup.find_all(['h1', 'h3'])

if headings:
    output_dir = "scraped_content"
    os.makedirs(output_dir, exist_ok=True)

    for i, heading in enumerate(headings):
        content = []
        for element in heading.find_all_next():
            if element in headings[i + 1:]:  # Stop at the next heading
                break
            content.append(element.get_text(strip=True))

        # Join the extracted content into a single string
        extracted_content = '\n'.join(content)

        # Save the content to a file
        title = heading.get_text(strip=True).replace('¶', '').replace(' ', '_')
        file_path = os.path.join(output_dir, f"{title}.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(extracted_content)
        print(f"Content saved for heading: {title}")
else:
    print("No headings found in the document.")

