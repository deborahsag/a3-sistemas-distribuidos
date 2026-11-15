# A3 Sistemas Distribuídos
Avaliação A3 da unidade curricular Sistemas Distribuídos e Mobile (2026/2) da UniBH.

Aluna: Deborah Santos Andrade Guimarães

# Cápsula
## Um novo jeito de guardar ideias
O objetivo do aplicativo Cápsula é capturar suas ideias enquanto você está ocupado no dia a dia e lembrá-lo de desenvolvê-las nos seus horários livres. Clique um botão, descreva rapidamente sua ideia, escolha em quanto tempo deseja ser lembrado e volte a fazer o que estava fazendo. Quando estiver com tempo, revisite sua ideia e crie um projeto - uma página na qual você poderá guardar listas de afazeres, imagens, textos e referências.

## O que será desenvolvido
Para a avaliação, será implementada uma API para o sistema de captura de ideias. Serão desenvolvidas as seguintes rotas:

POST: Registro de uma nova ideia;
GET: Retorna a lista de ideias capturadas até então;
PUT: Atualiza a frequência de notificações de uma ideia;
DELETE: Remove uma ideia do registro.

## Tecnologias
A API será desenvolvida em FastAPI com banco de dados Firebase.

## Dúvidas para o professor
1. Desacoplamento

Qual é a melhor maneira de desacoplar a camada de banco de dados da camada de modelos?

É vantajoso tentar fazer funções genéricas que funcionem para qualquer modelo e qualquer tabela do banco de dados?

2. Lógica de negócio

Qual é a melhor maneira de garantir que certos dados (exemplo: timestamp) nunca sejam alterados?

3. Segurança/execução do trabalho

O Firebase precisa de uma chave privada para acessar o banco de dados, e não é aconselhável que chaves sejam colocadas em repositórios públicos. Como vamos fazer nesse trabalho?
