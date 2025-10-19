# FastAPI Demo

A simple FastAPI app with users, posts, votes, and basic authentication.

## Features

- RESTful API for posts, users, votes
- JWT authentication
- Docker support
- Sample data loader
- Makefile for common dev tasks

## Installation

```bash
# Install Python & venv
sudo apt install python3-pip python3.13-venv

# Clone repo & enter project
git clone git@github.com:jerosanchez/fastapi-demo.git
cd fastapi-demo

# Create & activate virtualenv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Prepare .env file
cp .env.example .env
```

## Docker

```bash
# Install Docker
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
sudo reboot

# Create Docker network
docker network create internal
```

## Usage

```bash
# Start app (Docker)
make dev-up

# Load sample data
make db-sample-data
```

## Development

```bash
# Lint code
make lint

# Format code
make format
```

## Testing

```bash
# Run tests
make test
```

## Notes

- See `Makefile` for more commands.
- SSH setup for GitHub is optional and not required for running the app.
- For more info, see [FastAPI documentation](https://fastapi.tiangolo.com/).