FROM python:3.11-alpine

# pycファイル(および__pycache__)の生成を行わないようにする
ENV PYTHONDONTWRITEBYTECODE=1
# 標準出力・標準エラーのストリームのバッファリングを行わない
ENV PYTHONUNBUFFERED=1
# コンテナのワークディレクトリを/codeに指定
WORKDIR /var/task

RUN apk add gcc && \
    apk add musl-dev && \
    apk add mariadb-connector-c-dev && \
    apk add mariadb-dev

COPY --chmod=777 ./container/python/entrypoint.sh /tmp/entrypoint.sh
COPY --chmod=777 ./container/python/lib-update.sh /tmp/lib-update.sh
COPY ./container/python/requirements.txt /tmp/requirements.txt

# コンテナ内でpipをアップグレード
RUN pip install --upgrade pip

# pip install -r requirements.txtを実行
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY ./source /var/task

CMD ["sh", "/tmp/entrypoint.sh"]
