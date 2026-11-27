# ---- Base: dependências e código da aplicação ----
FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependências primeiro: esta camada só é reconstruída quando o requirements.txt muda
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

# ---- Testes: usada pela pipeline para correr o ruff e o pytest ----
FROM base AS teste

COPY requirements-dev.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY tests/ ./tests/

# ---- Final: a imagem que é publicada e implantada (sem testes nem ferramentas de dev) ----
FROM base AS final

# Não correr como root dentro do contentor
RUN useradd --create-home appuser
USER appuser

# SHA do commit, passado pela pipeline no build (RNF-17)
ARG APP_COMMIT_SHA=desconhecido
ENV APP_COMMIT_SHA=${APP_COMMIT_SHA}

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
