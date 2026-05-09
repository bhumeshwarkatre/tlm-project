# from scraper import scrape_google_maps
# from domain_utils import clean_domain
# from storage import (
#     load_existing_domains,
#     save_batch,
#     create_row
# )
# from tlm_checker import check_tlm
# from mx_checker import check_mx
# from logger import logger


# def run_pipeline(zip_code):
#     logger.info(f"Starting process for ZIP: {zip_code}")

#     existing_domains = load_existing_domains()
#     new_rows = []

#     companies = scrape_google_maps(zip_code)

#     for company in companies:
#         company_name = company.get("name")
#         website = company.get("website")

#         domain = clean_domain(website)

#         if not domain:
#             continue

#         if domain in existing_domains:
#             logger.info(f"Duplicate skipped: {domain}")
#             continue

#         # TLM domain check
#         tlm_status = check_tlm(domain)

#         if tlm_status != "fresh":
#             continue

#         # MX check
#         mx_type = check_mx(domain)

#         if mx_type not in ["Microsoft", "Private"]:
#             logger.info(f"Rejected MX: {domain}")
#             continue

#         row = create_row(
#             company_name,
#             domain,
#             zip_code,
#             tlm_status,
#             mx_type
#         )

#         new_rows.append(row)
#         existing_domains.add(domain)

#         logger.info(f"Approved: {domain}")

#     if new_rows:
#         save_batch(new_rows)

#     logger.info(f"Completed. Saved: {len(new_rows)} companies")

#     return len(new_rows)


# if __name__ == "__main__":
#     zip_code = input("Enter ZIP Code: ")
#     count = run_pipeline(zip_code)
#     print(f"Done. Saved: {count}")



# from scraper import scrape_google_maps
# from scraper_yellowpages import scrape_yellowpages

# from domain_utils import clean_domain
# from storage import (
#     load_existing_domains,
#     save_batch,
#     create_row
# )

# from tlm_checker import check_tlm
# from mx_checker import check_mx
# from logger import logger


# def run_pipeline(
#     source,
#     zip_code=None,
#     company_type=None,
#     location=None
# ):
#     """
#     Main automation pipeline

#     Supported sources:
#     - Google Maps
#     - Yellow Pages
#     """

#     logger.info(f"Starting process using source: {source}")

#     existing_domains = load_existing_domains()
#     new_rows = []

#     # -----------------------------------
#     # Source Selection
#     # -----------------------------------

#     if source == "Google Maps":
#         companies = scrape_google_maps(zip_code)

#     elif source == "Yellow Pages":
#         companies = scrape_yellowpages(
#             company_type=company_type,
#             location=location
#         )

#     else:
#         logger.warning("Invalid source selected")
#         companies = []

#     # -----------------------------------
#     # Processing Pipeline
#     # -----------------------------------

#     for company in companies:
#         company_name = company.get("name")
#         website = company.get("website")

#         if not website:
#             continue

#         domain = clean_domain(website)

#         if not domain:
#             continue

#         # Duplicate prevention
#         if domain in existing_domains:
#             logger.info(f"Duplicate skipped: {domain}")
#             continue

#         # -----------------------------------
#         # TLM Domain Check
#         # -----------------------------------

#         tlm_status = check_tlm(domain)

#         if tlm_status != "fresh":
#             logger.info(f"Skipped by TLM: {domain}")
#             continue

#         # -----------------------------------
#         # MX Check
#         # -----------------------------------

#         mx_type = check_mx(domain)

#         if mx_type not in ["Microsoft", "Private"]:
#             logger.info(f"Rejected MX: {domain}")
#             continue

#         # -----------------------------------
#         # Final Save Row
#         # -----------------------------------

#         row = create_row(
#             company_name=company_name,
#             domain=domain,
#             zip_code=zip_code if zip_code else location,
#             tlm_status=tlm_status,
#             mx_type=mx_type
#         )

#         new_rows.append(row)
#         existing_domains.add(domain)

#         logger.info(f"Approved: {domain}")

#     # -----------------------------------
#     # Save Batch
#     # -----------------------------------

#     if new_rows:
#         save_batch(new_rows)

#     logger.info(
#         f"Completed. Saved: {len(new_rows)} companies"
#     )

#     return len(new_rows)


# if __name__ == "__main__":
#     source = input("Select Source (Google Maps / Yellow Pages): ")

#     if source == "Google Maps":
#         zip_code = input("Enter ZIP Code: ")

#         count = run_pipeline(
#             source=source,
#             zip_code=zip_code
#         )

