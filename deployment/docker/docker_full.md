# 🐳 Docker — Learning Guide

> Docker is a platform for **building, shipping, and running applications in containers** — isolated, lightweight environments that work consistently across any machine.

---

## 📚 Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Installation](#2-installation)
3. [Docker Image](#3-docker-image)
4. [Dockerfile](#4-dockerfile)
5. [Docker Container](#5-docker-container)
6. [Docker Volume](#6-docker-volume)
7. [Docker Network](#7-docker-network)
8. [Docker Compose](#8-docker-compose)
9. [Docker Registry](#9-docker-registry)
10. [Multi-stage Build](#10-multi-stage-build)
11. [Best Practices](#11-best-practices)

---

## 1. Core Concepts

| Concept | Description |
|---|---|
| **Image** | A read-only template used to create containers (like a blueprint) |
| **Container** | A running instance of an image |
| **Dockerfile** | A script of instructions to build a custom image |
| **Volume** | Persistent storage that survives container restarts |
| **Network** | Virtual network allowing containers to communicate |
| **Registry** | A storage service for Docker images (e.g., Docker Hub) |
| **Docker Compose** | Tool for defining and running multi-container applications |

---

## 2. Installation

```bash
# Verify installation
docker --version
docker compose version

# Run a test container
docker run hello-world
```

> 📖 Install Docker: https://docs.docker.com/get-docker/

---

## 3. Docker Image

An **image** is a read-only, layered filesystem used to create containers.

```bash
# Pull an image from Docker Hub
docker pull python:3.11-slim

# List local images
docker images

# Remove an image
docker rmi python:3.11-slim

# Remove all unused images
docker image prune -a

# Inspect an image
docker inspect python:3.11-slim

# Show image layers/history
docker history python:3.11-slim
```

### Image naming convention

```
[registry/][username/]repository[:tag]

# Examples:
python:3.11-slim              # Official image, tag 3.11-slim
nginx:latest                  # Official image, latest tag
myuser/myapp:1.0.0            # User image on Docker Hub
ghcr.io/myorg/myapp:v2.0      # GitHub Container Registry
```

---

## 4. Dockerfile

A **Dockerfile** is a text file with instructions to build a custom image.

### Basic structure

```dockerfile
# Base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency file first (for layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose port (documentation only, does not publish)
EXPOSE 8000

# Default command to run when container starts
CMD ["python", "main.py"]
```

### Key Dockerfile instructions

| Instruction | Description |
|---|---|
| `FROM` | Base image to build from |
| `WORKDIR` | Set the working directory |
| `COPY` | Copy files from host to image |
| `ADD` | Like COPY but also supports URLs and auto-extracts archives |
| `RUN` | Execute a command during build |
| `ENV` | Set environment variables |
| `ARG` | Build-time variable (not available at runtime) |
| `EXPOSE` | Document which port the app listens on |
| `CMD` | Default command when container starts (overridable) |
| `ENTRYPOINT` | Fixed command, `CMD` becomes its arguments |
| `VOLUME` | Declare a mount point for persistent data |
| `USER` | Set the user to run subsequent commands |
| `LABEL` | Add metadata to the image |

### Build an image

```bash
# Build from Dockerfile in current directory
docker build -t myapp:1.0.0 .

# Build with a specific Dockerfile
docker build -f path/to/Dockerfile -t myapp:1.0.0 .

# Build with build arguments
docker build --build-arg ENV=production -t myapp:1.0.0 .

# Build without using cache
docker build --no-cache -t myapp:1.0.0 .
```

### ENV vs ARG

```dockerfile
# ARG — only available during build
ARG APP_VERSION=1.0.0

# ENV — available at runtime inside the container
ENV APP_ENV=production
ENV DATABASE_URL=postgresql://localhost/mydb
```

### ENTRYPOINT vs CMD

```dockerfile
# CMD only — fully overridable
CMD ["python", "main.py"]

# ENTRYPOINT + CMD — ENTRYPOINT is fixed, CMD is default args
ENTRYPOINT ["python"]
CMD ["main.py"]

# Running: docker run myapp other_script.py
# → executes: python other_script.py
```

---

## 5. Docker Container

A **container** is a running instance of an image.

```bash
# Run a container (foreground)
docker run python:3.11-slim python --version

# Run in detached mode (background)
docker run -d --name my_container nginx

# Run with port mapping (host:container)
docker run -d -p 8080:80 --name webserver nginx

# Run with environment variables
docker run -e DATABASE_URL=postgresql://... myapp

# Run interactively
docker run -it python:3.11-slim bash

# Run and remove container when it exits
docker run --rm python:3.11-slim python --version
```

### Managing containers

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop a container
docker stop my_container

# Start a stopped container
docker start my_container

# Restart a container
docker restart my_container

# Remove a container
docker rm my_container

# Remove all stopped containers
docker container prune

# View container logs
docker logs my_container
docker logs -f my_container        # Follow live logs
docker logs --tail 100 my_container

# Execute a command inside a running container
docker exec -it my_container bash
docker exec my_container ls /app

# Copy files between host and container
docker cp file.txt my_container:/app/file.txt
docker cp my_container:/app/output.txt ./output.txt

# View resource usage
docker stats

# Inspect container details
docker inspect my_container
```

### Restart policies

```bash
docker run -d --restart=always nginx
```

| Policy | Behavior |
|---|---|
| `no` | Never restart (default) |
| `always` | Always restart, even after Docker daemon restarts |
| `on-failure` | Restart only on non-zero exit code |
| `unless-stopped` | Always restart unless manually stopped |

---

## 6. Docker Volume

**Volumes** provide persistent storage that survives container restarts and deletions.

```bash
# Create a named volume
docker volume create mydata

# List volumes
docker volume ls

# Inspect a volume
docker volume inspect mydata

# Remove a volume
docker volume rm mydata

# Remove all unused volumes
docker volume prune
```

### Mount types

```bash
# Named volume (managed by Docker, recommended for persistent data)
docker run -d -v mydata:/app/data myapp

# Bind mount (maps a host directory directly into the container)
docker run -d -v $(pwd)/data:/app/data myapp

# Read-only bind mount
docker run -d -v $(pwd)/config:/app/config:ro myapp

# tmpfs mount (in-memory, not persisted)
docker run -d --tmpfs /tmp myapp
```

### In Dockerfile

```dockerfile
# Declare a volume mount point
VOLUME ["/app/data"]
```

---

## 7. Docker Network

**Networks** allow containers to communicate with each other securely.

```bash
# List networks
docker network ls

# Create a custom network
docker network create mynetwork

# Run a container connected to a network
docker run -d --name db --network mynetwork postgres

# Connect a running container to a network
docker network connect mynetwork my_container

# Disconnect from a network
docker network disconnect mynetwork my_container

# Inspect a network
docker network inspect mynetwork

# Remove a network
docker network rm mynetwork
```

### Network drivers

| Driver | Description |
|---|---|
| `bridge` | Default for standalone containers on the same host |
| `host` | Container shares the host's network namespace |
| `none` | No networking |
| `overlay` | Multi-host networking (Docker Swarm) |

### Container communication via DNS

Containers on the same custom network can reach each other by **container name**:

```python
# In your app code, use the container name as hostname:
db_url = "postgresql://postgres:password@db:5432/mydb"
#                                          ^^
#                                 container name acts as hostname
```

---

## 8. Docker Compose

**Docker Compose** defines and runs multi-container applications using a single YAML file.

### Basic `docker-compose.yaml`

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./app:/app
    networks:
      - backend

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "user"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

volumes:
  pgdata:

networks:
  backend:
```

### Common commands

```bash
# Start all services (build if needed)
docker compose up

# Start in detached mode
docker compose up -d

# Build images before starting
docker compose up -d --build

# Stop services
docker compose down

# Stop and remove volumes
docker compose down --volumes

# View logs
docker compose logs -f

# View logs of a specific service
docker compose logs -f app

# Scale a service
docker compose up -d --scale app=3

# Execute a command inside a service
docker compose exec app bash

# List running services
docker compose ps

# Pull latest images
docker compose pull

# Restart a specific service
docker compose restart app
```

### Using `.env` file with Compose

```dotenv
# .env
POSTGRES_USER=myuser
POSTGRES_PASSWORD=secret
APP_PORT=8000
```

```yaml
# docker-compose.yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
  app:
    ports:
      - "${APP_PORT}:8000"
```

### `depends_on` with health checks

```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy   # wait until DB is healthy
  db:
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 5s
      retries: 5
```

---

## 9. Docker Registry

A **registry** stores and distributes Docker images.

```bash
# Login to Docker Hub
docker login

# Tag an image for pushing
docker tag myapp:1.0.0 myusername/myapp:1.0.0

# Push to Docker Hub
docker push myusername/myapp:1.0.0

# Pull from Docker Hub
docker pull myusername/myapp:1.0.0

# Logout
docker logout
```

### Common registries

| Registry | URL |
|---|---|
| Docker Hub | `hub.docker.com` |
| GitHub Container Registry | `ghcr.io` |
| Google Artifact Registry | `gcr.io` |
| AWS ECR | `<account>.dkr.ecr.<region>.amazonaws.com` |

---

## 10. Multi-stage Build

Multi-stage builds produce **smaller, production-ready images** by separating build and runtime stages.

```dockerfile
# ─── Stage 1: Build ───────────────────────────────────────────────────────────
FROM python:3.11 AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ─── Stage 2: Runtime ─────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy only installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application source
COPY . .

ENV PATH=/root/.local/bin:$PATH

CMD ["python", "main.py"]
```

> The final image only contains the runtime stage — no build tools, no cache, much smaller.

---

## 11. Best Practices

### Dockerfile
- ✅ Use specific image tags (e.g., `python:3.11-slim`), not `latest`
- ✅ Use `.dockerignore` to exclude unnecessary files
- ✅ Copy `requirements.txt` before source code to leverage layer caching
- ✅ Use `--no-cache-dir` with `pip install` to reduce image size
- ✅ Use multi-stage builds for production images
- ✅ Run as a non-root user for security
- ✅ Combine `RUN` commands with `&&` to reduce layers

### `.dockerignore` example

```
.git
.venv
__pycache__
*.pyc
*.pyo
.env
logs/
*.log
README.md
tests/
```

### Security
```dockerfile
# Create and use a non-root user
RUN adduser --disabled-password --gecos "" appuser
USER appuser
```

### Layer caching — install dependencies first

```dockerfile
# ✅ Good: requirements.txt copied before source code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ❌ Bad: any source code change invalidates the pip install layer
COPY . .
RUN pip install -r requirements.txt
```

---

## 📎 Useful Links

- 📖 [Official Docker Docs](https://docs.docker.com)
- 📖 [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/)
- 📖 [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- 🐙 [Docker GitHub](https://github.com/docker)
- 🎓 [Play with Docker (browser sandbox)](https://labs.play-with-docker.com)