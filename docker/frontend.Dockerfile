FROM node:22-alpine AS builder

WORKDIR /app
COPY package.json package-lock.json ./
COPY frontend/package.json ./frontend/package.json
RUN npm ci
COPY frontend ./frontend
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
RUN npm run build --workspace=frontend

FROM nginx:1.27-alpine AS production

COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/frontend/out /usr/share/nginx/html
EXPOSE 80
