import dns.resolver
from logger import logger


def check_mx(domain):
    """
    Check MX records and classify:
    - Microsoft
    - Private
    - Reject
    """

    try:
        records = dns.resolver.resolve(domain, "MX")
        mx_records = [str(record.exchange).lower() for record in records]

        logger.info(f"MX records for {domain}: {mx_records}")

        for mx in mx_records:
            if "outlook" in mx or "office365" in mx:
                return "Microsoft"

            if "google" in mx or "gmail" in mx or "yahoo" in mx:
                return "Reject"

        return "Private"

    except Exception as e:
        logger.error(f"MX check failed for {domain}: {str(e)}")
        return "Unknown"