#     elif source == "Yellow Pages":
#         company_type = input("Enter Company Type: ")
#         location = input("Enter Location: ")

#         count = run_pipeline(
#             source=source,
#             company_type=company_type,
#             location=location
#         )

#     else:
#         print("Invalid source selected")
#         count = 0

#     print(f"Done. Saved: {count}")


# from scraper import scrape_google_maps
# from scraper_yellowpages import scrape_yellowpages

# from domain_utils import clean_domain
# from storage import (
#     load_existing_domains,
#     save_batch,
#     create_row
# )

# from tlm_checker import TLMChecker   # ✅ UPDATED
# from mx_checker import check_mx
# from logger import logger


# def run_pipeline(
#     source,
#     zip_code=None,
#     company_type=None,
#     location=None
# ):
#     """
#     Main automation pipeline

#     Supported sources:
#     - Google Maps
#     - Yellow Pages
#     """

#     logger.info(f"Starting process using source: {source}")

#     existing_domains = load_existing_domains()
#     new_rows = []

#     # -----------------------------------
#     # SOURCE SELECTION
#     # -----------------------------------

#     if source == "Google Maps":
#         companies = scrape_google_maps(zip_code)

#     elif source == "Yellow Pages":
#         companies = scrape_yellowpages(
#             company_type=company_type,
#             location=location
#         )

#     else:
#         logger.warning("Invalid source selected")
#         companies = []

#     # -----------------------------------
#     # INIT TLM (ONLY ONCE)
#     # -----------------------------------

#     tlm = TLMChecker()

#     # -----------------------------------
#     # PROCESSING PIPELINE
#     # -----------------------------------

#     for company in companies:
#         try:
#             company_name = company.get("name")
#             website = company.get("website")

#             if not website:
#                 continue

#             domain = clean_domain(website)

#             if not domain:
#                 continue

#             # Duplicate prevention
#             if domain in existing_domains:
#                 logger.info(f"Duplicate skipped: {domain}")
#                 continue

#             # -----------------------------------
#             # TLM CHECK (FAST - REUSED PAGE)
#             # -----------------------------------

#             tlm_status = tlm.check(domain)

#             if tlm_status != "fresh":
#                 logger.info(f"Skipped by TLM: {domain}")
#                 continue

#             # -----------------------------------
#             # MX CHECK
#             # -----------------------------------

#             mx_type = check_mx(domain)

#             if mx_type not in ["Microsoft", "Private"]:
#                 logger.info(f"Rejected MX: {domain}")
#                 continue

#             # -----------------------------------
#             # SAVE ROW
#             # -----------------------------------

#             row = create_row(
#                 company_name=company_name,
#                 domain=domain,
#                 zip_code=zip_code if zip_code else location,
#                 tlm_status=tlm_status,
#                 mx_type=mx_type
#             )

#             new_rows.append(row)
#             existing_domains.add(domain)

#             logger.info(f"Approved: {domain}")

#         except Exception as e:
#             logger.error(f"Error processing company: {str(e)}")
#             continue

#     # -----------------------------------
#     # CLEANUP TLM (VERY IMPORTANT)
#     # -----------------------------------

#     tlm.close()

#     # -----------------------------------
#     # SAVE CSV
#     # -----------------------------------

#     if new_rows:
#         save_batch(new_rows)

#     logger.info(
#         f"Completed. Saved: {len(new_rows)} companies"
#     )

#     return len(new_rows)


# # -----------------------------------
# # CLI MODE
# # -----------------------------------

# if __name__ == "__main__":
#     source = input("Select Source (Google Maps / Yellow Pages): ")

#     if source == "Google Maps":
#         zip_code = input("Enter ZIP Code: ")

#         count = run_pipeline(
#             source=source,
#             zip_code=zip_code
#         )

#     elif source == "Yellow Pages":
#         company_type = input("Enter Company Type: ")
#         location = input("Enter Location: ")

#         count = run_pipeline(
#             source=source,
#             company_type=company_type,
#             location=location
#         )

#     else:
#         print("Invalid source selected")
#         count = 0

#     print(f"Done. Saved: {count}")


# from scraper import scrape_google_maps
# from scraper_yellowpages import scrape_yellowpages
# from scraper_google_linkedin import scrape_google_linkedin   # ✅ NEW

# from domain_utils import clean_domain
# from storage import (
#     load_existing_domains,
#     save_batch,
#     create_row
# )

