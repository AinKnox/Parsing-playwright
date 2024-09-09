from playwright.sync_api import sync_playwright
import openpyxl

def parse_python_releases():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.python.org/downloads/")
        
        # Парсинг таблицы
        releases = page.query_selector_all(".list-row-container.menu li")
        release_data = []

        for release in releases:
            # Извлечение данных из заданных элементов
            try:
                version_element = release.query_selector(".release-number a")
                date_element = release.query_selector(".release-date")
                download_link_element = release.query_selector(".release-download a")
                
                if version_element and date_element and download_link_element:
                    version = version_element.inner_text().strip()
                    release_date = date_element.inner_text().strip()
                    download_link = download_link_element.get_attribute("href")

                    # Формируем ссылку на Release Notes вручную
                    version_number = version.split(" ")[1]
                    release_notes_link = f"https://docs.python.org/release/{version_number}/whatsnew/changelog.html#python-{version_number.replace('.', '-')}"
                    
                    release_data.append([version, release_date, download_link, release_notes_link])

            except Exception as e:
                print(f"Ошибка при парсинге релиза: {e}")

        browser.close()

        # Сохранение данных в Excel
        if release_data:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Python Releases"
            ws.append(["Release version", "Release date", "Download", "Release Notes"])
            for row in release_data:
                ws.append(row)

            wb.save("python_releases.xlsx")
            print("Данные успешно сохранены в файл python_releases.xlsx.")
        else:
            print("Не удалось найти данные для записи в Excel.")

parse_python_releases()
