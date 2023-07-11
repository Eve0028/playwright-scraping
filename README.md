# Website scraping

A simple project of scrapping quotes from a website:
http://quotes.toscrape.com <br>
It takes into account delayed content generation using JS, pagination and infinite scrolling.
The resulting file is in JSONL format and contains: text of the quote, author and tags.

### Technologies:
- Playwright
- BeautifulSoup.

### Instructions:

**1. Modify the .env file accordingly to your needs** <br>
- The script waits to generate a page element with selector: `PARENT_SELECTOR`.
- The `CHILD_SELECTOR` variable is a selector of a single quote.
- `NEXT_PAGE_BUTTON_SELECTOR` is the button selector for the next page of quotes.
- Add proxy: rename the variable from `PROXY_SAMPLE` to `PROXY` and enter the appropriate proxy data according to the given scheme:<br>
`login:password@www.proxy.com:8080`
