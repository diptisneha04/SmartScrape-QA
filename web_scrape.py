from bs4 import BeautifulSoup
import requests
import time
import os

def gfg_scrape():
# Base URL of the website
    root = 'https://www.geeksforgeeks.org'
    url = f'{root}/technical-interview-questions/#programming-language-tools-technologies-interview-questions'

# Fetch the main page
    r = requests.get(url)
    time.sleep(2)
    content = r.text
    soup = BeautifulSoup(content, 'html.parser')

# Find all divs with class "redirect"
    redirect_divs = soup.find_all('div', class_='redirect')

# Extract all links from the redirect divs
    links = []
    for div in redirect_divs:
        for link in div.find_all('a', href=True):
            links.append(link['href'])

    print("Extracted links:", links)

# Create a directory to save the content
    output_dir = "scraped_content"
    os.makedirs(output_dir, exist_ok=True)

# Iterate through each link and fetch its content
    for link in links:
    # Construct the full URL
        full_url = f'{root}{link}' if link.startswith('/') else link
        r = requests.get(full_url)
        time.sleep(2)
        sub_content = r.text
        sub_soup = BeautifulSoup(sub_content, 'html.parser')

    # Try multiple strategies to extract the main content
        main_content = sub_soup.find('div', class_='entry-content')
        if not main_content:
            main_content = sub_soup.find('article')  # Try finding an <article> tag
        if not main_content:
            main_content = sub_soup.find('div', id='content')  # Try finding a div with id="content"

        if main_content:
            title_tag = sub_soup.find(['h1', 'h2'])
            title = title_tag.get_text(strip=True) if title_tag else "untitled"
            transcript = main_content.get_text(strip=True, separator=' ')

        # Save the content to a file
            file_path = os.path.join(output_dir, f"{title}.txt")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(transcript)
        else:
            print(f"No main content found for {full_url}")

def javatpoint_scrape():
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

def bbs4():
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

if __name__ == "__main__":
    gfg_scrape()
    javatpoint_scrape()
    bbs4()