# from tlm_checker import TLMChecker
# from mx_checker import check_mx
# from logger import logger


# def run_pipeline(
#     source,
#     zip_code=None,
#     company_type=None,
#     location=None,
#     size=None   # ✅ NEW (LinkedIn filter)
# ):
#     """
#     Main automation pipeline

#     Supported sources:
#     - Google Maps
#     - Yellow Pages
#     - LinkedIn (Google search based)
#     """

#     logger.info(f"Starting process using source: {source}")

#     existing_domains = load_existing_domains()
#     new_rows = []

#     # -----------------------------------
#     # SOURCE SELECTION
#     # -----------------------------------

#     if source == "Google Maps":
#         companies = scrape_google_maps(zip_code)

#     elif source == "Yellow Pages":
#         companies = scrape_yellowpages(
#             company_type=company_type,
#             location=location
#         )

#     elif source == "LinkedIn":
#         companies = scrape_google_linkedin(
#             company_type=company_type,
#             location=location,
#             # size=size
#         )

#     else:
#         logger.warning("Invalid source selected")
#         companies = []

#     logger.info(f"Total companies scraped: {len(companies)}")

#     # -----------------------------------
#     # INIT TLM (ONLY ONCE - PERFORMANCE BOOST)
#     # -----------------------------------

#     tlm = TLMChecker()

#     # -----------------------------------
#     # PROCESSING PIPELINE
#     # -----------------------------------

#     for company in companies:
#         try:
#             company_name = company.get("name")
#             website = company.get("website")

#             if not website:
#                 continue

#             domain = clean_domain(website)

#             if not domain:
#                 continue

#             # -----------------------------------
#             # DUPLICATE PREVENTION
#             # -----------------------------------

#             if domain in existing_domains:
#                 logger.info(f"Duplicate skipped: {domain}")
#                 continue

#             # -----------------------------------
#             # TLM CHECK (REUSED SESSION)
#             # -----------------------------------

#             tlm_status = tlm.check(domain)

#             if tlm_status != "fresh":
#                 logger.info(f"Skipped by TLM: {domain}")
#                 continue

#             # -----------------------------------
#             # MX CHECK
#             # -----------------------------------

#             mx_type = check_mx(domain)

#             if mx_type not in ["Microsoft", "Private"]:
#                 logger.info(f"Rejected MX: {domain}")
#                 continue

#             # -----------------------------------
#             # SAVE ROW
#             # -----------------------------------

#             row = create_row(
#                 company_name=company_name,
#                 domain=domain,
#                 zip_code=zip_code if zip_code else location,
#                 tlm_status=tlm_status,
#                 mx_type=mx_type
#             )

#             new_rows.append(row)
#             existing_domains.add(domain)

#             logger.info(f"Approved: {domain}")

#         except Exception as e:
#             logger.error(f"Error processing company: {str(e)}")
#             continue

#     # -----------------------------------
#     # CLEANUP TLM (VERY IMPORTANT)
#     # -----------------------------------

#     try:
#         tlm.close()
#     except:
#         pass

#     # -----------------------------------
#     # SAVE CSV
#     # -----------------------------------

#     if new_rows:
#         save_batch(new_rows)

#     logger.info(f"Completed. Saved: {len(new_rows)} companies")

#     return len(new_rows)


# # -----------------------------------
# # CLI MODE (OPTIONAL)
# # -----------------------------------

# if __name__ == "__main__":
#     source = input("Select Source (Google Maps / Yellow Pages / LinkedIn): ")

#     if source == "Google Maps":
#         zip_code = input("Enter ZIP Code: ")

#         count = run_pipeline(
#             source=source,
#             zip_code=zip_code
#         )

#     elif source == "Yellow Pages":
#         company_type = input("Enter Company Type: ")
#         location = input("Enter Location: ")

#         count = run_pipeline(
#             source=source,
#             company_type=company_type,
#             location=location
#         )

#     elif source == "LinkedIn":
#         company_type = input("Enter Company Type: ")
#         location = input("Enter Location or ZIP: ")
#         size = input("Enter Size (2-10 / 11-50 / Both): ")

#         count = run_pipeline(
#             source=source,
#             company_type=company_type,
#             location=location,
#             size=size
#         )

#     else:
#         print("Invalid source selected")
#         count = 0

#     print(f"Done. Saved: {count}")


# from scraper import scrape_google_maps
# from scraper_yellowpages import scrape_yellowpages
# from scraper_google_linkedin import scrape_google_linkedin

