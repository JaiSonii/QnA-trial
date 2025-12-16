# frontend/Dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependency files
COPY package.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the Next.js application
RUN npm run build

# Production image, copy all the files and run next
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Copy necessary files from builder
COPY --from=builder /app/package.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000

CMD ["npm", "start"]