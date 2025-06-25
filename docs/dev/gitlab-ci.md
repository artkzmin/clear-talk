# Gitlab CI

## Установка Gitlab Runner
```bash
docker run -d --name gitlab-runner --restart always \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:alpine
```

## Регистрация Gitlab Runner внутри Docker
```bash
docker run --rm -it \
    -v /srv/gitlab-runner/config:/etc/gitlab-runner \
    gitlab/gitlab-runner:alpine register
```
- Выбрать executor - `docker`
- Выбрать default Docker image - `docker:dind`

## Редактирование конфига
```bash
vim /srv/gitlab-runner/config/config.toml
```
Изменяем `volumes = ["/cache"]` на:
```bash
volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]
```