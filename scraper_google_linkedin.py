import asyncio
import re
from urllib.parse import urlparse
from playwright.async_api import async_playwright
from logger import logger


# -----------------------------------
# BUILD QUERY
# -----------------------------------

def build_queries(company_type, location):
    return [
        # f'site:linkedin.com/company "construction" "Website" "2-10 employees" ("{location}")',
        # f'site:linkedin.com/company "manufacturing" "Website" "2-10 employees" ("{location}")'
        # f'site:linkedin.com/company "Website" "11-50 employees" "27405" ("manufacturing" OR "staffing" OR "finance" OR "financial services" OR "insurance")',
        f'site:linkedin.com/company "{company_type}" "Website" "2-10 employees" ("{location}")',
        f'site:linkedin.com/company "{company_type}" "Website" "11-50 employees" ("{location}")',
        f'site:linkedin.com/company "{company_type}" "Website" "51-200 employees" ("{location}")',

    ]


# -----------------------------------
# CLEAN DOMAIN
# -----------------------------------

def get_domain(url):
    try:
        return urlparse(url).netloc.replace("www.", "")
    except:
        return None


# -----------------------------------
# EXTRACT WEBSITE FROM SNIPPET
# -----------------------------------

def extract_website(text):
    match = re.search(r'Website:\s*(https?://[^\s]+)', text)
    return match.group(1) if match else None


# -----------------------------------
# HUMAN DELAY
# -----------------------------------

async def human_delay(a=2, b=5):
    import random
    await asyncio.sleep(random.uniform(a, b))


# -----------------------------------
# CAPTCHA HANDLER (MANUAL ONLY)
# -----------------------------------

async def handle_captcha(page):
    content = (await page.content()).lower()

    if "sorry" in page.url or "unusual traffic" in content:
        logger.warning("CAPTCHA detected → Solve manually...")

        while True:
            await asyncio.sleep(5)
            if "sorry" not in page.url:
                break

        logger.info("CAPTCHA solved → continuing...")


# -----------------------------------
# MAIN SCRAPER
# -----------------------------------

async def scrape_google_linkedin_async(company_type, location, pages=5):
    queries = build_queries(company_type, location)

    seen_domains = set()
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context()
        page = await context.new_page()

        for query in queries:
            logger.info(f"Running query: {query}")

            # FIRST PAGE
            await page.goto(f"https://www.google.com/search?q={query}")
            await human_delay(3, 6)

            for page_num in range(pages):

                await handle_captcha(page)

                cards = page.locator("div.tF2Cxc")
                total = await cards.count()

                logger.info(f"Page {page_num+1} | Results: {total}")

                for i in range(total):
                    try:
                        text = await cards.nth(i).inner_text()

                        website = extract_website(text)

                        if not website:
                            continue

                        domain = get_domain(website)

                        if not domain:
                            continue

                        # FILTER BAD DOMAINS
                        if any(x in domain for x in [
                            "linkedin",
                            "google",
                            "schema",
                            "static",
                            "licdn"
                        ]):
                            continue

                        if domain not in seen_domains:
                            seen_domains.add(domain)

                            results.append({
                                "name": "Google Result",
                                "website": website
                            })

                            logger.info(f"Found: {website}")

                    except Exception as e:
                        logger.warning(f"Error: {str(e)}")
                        continue

                # -----------------------------------
                # CODEGEN PAGINATION
                # -----------------------------------

                next_btn = page.get_by_role("link", name="Next")

                if await next_btn.count() > 0:
                    await next_btn.click()
                    await human_delay(4, 8)
                else:
                    # fallback (important)
                    next_btn = page.locator("#pnnext")

                    if await next_btn.count() > 0:
                        await next_btn.click()
                        await human_delay(4, 8)
                    else:
                        logger.info("No more pages")
                        break

        await browser.close()

    logger.info(f"Total results: {len(results)}")

    return results


# -----------------------------------
# WRAPPER
# -----------------------------------

def scrape_google_linkedin(company_type, location):
    return asyncio.run(
        scrape_google_linkedin_async(
            company_type,
            location,
            pages=10
        )
    )