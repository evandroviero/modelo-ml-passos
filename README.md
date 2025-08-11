# Arquitetura ML e Aprendizado

Faça um roteiro de estudo com explicações sobre machine learning abordando os temas modelos supervisionado, não supervisionado e recomendação passando por descrição dos principais modelos de cada seguimento com vantagens e desvantagens junto da aplicabilidade de cada modelo, passando também pelo pré-processamento informando qual é recomendado para cada tipo de modelo e no final as metricas de validação de cada modelo informando aonde usar cada uma

## Pré-processamento: Alicerçando o Aprendizado

O pré-processamento de dados é a etapa fundamental que prepara os dados brutos para serem utilizados pelos algoritmos de aprendizado de máquina.

* **Tratamento de valores ausentes**: preencher ou remover valores ausentes de forma estratégica, evitando distorções nas análises. Técnicas como média, mediana ou modelos preditivos podem ser utilizadas para preencher os valores ausentes, minimizando o impacto na qualidade do dado.

* **Detecção e remoção de outliers**: valores atípicos que se desviam significativamente da distribuição dos dados podem levar a modelos enviesados. O pré-processamento fornece ferramentas para identificar e remover esses outliers, garantindo que o modelo aprenda com a maioria representativa dos dados.

* **Normalização e padronização**: ajustar a escala dos dados para facilitar a interpretação e o aprendizado do modelo. Dados com escalas diferentes podem dificultar o aprendizado do modelo, pois algoritmos tendem a dar mais pesos a características com valores maiores. 
    * Normalização: ajusta os dados para um intervalo especifico, como entre 0 e 1
    * Padronização: ajusta os dados com média 0 e desvio padrão 1.
    * Algoritmos sensíveis à escala: algortimos como Regressão Linear, KNN e redes neurais com função de ativação sigmoide ou tanh são sensiveis à escala dos dados
    * Variáveis com escalas diferentes: se as variáveis em seu dataset possuem escalas significativamente diferentes, como idade em anos e renda mensal, a normalização garante que nenhuma variável domine o processo de aprendizado.

    
* **Tratamento de inconsistências**: erros de digitação, formatos incorretos e discrepâncias entre diferentes fontes de dados podem prejudicar a confiabilidade do modelo. O pré-processamento oferece técnicas para identificar e corrigir essas inconsistêncuas, garantindo a integridade dos dados.

* **Transformação de características**: criar novas features a partir das existentes, extraindo informações adicionais dos dados, caso necessário.

## Aprendizado Supervisionado

### Regresão Logística
Modelo clássico e robusto que se baseia tanto na probabiliade para classificar binários como pode lidar com mais de duas classes.

#### Vantagens
* **Simplicidade**: fácil de implementar e interpretar, ideal para iniciantes.
* **Robustez**: desempenho consistente em diversos datasets.
* **Eficiência**: treinamento rápido e com baixo custo operacional.

#### Desvantagens
* **Linearidade**: assume uma relação linear entre as variáveis e a classe alvo, o que pode limitar seu desempenho em casos com relações complexas.
* **Alta dimensionalidade**: pode ter dificuldade em lidar com datasets com muitas variaveis

#### Aplicações
* **Diagnostico médico**: prever a probabilidade de um paciente ter uma doença.
* **Análise de risco de crédito**: avaliar a probabilidade de inadimplência de um cliente.
* **Detecção de fraude**: identificar transações fraudulentas em cartões de crédito.

### KNN
Se baseia em um princípio simples, um dado é classificado de acordo com a classe mais frequente entre seus vizinhos mais próximos no espaço de características.


#### Vantagens
* **Simplicidade**: fácil de implementar e interpretar
* **Não paramétrico**: não faz suposições sobre a distribuição dos dados
* **Flexibilidade**: pode lidar com datasets com diferentes tipos de variáveis

#### Desvantagens
* **Armazenamento de dados**: pode ser computacionalmente custoso para grandes datasets
* **Sensibilidade à ruído:**: outliers podem afetar significativamente o desempenho do modelo
* **Escala**: encontrar os K vizinhos mais próximos pode ser lento 

#### Aplicações
* Em segmentos como a de recomendação de produtos ao sugerir produtos para um cliente
* Reconhecimento de padrões.
* Análise de mercado para segmentar clientes

### Árvore de decisão
Modelo baseado em uma estrutura hierárquica de decisões, onde cada nó representa uma condição sobre uma variável, levando a ramificações que terminam em folhas com a classe prevista.
#### Vantagens
* Interpretabilidade: fácil de visualizar e entender como as decisões são tomadas.
* Não linearidade: lida bem com relações complexas entre variáveis.
* Pré-processamento mínimo: não exige normalização dos dados nem transformação de variáveis categóricas.

#### Desvantagens
* Sobreajuste (overfitting): pode se ajustar demais aos dados de treino, perdendo capacidade de generalização.
* Instabilidade: pequenas mudanças nos dados podem gerar árvores muito diferentes.
* Desempenho: modelos únicos podem ser menos precisos que métodos mais avançados (como Random Forest ou XGBoost).

#### Aplicações
* Tomada de decisão médica: auxiliar médicos a decidirem entre tratamentos com base em sintomas e histórico.
* Crédito e finanças: identificar clientes com maior risco de inadimplência.
* Detecção de falhas: prever falhas em equipamentos a partir de sinais de sensores.

### SVM (Máquinas de Vetores de Suporte)
Modelo que busca encontrar o hiperplano ótimo que separa as classes com a maior margem possível, sendo eficaz mesmo em espaços de alta dimensão.

#### Vantagens
* Alta eficácia: especialmente útil em problemas com fronteiras de decisão não lineares.
* Versatilidade: pode usar diferentes funções de kernel para adaptar-se a diversos tipos de dados.
* Robustez: funciona bem em espaços com muitas dimensões e poucos dados.

#### Desvantagens
* Custo computacional: treinamento pode ser lento em grandes datasets.
* Escolha do kernel: exige cuidado na seleção e parametrização do kernel para obter bons resultados.
* Interpretabilidade: é mais difícil de interpretar comparado a modelos como regressão ou árvore.

#### Aplicações
* Classificação de imagens: distinguir objetos em fotos com alta precisão.
* Bioinformática: identificar genes associados a doenças.
* Filtragem de spam: distinguir entre emails legítimos e indesejados com base em padrões textuais.