# from domain_utils import clean_domain
# from storage import (
#     load_existing_domains,
#     save_batch,
#     create_row
# )

# from tlm_checker import TLMChecker
# from mx_checker import check_mx
# from logger import logger


# def run_pipeline(
#     source,
#     zip_code=None,
#     company_type=None,
#     location=None,
#     size=None
# ):
#     """
#     Main automation pipeline

#     Supported sources:
#     - Google Maps
#     - Yellow Pages
#     - LinkedIn (Google-based)
#     """

#     logger.info(f"Starting process using source: {source}")

#     # -----------------------------------
#     # LOAD EXISTING DOMAINS (CSV)
#     # -----------------------------------
#     existing_domains = load_existing_domains()

#     # 🔥 NEW: avoid duplicates in SAME RUN
#     processed_in_run = set()

#     new_rows = []

#     # -----------------------------------
#     # SOURCE SELECTION
#     # -----------------------------------

#     if source == "Google Maps":
#         companies = scrape_google_maps(zip_code)

#     elif source == "Yellow Pages":
#         companies = scrape_yellowpages(
#             company_type=company_type,
#             location=location
#         )

#     elif source == "LinkedIn":
#         companies = scrape_google_linkedin(
#             company_type=company_type,
#             location=location
#         )

#     else:
#         logger.warning("Invalid source selected")
#         companies = []

#     logger.info(f"Total companies scraped: {len(companies)}")

#     if not companies:
#         return 0

#     # -----------------------------------
#     # INIT TLM (ONLY ONCE)
#     # -----------------------------------
#     tlm = TLMChecker()

#     # -----------------------------------
#     # PROCESSING PIPELINE
#     # -----------------------------------

#     for company in companies:
#         try:
#             company_name = company.get("name")
#             website = company.get("website")

#             if not website:
#                 continue

#             # -----------------------------------
#             # DOMAIN CLEANING
#             # -----------------------------------

#             domain = clean_domain(website)

#             if not domain:
#                 continue

#             # normalize again (safety)
#             domain = domain.strip().lower().rstrip(".")

#             # -----------------------------------
#             # DUPLICATE CHECKS
#             # -----------------------------------

#             # 🔥 CSV duplicate
#             if domain in existing_domains:
#                 logger.info(f"SKIPPED (CSV): {domain}")
#                 continue

#             # 🔥 Same run duplicate
#             if domain in processed_in_run:
#                 continue

#             processed_in_run.add(domain)

#             # -----------------------------------
#             # TLM CHECK
#             # -----------------------------------

#             tlm_status = tlm.check(domain)

#             if tlm_status != "fresh":
#                 logger.info(f"Skipped by TLM: {domain}")
#                 continue

#             # -----------------------------------
#             # MX CHECK
#             # -----------------------------------

#             mx_type = check_mx(domain)

#             if mx_type not in ["Microsoft", "Private"]:
#                 logger.info(f"Rejected MX: {domain}")
#                 continue

#             # -----------------------------------
#             # SAVE ROW
#             # -----------------------------------

#             row = create_row(
#                 company_name=company_name,
#                 domain=domain,
#                 zip_code=zip_code if zip_code else location,
#                 tlm_status=tlm_status,
#                 mx_type=mx_type
#             )

#             new_rows.append(row)
#             existing_domains.add(domain)

#             logger.info(f"APPROVED: {domain}")

#         except Exception as e:
#             logger.error(f"Error processing company: {str(e)}")
#             continue

#     # -----------------------------------
#     # CLEANUP TLM
#     # -----------------------------------

#     try:
#         tlm.close()
#     except:
#         pass

#     # -----------------------------------
#     # SAVE CSV
#     # -----------------------------------

#     if new_rows:
#         save_batch(new_rows)

#     logger.info(f"Completed. Saved: {len(new_rows)} companies")

#     return len(new_rows)


# # -----------------------------------
# # CLI MODE (OPTIONAL)
# # -----------------------------------

# if __name__ == "__main__":
#     source = input("Select Source (Google Maps / Yellow Pages / LinkedIn): ")

#     if source == "Google Maps":
#         zip_code = input("Enter ZIP Code: ")

#         count = run_pipeline(
#             source=source,
#             zip_code=zip_code
#         )

#     elif source == "Yellow Pages":
#         company_type = input("Enter Company Type: ")
#         location = input("Enter Location: ")

#         count = run_pipeline(
#             source=source,
#             company_type=company_type,
#             location=location
#         )

#     elif source == "LinkedIn":
#         company_type = input("Enter Company Type: ")
#         location = input("Enter Location or ZIP: ")

