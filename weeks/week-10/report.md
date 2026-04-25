# Отчет по Docker

## Команды

```bash
docker build -t products-s10 -f weeks/week-10/Dockerfile .
docker run --rm -p 8183:8183 products-s10
```

## Размер (size)

- size: (укажите размер из `docker images`)

## Слои (layers)

- layers: multi-stage (builder + runtime), отдельный слой под установку зависимостей из `requirements.txt`.
