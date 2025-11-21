#!/usr/bin/env python3
"""
Simple NotebookLM Question Interface
Based on MCP server implementation - simplified without sessions

Implements hybrid auth approach:
- Persistent browser profile (user_data_dir) for fingerprint consistency
- Manual cookie injection from state.json for session cookies (Playwright bug workaround)
See: https://github.com/microsoft/playwright/issues/36139
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

from patchright.sync_api import sync_playwright

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from auth_manager import AuthManager
from notebook_manager import NotebookLibrary
from browser_session import StealthUtils


# Follow-up reminder (adapted from MCP server for stateless operation)
# Since we don't have persistent sessions, we encourage comprehensive questions
FOLLOW_UP_REMINDER = (
    "\n\nEXTREMELY IMPORTANT: Is that ALL you need to know? "
    "You can always ask another question! Think about it carefully: "
    "before you reply to the user, review their original request and this answer. "
    "If anything is still unclear or missing, ask me another comprehensive question "
    "that includes all necessary context (since each question opens a new browser session)."
)


# MCP Server selectors (exact match!)
QUERY_INPUT_SELECTORS = [
    "textarea.query-box-input",  # Primary
    'textarea[aria-label="Feld für Anfragen"]',  # Fallback
]

RESPONSE_SELECTORS = [
    ".to-user-container .message-text-content",  # Primary
    "[data-message-author='bot']",
    "[data-message-author='assistant']",
]


def ask_notebooklm(question: str, notebook_url: str, headless: bool = True, max_retries: int = 3) -> str:
    """
    Ask a question to NotebookLM with retry logic

    Args:
        question: Question to ask
        notebook_url: NotebookLM notebook URL
        headless: Run browser in headless mode
        max_retries: Maximum number of retry attempts

    Returns:
        Answer text from NotebookLM
    """
    auth = AuthManager()

    if not auth.is_authenticated():
        print("⚠️ Not authenticated. Run: python auth_manager.py setup")
        return None

    print(f"💬 Asking: {question}")
    print(f"📚 Notebook: {notebook_url}")

    last_error = None

    for attempt in range(1, max_retries + 1):
        if attempt > 1:
            print(f"\n🔄 Retry attempt {attempt}/{max_retries}...")
            time.sleep(5)  # Wait before retry

        playwright = None
        context = None

        try:
            # Start playwright
            playwright = sync_playwright().start()

            # Launch persistent browser context with real Chrome (not Chromium)
            context = playwright.chromium.launch_persistent_context(
                user_data_dir=str(auth.browser_state_dir / "browser_profile"),
                channel="chrome",
                headless=headless,
                no_viewport=True,
                ignore_default_args=["--enable-automation"],
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--no-first-run',
                    '--no-default-browser-check'
                ]
            )

            # WORKAROUND: Manually inject cookies from state.json
            if auth.state_file.exists():
                try:
                    print("  🔧 Loading authentication state...")
                    with open(auth.state_file, 'r') as f:
                        state = json.load(f)
                        if 'cookies' in state and len(state['cookies']) > 0:
                            context.add_cookies(state['cookies'])
                            print(f"  ✅ Injected {len(state['cookies'])} cookies")
                except Exception as e:
                    print(f"  ⚠️  Could not load state.json: {e}")

            # Navigate to notebook
            page = context.new_page()
            print("  🌐 Opening notebook...")
            
            # INCREASED TIMEOUT: 90s
            page.goto(notebook_url, wait_until="domcontentloaded", timeout=90000)

            # Check if we're on NotebookLM
            current_url = page.url
            if not current_url.startswith("https://notebooklm.google.com/"):
                print("  ⏳ Waiting for redirect to NotebookLM...")
                # INCREASED TIMEOUT: 90s
                page.wait_for_url(re.compile(r"^https://notebooklm\.google\.com/"), timeout=90000)
            else:
                print("  ✓ Already on NotebookLM")

            # Wait for query input
            print("  ⏳ Waiting for query input...")
            query_element = None

            for selector in QUERY_INPUT_SELECTORS:
                try:
                    query_element = page.wait_for_selector(
                        selector,
                        timeout=15000, # Increased from 10s
                        state="visible"
                    )
                    if query_element:
                        print(f"  ✓ Found input: {selector}")
                        break
                except:
                    continue

            if not query_element:
                raise Exception("Could not find query input")

            # Type question
            print("  ⏳ Typing question...")
            page.click(QUERY_INPUT_SELECTORS[0])
            time.sleep(0.5)
            
            if len(question) > 200:
                page.fill(QUERY_INPUT_SELECTORS[0], question)
            else:
                page.type(QUERY_INPUT_SELECTORS[0], question, delay=50)

            # Submit
            print("  📤 Submitting...")
            page.keyboard.press("Enter")
            time.sleep(1)

            # Wait for response
            print("  ⏳ Waiting for answer...")

            answer = None
            stable_count = 0
            last_text = None
            deadline = time.time() + 180  # INCREASED TIMEOUT: 3 minutes

            while time.time() < deadline:
                for selector in RESPONSE_SELECTORS:
                    try:
                        elements = page.query_selector_all(selector)
                        if elements:
                            latest = elements[-1]
                            text = latest.inner_text().strip()

                            if text and len(text) > 10:
                                if text == last_text:
                                    stable_count += 1
                                    if stable_count >= 3:
                                        answer = text
                                        break
                                else:
                                    stable_count = 0
                                    last_text = text
                    except:
                        continue

                if answer:
                    break
                time.sleep(1)

            if not answer:
                raise TimeoutError("Timeout waiting for answer")

            print("  ✅ Got answer!")
            return answer + FOLLOW_UP_REMINDER

        except Exception as e:
            print(f"  ❌ Error (Attempt {attempt}): {e}")
            last_error = e
            # Continue to next retry
            
        finally:
            if context:
                try:
                    context.close()
                except:
                    pass
            if playwright:
                try:
                    playwright.stop()
                except:
                    pass

    print(f"❌ Failed after {max_retries} attempts. Last error: {last_error}")
    return None


def main():
    parser = argparse.ArgumentParser(description='Ask NotebookLM a question')

    parser.add_argument('--question', required=True, help='Question to ask')
    parser.add_argument('--notebook-url', help='NotebookLM notebook URL')
    parser.add_argument('--notebook-id', help='Notebook ID from library')
    parser.add_argument('--show-browser', action='store_true', help='Show browser')

    args = parser.parse_args()

    # Resolve notebook URL
    notebook_url = args.notebook_url

    if not notebook_url and args.notebook_id:
        library = NotebookLibrary()
        notebook = library.get_notebook(args.notebook_id)
        if notebook:
            notebook_url = notebook['url']
        else:
            print(f"❌ Notebook '{args.notebook_id}' not found")
            return 1

    if not notebook_url:
        # Check for active notebook first
        library = NotebookLibrary()
        active = library.get_active_notebook()
        if active:
            notebook_url = active['url']
            print(f"📚 Using active notebook: {active['name']}")
        else:
            # Show available notebooks
            notebooks = library.list_notebooks()
            if notebooks:
                print("\n📚 Available notebooks:")
                for nb in notebooks:
                    mark = " [ACTIVE]" if nb.get('id') == library.active_notebook_id else ""
                    print(f"  {nb['id']}: {nb['name']}{mark}")
                print("\nSpecify with --notebook-id or set active:")
                print("python scripts/run.py notebook_manager.py activate --id ID")
            else:
                print("❌ No notebooks in library. Add one first:")
                print("python scripts/run.py notebook_manager.py add --url URL --name NAME --description DESC --topics TOPICS")
            return 1

    # Ask the question
    answer = ask_notebooklm(
        question=args.question,
        notebook_url=notebook_url,
        headless=not args.show_browser
    )

    if answer:
        print("\n" + "=" * 60)
        print(f"Question: {args.question}")
        print("=" * 60)
        print()
        print(answer)
        print()
        print("=" * 60)
        return 0
    else:
        print("\n❌ Failed to get answer")
        return 1


if __name__ == "__main__":
    sys.exit(main())
