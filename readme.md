# CSV Mapper
An online platform that provides real-time graphs driven by CSV data.

![Docker Publish Result](https://github.com/alexjthomson/csv-mapper/actions/workflows/docker_publish.yml/badge.svg)
![Django Test Result](https://github.com/alexjthomson/csv-mapper/actions/workflows/django_tests.yml/badge.svg)
![Security Scan Result](https://github.com/alexjthomson/csv-mapper/actions/workflows/security_scan.yml/badge.svg)

## Online Demo
An online demonstration of the application can be found at
[https://csv.alexthomson.dev](https://csv.alexthomson.dev/account/login).

![Screenshot of the application dashboard](https://github.com/alexjthomson1882/csv-mapper/blob/master/docs/images/screenshots/dashboard/user_standard.png)

## Rationale
This project was created to allow Gamma Telecom to view performance critical
business systems.

## Dependencies
This application was built to run inside a Docker container on a Linux host. The
following dependencies are required:
- `docker`
- `docker-compose`

## Quick-Start Guide
This application was built to run in a Docker container in a stack alongside a
MySQL container. This guide is written for Arch based Linux distributions.
Please ensure each of the required packages listed above have been installed
before continuing with this guide.

1. Clone the git repository to a Linux host.
2. Start the `docker.service` service. On Systemd based distributions this can
   be done by running `systemctl start docker.service` with super-user access.
3. Run `setup.sh`. This will create any missing files or directories on your
   system. Unless you have the secrets used to create the original database,
   please also empty the contents of the MySQL directory found at `data/mysql`.
4. The container and MySQL database should now be setup. The application can be
   started by running `docker-compose up -d`. You may need to run this as a
   superuser if you do not have a rootless Docker configuration.

## Developer Guide
To continue development of this project, please follow the
[Quick-Start Guide](#quick-start-guide) above.

Once the project is setup on your local system, run the Docker Compose file
[`docker-compose-dev.yaml`](docker-compose.yaml) using the command:
`docker-compose -f docker-compose-dev.yaml up --build` to rebuild the container
from the local source files and run it on your system. Unless you are changing
anything related to the [`dockerfile`](dockerfile), you can omit the `--build`
flags on the command.

Once the command has finished, you will have an instance of the project running
which reacts to any changes made to the [`src`](src/) directory.

## Technologies Used
A high-level overview of each of the primary technologies to create the
application.

- Docker, Docker Compose
- Python, Pip, Django
- Bootstrap, HTML, CSS, JavaScript, jQuery, ChartJS
- MySQL
- Visual Studio Code
- Obsidian (note taking)
- Arch Linux (deployment server)
- Bandit, Safety (security & vulnerability testing)
- GitHub, GitHub Actions (automated testing)

---

## Useful Links
- [Online Demo](https://csv.alexthomson.dev/account/login)
- [Portfolio](https://alexthomson.dev/)
- [Quick-Start: Docker & Docker Compose](https://docs.docker.com/compose/gettingstarted/)
- [Quick-Start: Compose & Django](https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/django/)