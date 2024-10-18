# The builder image, used to build the virtual environment
# The builder image has more dependencies, like gcc, since it need to compile and build the packages
# The runtime image used later does not need these things, and can be leaner. Hence having separate images
# for building and running, so the running image can be lighter
# The builder basically created the virtual environment (i.e the .venv directory), which the runtime image can then just use and copy over

# DOCKER_BUILDKIT=1 docker build --target=runtime . -t langchain-chainlit-chat-app:latest
# docher-compose up

FROM python:3.12-bookworm as builder

RUN apt-get update \
    && apt-get install -y git \
    && apt-get install -y default-libmysqlclient-dev \
    && apt-get install -y gcc

ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mariadb -I/usr/include/mariadb/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu/ -lmariadb"

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

ENV HOST=0.0.0.0
ENV LISTEN_PORT 8000
EXPOSE 8000

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR
RUN pip install pysqlite3-binary

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.12-bookworm as runtime

RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev \
    && apt-get install -y sqlite3

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

ENV DATA_SOURCE_URI=mysql+mysqldb://user:password@db/feedback
ENV OPENAI_API_KEY=""
ENV AZURE_OPENAI_API_VERSION=2023-12-01-preview
ENV AZURE_OPENAI_ENDPOINT=https://kanari-chatbot-instance-us.openai.azure.com/
ENV AZURE_OPENAI_API_KEY=081c3bc206a440938eac11b62a222bd6
ENV AZURE_OPENAI_REGION=eastus
ENV AZURE_OPENAI_DEPLOYMENT_NAME=kanariGpt35
ENV VECTOR_STORE_DIRECTORY=./.cache/vector_store

# Copy the virtual environment directory that was created in the builder image
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY ./public ./public
COPY ./sql_bot ./sql_bot
COPY ./.chainlit ./.chainlit
COPY chainlit.md ./

CMD ["bash", "-m", "chainlit", "run", "sql_bot/app.py", "-h", "--port", "8000"]
