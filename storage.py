# import csv
# import os
# from datetime import datetime
# from config import COMPANIES_CSV, RAW_CSV

# # -----------------------------------
# # HEADERS
# # -----------------------------------

# HEADERS = [
#     "company_name",
#     "domain",
#     "zip_code",
#     "tlm_status",
#     "mx_type",
#     "created_at"
# ]

# RAW_HEADERS = [
#     "company_name",
#     "domain",
#     "source",
#     "created_at"
# ]


# # -----------------------------------
# # DOMAIN NORMALIZATION (CRITICAL)
# # -----------------------------------
# def normalize_domain(domain):
#     if not domain:
#         return None

#     domain = str(domain).strip().lower()

#     # remove protocol
#     domain = domain.replace("http://", "").replace("https://", "")

#     # remove www
#     if domain.startswith("www."):
#         domain = domain[4:]

#     # remove trailing junk
#     domain = domain.strip().rstrip("/").rstrip(".")

#     return domain


# # -----------------------------------
# # LOAD FINAL CSV DOMAINS
# # -----------------------------------
# def load_existing_domains():
#     domains = set()

#     if not os.path.exists(COMPANIES_CSV):
#         print("⚠️ companies.csv not found")
#         return domains

#     try:
#         with open(COMPANIES_CSV, "r", encoding="utf-8-sig") as file:
#             reader = csv.DictReader(file)

#             for row in reader:
#                 d = normalize_domain(row.get("domain"))
#                 if d:
#                     domains.add(d)

#         print(f"📂 Loaded FINAL domains: {len(domains)}")

#     except Exception as e:
#         print(f"❌ Error loading companies.csv: {str(e)}")

#     return domains


# # -----------------------------------
# # LOAD RAW DOMAINS (IMPORTANT)
# # -----------------------------------
# def load_raw_domains():
#     domains = set()

#     if not os.path.exists(RAW_CSV):
#         print("⚠️ raw_companies.csv not found")
#         return domains

#     try:
#         with open(RAW_CSV, "r", encoding="utf-8-sig") as file:
#             reader = csv.DictReader(file)

#             for row in reader:
#                 d = normalize_domain(row.get("domain"))
#                 if d:
#                     domains.add(d)

#         print(f"📂 Loaded RAW domains: {len(domains)}")

#     except Exception as e:
#         print(f"❌ Error loading RAW CSV: {str(e)}")

#     return domains


# # -----------------------------------
# # SAVE FINAL CSV (SAFE)
# # -----------------------------------
# def save_batch(rows):
#     if not rows:
#         print("⚠️ No rows to save")
#         return

#     file_exists = os.path.exists(COMPANIES_CSV)
#     existing_domains = load_existing_domains()

#     filtered_rows = []

#     for row in rows:
#         try:
#             domain = normalize_domain(row[1])

#             if not domain:
#                 continue

#             if domain in existing_domains:
#                 print(f"⛔ Skip duplicate (FINAL): {domain}")
#                 continue

#             filtered_rows.append(row)
#             existing_domains.add(domain)

#         except Exception as e:
#             print(f"❌ Row error: {str(e)}")

#     if not filtered_rows:
#         print("⚠️ No unique rows to save")
#         return

#     try:
#         with open(
#             COMPANIES_CSV,
#             "a",
#             newline="",
#             encoding="utf-8"
#         ) as file:
#             writer = csv.writer(file)

#             if not file_exists:
#                 writer.writerow(HEADERS)

#             writer.writerows(filtered_rows)

#         print(f"✅ Saved FINAL rows: {len(filtered_rows)}")

#     except Exception as e:
#         print(f"❌ Save error (FINAL): {str(e)}")


# # -----------------------------------
# # SAVE RAW CSV (VERY IMPORTANT)
# # -----------------------------------
# def save_raw_batch(rows):
#     if not rows:
#         return

#     file_exists = os.path.exists(RAW_CSV)

#     try:
#         with open(
#             RAW_CSV,
#             "a",
#             newline="",
#             encoding="utf-8"
#         ) as file:
#             writer = csv.writer(file)

#             if not file_exists:
#                 writer.writerow(RAW_HEADERS)

#             writer.writerows(rows)

#         print(f"📦 Saved RAW rows: {len(rows)}")

#     except Exception as e:
#         print(f"❌ Save error (RAW): {str(e)}")


# # -----------------------------------
# # CREATE FINAL ROW
# # -----------------------------------
# def create_row(
#     company_name,
#     domain,
#     zip_code,
#     tlm_status,
#     mx_type
# ):
#     domain = normalize_domain(domain)

#     return [
#         company_name,
#         domain,
#         zip_code,
#         tlm_status,
#         mx_type,
#         datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     ]


# # -----------------------------------
# # CREATE RAW ROW
# # -----------------------------------
# def create_raw_row(company_name, domain, source):
#     domain = normalize_domain(domain)

