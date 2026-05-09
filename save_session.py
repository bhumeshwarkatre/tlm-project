from playwright.sync_api import sync_playwright
from config import SESSION_FILE


def save_login_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context()
        page = context.new_page()

        # IMPORTANT:
        # Replace with your real TLM login page
        page.goto("https://partners.tlminsidesales.com/domain_search")

        print("\nLogin manually now...")
        input("After login is complete, press ENTER here...")

        context.storage_state(path=SESSION_FILE)

        print(f"Session saved successfully → {SESSION_FILE}")

        browser.close()


if __name__ == "__main__":
    save_login_session()