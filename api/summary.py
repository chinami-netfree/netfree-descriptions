from firecrawl import FirecrawlApp
from pydantic import BaseModel, HttpUrl
from typing import Any, Optional, List
import openai
from openai.types.chat_model import ChatModel
import os

# קריאת כתובת ה-API ממשתנה סביבה או שימוש בברירת מחדל
api_url = os.getenv("FIRECRAWL_API_URL", "http://127.0.0.1:3002/")

app = FirecrawlApp(
    # api_key='',
    api_url=api_url
)
openai_client = openai.Client()


class ExtractSchema(BaseModel):
    website_description: str

# ANSI color codes for pretty terminal output
class Colors:
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"
    RESET = "\033[0m"


def scrape_website(url: HttpUrl):
    """
    Scrape a website using Firecrawl.

    Args:
        url (str): The URL to scrape

    Returns:
        dict: The scraped data
    """
    try:
        print(f"{Colors.YELLOW}Scraping website: {url}{Colors.RESET}")
        scrape_result = app.scrape_url(str(url), params={"formats": ["markdown"]})
        print(f"{Colors.GREEN}Website scraped successfully.{Colors.RESET}")
        return scrape_result["markdown"]
    except Exception as e:
        print(f"{Colors.RED}Error scraping website: {str(e)}{Colors.RESET}")
        return None

SYSTEM_PROMPT = '''Your task is to send requests in Hebrew to open a website in a whitelist-based website filtering system by providing very short and concise information in one sentence about the website you are requesting to open.

Ensure that your response includes only the most relevant details about the website content, which is provided to you in Markdown format. Do not include any additional explanations or specify that it is a website.

# Output Format

- A single sentence in Hebrew, describing the website's core purpose or content without explicitly mentioning that it is a website.

# Examples

**Example:**

- Input: (Markdown content describing an educational platform that offers online math courses for students)
  
  Output: פלטפורמה ללמידת מתמטיקה מקוונת לתלמידים

**Example:**

- Input: (Markdown content describing a travel agency providing vacation planning services)

  Output: שירות לתכנון חופשות מטעם סוכנות נסיעות'''

def summarize_content(content: str, model: ChatModel = "gpt-4o-mini", max_input_tokens: int = 1000):
    """
    Summarize content using OpenAI's API.

    Args:
        content (str): The content to summarize
        model (str): The model to use for summarization
    """
    if len(content) > max_input_tokens:
        content = content[:max_input_tokens]  # Limit input tokens to avoid OpenAI API limits
    try:
        print(f"{Colors.YELLOW}Generating summary using OpenAI's {model} model...{Colors.RESET}")

        prompt = f"""
        Please provide a concise summary of the following website content.
        The summary should:
        - Be around 3-5 paragraphs
        - Highlight the main purpose of the website
        - Include key features or offerings
        - Mention any unique selling points

        Content:
        {content}
        """

        response = openai_client.beta.chat.completions.parse(
            model=model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": content}],
            temperature=0,
            max_tokens=1000,
        )

        summary = response.choices[0].message.content
        print(f"{Colors.GREEN}Summary generated successfully.{Colors.RESET}")

        return summary
    except Exception as e:
        print(f"{Colors.RED}Error generating summary: {str(e)}{Colors.RESET}")
        return None


if __name__ == "__main__":
    url = "https://prog.co.il"
    # url = "https://medium.com/@datajournal/web-scraping-with-firecrawl-570f10a736c5"
    website_data = scrape_website(HttpUrl(url))
    if website_data:
        content = website_data
        summary = summarize_content(content)
        print(f"{Colors.MAGENTA}Summary:{Colors.RESET}\n{summary}")
