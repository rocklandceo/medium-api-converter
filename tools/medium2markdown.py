
# Import required libraries
import os
from dotenv import load_dotenv
from medium_api import Medium
import re  # for regex operations
import requests
from bs4 import BeautifulSoup

# Prompt the user for the article URL
article_url = input("Enter the URL of the Medium article to convert: ")

# Specify the path to the .env file
env_path = '../.env'

# Load the RAPIDAPI_KEY from the .env file into the environment
load_dotenv(dotenv_path=env_path)

# Fetch the article content
response = requests.get(article_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the post title using BeautifulSoup
title_element = soup.find(attrs={"data-testid": "storyTitle"})
title = title_element.text if title_element else "default-title"

# Format the title to be used as a filename
formatted_title = re.sub('[^a-zA-Z0-9\s]', '', title).replace(' ', '-').lower()

# Create a Medium Object
medium = Medium(os.getenv('RAPIDAPI_KEY'))

# Get an Article object using the provided article_url
article_id = medium.extract_article_id(article_url)
article = medium.article(article_id)

# Define output paths
markdown_output_path = f"../file_output/markdown/{formatted_title}.md"

# Ensure directory exists or create it
os.makedirs(os.path.dirname(markdown_output_path), exist_ok=True)

# Save the Markdown output
with open(markdown_output_path, 'w', encoding='utf-8') as f:
    f.write(article.markdown)

print(f"Markdown content from the URL has been saved to '{markdown_output_path}'.")
