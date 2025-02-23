# MeetUp 212 - Beginners' Python and Machine Learning - 19 Feb 2025 - Using Python with Podman

- Youtube: [https://youtu.be/IYhghxB_h18]
- Github: [https://github.com/timcu/session-summaries/blob/master/online/meetup212_tim_python_with_podman.md]
- Meetup ONLINE: [https://www.meetup.com/beginners-python-machine-learning/events/305896090/]

To follow this tutorial you need to install Podman [https://podman.io] but you don't need to install Python.

For Windows and Mac, recommend that you install Podman Desktop

Podman is an alternative to Docker

Docker engine is free. Docker Desktop is free except for commercial use in a company with 250 employees or more than US$10 million annual revenue.

Podman engine and Podman Desktop are both free. Podman Desktop can manage Podman and Docker containers with Podman engine or Docker engine.

Podman is daemonless which solves a problem I was having with Docker. Docker Desktop starts a different daemon to the Docker engine and I was having compatibility problems with different daemons.

Podman has rootless containers so don't need to use `sudo` on Mac or Linux or `Administrator` on Windows.

## Installing podman

- Windows [https://github.com/containers/podman/blob/main/docs/tutorials/podman-for-windows.md] We only need podman CLI for this session.
- Mac [https://podman.io]
- Debian based Linux `sudo apt install podman`
- Red Hat based Linux. Usually installed by default. If not `sudo dnf install podman`

References:

- [https://podman.io/]
- [https://developers.redhat.com/cheat-sheets/podman-cheat-sheet]
- [https://opensource.com/article/19/2/how-does-rootless-podman-work]
- [https://pythonspeed.com/articles/base-image-python-docker-images/]
- [https://hub.docker.com/_/python]  documentation on the python image
- [https://hub.docker.com/r/dockercore/docker/]  old but best explains why to use containers rather than VMs
- [https://www.redhat.com/en/blog/compose-podman-pods] Using podman pods rather than docker compose

Like Docker, Podman creates lightweight portable containers. Much lighter than virtual machines. Each container should do one task and do it well. Containers can be linked through networks.

Check that podman is installed correctly.

```shell
podman run quay.io/podman/hello
```

Can also run the Docker hello-world

```shell
podman run hello-world  # or explicitly `podman run docker.io/library/hello-world`
```

Create project folder `bpaml212-podman` and inside it task folder `task-hi-from-py` and change into that directory

```shell
mkdir bpaml212-podman
cd bpaml212-podman
mkdir task-hi-from-py
```

Create file `hi_from.py` in directory `task-hi-from-py`

```python
import sys
print(f'Hi from Python {sys.version}')
```

Create file `Containerfile` in directory `task-hi-from-py`. This file could also be called `Dockerfile` if you want to stay compatible with Docker.

```text
FROM docker.io/library/python:3.11
WORKDIR /bpaml212
COPY . /bpaml212
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

- build image using `Containerfile` in current directory (.) and give it the tag name 'bpaml212-hi-from-py-image'
- run podman container based on image with tag name 'bpaml212-hi-from-py-image'

```shell
cd task-hi-from-py
podman build -t bpaml212-hi-from-py-image .
podman run bpaml212-hi-from-py-image
cd ..
```

Notice how program uses Python 3.11 even if the latest Python installed on your computer is Python 3.10

Some podman commands

```shell
podman ps  # view running containers
podman ps -a  # view all containers, even those not running
podman rm <container-id>  # Remove previously exited container with id or partial id.
podman run --rm bpaml212-hi-from-py-image  # run podman container and then automatically remove container when finished
podman run --rm -it --entrypoint bash bpaml212-hi-from-py-image # run podman container interactively and replace ENTRYPOINT with bash shell 
podman run --rm -it bpaml212-hi-from-py-image bash # run podman container interactively and replace CMD with bash shell 
podman exec -ti my_container ls  # run command ls in running container with name `my_container`, -t = pseudo-TTY, -i = interactive
podman cp my_container:/bpaml212-container ./bak/  # copy files to or from existing container which doesn't need to be running
podman images  # list available images
podman history my_container  # view how image created
```

Build container in directory task-flask for running flask app bpaml-prime-minister

```shell
mkdir task-flask
```

`Containerfile` in directory `task-flask` to contain

```text
FROM docker.io/library/python:3.11
WORKDIR /bpaml212
RUN git clone https://github.com/timcu/bpaml-prime-minister.git
WORKDIR bpaml-prime-minister
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN flask init-db
CMD ["flask", "run", "--host=0.0.0.0"]
```

To run the flask app we need to use `--host=0.0.0.0` so that app is visible on the network, not just the container IP address 127.0.0.1 .

The ENV command sets an environment variable which suppresses a warning when using pip as root which is OK when in podman containers but not OK normally

- build image using `Containerfile` in current directory (.) and give image the tag name 'bpaml212-flask'
- run the podman container using image with tag name 'bpaml212-flask'

```shell
cd task-flask
podman build -t bpaml212-flask .
podman run --rm -p 4000:5000 bpaml212-flask
cd ..
```

Docker `podman run` flags

- `--rm` Remove the container when finished running
- `-p` Map the hosts port 4000 to container network port 5000
- `-d` Detach the running container from the shell. Then to stop the container you need to use `podman stop <CONTAINER_ID>`
- `-i` Run interactively
- `-t` Start a pseudo-TTY so can type in interactive podman (-i and -t normally used together as -ti)

Try URL [http://127.0.0.1:4000] in web browser

Create a new directory `task-gunicorn` and a new `Containerfile` based on previous image

```text
FROM bpaml212-flask:latest
WORKDIR /bpaml212/bpaml-prime-minister
RUN pip install gunicorn
CMD ["/usr/local/bin/gunicorn", "--bind", "0.0.0.0:8000", "prime_minister:create_app()"]
```

- build container using `Containerfile` in current directory (.) and give it the tag name 'bpaml212-gunicorn'
- run gunicorn in the podman container with tag name 'bpaml212-gunicorn'

```shell
cd task-gunicorn
podman build -t bpaml212-gunicorn .  
podman run --rm -p 7000:8000 bpaml212-gunicorn
cd ..
```

Try URL [http://127.0.0.1:7000] in web browser

Add a container for web server nginx to handle client requests, serve static resources, virtual hosting, security certificates, javascript clients

Create a folder `task-nginx` and files `nginx.conf` and `Containerfile`

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

`Containerfile` in directory `task-nginx`

```text
FROM docker.io/nginx:1.23
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
```

Create a podman network so gunicorn can talk to flask then build nginx server

```shell
podman network create nw-bpaml212
```

```shell
cd task-nginx
podman build -t bpaml212-nginx .  
podman run --rm -d --name con-gunicorn --network nw-bpaml212 bpaml212-gunicorn
podman run --rm -d -p 8888:80 --name con-nginx --network nw-bpaml212 bpaml212-nginx
cd ..
```

Don't need to expose con-gunicorn to localhost because all access should be through nginx

Test URL [http://127.0.0.1:8888] in browser

See which containers are running. Note that they are running in background because `-d` means detached.

```shell
podman ps
podman stop con-nginx con-gunicorn
```

Can use container names to stop because we defined names when running the containers

When rootless on Ubuntu, this gives warning message about not having permission to clean up network.

### Using pod rather than network (podman only. not docker)

```shell
podman pod create -p 8888:80 pod-bpaml212
podman run --rm -d --name con-gunicorn --pod pod-bpaml212 bpaml212-gunicorn
podman run --rm -d --name con-nginx --pod pod-bpaml212 bpaml212-nginx
podman ps  # see all running containers including pod
podman pod ps  # list all pods and their state, running or exited
podman pod stop pod-bpaml212  # stop all containers in pod and then pod.
podman pod rm pod-bpaml212  # remove the pod
```

No warning messages shutting down, even when rootless on Ubuntu.