#         count = run_pipeline(
#             source=source,
#             company_type=company_type,
#             location=location
#         )

#     else:
#         print("Invalid source selected")
#         count = 0

#     print(f"Done. Saved: {count}")


# from scraper import scrape_google_maps
# from scraper_yellowpages import scrape_yellowpages
# from scraper_google_linkedin import scrape_google_linkedin

# from domain_utils import clean_domain
# from storage import (
#     load_existing_domains,
#     save_batch,
#     create_row,
#     normalize_domain   # ✅ IMPORTANT
# )

# from tlm_checker import TLMChecker
# from mx_checker import check_mx
# from logger import logger


# def run_pipeline(
#     source,
#     zip_code=None,
#     company_type=None,
#     location=None,
#     size=None
# ):
#     """
#     Main automation pipeline

#     Supported sources:
#     - Google Maps
#     - Yellow Pages
#     - LinkedIn
#     """

#     logger.info(f"Starting process using source: {source}")

#     # -----------------------------------
#     # LOAD EXISTING DOMAINS
#     # -----------------------------------
#     existing_domains = load_existing_domains()

#     # Avoid duplicates in same run
#     processed_in_run = set()

#     new_rows = []

#     # -----------------------------------
#     # SOURCE SELECTION
#     # -----------------------------------

#     if source == "Google Maps":
#         companies = scrape_google_maps(zip_code)

#     elif source == "Yellow Pages":
#         companies = scrape_yellowpages(
#             company_type=company_type,
#             location=location
#         )

#     elif source == "LinkedIn":
#         companies = scrape_google_linkedin(
#             company_type=company_type,
#             location=location
#         )

#     else:
#         logger.warning("Invalid source selected")
#         companies = []

#     logger.info(f"Total companies scraped: {len(companies)}")

#     if not companies:
#         return 0

#     # -----------------------------------
#     # INIT TLM (ONLY ONCE)
#     # -----------------------------------
#     tlm = TLMChecker()

#     # -----------------------------------
#     # PROCESS LOOP
#     # -----------------------------------

#     for company in companies:
#         try:
#             company_name = company.get("name")
#             website = company.get("website")

#             if not website:
#                 continue

#             # -----------------------------------
#             # CLEAN + NORMALIZE DOMAIN
#             # -----------------------------------
#             raw_domain = clean_domain(website)

#             if not raw_domain:
#                 continue

#             domain = normalize_domain(raw_domain)

#             if not domain:
#                 continue

#             logger.info(f"Processing: {domain}")

#             # -----------------------------------
#             # DUPLICATE CHECK (FAST SKIP)
#             # -----------------------------------

#             # CSV duplicate
#             if domain in existing_domains:
#                 logger.info(f"⛔ SKIPPED CSV: {domain}")
#                 continue

#             # Same run duplicate
#             if domain in processed_in_run:
#                 logger.info(f"⛔ SKIPPED RUN DUP: {domain}")
#                 continue

#             processed_in_run.add(domain)

#             # -----------------------------------
#             # TLM CHECK
#             # -----------------------------------
#             tlm_status = tlm.check(domain)

#             if tlm_status != "fresh":
#                 logger.info(f"⛔ SKIPPED TLM: {domain}")
#                 continue

#             # -----------------------------------
#             # MX CHECK
#             # -----------------------------------
#             mx_type = check_mx(domain)

#             if mx_type not in ["Microsoft", "Private"]:
#                 logger.info(f"⛔ REJECTED MX: {domain}")
#                 continue

#             # -----------------------------------
#             # CREATE ROW
#             # -----------------------------------
#             row = create_row(
#                 company_name=company_name,
#                 domain=domain,
#                 zip_code=zip_code if zip_code else location,
#                 tlm_status=tlm_status,
#                 mx_type=mx_type
#             )

#             new_rows.append(row)
#             existing_domains.add(domain)

#             logger.info(f"✅ APPROVED: {domain}")

#         except Exception as e:
#             logger.error(f"Error processing company: {str(e)}")
#             continue

#     # -----------------------------------
#     # CLOSE TLM
#     # -----------------------------------
#     try:
#         tlm.close()
#     except Exception as e:
#         logger.warning(f"TLM close issue: {str(e)}")

#     # -----------------------------------
#     # SAVE CSV
#     # -----------------------------------
#     logger.info(f"Rows ready to save: {len(new_rows)}")

