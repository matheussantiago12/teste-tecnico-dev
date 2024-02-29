
# Execício 1:

Para rodar o programa utilize o comando `python index.py`.

# Execício 2:

Sistema para controle de estacionamentos.

## Tecnologias

### Backend

Django e Django REST Framework

**Banco de dados**: SQLite

### Frontend

Angular com Material UI

## Setup

### Backend

**Requisitos**: Python e pip

**Pasta**: park_api

Os pacote utilizados estão no arquivo `requirements.txt`. Para baixá-los utilize o comando `pip install -r requirements.txt`

Como o banco utilizado é o SQLite, não há necessidade de nenhum configuração adicional. Basta utilizar o comando `python manage.py makemigrations` para criar as migrations, e `python manage.py migrate` para aplicá-las.

> **Observação**: as migrations irão criar também as tabelas que vem por padrão em um projeto Django, porém as tabelas específicas do sistema tem o prefixo `base_`.

Para iniciar a api, use o comando `python manage.py runserver`.

> **Observação**: no arquivo `park_api/park_api/settings.py` há a configuração das origins permitadas do CORS. O valor atual é `http://localhost:4200` (URL do front). Se no seu caso a URL do front-end for diferente, altere a variável CORS_ALLOWED_ORIGINS.


### Frontend

**Requisitos**: Node e npm

**Pasta**: frontend

Para instalar as dependências use `npm install`. Para iniciar o front-end use `npm start`.

> **Observação**: a URL padrão para a chamada da API está definida como `http://localhost:8000`. Se no seu caso a porta for diferente, altere a variável `BASE_URL` no arquivo `frontend/src/app/app.module.ts`.

## Sistema

