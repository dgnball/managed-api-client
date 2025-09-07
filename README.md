# Managed API Client

This project demonstrates a context-managed API client in both sync and async styles.

## Testing

Run the tests:
```bash
pytest
```

## UV Setup

```bash
# install uv (mac)
brew install uv

# install python 3.13
uv python install 3.13

# create a virtual env
uv venv

# pin the version to the project
uv python pin 3.13

# get all the dependencies from the lock file
uv sync
```