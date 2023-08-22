import requests
from bs4 import BeautifulSoup
import csv
import os

def getting_html_table(html_table):
    if html_table:
        for index, _ in enumerate(html_table):
            
            primeira_tabela = html_table[index]

            
            with open(f'./{file_name}/tabela_{index+1}.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                
                for linha in primeira_tabela.find_all('tr'):
                    dados_linha = []

                    
                    for celula in linha.find_all(['th', 'td']):
                        dados_linha.append(celula.get_text(strip=True))

                    writer.writerow(dados_linha)
    else:
        pass

def remove_html_tags(html_text):
    soup = BeautifulSoup(str(html_text), 'html.parser')
    cleaned_text = soup.get_text()

    return cleaned_text


nome_arquivo = 'products_urls_list.txt'

with open(nome_arquivo, 'r') as arquivo:
    
    for index, linha in enumerate(arquivo):
        
        url = linha.strip()
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            description = soup.find_all("div", class_="pr-md-0 pl-md-0 pl-lg-14 pl-0 col-12 col-md-6 col-lg-12")
            description = remove_html_tags(description)
            
            product = soup.find_all("h1", class_="bsc-product-title")
            product = remove_html_tags(product)
            file_name = product.lower()[1:-1]
            
            if "/" in file_name:
                file_name = file_name.split('/')[0]
            
            file_name = ' '.join(file_name.split())
            
            try:
                os.mkdir(f'./{file_name}')
            except OSError:
                pass


            tag = ["table", "section"]
            class_ = ["row-header-table", "row bsc-table", "row bsc-table bsc-row-color-table", "row bsc-table bsc-basic-table"]

            for _, tag in enumerate(tag):
                for _, _class_ in enumerate(class_):
                    tables = soup.find_all(tag, class_=_class_)
                    getting_html_table(tables)


            text_block = soup.find_all("section", class_="row bsc-text-block")
            character_list = ["[", "]", ",", " ", ", ", " , ", "\t", "\t\xa0", "\xa0\xa0" "\n", "'", "'"]
            new_text_block = []

            for index, element in enumerate(text_block):
                text_block = remove_html_tags(element).split('\n')

                for index in range(len(text_block)):
                    element_index = text_block[index]

                    if element_index in character_list or len(element_index) == 0:
                        pass
                    else:
                        new_text_block.append(element_index)


            with open(f'./{file_name}/page_text{index}.txt', 'a') as file:
                file.write(f"{description[1:-1]}\n")
                for _, element in enumerate(new_text_block):
                    file.write(f"{element}\n")           