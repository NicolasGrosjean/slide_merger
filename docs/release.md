# Release

## [RECOMMENDED] Automatically with GitHub Actions

Create a tag with the following commands

```bash
export SLIDE_MERGER_VERSION=0.0.1
git tag $SLIDE_MERGER_VERSION
git push origin $SLIDE_MERGER_VERSION
```

Docker images will be built and push to DockerHub.

## Manually with GitHub Actions

Go to [CD GitHub Actions page](https://github.com/NicolasGrosjean/slide_merger/actions/workflows/cd.yml).

Click on `Run workflow` selector and enter the image name.

## Manually build with commands

Connect to DockerHub

```bash
docker login docker.io -u nicolasgrosjean38
# Fill with token get from https://app.docker.com/accounts/nicolasgrosjean38/settings/personal-access-tokens
```

Build and push images

```bash
export SLIDE_MERGER_VERSION="0.0.1"
docker build -t docker.io/nicolasgrosjean38/slide_merger_backend:$SLIDE_MERGER_VERSION backend/
docker push docker.io/nicolasgrosjean38/slide_merger_backend:$SLIDE_MERGER_VERSION
docker build -t docker.io/nicolasgrosjean38/slide_merger_cli:$SLIDE_MERGER_VERSION cli/
docker push docker.io/nicolasgrosjean38/slide_merger_cli:$SLIDE_MERGER_VERSION
```

## Delete a tag

```bash
git tag -d $SLIDE_MERGER_VERSION
git push --delete origin $SLIDE_MERGER_VERSION
```
