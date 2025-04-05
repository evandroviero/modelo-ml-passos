import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import Optional, List, Dict


class VitibrasilScraper:
    BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php"
    OPTION_CODES = {
        "production": "opt_02",
        "processing": "opt_03",
        "marketing": "opt_04",
        "import": "opt_05",
        "export": "opt_06"
    }

    def __init__(self, year: int):
        self.year = year

    def _build_url(self, category: str) -> Optional[str]:
        option = self.OPTION_CODES.get(category)
        if not option:
            return None
        return f"{self.BASE_URL}?ano={self.year}&opcao={option}"

    def fetch_data(self, category: str) -> pd.DataFrame:
        """
        Scrapes data from the Embrapa Vitibrasil website based on the given category.

        Args:
            category (str): One of "production", "processing", "marketing", "import", or "export".

        Returns:
            pd.DataFrame: DataFrame containing the structured data.
        """
        url = self._build_url(category)
        if not url:
            raise ValueError(f"Invalid category: {category}")

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed for {url}: {e}")

        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="tb_base tb_dados")
        if not table or not table.tbody:
            raise ValueError(f"No valid table found for category: {category}")

        return self._parse_table(table)

    def _parse_table(self, table) -> pd.DataFrame:
        """
        Parses the given BeautifulSoup table element into a DataFrame.

        Args:
            table: BeautifulSoup object representing the HTML table.

        Returns:
            pd.DataFrame: Structured table data.
        """
        records: List[Dict[str, str]] = []
        current_category = None

        for row in table.tbody.find_all("tr"):
            cols = row.find_all("td")
            if not cols:
                continue

            name = cols[0].get_text(strip=True)
            quantity = cols[1].get_text(strip=True)
            cell_class = cols[0].get("class", [])

            if "tb_item" in cell_class:
                current_category = name
                records.append({
                    "Category": current_category,
                    "Product": "",
                    "Quantity (L)": quantity
                })
            elif "tb_subitem" in cell_class:
                records.append({
                    "Category": current_category,
                    "Product": name,
                    "Quantity (L)": quantity
                })

        return pd.DataFrame(records)
