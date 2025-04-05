from flask import Flask, render_template, request, jsonify
import pandas as pd
import requests
from bs4 import BeautifulSoup
from typing import Optional, List, Dict

app = Flask(__name__)

# Classe fornecida
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

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# API que retorna a tabela HTML com base na categoria
@app.route('/api/get_data', methods=['POST'])
def get_data():
    dados_requisicao = request.get_json()

    categoria = dados_requisicao.get("categoria")
    ano_str = dados_requisicao.get("ano", "2022")  # valor padrão

    try:
        ano = int(ano_str)  # garante que seja inteiro
        scraper = VitibrasilScraper(year=ano)
        df = scraper.fetch_data(categoria)
        tabela_html = df.to_html(index=False, classes="tabela", border=0)
        return jsonify({"html": tabela_html})
    except Exception as e:
        return jsonify({"html": f"<p>Erro ao buscar dados: {str(e)}</p>"}), 500

if __name__ == '__main__':
    app.run(debug=True)
