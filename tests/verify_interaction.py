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
            insight_counter = page.locator("#insight-counter")
            assert insight_counter.inner_text() == "0"

            print("Navigating to DEMO Level 2...")
            page.click("text=¡Vámonos pal Nivel 2 (SRAP)! 🚀")
            page.wait_for_selector("#level-2", state="visible")
            assert not page.is_visible("#level-0")

            print("Clicking first SRAP step...")
            step_scan = page.locator("#srap-scan")
            step_scan.click()

            print("Dismissing modal...")
            page.click("text=Entendido, Carnal")

            assert insight_counter.inner_text() == "1"
            assert "srap-active" in step_scan.get_attribute("class")

            print("Clicking same step again...")
            step_scan.click()

            print("Dismissing modal again...")
            page.click("text=Entendido, Carnal")

            assert insight_counter.inner_text() == "1"

            print("Testing DEMO paywall...")
            page.click("text=¡Nivel 3: Caos Controlado! 🌪")

            page.wait_for_selector("#custom-modal", state="visible")
            assert page.locator("#modal-title").inner_text() == "ZONA VIP BLOQUEADA"
            assert "Caos Controlado (Nivel 3)" in page.locator("#modal-message").inner_text()
            assert not page.is_visible("#level-3")

            page.click("text=Entendido, Carnal")

            # ============================================================
            # 2. PRIVATE-FULL: comprobar contenido premium real
            # ============================================================
            print("Opening PRIVATE-FULL...")
            page.goto("http://localhost:8000/private-full/index.html")

            # Aislar la prueba de cualquier estado local anterior.
            page.evaluate("localStorage.clear()")
            page.reload()

            print("Initializing game in FULL mode...")
            page.evaluate("window.initGame('full')")

            print("Verifying initial FULL state...")
            assert page.is_visible("#level-0")
            assert page.locator("#insight-counter").inner_text() == "0"

            print("Navigating to FULL Level 2...")
            page.click("text=¡Vámonos pal Nivel 2 (SRAP)! 🚀")
            page.wait_for_selector("#level-2", state="visible")

            print("Navigating to Level 3...")
            page.click("text=¡Nivel 3: Caos Controlado! 🌪")
            page.wait_for_selector("#level-3", state="visible")

            print("Navigating to Level 5...")
            page.click("text=¡Nivel 5: Mandala Multiconsciente! 🎩")
            page.wait_for_selector("#level-5", state="visible")

            print("Clicking a Hat...")
            hat_creativo = page.locator("#hat-creativo")
            hat_creativo.click()

            print("Dismissing modal...")
            page.click("text=Entendido, Carnal")

            assert page.locator("#insight-counter").inner_text() == "3"
            assert "hat-revealed" in hat_creativo.get_attribute("class") or \
                   "var(--neon-lime)" in (hat_creativo.get_attribute("style") or "")

            print("Test PASSED!")

            browser.close()

    except Exception as e:
        print(f"Test FAILED: {e}")
        sys.exit(1)
    finally:
        server.terminate()
        server.wait()


if __name__ == "__main__":
    run_test()
