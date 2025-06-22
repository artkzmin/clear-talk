# БД

## Создание БД
```bash
sudo docker run -d \
  --name ct-postgres \
  --restart unless-stopped \
  -e POSTGRES_USER=ct-postgres \
  -e POSTGRES_PASSWORD=ct-postgres \
  -e POSTGRES_DB=ct-postgres \
  -v ct-pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15
```

## Пересоздание БД
```bash
sudo docker rm -f ct-postgres && \
sudo docker volume rm ct-pgdata && \
sudo docker run -d \
  --name ct-postgres \
  --restart unless-stopped \
  -e POSTGRES_USER=ct-postgres \
  -e POSTGRES_PASSWORD=ct-postgres \
  -e POSTGRES_DB=ct-postgres \
  -v ct-pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15
```

## Генерация ключа для хеширования/шифрования
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```