#     if new_rows:
#         save_batch(new_rows)
#     else:
#         logger.warning("⚠️ No new rows to save")

#     logger.info(f"Completed. Saved: {len(new_rows)} companies")

#     return len(new_rows)


# # -----------------------------------
# # CLI MODE
# # -----------------------------------

# if __name__ == "__main__":
#     source = input("Select Source (Google Maps / Yellow Pages / LinkedIn): ")

#     if source == "Google Maps":
#         zip_code = input("Enter ZIP Code: ")

#         count = run_pipeline(
#             source=source,
#             zip_code=zip_code
#         )

#     elif source == "Yellow Pages":
#         company_type = input("Enter Company Type: ")
#         location = input("Enter Location: ")

#         count = run_pipeline(
#             source=source,
#             company_type=company_type,
#             location=location
#         )

#     elif source == "LinkedIn":
#         company_type = input("Enter Company Type: ")
#         location = input("Enter Location or ZIP: ")

#         count = run_pipeline(
#             source=source,
#             company_type=company_type,
#             location=location
#         )

#     else:
#         print("Invalid source selected")
#         count = 0

#     print(f"Done. Saved: {count}")



# from scraper import scrape_google_maps
# from scraper_yellowpages import scrape_yellowpages
# from scraper_google_linkedin import scrape_google_linkedin

# from domain_utils import clean_domain
# from storage import (
#     load_existing_domains,
#     save_batch,
#     create_row,
#     normalize_domain,
#     save_raw_batch,          # ✅ NEW
#     load_raw_domains         # ✅ NEW
# )

# from tlm_checker import TLMChecker
# from mx_checker import check_mx
# from logger import logger


# def run_pipeline(
#     source,
#     zip_code=None,
#     company_type=None,
#     location=None,
#     size=None
# ):
#     """
#     FINAL OPTIMIZED PIPELINE

#     FLOW:
#     Scraper → RAW CSV (all data)
#             → Skip RAW duplicates
#             → Skip FINAL CSV duplicates
#             → TLM check
#             → MX check
#             → Final CSV
#     """

#     logger.info(f"Starting process using source: {source}")

#     # -----------------------------------
#     # LOAD EXISTING DATA
#     # -----------------------------------

#     existing_domains = load_existing_domains()   # FINAL CSV
#     raw_domains = load_raw_domains()             # RAW CSV

#     processed_in_run = set()

#     new_rows = []
#     raw_rows = []

#     # -----------------------------------
#     # SOURCE SELECTION
#     # -----------------------------------

#     if source == "Google Maps":
#         companies = scrape_google_maps(zip_code)

#     elif source == "Yellow Pages":
#         companies = scrape_yellowpages(
#             company_type=company_type,
#             location=location
#         )

#     elif source == "LinkedIn":
#         companies = scrape_google_linkedin(
#             company_type=company_type,
#             location=location
#         )

#     else:
#         logger.warning("Invalid source selected")
#         companies = []

#     logger.info(f"Total companies scraped: {len(companies)}")

#     if not companies:
#         return 0

#     # -----------------------------------
#     # INIT TLM (ONLY ONCE)
#     # -----------------------------------

#     tlm = TLMChecker()

#     # -----------------------------------
#     # PROCESS LOOP
#     # -----------------------------------

#     for company in companies:
#         try:
#             company_name = company.get("name")
#             website = company.get("website")

#             if not website:
#                 continue

#             # -----------------------------------
#             # DOMAIN CLEANING
#             # -----------------------------------

#             raw_domain = clean_domain(website)

#             if not raw_domain:
#                 continue

#             domain = normalize_domain(raw_domain)

#             if not domain:
#                 continue

#             logger.info(f"Processing: {domain}")

#             # -----------------------------------
#             # SAVE RAW FIRST (ALL SCRAPED DATA)
#             # -----------------------------------

#             if domain not in raw_domains:
#                 raw_rows.append([
#                     company_name,
#                     domain,
#                     zip_code if zip_code else location
#                 ])
#                 raw_domains.add(domain)

#             # -----------------------------------
#             # SKIP IF ALREADY SCRAPED BEFORE (RAW CSV)
#             # -----------------------------------

#             if domain in raw_domains and domain in existing_domains:
#                 logger.info(f"⛔ SKIPPED (Already processed): {domain}")
#                 continue

#             # -----------------------------------
#             # DUPLICATE CHECKS
#             # -----------------------------------

#             if domain in existing_domains:
#                 logger.info(f"⛔ SKIPPED CSV: {domain}")
#                 continue

