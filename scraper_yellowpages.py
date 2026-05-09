# from playwright.sync_api import sync_playwright
# from logger import logger


# def scrape_yellowpages(company_type, location):
#     """
#     Yellow Pages scraper

#     Input Example:
#     company_type = construction
#     location = Brooklyn, NY

#     Returns:
#     [
#         {
#             "name": "ABC Company",
#             "website": "https://abccompany.com"
#         }
#     ]
#     """

#     results = []
#     seen_websites = set()

#     # -----------------------------------
#     # Search URL
#     # -----------------------------------

#     search_url = (
#         f"https://www.yellowpages.com/search?"
#         f"search_terms={company_type}&"
#         f"geo_location_terms={location}"
#     )

#     logger.info(f"Opening Yellow Pages: {search_url}")

#     with sync_playwright() as p:
#         browser = p.chromium.launch(
#             headless=False,
#             slow_mo=300
#         )

#         page = browser.new_page()

#         try:
#             page.goto(
#                 search_url,
#                 timeout=60000
#             )

#             page.wait_for_timeout(5000)

#             # -----------------------------------
#             # Result Listings
#             # -----------------------------------

#             listings = page.locator(".result")

#             total = listings.count()

#             logger.info(
#                 f"Yellow Pages listings found: {total}"
#             )

#             if total == 0:
#                 logger.warning(
#                     "No listings found from Yellow Pages"
#                 )

#             for i in range(min(total, 30)):
#                 try:
#                     item = listings.nth(i)

#                     # -----------------------------------
#                     # Company Name
#                     # -----------------------------------

#                     try:
#                         company_name = item.locator(
#                             ".business-name"
#                         ).inner_text().strip()
#                     except:
#                         continue

#                     # -----------------------------------
#                     # Website Button
#                     # -----------------------------------

#                     website = None

#                     try:
#                         website = item.locator(
#                             "a.track-visit-website"
#                         ).get_attribute("href")
#                     except:
#                         website = None

#                     if not website:
#                         logger.info(
#                             f"No website found: {company_name}"
#                         )
#                         continue

#                     # -----------------------------------
#                     # Duplicate Prevention
#                     # -----------------------------------

#                     if website in seen_websites:
#                         logger.info(
#                             f"Duplicate skipped: {website}"
#                         )
#                         continue

#                     seen_websites.add(website)

#                     # -----------------------------------
#                     # Save Result
#                     # -----------------------------------

#                     results.append({
#                         "name": company_name,
#                         "website": website
#                     })

#                     logger.info(
#                         f"Found: {company_name} | {website}"
#                     )

#                 except Exception as e:
#                     logger.warning(
#                         f"Skipping listing {i}: {str(e)}"
#                     )
#                     continue

#         except Exception as e:
#             logger.error(
#                 f"Yellow Pages scrape failed: {str(e)}"
#             )

#         browser.close()

#     logger.info(
#         f"Total Yellow Pages companies found: {len(results)}"
#     )

#     return results


# import asyncio
# from playwright.async_api import async_playwright
# from logger import logger


# async def scrape_single_page(page, url, seen_websites):
#     results = []

#     try:
#         await page.goto(url, timeout=60000)
#         await page.wait_for_selector(".result", timeout=10000)

#         listings = page.locator(".result")
#         total = await listings.count()

#         logger.info(f"Scraping: {url} | Listings: {total}")

#         for i in range(min(total, 30)):
#             try:
#                 item = listings.nth(i)

#                 # Company name
#                 try:
#                     company_name = await item.locator(".business-name").inner_text()
#                     company_name = company_name.strip()
#                 except:
#                     continue

#                 # Website
#                 website = None

#                 try:
#                     website = await item.locator("a.track-visit-website").get_attribute("href")
#                 except:
#                     pass

#                 if not website:
#                     continue

#                 if website in seen_websites:
#                     continue

#                 seen_websites.add(website)

#                 results.append({
#                     "name": company_name,
#                     "website": website
#                 })

#                 logger.info(f"Found: {company_name} | {website}")

#             except:
#                 continue

#     except Exception as e:
#         logger.error(f"Page scrape failed: {url} | {str(e)}")

#     return results


# async def scrape_yellowpages_async(company_type, location, max_pages=5):
#     """
#     Async Yellow Pages scraper using pagination URL

