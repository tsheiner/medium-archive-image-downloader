# this script written by chatGPT4

import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def modify_url(url):
    if '/max/' in url:
        # Original format: Remove '/max/[some number]'
        parts = url.split('/')
        modified_parts = [part for part in parts if not part.startswith('max') and not part.isdigit()]
        return '/'.join(modified_parts)
    else:
        # New format: Adjust URL to the new base
        base_url = 'https://miro.medium.com/v2/format:webp/'
        parts = url.split('/')
        image_id = parts[-1]  # Assume the last part is the image ID
        return urljoin(base_url, image_id)


def get_file_extension(url):
    # Extract the file extension from the URL
    path = urlparse(url).path
    return os.path.splitext(path)[1]

def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"    Downloaded: {os.path.basename(save_path)}")
            return None
        else:
            return f"Failed to download (HTTP status code {response.status_code})"
    except Exception as e:
        return str(e)

def process_html_file(html_file, base_url, export_dir):
    print(f"\nProcessing file: {html_file}")
    # Extract 'user-friendly name' by removing the prefix and token part
    name_parts = html_file.split('_')
    user_friendly_name = '_'.join(name_parts[1:-1]) if len(name_parts) > 2 else name_parts[1]

    # Remove .html suffix from the user-friendly name, if present
    user_friendly_name = user_friendly_name.replace('.html', '')

    # Rest of the code for creating directories and processing HTML file
    new_dir_path = os.path.join(export_dir, user_friendly_name)
    img_dir_path = os.path.join(new_dir_path, 'img')
    error_log = {}

    # Create directories, overwriting if necessary
    os.makedirs(img_dir_path, exist_ok=True)

    # Copy and rename HTML file
    new_html_path = os.path.join(new_dir_path, user_friendly_name + '.html')
    with open(html_file, 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    img_counter = 1
    for img_tag in soup.find_all('img'):
        original_src = img_tag['src']

        # Convert relative URL to absolute URL if necessary
        if not urlparse(original_src).scheme:
            original_src = urljoin(base_url, original_src)

        modified_src = modify_url(original_src)
        file_ext = get_file_extension(modified_src)
        
        # First try to get a meaningful name from the figure caption
        if figure_parent := img_tag.find_parent('figure'):
            if figcaption := figure_parent.find('figcaption'):
                caption = figcaption.get_text().strip()
                # Remove "Photo by..." and everything after
                if "Photo by" in caption:
                    caption = caption.split("Photo by")[0]
                # Clean the caption to make it filename-friendly
                img_name = "".join(c for c in caption if c.isalnum() or c in (' ','-','_')).strip()
                img_name = img_name.replace(' ', '-')[:50]  # limit length
        
        # If no caption or caption was empty, try alt text
        if not locals().get('img_name') or not img_name:
            alt_text = img_tag.get('alt', '').strip()
            if alt_text:
                img_name = "".join(c for c in alt_text if c.isalnum() or c in (' ','-','_')).strip()
                img_name = img_name.replace(' ', '-')[:50]  # limit length
        
        # If neither caption nor alt text provided a name, use image ID or counter
        if not locals().get('img_name') or not img_name:
            data_image_id = img_tag.get('data-image-id', '')
            if data_image_id:
                img_name = data_image_id.replace('*', '').replace('/', '-')
            else:
                img_name = f"{user_friendly_name}-image-{img_counter}"
        
        img_counter += 1
        
        # Append the file extension if not already present
        if not img_name.endswith(file_ext):
            img_name += file_ext

        save_path = os.path.join(img_dir_path, img_name)

        error_msg = download_image(modified_src, save_path)
        if error_msg:
            error_log[modified_src] = error_msg

        img_tag['src'] = os.path.join('img', img_name)

    with open(new_html_path, 'w') as file:
        file.write(str(soup))

    if error_log:
        error_file = os.path.join(img_dir_path, 'errors.txt')
        print(f"    Writing errors to: {error_file}")
        with open(error_file, 'w') as file:
            json.dump(error_log, file, indent=4)
    print(f"Completed processing: {html_file}")

# Create the 'export' directory and process each HTML file in the current directory
base_url = 'https://cdn-images-1.medium.com/'
export_dir = os.path.join(os.getcwd(), 'export')
os.makedirs(export_dir, exist_ok=True)
print(f"Starting processing - output will be in: {export_dir}")

for filename in os.listdir(os.getcwd()):
    if filename.endswith('.html'):
        process_html_file(filename, base_url, export_dir)

# Note: This script assumes that it's placed in the same directory as the HTML files.