### Tela de operação
![imagem](https://i.imgur.com/z0VmC8t.png)

Ao fazer uma entrada, caso seja informado uma placa que não esteja registrada no sistema, um novo veículo (sem modelo, descrição e cliente) é registrado junto com a entrada.

Caso a placa informada seja de um veículo já registrado, esse veículo é utilizado na entrada.

A tabela mostra os veículos que atualmente estão no estacionamento. Para efetuar a saída, clique no botão vermelho do respectivo veículo.

### Tela de clientes
![imagem](https://i.imgur.com/GSr9YKb.png)

No campo de planos são listados todos os planos cadastrados no sistema. Esse campo é um select multiple, ou seja, você pode escolher vários planos, somente um ou nenhum.

### Tela de veículos
![imagem](https://i.imgur.com/nSCeadd.png)

### Tela de planos
![imagem](https://i.imgur.com/nMRshvF.png)

### Tela de contrato
![imagem](https://i.imgur.com/AXppczo.png)

Como foi pedido no desafio, limitei a quantidade de contratos para 1, ou seja, você só pode cadastrar o contrato apenas uma vez. 

Para cadastrar/atualizar um contrato, é preciso ter ao menos 1 regra.


## Documentação da API

### Cliente

#### Retorna todos os clientes

```
  GET /api/v1/customer/
```

#### Cadastra cliente
```
  POST /api/v1/customer/
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `name` | `string` | **(Obrigatório)** Nome do cliente |
| `card_id` | `string` | **(Obrigatório)** Card ID do cliente |
| `plans_ids` | `int[]` | **(Opcional)** Lista de IDs dos planos |

#### Atualiza cliente
```
  PUT /api/v1/customer/${id}/
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `name` | `string` | **(Obrigatório)** Nome do cliente |
| `card_id` | `string` | **(Obrigatório)** Card ID do cliente |
| `plans_ids` | `int[]` | **(Opcional)** Lista de IDs dos planos |

### Veículo

#### Retorna todos os veículos

```
  GET /api/v1/vehicle/
```

#### Cadastra veículo
```
  POST /api/v1/vehicle/
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `plate` | `string` | **(Obrigatório)** Placa do veículo |
| `description` | `string` | **(Opcional)** Descrição |
| `model` | `string` | **(Opcional)** Modelo |
| `customer_id` | `int` | **(Opcional)** ID do dono do veículo (cliente) |

#### Atualiza veículo
```
  PUT /api/v1/vehicle/${id}/
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `plate` | `string` | **(Obrigatório)** Placa do veículo |
| `description` | `string` | **(Opcional)** Descrição |
| `model` | `string` | **(Opcional)** Modelo |
| `customer_id` | `int` | **(Opcional)** ID do dono do veículo (cliente) |

### Plano

#### Retorna todos os planos

```
  GET /api/v1/plan/
```

#### Cadastra plano
```
  POST /api/v1/plan/
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `description` | `string` | **(Obrigatório)** Descrição |
| `value` | `number` | **(Obrigatório)** Valor |

#### Atualiza plano
```
  PUT /api/v1/plan/${id}/
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `description` | `string` | **(Obrigatório)** Descrição |
| `value` | `number` | **(Obrigatório)** Valor |

### Contrato

#### Retorna todos os contratos

```
  GET /api/v1/contract/
```

#### Cadastra contrato
```
  POST /api/v1/contract/
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `description` | `string` | **(Obrigatório)** Descrição |
| `max_value` | `number` | **(Obrigatório)** Valor máximo |
| `contract_rules` | `[{}]` | **(Obrigatório)** Lista de regras de contrato |

O campo `contract_rules` deve conter um array de objetos contendo `until` e `value`. 
Exemplo:

```json
[
    {
        "until": 5,
        "value": 10
    },
    {
        "until": 10,
        "value": 20
    }
]
```

Lembrando que o array deve ter pelo menos 1 regra.

#### Atualiza contrato
```
  PUT /api/v1/contract/
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `description` | `string` | **(Obrigatório)** Descrição |
| `max_value` | `number` | **(Obrigatório)** Valor máximo |
| `contract_rules` | `[{}]` | **(Obrigatório)** Lista de regras de contrato |

Para atualizar um contrato já existente, o campo `contract_rules` deve ser um array de objetos. 

Caso queira manter alguma regra que o contrato já tinha antes, o objeto deve conter o campo `id`. 

Caso o objeto não contenha `id`, será considerado uma nova regra e será cadastrada. 

Caso queira que alguma regra já existente seja excluída do contrato, basta apenas não enviá-la no array.

**Simplificando**: envie apenas as regras que você quer que o contrato tenha. Exemplo:

```json
[
    {
        "id": 1,
        "until": 5,
        "value": 10
    },
    {
        "id": 2,
        "until": 10,
        "value": 20
    },
    {
        "until": 15,
        "value": 30
    }
]
```

Lembrando que o array deve ter pelo menos 1 regra.

### Operação (park movement)

#### Retorna todos os registros ativos (que estão no estacionamento)

```
  GET /api/v1/parkmovement/
```

#### Cadastra entrada no estacionamento
```
  POST /api/v1/parkmovement/
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `card_id` | `string` | **(Obrigatório)** Card ID do cliente |
| `plate` | `string` | **(Obrigatório)** Placa do carro |

A data de entrada é gerada pelo back-end, então não há necessidade de mandá-la.

#### Efetua saída do estacionamento
```
  PUT /api/v1/parkmovement/${id}/
```

Basta apenas mandar o ID do park movement à ser alterado. Essa rota irá retornar o **valor (value)** que o cliente deverá pagar e o **horário de saída (exit_date)**.

### Observações

Pela forma que eu fiz, não vi a necessidade de implementar as seguintes rotas que foram especificadas no documento do teste:

- api/v1/customervehicle - Para cadastro de veículos
- api/v1/customerplan - Para efetuar o vínculo do plano com o cliente

Não entendi exatamente qual seria a funcionalidade da rota `/customervehicle`, então acabei deixando apenas a rota `/vehicle` para cadastro de veículos.

Já a rota `/customerplan` não foi necessária, já que da forma que fiz, os planos são vinculados na própria rota de cadastro/atualização de cliente (`/customer`) (ver documentação). 

Investi bastante energia e esforços para a implementação desse projeto, espero que gostem!
