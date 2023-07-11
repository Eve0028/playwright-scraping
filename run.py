from os import environ
import json

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from playwright_session import PlaywrightSession


def get_quotes(soup: BeautifulSoup) -> list:
    """Get quotes from soup."""

    return [{
        # Skip non-ascii characters.
        'text': "".join(list(filter(lambda x: x.isascii(), item.select_one('.text').text))),
        'by': item.select_one('.author').text,
        'tags': [tag.text for tag in item.select('.tag')],
    } for item in soup.select(".quote")]


def save_to_jsonl(data: list, filename: str) -> None:
    """
    Saves list of dicts into jsonl file.

    :param data: list of dicts to be stored,
    :param filename: path to the output file. If suffix .jsonl is not given then methods appends
        .jsonl suffix into the file.
    """
    jsonl_extension = '.jsonl'
    # Check filename.
    if not filename.endswith(jsonl_extension):
        filename = filename + jsonl_extension

    # Save data.
    with open(filename, 'w') as out:
        for dict_ in data:
            out.write(json.dumps(dict_) + '\n')


if __name__ == "__main__":
    load_dotenv()

    all_quotes = []
    session = PlaywrightSession(environ['INPUT_URL'],
                                environ.get('PROXY'))

    with sync_playwright() as playwright:
        wait_selector = environ['PARENT_SELECTOR']
        session.setup_playwright(playwright, wait_selector)
        try:
            while True:
                session.scroll_to_last_element(environ['PARENT_SELECTOR'], environ['CHILD_SELECTOR'])
                all_quotes += get_quotes(BeautifulSoup(session.page.content(), 'html.parser'))
                try:
                    session.click_button(environ['NEXT_PAGE_BUTTON_SELECTOR'])
                except PlaywrightTimeoutError:
                    break
                session.wait_for_content(wait_selector)
        finally:
            session.teardown_playwright()

    save_to_jsonl(all_quotes, environ['OUTPUT_FILE'])