#     Example:
#     page=1, page=2, page=3...
#     """

#     base_url = (
#         f"https://www.yellowpages.com/search?"
#         f"search_terms={company_type}&"
#         f"geo_location_terms={location}"
#     )

#     seen_websites = set()
#     all_results = []

#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)

#         context = await browser.new_context()

#         tasks = []

#         # Create parallel tasks
#         for page_num in range(1, max_pages + 1):
#             url = f"{base_url}&page={page_num}"

#             page = await context.new_page()

#             task = scrape_single_page(page, url, seen_websites)
#             tasks.append(task)

#         # Run all pages in parallel
#         results_list = await asyncio.gather(*tasks)

#         # Flatten results
#         for res in results_list:
#             all_results.extend(res)

#         await browser.close()

#     logger.info(f"Total companies found: {len(all_results)}")

#     return all_results


# # Wrapper for compatibility with your existing pipeline
# def scrape_yellowpages(company_type, location):
#     return asyncio.run(
#         scrape_yellowpages_async(company_type, location, max_pages=5)
#     )


import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urlparse
from logger import logger

# -----------------------------------
# FILTER BAD DOMAINS
# -----------------------------------

INVALID_KEYWORDS = [
    "localsearch",
    "yelp",
    "facebook",
    "linkedin",
    "instagram",
    "twitter",
    "mapquest",
    "yellowpages",
]


def is_valid_website(url):
    if not url:
        return False

    url = url.lower()

    if not url.startswith("http"):
        return False

    for bad in INVALID_KEYWORDS:
        if bad in url:
            return False

    return True


def normalize_domain(url):
    try:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    except:
        return None


# -----------------------------------
# SCRAPE SINGLE PAGE
# -----------------------------------

async def scrape_single_page(page, url, seen_domains):
    results = []

    try:
        await page.goto(url, timeout=60000)
        await page.wait_for_selector(".result", timeout=10000)

        listings = page.locator(".result")
        total = await listings.count()

        logger.info(f"Scraping: {url} | Listings: {total}")

        for i in range(min(total, 30)):
            try:
                item = listings.nth(i)

                # Company Name
                try:
                    company_name = await item.locator(".business-name").inner_text()
                    company_name = company_name.strip()
                except:
                    continue

                # Website
                website = None

                try:
                    website = await item.locator(
                        "a.track-visit-website"
                    ).get_attribute("href")
                except:
                    pass

                # -----------------------------------
                # FILTER INVALID LINKS
                # -----------------------------------

                if not is_valid_website(website):
                    logger.info(f"Skipped invalid: {website}")
                    continue

                clean_domain = normalize_domain(website)

                if not clean_domain:
                    continue

                if clean_domain in seen_domains:
                    continue

                seen_domains.add(clean_domain)

                results.append({
                    "name": company_name,
                    "website": clean_domain
                })

                logger.info(f"Found: {company_name} | {clean_domain}")

            except Exception as e:
                logger.warning(f"Skipping listing {i}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Page scrape failed: {url} | {str(e)}")

    return results


# -----------------------------------
# MAIN ASYNC SCRAPER
# -----------------------------------

async def scrape_yellowpages_async(company_type, location, max_pages=5):

    base_url = (
        f"https://www.yellowpages.com/search?"
        f"search_terms={company_type}&"
        f"geo_location_terms={location}"
    )

    seen_domains = set()
    all_results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context()

        tasks = []

        # -----------------------------------
        # PARALLEL PAGE SCRAPING
        # -----------------------------------

        for page_num in range(1, max_pages + 1):
            url = f"{base_url}&page={page_num}"

            page = await context.new_page()

            task = scrape_single_page(page, url, seen_domains)
            tasks.append(task)

        results_list = await asyncio.gather(*tasks)

        # Flatten results
        for res in results_list:
            all_results.extend(res)

        await browser.close()

    logger.info(f"Total companies found: {len(all_results)}")

    return all_results


# -----------------------------------
# WRAPPER (FOR YOUR PIPELINE)
# -----------------------------------

def scrape_yellowpages(company_type, location):
    return asyncio.run(
        scrape_yellowpages_async(
            company_type,
            location,
            max_pages=6  # you can increase later
        )
    )