#             if domain in processed_in_run:
#                 logger.info(f"⛔ SKIPPED RUN: {domain}")
#                 continue

#             processed_in_run.add(domain)

#             # -----------------------------------
#             # TLM CHECK
#             # -----------------------------------

#             tlm_status = tlm.check(domain)

#             if tlm_status != "fresh":
#                 logger.info(f"⛔ SKIPPED TLM: {domain}")
#                 continue

#             # -----------------------------------
#             # MX CHECK
#             # -----------------------------------

#             mx_type = check_mx(domain)

#             if mx_type not in ["Microsoft", "Private"]:
#                 logger.info(f"⛔ REJECTED MX: {domain}")
#                 continue

#             # -----------------------------------
#             # CREATE FINAL ROW
#             # -----------------------------------

#             row = create_row(
#                 company_name=company_name,
#                 domain=domain,
#                 zip_code=zip_code if zip_code else location,
#                 tlm_status=tlm_status,
#                 mx_type=mx_type
#             )

#             new_rows.append(row)
#             existing_domains.add(domain)

#             logger.info(f"✅ APPROVED: {domain}")

#         except Exception as e:
#             logger.error(f"Error processing company: {str(e)}")
#             continue

#     # -----------------------------------
#     # CLOSE TLM
#     # -----------------------------------

#     try:
#         tlm.close()
#     except Exception as e:
#         logger.warning(f"TLM close issue: {str(e)}")

#     # -----------------------------------
#     # SAVE RAW CSV
#     # -----------------------------------

#     if raw_rows:
#         save_raw_batch(raw_rows)
#         logger.info(f"Saved RAW: {len(raw_rows)}")

#     # -----------------------------------
#     # SAVE FINAL CSV
#     # -----------------------------------

#     logger.info(f"Rows ready to save: {len(new_rows)}")

#     if new_rows:
#         save_batch(new_rows)
#     else:
#         logger.warning("⚠️ No new rows to save")

#     logger.info(f"Completed. Saved: {len(new_rows)} companies")

#     return len(new_rows)


# # -----------------------------------
# # CLI MODE
# # -----------------------------------

# if __name__ == "__main__":
#     source = input("Select Source (Google Maps / Yellow Pages / LinkedIn): ")

#     if source == "Google Maps":
#         zip_code = input("Enter ZIP Code: ")

#         count = run_pipeline(
#             source=source,
#             zip_code=zip_code
#         )

#     elif source == "Yellow Pages":
#         company_type = input("Enter Company Type: ")
#         location = input("Enter Location: ")

#         count = run_pipeline(
#             source=source,
#             company_type=company_type,
#             location=location
#         )

#     elif source == "LinkedIn":
#         company_type = input("Enter Company Type: ")
#         location = input("Enter Location or ZIP: ")

#         count = run_pipeline(
#             source=source,
#             company_type=company_type,
#             location=location
#         )

#     else:
#         print("Invalid source selected")
#         count = 0

#     print(f"Done. Saved: {count}")



from scraper import scrape_google_maps
from scraper_yellowpages import scrape_yellowpages
from scraper_google_linkedin import scrape_google_linkedin

from domain_utils import clean_domain
from storage import (
    load_existing_domains,
    save_batch,
    create_row,
    normalize_domain,
    save_raw_batch,
    load_raw_domains,
    ensure_csv_files   # ✅ IMPORTANT
)

from tlm_checker import TLMChecker
from mx_checker import check_mx
from logger import logger


