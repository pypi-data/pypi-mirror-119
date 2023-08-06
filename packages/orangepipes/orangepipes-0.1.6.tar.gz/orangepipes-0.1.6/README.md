## Setup
Para configurar a aplicação é necessário o python 3 será necessário instalar as seguintes módulos:

```
sudo apt install python3-pip
pip3 install --user pipenv
```

Para gerenciamento de dependências do projeto, é utilizado o [pipenv](https://pipenv.pypa.io/en/latest/).

Com os módulos devidamente instalados, agora é só configurar o projeto. Após clonar o repositório, basta executar o comando:


```
make install
```

Este comando irá criar:

Diretório .venv onde o pipenv irá criar o virtualenv do python.
* Diretório `.venv` onde o pipenv irá criar o `virtualenv` do python. 
* Executar o `pipenv install` para criar o `virtualenv` e instalar todas as dependências
* Ativar o `shell` do `virtualenv` do projeto

Com os módulos devidamente instalados, agora é só configurar o projeto. Após clonar o repositório, basta executar o comando:

## How to use
[read the DOC](./DOC.md)