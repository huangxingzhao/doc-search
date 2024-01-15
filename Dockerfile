# syntax=docker/dockerfile:1
# 保留上面这个注释以使用 Docker BuildKit

################################
# PYTHON-BASE
# 准备好所有构建和运行时的环境变量，替换国内软件源。
################################
FROM python:3.9.13-slim

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple && pip install poetry==1.6.1 && poetry self add poetry-plugin-pypi-mirror

COPY pyproject.toml poetry.lock /APP/

WORKDIR /APP

RUN export POETRY_PYPI_MIRROR_URL=https://mirrors.cloud.tencent.com/pypi/simple/ && poetry install && playwright install chrome

COPY . /APP/

WORKDIR /APP

CMD poetry run python main.py

#RUN poetry run python main.py