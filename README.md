# Slide merger

> Create a slide show by merging slides from library

## Architecture

This project is split into

- [Python Backend](backend/README.md)
- [Python CLI](cli/README.md)
- FrontEnd (**TODO**)

Click on the links above to run these components individually

All theses components can also be run with [docker compose](docker-compose.yaml)

## Run with docker compose

### User mode

```bash
docker-compose up

# In another terminal
docker exec -it slide_merger_cli bash
uv run src/main.py output.pptx
```

### Developer mode

```bash
docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build --force-recreate

# In another terminal
docker exec -it slide_merger_cli bash
uv run src/main.py output.pptx
```

### Stop containers

```bash
docker-compose down
```
