# Slide merger

> Create a slide show by merging slides from library

## Architecture

This project is split into

- [Python Backend](backend/README.md)
- [Python CLI](cli/README.md)
- A vibe-coded [Angular Frontend](frontend/README.md)

Click on the links above to run these components individually

All theses components can also be run with [docker compose](docker-compose.yaml)

## Run with docker compose

### User mode

```bash
docker-compose up
```

Open the [application with a web browser](http://localhost:4200/)

### Developer mode

```bash
docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build --force-recreate
```

Open the [application with a web browser](http://localhost:4200/)

### Stop containers

```bash
docker-compose down
```
