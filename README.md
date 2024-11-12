
# Servidor Back End com Django

O projeto atual foi feito para a disciplina de Back-end: Web Services.

Os conceitos colocados em prática no software foram a implementação de pelo menos 2 classes onde  devem estar relacionadas em uma relação one-to-many ou many-to-many.

Operações de:
Create,
Read,
Update,
Delete, das informações principais de nossa API.

End-point onde relaciona o processo N da relação entre as duas classes. Por meio de parâmetros de Query.

## Link video análise do código
- [Clique aqui](https://www.youtube.com/watch?v=rvj0Tu4mJXM)


## Boas Práticas do Software

- Logs.
- Tratamento de exceções.
- Testes unitários com Mock para caso de 200 e 400.
- Swagger
- Validações
## Rodando Localmente

Clone the project

```bash
  git clone https://github.com/kyoulau/back-End-Django
```

Go to the project directory

```bash
  cd albumDjango
```

Criar o ambiente virtual
```bash
  python -m venv myenv
```

Ativar o ambiente virtual
```bash
 No Windows
myenv\Scripts\activate
```

```bash
  No MacOS/Linux
  source myenv/bin/activate
```

Instale as dependências

```bash
    pip install -r requirements.txt

```

Startar o servidor

```bash
  python manage.py runserver
```


## Running Tests

Para rodar os testes, utilize o comando

```bash
  python manage.py test                                                               
```
```bash
  python .\albumDjango\manage.py test                                                                  
```


## Authors

- [@andretini](https://www.github.com/andretini)
- [@Laura Santos](https://www.github.com/kyoulau)

