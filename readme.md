# CSV Mapper
CSV mapper maps CSV files containing critical infrastructure performance metrics
to a live graph.

## Dependencies
This application was built on and for Linux and requires the following
dependencies:
- `docker`
- `docker-compose`

## Running the Project
This project has been designed to run within Docker containers. To setup the
project simply install the dependencies and execute `setup.sh`:

```bash
chmod +x setup.sh
./setup.sh
```

After the project has been setup, it can be started with:
```bash
sudo docker-compose up -d
```

## Repo Structure
- `/csv_mapper`
  This is the Django project.
- `/docs`
  This is where project documentation is stored.