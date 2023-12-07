# CSV Mapper
CSV mapper maps CSV files containing critical infrastructure performance metrics
to a live graph.

## Dependencies
This application was built on and for Linux and requires the following
dependencies:
- `docker`
- `docker-compose`

## Quick Start
This project has been designed to run within Docker containers. To setup the
project simply the `docker` and `docker-compose` dependencies. Please note that
the quick start guide has been written for Arch-based linux distributions:

```bash
sudo pacman -S docker docker-compose
```

Next start the Docker service:
```bash
sudo systemctl start docker.service
```

Finally, run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

After the project has been setup, it can be started with:
```bash
sudo docker-compose up -d
```

## Repo Structure
- `data`
  This is where Docker containers store data. Currently only the `mysql`
  container needs to store any data.
- `docker`
  This is where Docker-files are defined to build Docker containers. Each
  container that requires its own Docker-file has its own sub-directory who's
  name matches the name of the container.
- `/src`
  This is the Django project.
- `/docs`
  This is where project documentation is stored.

---

## Useful Links
- [Quickstart: Compose and Django](https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/django/)