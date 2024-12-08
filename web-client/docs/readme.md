# Общее 
Базовое описание клиентской части приложения. Workflow описан в [./workflow.md].

# Стек
Основными инструментами для клиентской части выступают:
- Nuxt3 (Vue)
- Tailwindcss
- NuxtUI

# Запуск
1. Необходимо загрузить зависимости с помощью пакетного менеджера:
```bash
pnpm install
```
2. Скопируйте .env.example в .env:
```bash
cp .env.example .env
```
3. В зависимости от окружения установите необходимые значения для переменных окружения в .env.
4. Для режима разработки выполните:
```bash
pnpm run dev
```
Для production сборки необходимо выполнить:
```bash
pnpm run build
```