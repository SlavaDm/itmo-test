## Информация от меня (Дмитриев Вячеслав Сергеевич)

Убрал logger, чтобы сэкономить время

Доступ к api https://vilingvum.com/itmo-test/api/request

Точность ответов может упасть, (gpt-4o дороже в несколько раз чем gpt-4o-min)

## Сборка

Для запуска выполните команду:

```bash
docker-compose up -d
```

Она соберёт Docker-образ, а затем запустит контейнер.

После успешного запуска контейнера приложение будет доступно на http://localhost:8080.

## Проверка работы

Отправьте POST-запрос на эндпоинт /api/request. Например, используйте curl:

```bash
curl --location --request POST 'https://vilingvum.com/itmo-test/api/request' \
--header 'Content-Type: application/json' \
--data-raw '{
  "query": "В каком городе находится главный кампус Университета ИТМО?\n1. Москва\n2. Санкт-Петербург\n3. Екатеринбург\n4. Нижний Новгород",
  "id": 1
}'
```

В ответ вы получите JSON вида:

```json
{
  "id": 1,
  "answer": 2,
  "reasoning": "Из информации на сайте",
  "sources": ["https://itmo.ru/ru/", "https://abit.itmo.ru/"]
}
```
