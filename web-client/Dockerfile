FROM node:lts-slim as base
RUN apt-get update && apt-get install -y python3
RUN corepack enable
RUN corepack prepare pnpm@9.0.6 --activate
ARG PORT=3000


WORKDIR /src

# Build
FROM base as build

COPY package.json pnpm-lock.yaml .
RUN pnpm install

COPY . .
RUN python3 bypass.py
RUN pnpm run build

# Run
FROM base

ENV PORT=$PORT

COPY --from=build /src/.output /src/.output
# Optional, only needed if you rely on unbundled dependencies
# COPY --from=build /src/node_modules /src/node_modules

CMD [ "node", ".output/server/index.mjs" ]