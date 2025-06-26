import requests
import logging

from bs4 import BeautifulSoup
from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/data')
def get_data():
  return jsonify({'message': 'Hello from Flask!'})

@app.route('/api/produto')
def buscar_produto():
  userSearchText = 'formula-natural-life-gato-frango'
  userSearchTextSplitada = userSearchText.split('-')

  url = f'https://lista.mercadolivre.com.br/{userSearchText}'

  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  
  # Procurando o JSON dentro da tag <script> com o contexto da busca
  script_tag = soup.find('script', type='application/ld+json')  # Encontrar a tag que contém o JSON

  if script_tag:
    # Carregar o JSON da tag
    data = json.loads(script_tag.string)

    # Acessar os produtos no gráfico de dados
    produtos_json = data.get('@graph', [])
    
    # Filtrar os produtos que contêm as palavras-chave da pesquisa
    produtos_filtrados = []
    for produto in produtos_json:
      nome_produto = produto.get('name', '')
      preco_produto = produto.get('offers', {}).get('price', '')
      
      # Verificar se todas as palavras-chave estão no nome do produto
      if all(keyword.lower() in nome_produto.lower() for keyword in userSearchTextSplitada):
        try:
          preco_produto = float(preco_produto.replace('R$', '').replace('.', '').replace(',', '.'))
          produtos_filtrados.append({'nome': nome_produto, 'preco': preco_produto})
        except ValueError:
          continue  # Se não conseguir converter o preço, ignora o produto

    # Se houver produtos filtrados, pegar o produto com o menor preço
    if produtos_filtrados:
      produto_com_menor_preco = min(produtos_filtrados, key=lambda x: x['preco'])
      produto_nome = produto_com_menor_preco['nome']
      produto_preco = produto_com_menor_preco['preco']
    else:
      produto_nome = 'Produto não encontrado'
      produto_preco = 'Preço não encontrado'

    return jsonify({
        'nome': produto_nome,
        'preco': produto_preco
    })

  return jsonify({'error': 'JSON com os produtos não encontrado ou não acessível'})

if __name__ == '__main__':
  app.run(debug=True)