def run_pipeline(
    source,
    zip_code=None,
    company_type=None,
    location=None,
    size=None
):
    """
    FINAL OPTIMIZED PIPELINE

    FLOW:
    SCRAPE → SAVE RAW → SKIP RAW → SKIP FINAL → TLM → MX → SAVE FINAL
    """

    logger.info(f"Starting process using source: {source}")

    # -----------------------------------
    # ENSURE FILES EXIST
    # -----------------------------------
    ensure_csv_files()

    # -----------------------------------
    # LOAD EXISTING DATA
    # -----------------------------------
    existing_domains = load_existing_domains()   # FINAL CSV
    raw_domains = load_raw_domains()             # RAW CSV

    logger.info(f"📂 FINAL domains loaded: {len(existing_domains)}")
    logger.info(f"📂 RAW domains loaded: {len(raw_domains)}")

    processed_in_run = set()

    new_rows = []
    raw_rows = []

    # -----------------------------------
    # SOURCE SELECTION
    # -----------------------------------
    if source == "Google Maps":
        companies = scrape_google_maps(zip_code)

    elif source == "Yellow Pages":
        companies = scrape_yellowpages(
            company_type=company_type,
            location=location
        )

    elif source == "LinkedIn":
        companies = scrape_google_linkedin(
            company_type=company_type,
            location=location
        )

    else:
        logger.warning("Invalid source selected")
        companies = []

    logger.info(f"Total companies scraped: {len(companies)}")

    if not companies:
        return 0

    # -----------------------------------
    # INIT TLM (ONLY ONCE)
    # -----------------------------------
    tlm = TLMChecker()

    # -----------------------------------
    # PROCESS LOOP
    # -----------------------------------
    for company in companies:
        try:
            company_name = company.get("name")
            website = company.get("website")

            if not website:
                continue

            # -----------------------------------
            # DOMAIN CLEANING
            # -----------------------------------
            raw_domain = clean_domain(website)

            if not raw_domain:
                continue

            domain = normalize_domain(raw_domain)

            if not domain:
                continue

            logger.info(f"Processing: {domain}")

            # -----------------------------------
            # 🚀 RAW DUPLICATE CHECK (FASTEST)
            # -----------------------------------
            if domain in raw_domains:
                logger.info(f"⛔ SKIPPED RAW: {domain}")
                continue

            # -----------------------------------
            # SAVE RAW (ONLY NEW)
            # -----------------------------------
            raw_rows.append([
                company_name,
                domain,
                source
            ])

            raw_domains.add(domain)

            # -----------------------------------
            # FINAL CSV DUPLICATE CHECK
            # -----------------------------------
            if domain in existing_domains:
                logger.info(f"⛔ SKIPPED FINAL: {domain}")
                continue

            # SAME RUN DUPLICATE
            if domain in processed_in_run:
                logger.info(f"⛔ SKIPPED RUN: {domain}")
                continue

            processed_in_run.add(domain)

            # -----------------------------------
            # TLM CHECK
            # -----------------------------------
            tlm_status = tlm.check(domain)

            if tlm_status != "fresh":
                logger.info(f"⛔ SKIPPED TLM: {domain}")
                continue

            # -----------------------------------
            # MX CHECK
            # -----------------------------------
            mx_type = check_mx(domain)

            if mx_type not in ["Microsoft", "Private"]:
                logger.info(f"⛔ REJECTED MX: {domain}")
                continue

            # -----------------------------------
            # SAVE FINAL ROW
            # -----------------------------------
            row = create_row(
                company_name=company_name,
                domain=domain,
                zip_code=zip_code if zip_code else location,
                tlm_status=tlm_status,
                mx_type=mx_type
            )

            new_rows.append(row)
            existing_domains.add(domain)

            logger.info(f"✅ APPROVED: {domain}")

        except Exception as e:
            logger.error(f"Error processing company: {str(e)}")
            continue

    # -----------------------------------
    # CLOSE TLM
    # -----------------------------------
    try:
        tlm.close()
    except Exception as e:
        logger.warning(f"TLM close issue: {str(e)}")

    # -----------------------------------
    # SAVE RAW CSV
    # -----------------------------------
    if raw_rows:
        save_raw_batch(raw_rows)
        logger.info(f"📦 RAW saved: {len(raw_rows)}")

    # -----------------------------------
    # SAVE FINAL CSV
    # -----------------------------------
    if new_rows:
        save_batch(new_rows)
        logger.info(f"✅ FINAL saved: {len(new_rows)}")
    else:
        logger.warning("⚠️ No final rows to save")

    logger.info(f"Completed. Saved: {len(new_rows)} companies")

    return len(new_rows)


# -----------------------------------
# CLI MODE
# -----------------------------------
if __name__ == "__main__":
    source = input("Select Source (Google Maps / Yellow Pages / LinkedIn): ")

    if source == "Google Maps":
        zip_code = input("Enter ZIP Code: ")

        count = run_pipeline(
            source=source,
            zip_code=zip_code
        )

    elif source == "Yellow Pages":
        company_type = input("Enter Company Type: ")
        location = input("Enter Location: ")

        count = run_pipeline(
            source=source,
            company_type=company_type,
            location=location
        )

    elif source == "LinkedIn":
        company_type = input("Enter Company Type: ")
        location = input("Enter Location or ZIP: ")

        count = run_pipeline(
            source=source,
            company_type=company_type,
            location=location
        )

    else:
        print("Invalid source selected")
        count = 0

    print(f"Done. Saved: {count}")



