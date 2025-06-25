# Генерация ключа для хеширования/шифрования
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

# Создание сети для Docker контейнеров
```bash
docker network create clear-talk-network
```