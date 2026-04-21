FROM node:20-alpine

WORKDIR /app

COPY package.json ./
RUN corepack enable && corepack prepare pnpm@9.0.0 --activate && pnpm install

COPY . .

EXPOSE 3000
CMD ["pnpm", "dev", "--host", "0.0.0.0", "--port", "3000"]
