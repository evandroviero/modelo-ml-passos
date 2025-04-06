import requests
from bs4 import BeautifulSoup
import pandas as pd

ano = 2023
url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_02'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
print(f"Status da requisição: {response.status_code}")
table = soup.find('table', class_='tb_base tb_dados')
rows = table.find_all("tr")

data = []

for row in rows:
    cells = row.find_all(["th", "td"])
    cells_text = [cell.get_text(strip=True) for cell in cells]
    data.append(cells_text)


df = pd.DataFrame(data[1:], columns=data[0])
print(df.head())