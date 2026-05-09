from playwright.sync_api import sync_playwright
from utils import random_delay
from logger import logger
from config import DEFAULT_KEYWORDS


def scrape_google_maps(zip_code, keywords=None):
    """
    Improved Google Maps scraper

    Returns:
    [
        {
            "name": "ABC Company",
            "website": "https://abc.com"
        }
    ]
    """

    if not keywords:
        keywords = DEFAULT_KEYWORDS

    results = []
    seen_domains = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        for keyword in keywords:
            query = f"{keyword} in {zip_code}"

            logger.info(f"Searching: {query}")

            try:
                page.goto(
                    f"https://www.google.com/maps/search/{query}",
                    timeout=60000
                )

                random_delay()

                # Wait for results panel
                page.wait_for_timeout(5000)

                # Left results panel
                results_panel = page.locator(
                    'div[role="feed"]'
                )

                # Scroll multiple times to load more companies
                for _ in range(5):
                    results_panel.evaluate(
                        "(el) => el.scrollBy(0, 2000)"
                    )
                    page.wait_for_timeout(2000)

                # Get all place links
                place_links = page.locator(
                    'a[href*="/place/"]'
                )

                total = place_links.count()

                logger.info(f"Found total cards: {total}")

                for i in range(min(total, 20)):
                    try:
                        link = place_links.nth(i)

                        link.click()
                        page.wait_for_timeout(3000)

                        # Company name
                        try:
                            name = page.locator("h1").first.inner_text()
                        except:
                            name = "Unknown"

                        # Website extraction
                        website = None

                        all_links = page.locator("a")

                        for j in range(all_links.count()):
                            href = all_links.nth(j).get_attribute("href")

                            if (
                                href
                                and href.startswith("http")
                                and "google" not in href
                                and "maps" not in href
                            ):
                                website = href
                                break

                        if not website:
                            continue

                        # Domain duplicate prevention
                        domain = website.lower()

                        if domain in seen_domains:
                            continue

                        seen_domains.add(domain)

                        results.append({
                            "name": name,
                            "website": website
                        })

                        logger.info(
                            f"Found: {name} | {website}"
                        )

                    except Exception as e:
                        logger.warning(
                            f"Skipping company: {str(e)}"
                        )
                        continue

            except Exception as e:
                logger.error(
                    f"Google Maps scraping failed: {str(e)}"
                )

        browser.close()

    logger.info(
        f"Total unique companies found: {len(results)}"
    )

    return results