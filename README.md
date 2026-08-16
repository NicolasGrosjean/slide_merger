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

**TODO:** Make it

### Developer mode

```bash
docker-compose up --build --force-recreate
docker exec -it slide_merger_cli_1 bash
uv run src/main.py output.pptx
```

### Stop containers

```bash
docker-compose down
```
