from bs4 import BeautifulSoup
import requests
import os
import time

# Base URL of the website
root = 'https://www.tpointtech.com'

# Path to the local HTML file
html_file_path = 'c:/Users/user/Desktop/Tpoint Tech - Free Online Tutorials.html'

# Read the local HTML file
with open(html_file_path, 'r', encoding='utf-8') as file:
    content = file.read()

soup = BeautifulSoup(content, 'html.parser')

# Find the B.Tech/MCA section
btech_mca_section = soup.find('h3', string='B.Tech/MCA')

if btech_mca_section:
    print("B.Tech/MCA section found.")

    # Find all links within the B.Tech/MCA section
    links_container = btech_mca_section.find_next('div', class_='courses-grid')
    if links_container:
        links = links_container.find_all('a', href=True)
        print(f"Found {len(links)} links in the B.Tech/MCA section.")

        for link in links:
            href = link['href']
            full_url = f'{root}{href}' if href.startswith('/') else href
            print(f"Processing link: {full_url}")

            try:
                # Fetch the content of the link using requests
                response = requests.get(full_url)
                response.raise_for_status()  # Raise an error for bad status codes
                time.sleep(2)  # To avoid overwhelming the server
                sub_soup = BeautifulSoup(response.text, 'html.parser')

                # Extract the main content of the page
                main_content = sub_soup.find('div', class_='entry-content')
                if not main_content:
                    main_content = sub_soup.find('div', id='content')

                if main_content:
                    text_content = main_content.get_text(strip=True, separator='\n')
                else:
                    # Fallback to extracting all text from the page
                    text_content = sub_soup.get_text(strip=True, separator='\n')
                    print(f"Using fallback to extract all text for {full_url}")

                # Save the content to the existing scraped_content directory
                title_tag = sub_soup.find(['h1', 'h2'])
                title = title_tag.get_text(strip=True) if title_tag else "untitled"
                file_path = os.path.join("scraped_content", f"{title}.txt")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                print(f"Content saved for {full_url}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch {full_url}: {e}")
    else:
        print("No links container found in the B.Tech/MCA section.")
else:
    print("B.Tech/MCA section not found in the HTML file.")



