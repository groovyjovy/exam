FROM python:3.12

WORKDIR /app

RUN apt-get update -qq

RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH /root/.local/bin:$PATH

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/

RUN poetry install

COPY ./ /app

CMD ["bash"]
