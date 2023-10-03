# CONTRIBUTING

## How to run the Dockerfile locally on linux/mac

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run"
```
## How to run the Dockerfile locally on windows

```
docker run -dp 5005:5000 -w /app -v "%cd%:/app" zura sh -c "flask run"
```