# ---- Base: dependências e código da aplicação ----
FROM node:24.22.3-alpine AS base

WORKDIR /app

# Dependências primeiro: esta camada só é reconstruída quando o package-lock.json muda
COPY package.json package-lock.json ./
RUN npm ci --no-fund --no-audit

COPY . .

# ---- Testes: usada pela pipeline para correr o ESLint e o Vitest ----
FROM base AS teste

# ---- Build: gera os ficheiros estáticos em dist/ ----
FROM base AS build

RUN npm run build

# ---- Final: a imagem que é publicada e implantada (só nginx e os ficheiros estáticos) ----
# Imagem do nginx que não corre como root e escuta na porta 8080
FROM nginxinc/nginx-unprivileged:1.30.6-alpine AS final

# SHA do commit, passado pela pipeline no build (RNF-17)
ARG APP_COMMIT_SHA=desconhecido

USER root
RUN mkdir -p /usr/share/nginx/metro \
    && printf '{"servico":"web","commit":"%s"}' "$APP_COMMIT_SHA" > /usr/share/nginx/metro/version.json
USER nginx

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080
