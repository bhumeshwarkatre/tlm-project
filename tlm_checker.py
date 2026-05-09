# import re
# from playwright.sync_api import sync_playwright, TimeoutError
# from config import SESSION_FILE
# from utils import random_delay
# from logger import logger


# def check_tlm(domain):
#     """
#     TLM Domain Checker

#     Full safe flow:
#     1. Open TLM Domain Search page
#     2. Use saved browser session
#     3. Select Account dropdown
#     4. Enter domain
#     5. Click Search
#     6. WAIT until final result appears
#     7. Detect:
#         - Fresh domain
#         - Existing domain
#     8. Only then proceed next domain

#     Returns:
#         fresh
#         exists
#         failed
#     """

#     try:
#         with sync_playwright() as p:
#             browser = p.chromium.launch(
#                 headless=False
#             )

#             context = browser.new_context(
#                 storage_state=SESSION_FILE
#             )

#             page = context.new_page()

#             # -----------------------------------
#             # Open TLM Domain Search Page
#             # -----------------------------------

#             page.goto(
#                 "https://partners.tlminsidesales.com/domain_search",
#                 timeout=60000
#             )

#             random_delay()

#             # -----------------------------------
#             # STEP 1: Select Account Dropdown
#             # -----------------------------------

#             page.locator("span").filter(
#                 has_text=re.compile(r"^Select Account$")
#             ).click()

#             random_delay()

#             page.get_by_text(
#                 "teamlogic-it-fort-lauderdale",
#                 exact=True
#             ).click()

#             random_delay()

#             # -----------------------------------
#             # STEP 2: Enter Domain
#             # -----------------------------------

#             domain_box = page.get_by_role(
#                 "textbox",
#                 name="Domain"
#             )

#             domain_box.click()
#             domain_box.fill(domain)

#             random_delay()

#             # -----------------------------------
#             # STEP 3: Click Search
#             # -----------------------------------

#             page.get_by_role(
#                 "button",
#                 name="Search"
#             ).click()

#             logger.info(f"Searching domain: {domain}")

#             # -----------------------------------
#             # STEP 4: WAIT FOR FINAL RESULT
#             #
#             # Must wait until:
#             # A) Fresh domain message appears
#             # OR
#             # B) Existing table rows appear
#             # -----------------------------------

#             try:
#                 # CASE A → Fresh domain message
#                 page.wait_for_selector(
#                     "text=Data is not present for this domain",
#                     timeout=15000
#                 )

#                 logger.info(f"FRESH DOMAIN: {domain}")

#                 browser.close()
#                 return "fresh"

#             except TimeoutError:
#                 pass

#             try:
#                 # CASE B → Existing domain table appears
#                 page.wait_for_selector(
#                     "table tbody tr",
#                     timeout=10000
#                 )

#                 table_rows = page.locator(
#                     "table tbody tr"
#                 ).count()

#                 if table_rows > 0:
#                     logger.info(f"DOMAIN EXISTS: {domain}")

#                     browser.close()
#                     return "exists"

#             except TimeoutError:
#                 pass

#             # -----------------------------------
#             # Unknown Result
#             # -----------------------------------

#             logger.warning(
#                 f"FAILED / UNKNOWN RESULT: {domain}"
#             )

#             browser.close()
#             return "failed"

#     except Exception as e:
#         logger.error(
#             f"TLM check failed for {domain}: {str(e)}"
#         )

#         return "failed"



import re
from playwright.sync_api import sync_playwright, TimeoutError
from config import SESSION_FILE
from utils import random_delay
from logger import logger


class TLMChecker:
    def __init__(self):
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False
        )

        self.context = self.browser.new_context(
            storage_state=SESSION_FILE
        )

        self.page = self.context.new_page()

        self._setup()

    # -----------------------------------
    # INITIAL SETUP (RUN ONLY ONCE)
    # -----------------------------------

    def _setup(self):
        try:
            self.page.goto(
                "https://partners.tlminsidesales.com/domain_search",
                timeout=60000
            )

            random_delay()

            # Select Account (ONLY ONCE)
            try:
                self.page.locator("span").filter(
                    has_text=re.compile(r"^Select Account$")
                ).click()

                random_delay()

                self.page.get_by_text(
                    "teamlogic-it-fort-lauderdale",
                    exact=True
                ).click()

                logger.info("Account selected")

                random_delay()

            except Exception:
                logger.info("Account already selected or skipped")

        except Exception as e:
            logger.error(f"TLM setup failed: {str(e)}")

    # -----------------------------------
    # MAIN DOMAIN CHECK
    # -----------------------------------

    def check(self, domain):
        try:
            logger.info(f"Checking domain: {domain}")

            # Clear previous input
            domain_box = self.page.get_by_role(
                "textbox",
                name="Domain"
            )

            domain_box.click()
            domain_box.fill("")
            domain_box.fill(domain)

            random_delay()

            # Click search
            self.page.get_by_role(
                "button",
                name="Search"
            ).click()

            # -----------------------------------
            # WAIT FOR RESULT
            # -----------------------------------

            try:
                # Fresh case
                self.page.wait_for_selector(
                    "text=Data is not present for this domain",
                    timeout=12000
                )

                logger.info(f"FRESH: {domain}")
                return "fresh"

            except TimeoutError:
                pass

            try:
                # Exists case
                self.page.wait_for_selector(
                    "table tbody tr",
                    timeout=8000
                )

                rows = self.page.locator(
                    "table tbody tr"
                ).count()

                if rows > 0:
                    logger.info(f"EXISTS: {domain}")
                    return "exists"

            except TimeoutError:
                pass

            logger.warning(f"UNKNOWN RESULT: {domain}")
            return "failed"

        except Exception as e:
            logger.error(f"TLM error: {domain} | {str(e)}")
            return "failed"

    # -----------------------------------
    # CLEANUP
    # -----------------------------------

    def close(self):
        try:
            self.browser.close()
            self.playwright.stop()
        except:
            pass

