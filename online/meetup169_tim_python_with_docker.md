# MeetUp 169 - Beginners' Python and Machine Learning - 18 Jan 2023 - Using Python with Docker

- Youtube: [https://youtu.be/eELmAk_zJIs]
- Github: [https://github.com/timcu/session-summaries/blob/master/online/meetup169_tim_python_with_docker.md]
- Meetup ONLINE: [https://www.meetup.com/beginners-python-machine-learning/events/290508652/]
- Meetup IN-PERSON: [https://www.meetup.com/beginners-python-machine-learning/events/290508637/]

To follow this tutorial you need to install Docker [https://www.docker.com] but you don't need to install Python.
For Windows and Mac, recommend that you install Docker Desktop

Docker Engine is free. Docker Desktop is free except for commercial use in a company with 250 employees or more than US$10 million annual revenue.

On Windows you will also need to install WSL 2 (Windows Subsystem for Linux 2) in features or [https://aka.ms/wsl2kernel ]

References:

- [https://docs.docker.com/get-started/]
- [https://pythonspeed.com/articles/base-image-python-docker-images/]
- [https://testdriven.io/blog/docker-best-practices/]
- [https://hub.docker.com/r/dockercore/docker/]  # old but best explains why to use containers rather than VMs

Docker creates lightweight portable containers. Much lighter than virtual machines. Each container should do one task and do it well. Containers can be linked through networks.

Check that docker is installed correctly. May need to prefix with `sudo` on Linux or Mac.

```shell
docker run hello-world
```

Create project folder `bpaml169-docker` and inside it task folder `task-hi-from-py` and change into that directory

```shell
mkdir bpaml169-docker
cd bpaml169-docker
mkdir task-hi-from-py
```

Create file `hi_from.py` in directory `task-hi-from-py`

```python
import sys
print(f'Hi from Python {sys.version}')
```

Create file `Dockerfile` in directory `task-hi-from-py`

```text
FROM python:3.11
WORKDIR /bpaml169
COPY . /bpaml169
ENTRYPOINT ["python", "hi_from.py"]
```

- FROM: Always start with a FROM instruction. This sets the base image from hub.docker.com for subsequent instructions. There are several python images for each version of python. We have specified version 3.11 of python.
- WORKDIR: sets the working directory in container for RUN CMD ENTRYPOINT COPY and ADD instructions that follow. Directory is created if it doesn't exist.
- COPY: Copy files from local machine to container. In example, first argument is rel path on local machine and second argument is absolute path in container. We could have used the equivalent `COPY . .`
- ENTRYPOINT: allows configuring a container which will run as executable. This will run `python hi_from.py` in the working directory when container is run and then container will quit when finished.

Other instructions we can provide for building

- RUN: Execute the command in a new layer on top of the current image and commit the results. For example `RUN pip install -r requirements.txt`
- CMD: Similar to ENTRYPOINT but command line arguments will replace and CMD instruction arguments, but be appended to ENTRYPOINT instruction arguments. Don't worry about this distinction for now.
- ENV: Set environment variables

Build and run

- build image using Dockerfile in current directory (.) and give it the tag name 'bpaml169-hi-from-py-image'
- run docker container based on image with tag name 'bpaml169-hi-from-py-image'

```shell
cd task-hi-from-py
docker build -t bpaml169-hi-from-py-image .
docker run bpaml169-hi-from-py-image
cd ..
```

Notice how program uses Python 3.11 even if the latest Python installed on your computer is Python 3.10

Some docker commands

```shell
docker ps  # view running containers
docker ps -a  # view all containers, even those not running
docker rm <container-id>  # Remove previously exited container with id or partial id.
docker run --rm bpaml169-hi-from-py-image  # run docker container and then automatically remove container when finished
docker run --rm -it --entrypoint bash bpaml169-hi-from-py-image # run docker container interactively and replace ENTRYPOINT with bash shell 
docker run --rm -it bpaml169-hi-from-py-image bash # run docker container interactively and replace CMD with bash shell 
docker exec -ti my_container ls  # run command ls in running container with name `my_container`, -t = pseudo-TTY, -i = interactive
docker cp my_container:/bpaml169-container ./bak/  # copy files to or from existing container which doesn't need to be running
docker images  # list available images
docker history my_container  # view how image created
```

Build container in directory task-flask for running flask app bpaml-prime-minister

```shell
mkdir task-flask
```

`Dockerfile` in directory `task-flask` to contain

```text
FROM python:3.11
WORKDIR /bpaml169
RUN git clone https://github.com/timcu/bpaml-prime-minister.git
WORKDIR bpaml-prime-minister
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN flask init-db
CMD ["flask", "run", "--host=0.0.0.0"]
```

To run the flask app we need to use `--host=0.0.0.0` so that app is visible on the network, not just the container IP address 127.0.0.1 .

The ENV command sets an environment variable which suppresses a warning when using pip as root which is OK when in docker containers but not OK normally

- build image using Dockerfile in current directory (.) and give image the tag name 'bpaml169-flask'
- run the docker container using image with tag name 'bpaml169-flask'

```shell
cd task-flask
docker build -t bpaml169-flask .
docker run --rm -p 4000:5000 bpaml169-flask
cd ..
```

Docker `docker run` flags

- `--rm` Remove the container when finished running
- `-p` Map the hosts port 4000 to container network port 5000
- `-d` Detach the running container from the shell. Then to stop the container you need to use `docker stop <CONTAINER_ID>`
- `-i` Run interactively
- `-t` Start a pseudo-TTY so can type in interactive docker (-i and -t normally used together as -ti)

Try URL [http://127.0.0.1:4000] in web browser

Create a new directory `task-gunicorn` and a new `Dockerfile` based on previous image

```text
FROM bpaml169-flask:latest
WORKDIR /bpaml169/bpaml-prime-minister
RUN pip install gunicorn
CMD ["/usr/local/bin/gunicorn", "--bind", "0.0.0.0:8000", "prime_minister:create_app()"]
```

- build container using Dockerfile in current directory (.) and give it the tag name 'bpaml169-gunicorn'
- run gunicorn in the docker container with tag name 'bpaml169-gunicorn'

```shell
cd task-gunicorn
docker build -t bpaml169-gunicorn .  
docker run --rm -p 7000:8000 bpaml169-gunicorn
cd ..
```

Try URL [http://127.0.0.1:7000] in web browser

Add a container for web server nginx to handle client requests, serve static resources, virtual hosting, security certificates, javascript clients

Create a folder `task-nginx` and files nginx.conf and Dockerfile

`nginx.conf` in directory `task-nginx`

```text
server {
    listen 80;
    location / {
        # con-gunicorn = name of container running gunicorn
        proxy_pass http://con-gunicorn:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

`Dockerfile` in directory `task-nginx`

```text
FROM nginx:1.23
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
```

Create a docker network so gunicorn can talk to flask then build nginx server

```shell
docker network create nw-bpaml169
```

```shell
cd task-nginx
docker build -t bpaml169-nginx .  
docker run --rm -d --name con-gunicorn --network nw-bpaml169 bpaml169-gunicorn
docker run --rm -d -p 8888:80 --name con-nginx --network nw-bpaml169 bpaml169-nginx
cd ..
```

Don't need to expose con-gunicorn to localhost because all access should be through nginx

Test URL [http://localhost:8888] in browser

See which containers are running. Note that they are running in background because `-d` means detached.

```shell
docker ps
docker stop con-nginx
docker stop con-gunicorn
```

Can stop using container names because we defined names when running the containers