#     return [
#         company_name,
#         domain,
#         source,
#         datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     ]


# import csv
# import os
# from datetime import datetime
# from config import COMPANIES_CSV, RAW_CSV

# # -----------------------------------
# # HEADERS
# # -----------------------------------

# HEADERS = [
#     "company_name",
#     "domain",
#     "zip_code",
#     "tlm_status",
#     "mx_type",
#     "created_at"
# ]

# RAW_HEADERS = [
#     "company_name",
#     "domain",
#     "source",
#     "created_at"
# ]


# # -----------------------------------
# # DOMAIN NORMALIZATION (CRITICAL)
# # -----------------------------------
# def normalize_domain(domain):
#     if not domain:
#         return None

#     domain = str(domain).strip().lower()

#     domain = domain.replace("http://", "").replace("https://", "")

#     if domain.startswith("www."):
#         domain = domain[4:]

#     domain = domain.rstrip("/").rstrip(".")

#     return domain


# # -----------------------------------
# # ENSURE CSV FILES EXIST (IMPORTANT)
# # -----------------------------------
# def ensure_csv_files():
#     if not os.path.exists(COMPANIES_CSV):
#         with open(COMPANIES_CSV, "w", newline="", encoding="utf-8") as f:
#             writer = csv.writer(f)
#             writer.writerow(HEADERS)

#     if not os.path.exists(RAW_CSV):
#         with open(RAW_CSV, "w", newline="", encoding="utf-8") as f:
#             writer = csv.writer(f)
#             writer.writerow(RAW_HEADERS)


# # -----------------------------------
# # GENERIC DOMAIN LOADER (ROBUST)
# # -----------------------------------
# def _load_domains(file_path):
#     domains = set()

#     if not os.path.exists(file_path):
#         print(f"⚠️ File not found: {file_path}")
#         return domains

#     try:
#         with open(file_path, "r", encoding="utf-8-sig") as file:
#             reader = csv.reader(file)

#             header = next(reader, None)

#             if not header:
#                 print(f"⚠️ Empty file: {file_path}")
#                 return domains

#             if "domain" not in header:
#                 print(f"❌ 'domain' column missing in {file_path}")
#                 return domains

#             idx = header.index("domain")

#             for row in reader:
#                 if len(row) <= idx:
#                     continue

#                 d = normalize_domain(row[idx])

#                 if d:
#                     domains.add(d)

#         print(f"📂 Loaded {len(domains)} domains from {file_path}")

#     except Exception as e:
#         print(f"❌ Error reading {file_path}: {str(e)}")

#     return domains


# # -----------------------------------
# # LOAD FINAL DOMAINS
# # -----------------------------------
# def load_existing_domains():
#     return _load_domains(COMPANIES_CSV)


# # -----------------------------------
# # LOAD RAW DOMAINS
# # -----------------------------------
# def load_raw_domains():
#     return _load_domains(RAW_CSV)


# # -----------------------------------
# # SAVE FINAL CSV
# # -----------------------------------
# def save_batch(rows):
#     if not rows:
#         print("⚠️ No FINAL rows to save")
#         return

#     file_exists = os.path.exists(COMPANIES_CSV)

#     try:
#         with open(COMPANIES_CSV, "a", newline="", encoding="utf-8") as file:
#             writer = csv.writer(file)

#             if not file_exists:
#                 writer.writerow(HEADERS)

#             writer.writerows(rows)

#         print(f"✅ Saved FINAL rows: {len(rows)}")

#     except Exception as e:
#         print(f"❌ FINAL save error: {str(e)}")


# # -----------------------------------
# # SAVE RAW CSV (MATCHES main.py)
# # -----------------------------------
# def save_raw_batch(rows):
#     """
#     rows format (from main.py):
#     [
#         [company_name, domain, source]
#     ]
#     """

#     if not rows:
#         print("⚠️ No RAW rows to save")
#         return

#     file_exists = os.path.exists(RAW_CSV)

#     try:
#         with open(RAW_CSV, "a", newline="", encoding="utf-8") as file:
#             writer = csv.writer(file)

#             if not file_exists:
#                 writer.writerow(RAW_HEADERS)

#             for row in rows:
#                 if len(row) < 3:
#                     continue

#                 company_name, domain, source = row

#                 domain = normalize_domain(domain)

#                 if not domain:
#                     continue

#                 writer.writerow([
#                     company_name,
#                     domain,
#                     source,
#                     datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 ])

#         print(f"📦 Saved RAW rows: {len(rows)}")

#     except Exception as e:
#         print(f"❌ RAW save error: {str(e)}")


# # -----------------------------------
# # CREATE FINAL ROW
# # -----------------------------------
# def create_row(
#     company_name,
#     domain,
#     zip_code,
#     tlm_status,
#     mx_type
# ):
#     domain = normalize_domain(domain)

