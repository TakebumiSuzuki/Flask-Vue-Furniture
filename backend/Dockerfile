FROM python:3.12.11-slim-bullseye

# キャッシュファイルである .pyc ファイルを生成させないようにする設定
# 1 は true（真）や「有効」を意味すると考えてよい
ENV PYTHONDONTWRITEBYTECODE=1

# print() 文などが即座に出力ストリームに送られるため、デバッグが非常にしやすくなります。
ENV PYTHONUNBUFFERED=1

# WORKDIRの機能: WORKDIR /app と記述すると、/app ディレクトリが存在しない場合は自動的に作成してくれます
WORKDIR /backend

COPY requirements.txt .

# pip はダウンロードしたパッケージをキャッシュとして一時的に保存します。--no-cache-dirでこれを無効に。
# -r と書くと個別パッケージではなく、requirements.txt に記述されているパッケージを一括インストール。
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 実際にネットワークを設定するのではなく、5000番ポートで通信を待ち受ける予定だ、ということを記しているのみ
EXPOSE 5000

# --host=0.0.0.0 により、コンテナ内部（127.0.0.1）からのアクセスも含め全ての宛先からの通信を受ける
CMD [ "flask", "run", "--host=0.0.0.0" ]

