from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP

from datetime import timedelta as td
from datetime import datetime as dt
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Browser(Selenium):
    def __init__(self, url:str):
        super().__init__()

        self._sections = getenv("SECTIONS").split()
        self._search_for = getenv("SEARCH_PHRASE")
        self._types = getenv("TYPES").split()
        self._months = int(getenv("MONTHS"))

        self.open_available_browser(url)
        self.maximize_browser_window()

    def __del__(self):
        self.close_browser()

    def __get_start_end_dates(self) -> tuple:

        end = dt.today()
        start = end.replace(day=1)

        if self._months > 1:
            start = (start - td(days=1)).replace(day=1)
        return start.strftime(r"%m/%d/%Y"), end.strftime(r"%m/%d/%Y")

    def __filter_by(self, by:str, categories:list) -> None:

        if categories:
            self.find_element("css:div[data-testid='{}']".format(by)).click()

            for item in categories:
                try: self.find_element("xpath://span[contains(text(),'{}')]".format(item)).click()
                except: print(f"{by} {item} not found")

            self.find_element("class:popup-visible").click()
    
    def __load_more(self) -> None:
        show_more = "css:button[data-testid='search-show-more-button']"

        while self.is_element_visible(show_more):
            self.find_element(show_more).click()

    def __search(self) -> None:
        btn_search = self.find_element("css:button[data-testid='search-button']")
        btn_search.click()

        self.press_keys("css:input[data-testid='search-input']", self._search_for)
        btn_search.click()

    def __filter_by_date(self) -> None:
        self.wait_until_element_is_visible("css:button[data-testid='search-date-dropdown-a']", 30).click()

        self.find_element("css:button[aria-label='Specific Dates']").click()
        start, end = self.__get_start_end_dates()

        self.input_text("css:input[aria-label='start date']", start)
        self.input_text("css:input[aria-label='end date']", end)

        self.find_element("css:button[data-testid='search-submit']").click()

    def __sort_by(self) -> None:
        sort_by = self.find_element("css:select[data-testid='SearchForm-sortBy']")
        sort_by.click()

        self.find_element("css:option[value='newest']").click()
        sort_by.click()

    def __save_spreadsheet(self, items:list) -> None:
        spreadsheet = Files()

        spreadsheet.create_workbook("nytimes.xlsx", sheet_name="nytimes")
        spreadsheet.append_rows_to_worksheet(items, header=True)
        spreadsheet.save_workbook()

    def run(self):
        self.__search()
        self.__filter_by_date()
        self.__filter_by("type", self._types)
        self.__filter_by("section", self._sections)

        self.__sort_by()
        self.__load_more()

        items = []
        for item in self.find_elements("css:li[data-testid='search-bodega-result']"):

            title = self.find_element("tag:h4", item).text
            description = self.find_element("css:a > p", item).text

            imgs = self.find_elements("tag:img", item)
            if imgs:
                img_source = imgs[0].get_attribute("src")
                img_name = img_source.split("/")[-1].split("?")[0]

            else: img_source, img_name = "", ""

            items.append({
                "dollar's count": any([dolar.lower() in (title + description).lower() for dolar in ["$", "USD", "Dollar"]]),
                "date": self.find_element("css:span[data-testid='todays-date']", item).text,
                "search's count": (title + description).count(self.__search_for.lower()),
                "title": title, "description": description, "image name": img_name
            })

            HTTP().download(img_source, f"images/{img_name}")
        self.__save_spreadsheet(items)

if "__main__" == __name__:
    Browser("https://www.nytimes.com/").run()
