## Информация от меня (Дмитриев Вячеслав Сергеевич)

Убрал logger, чтобы сэкономить время

Доступ к api https://vilingvum.com/itmo-test/api/request

Точность ответов может упасть, (gpt-4o дороже в несколько раз чем gpt-4o-min), если в ходе тестирования вылезет ошибка, что деньги закончились, напишите в тг, если будет смысл, @VDmitriev1, я пополню баланс

## Сборка

docker-compose up -d

docker-compose down

## Проверка работы

![Пример работы запроса]([http://url/to/img.png](https://github.com/SlavaDm/itmo-test/tree/master/example-of-usage.png))

Отправьте POST-запрос https://vilingvum.com/itmo-test/api/request. Используйте Postman (с curl выходят ошибки, не успевал разобраться):

```json
{
  "query": "В каком городе находится главный кампус Университета ИТМО?\n1. Москва\n2. Санкт-Петербург\n3. Екатеринбург\n4. Нижний Новгород",
  "id": 1
}
```

В ответ вы получите JSON вида:

```json
{
  "id": 1,
  "answer": 2,
  "reasoning": "Ответ: answer=2\n\nОбоснование: Главный кампус Университета ИТМО находится в Санкт-Петербурге. Это утверждение подтверждается информацией из текстов, где упоминается, что университет был основан в Санкт-Петербурге и расположен по юридическому адресу на Кронверкском проспекте, 49. В предложенных вариантах ответов правильным является '2. Санкт-Петербург'.",
  "sources": [
    "https://itmo.ru/",
    "https://ru.wikipedia.org/wiki/%D0%A3%D0%BD%D0%B8%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D1%82%D0%B5%D1%82_%D0%98%D0%A2%D0%9C%D0%9E",
    "https://itmo.ru/ru/page/207/ob_universitete.htm"
  ]
}
```
