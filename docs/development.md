# БД

## Создание БД
```bash
sudo docker run -d \
  --name clear-talk-postgres \
  --restart unless-stopped \
  -e POSTGRES_USER=clear-talk-postgres \
  -e POSTGRES_PASSWORD=clear-talk-postgres \
  -e POSTGRES_DB=clear-talk-postgres \
  -v clear-talk-pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network clear-talk-network \
  postgres:15
```

## Пересоздание БД
```bash
sudo docker rm -f clear-talk-postgres && \
sudo docker volume rm clear-talk-pgdata && \
sudo docker run -d \
  --name clear-talk-postgres \
  --restart unless-stopped \
  -e POSTGRES_USER=clear-talk-postgres \
  -e POSTGRES_PASSWORD=clear-talk-postgres \
  -e POSTGRES_DB=clear-talk-postgres \
  -v clear-talk-pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network clear-talk-network \
  postgres:15
```

## Генерация ключа для хеширования/шифрования
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## Создание сети для Docker контейнеров
```
sudo docker network create clear-talk-network
```
