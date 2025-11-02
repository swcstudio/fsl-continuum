FROM node:18-alpine AS builder

# Install build dependencies
RUN apk add --no-cache python3 make g++

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY src ./src

# Build TypeScript
RUN npm run build

# Production stage
FROM node:18-alpine AS production

# Install runtime dependencies
RUN apk add --no-cache curl bind-tools

# Create non-root user
RUN addgroup -g 1001 -S zeroserve && \
    adduser -S zeroserve -u 1001

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install only production dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy built application
COPY --from=builder /app/dist ./dist

# Change ownership
RUN chown -R zeroserve:zeroserve /app

# Switch to non-root user
USER zeroserve

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV ZEROSERVE_CACHE_TTL=300000
ENV ZEROSERVE_RATE_LIMIT=30

# Default command (HTTP transport)
CMD ["node", "dist/cli.js", "http"]

# Labels
LABEL maintainer="ZeroServe Team" \
      version="1.0.0" \
      description="ZeroServe MCP Server - AI-native domain scanning and infrastructure analysis" \
      org.opencontainers.image.title="zeroserve-mcp-server" \
      org.opencontainers.image.description="ZeroServe MCP Server - AI-native domain scanning and infrastructure analysis" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.vendor="ZeroServe" \
      org.opencontainers.image.licenses="MIT"
