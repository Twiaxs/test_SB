### Установка / Installation

    docker-compose up --build
  
### Запуск / Run

    docker-compose up

### Использование / Usage

##### URL:

    http://127.0.0.1:8000/api/deals/

Для отправки get запроса необходимо просто зайти на страницу через браузер, либо
отправить get запрос через postman или с помощью чего то аналогичного, например так:

## POST запрос через пайтон:

    import requests

    url = 'http://localhost:8000/api/deals/'
    file_path = 'deals.csv'
    
    with open(file_path, 'rb') as file:
        files = {'deals': file}
        response = requests.post(url, files=files)
    
    print(response.json())


### Ответы:

- `201 Created`: Файл был успешно обработан и данные сохранены в базе данных.

- `400 Bad Request`: Произошла ошибка при обработке файла или файл не был передан.

- `500 Internal Server Error`: Произошла ошибка сохранения данных в базе данных.



## Получение информации о клиентах
GET /api/clients/

Ответы:

- `200 OK`: Успешный запрос. В ответе содержится список из 5 клиентов, потративших наибольшую сумму за весь период.

- `500 Internal Server Error`: Произошла ошибка при получении данных.

Примечание: Для загрузки файла с данными о сделках, используйте поле с именем `deals`. Формат файла должен быть CSV, с полями `customer`, `item`, `total`, `quantity` и `date`. При успешной загрузке, данные из файла будут сохранены в базе данных для последующей обработки.

При выполнении GET-запроса для получения информации о клиентах, в ответе будет содержаться список из 5 клиентов, описанных полями `username`, `spent_money` и `gems`. Поле `username` содержит логин клиента, `spent_money` - сумма потраченных средств за весь период, а `gems` - список из названий камней, которые купили как минимум двое из клиентов, включенных в список "5 клиентов, потративших наибольшую сумму за весь период".
