# README

A simple FastAPI demo app to showcase basic backend development concepts.

The app exposes an API to work with posts, users, and votes, behind a simple auth layer.

## Getting started

### Prerequistes

The following requirements are aimed for Debian systems.

```bash
# --- Install `pip` dependency manager

$ sudo apt install python3-pip

# --- Install Docker service

$ sudo apt install ca-certificates curl
$ sudo install -m 0755 -d /etc/apt/keyrings
$ sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
$ sudo chmod a+r /etc/apt/keyrings/docker.asc

$ echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
$ sudo apt update

$ sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

$ sudo usermod -aG docker jero
```

### Setup (only once)

```bash
# --- Create SSH key and upload to GitHub

$ cd ~/.ssh
$ ssh-keygen -f github-jerosanchez
$ nano config

# jerosanchez @ GitHub
Host github-jerosanchez
    HostName github.com
    User git
    IdentityFile ~/.ssh/github-jerosanchez
    IdentitiesOnly yes

# --- Clone the project from GitHub

$ cd path/to/projects
$ git clone git@github.com:jerosanchez/fastapi-demo.git
$ cd fastapi-demo

# --- Create virtual environment

$ python -m venv .venv

# --- Activate local virtual environment

$ source venv/bin/activate

# --- Install dependencies

$ pip install -r requirements.txt

# --- Create Docker network

$ docker network create internal

# --- Prepare .env file

$ cp .env.example .env
```

### Run

```bash
# Start/Restart dockerized app
$ make dev-up

# (Optional) Insert sample data
$ make db-sample-data
```

### Dev process

This project includes a `Makefile` to ease the development process.

Please, use the following comands as part of your QA process before you commit and push changes:

```bash
# Check for linting issues
$ make lint

# Format source code according to rules
$ make format

# Run all tests
$ make test
```

Take a look into `Makefile` to see other usefull commands available.