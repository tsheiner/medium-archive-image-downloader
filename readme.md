# Medium Archive Image Downloader

## Overview
The backup archive you can request from Medium does not include the images in the posts. This script addresses that limitation.

The script creates an `export` subdirectory inside the `posts` directory of the archive and then, for every original html file in the `posts` directory it:
- creates an appropriately named subdirectory
- creates in that subdirectory a copy of the original html file and an `img` directory
- downloads all images referenced in each HTML file
- updates the `src` attributes in the copied html file to point to the downloaded images.



## Installation

### Prerequisites
- Python 3.x
- Pip (Python package installer)

### Dependencies
The script requires the following Python libraries:
- `requests`
- `beautifulsoup4`

To install these dependencies, run the following command at your terminal: 
```
pip install beautifulsoup4
pip install requests
```


## Usage

1. **Request a backup archive from Medium**
    1. Access your Medium account by going to Medium's website and logging in with your credentials.
    1. Once logged in, navigate to your profile picture in the upper right corner and select it to reveal a dropdown menu. From this menu, choose "Settings."
    1. Go to the "Security and apps" tab and click on "Download Your Information."
    1. After requesting your data, Medium will process this request, which may take some time. They will send you an email with a link to download your data once it is ready.
    1. Follow the link in the email to download your writings. The data will typically be in a ZIP file containing your posts and other information associated with your Medium account.
    1. Once you have downloaded the ZIP file, extract it and review the contents to find your writings.
1. **Place the `medium-archive-image-downloader.py` in the `posts` directory of the archive**:
2. **Execute the script by running**:
     ```
     python medium_archive_processor.py
     ```

3. **Check the Output**:
   - After running the script, you'll find each HTML file processed into its own directory within an 'export' directory.
   - if any download errors occurred the will be listed in a file `errors.txt`

## Background
This script was created as a [collaborative effort](https://chat.openai.com/share/9b9672d3-1335-45b7-8254-e87aa270e47e) between Tim Sheiner (who provided the requirements) and ChatGPT4 developed by OpenAI (who wrote the script). It was inspired by two pre-existing scripts that no longer function correctly probably because Medium changed the archive format since the scripts were written:
  - https://github.com/midorikocak/medium-images-downloader
  - https://github.com/mwichary/medium-export-image-fill



## License
No restrictions



