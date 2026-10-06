import time
import subprocess
import sys
from playwright.sync_api import sync_playwright


def run_test():
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(2)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # ============================================================
            # 1. DEMO: comprobar acceso público + paywall
            # ============================================================
            print("Opening DEMO...")
            page.goto("http://localhost:8000/demo/index.html")

            print("Initializing game in DEMO mode...")
            page.evaluate("window.initGame('demo')")

            print("Verifying initial DEMO state...")
            assert page.is_visible("#level-0")
            assert page.get_by_role("heading", name="Blueprint Chalamandra™").count() == 1
            assert page.locator('meta[name="description"]').count() == 1
            structured_data = page.locator(
                'script[type="application/ld+json"]'
            ).evaluate("(element) => JSON.parse(element.textContent)")
            assert structured_data["@type"] == "WebApplication"
            assert page.get_by_role("navigation", name="Navegación por niveles").count() == 1
            insight_counter = page.locator("#insight-counter")
            assert insight_counter.inner_text() == "0"

            print("Navigating to DEMO Level 2...")
            page.click("text=¡Vámonos pal Nivel 2 (SRAP)! 🚀")
            page.wait_for_selector("#level-2", state="visible")
            assert not page.is_visible("#level-0")

            print("Clicking first SRAP step...")
            step_scan = page.locator("#srap-scan")
            step_scan.click()

            dialog = page.get_by_role("dialog")
            assert dialog.is_visible()
            assert dialog.get_attribute("aria-modal") == "true"
            assert page.evaluate("document.activeElement.tagName") == "BUTTON"
            page.keyboard.press("Tab")
            assert page.evaluate("document.activeElement.tagName") == "BUTTON"
            page.keyboard.press("Escape")
            assert "srap-scan" in page.evaluate("document.activeElement.id")
            assert not dialog.is_visible()

            assert insight_counter.inner_text() == "1"
            assert "srap-active" in step_scan.get_attribute("class")

            print("Clicking same step again...")
            step_scan.focus()
            page.keyboard.press("Enter")

            assert dialog.is_visible()
            assert page.locator("#modal-title").inner_text() == "Paso Completo"
            page.click("text=Entendido, Carnal")

            assert insight_counter.inner_text() == "1"

            print("Testing DEMO paywall...")
            page.click("text=¡Nivel 3: Caos Controlado! 🌪")

            page.wait_for_selector("#custom-modal", state="visible")
            assert page.locator("#modal-title").inner_text() == "ZONA VIP BLOQUEADA"
            assert "Caos Controlado (Nivel 3)" in page.locator("#modal-message").inner_text()
            assert not page.is_visible("#level-3")

            page.click("text=Entendido, Carnal")

            print("DEMO interaction test PASSED!")

            browser.close()

    except Exception as e:
        print(f"Test FAILED: {e!r}")
        sys.exit(1)
    finally:
        server.terminate()
        server.wait()


if __name__ == "__main__":
    run_test()