#     return [
#         company_name,
#         domain,
#         zip_code,
#         tlm_status,
#         mx_type,
#         datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     ]


import csv
import os
from datetime import datetime
from config import COMPANIES_CSV, RAW_CSV

# -----------------------------------
# HEADERS
# -----------------------------------

HEADERS = [
    "company_name",
    "domain",
    "zip_code",
    "tlm_status",
    "mx_type",
    "created_at"
]

RAW_HEADERS = [
    "company_name",
    "domain",
    "source",
    "created_at"
]


# -----------------------------------
# DOMAIN NORMALIZATION (STRICT)
# -----------------------------------
def normalize_domain(domain):
    if not domain:
        return None

    domain = str(domain).strip().lower()

    # remove protocol
    domain = domain.replace("http://", "").replace("https://", "")

    # remove www
    if domain.startswith("www."):
        domain = domain[4:]

    # remove path if exists
    domain = domain.split("/")[0]

    # remove trailing junk
    domain = domain.rstrip(".").rstrip("/")

    return domain


# -----------------------------------
# ENSURE CSV FILES EXIST
# -----------------------------------
def ensure_csv_files():
    if not os.path.exists(COMPANIES_CSV):
        with open(COMPANIES_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)

    if not os.path.exists(RAW_CSV):
        with open(RAW_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(RAW_HEADERS)


# -----------------------------------
# GENERIC DOMAIN LOADER (ROBUST)
# -----------------------------------
def _load_domains(file_path):
    domains = set()

    if not os.path.exists(file_path):
        print(f"⚠️ File not found: {file_path}")
        return domains

    try:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)

            header = next(reader, None)

            if not header:
                print(f"⚠️ Empty file: {file_path}")
                return domains

            # normalize headers (IMPORTANT FIX)
            header = [h.strip().lower() for h in header]

            if "domain" not in header:
                print(f"❌ 'domain' column missing in {file_path}")
                return domains

            idx = header.index("domain")

            for row in reader:
                if len(row) <= idx:
                    continue

                d = normalize_domain(row[idx])

                if d:
                    domains.add(d)

        print(f"📂 Loaded {len(domains)} domains from {file_path}")

    except Exception as e:
        print(f"❌ Error reading {file_path}: {str(e)}")

    return domains


# -----------------------------------
# LOAD FINAL DOMAINS
# -----------------------------------
def load_existing_domains():
    ensure_csv_files()
    return _load_domains(COMPANIES_CSV)


# -----------------------------------
# LOAD RAW DOMAINS
# -----------------------------------
def load_raw_domains():
    ensure_csv_files()
    return _load_domains(RAW_CSV)


# -----------------------------------
# SAVE FINAL CSV (WITH DUP CHECK)
# -----------------------------------
def save_batch(rows):
    if not rows:
        print("⚠️ No FINAL rows to save")
        return

    ensure_csv_files()

    existing_domains = load_existing_domains()
    filtered = []

    for row in rows:
        domain = normalize_domain(row[1])

        if not domain:
            continue

        if domain in existing_domains:
            print(f"⛔ Skip FINAL duplicate: {domain}")
            continue

        filtered.append(row)
        existing_domains.add(domain)

    if not filtered:
        print("⚠️ No unique FINAL rows")
        return

    try:
        with open(COMPANIES_CSV, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(filtered)

        print(f"✅ Saved FINAL rows: {len(filtered)}")

    except Exception as e:
        print(f"❌ FINAL save error: {str(e)}")


# -----------------------------------
# SAVE RAW CSV (WITH DUP CHECK)
# -----------------------------------
def save_raw_batch(rows):
    if not rows:
        print("⚠️ No RAW rows to save")
        return

    ensure_csv_files()

    existing_raw = load_raw_domains()
    filtered = []

    for row in rows:
        if len(row) < 3:
            continue

        company_name, domain, source = row
        domain = normalize_domain(domain)

        if not domain:
            continue

        if domain in existing_raw:
            print(f"⛔ Skip RAW duplicate: {domain}")
            continue

        filtered.append([
            company_name,
            domain,
            source,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

        existing_raw.add(domain)

    if not filtered:
        print("⚠️ No unique RAW rows")
        return

    try:
        with open(RAW_CSV, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(filtered)

        print(f"📦 Saved RAW rows: {len(filtered)}")

    except Exception as e:
        print(f"❌ RAW save error: {str(e)}")


# -----------------------------------
# CREATE FINAL ROW
# -----------------------------------
def create_row(
    company_name,
    domain,
    zip_code,
    tlm_status,
    mx_type
):
    domain = normalize_domain(domain)

    return [
        company_name,
        domain,
        zip_code,
        tlm_status,
        mx_type,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]