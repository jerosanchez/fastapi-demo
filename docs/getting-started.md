# Getting Started

## Prerequisites

### Python & venv

To run the project locally, you need Python 3 and the venv module for virtual environments.

```bash
sudo apt install python3-pip python3.13-venv
```

### Docker

Docker is required for running the app and its dependencies in containers.

#### Install Docker and dependencies

```bash
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
sudo reboot
```

#### Create Docker network

Create a dedicated Docker network for internal communication between containers.

```bash
docker network create internal
```

---

## Installation

Clone the repository and set up your Python environment.

```bash
git clone git@github.com:jerosanchez/fastapi-demo.git
cd fastapi-demo

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
```

---

## Usage

Start the application and load sample data.

```bash
make dev-up
make db-sample-data
```

---

## Development

Lint and format your code to maintain consistency.

```bash
make lint
make format
```

---

## Testing

Run the test suite to verify functionality.

```bash
make test
```

---

## Notes

- See `Makefile` for more commands.
- SSH setup for GitHub is optional and not required for running the app.
- For more info, see [FastAPI documentation](https://fastapi.tiangolo.com/).
