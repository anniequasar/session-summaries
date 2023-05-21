# MeetUp 183 - Beginners' Python and Machine Learning - 24 May 2023 - Using Python with AMQP and Docker

- Youtube: https://youtu.be/eELmAk_zJIs
- Github:  https://github.com/timcu/session-summaries/blob/master/online/meetup183_tim_python_rabbitmq_and_docker.md
- Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/293609551/

To follow this tutorial you need to install Docker https://www.docker.com and Python https://python.org . I would also recommend the free PyCharm Community Edition from https://jetbrains.com .
For Windows and Mac, recommend that you install Docker Desktop

Docker Engine is free. Docker Desktop is free except for commercial use in a company with 250 employees or more than US$10 million annual revenue.

On Windows you will also need to install WSL 2 (Windows Subsystem for Linux 2) in features or https://aka.ms/wsl2kernel 

References:
- https://docs.docker.com/get-started/
- https://pythonspeed.com/articles/base-image-python-docker-images/
- https://testdriven.io/blog/docker-best-practices/
- https://rabbitmq.com
- https://pika.readthedocs.io/en/stable/

Docker creates lightweight portable containers. Much lighter than virtual machines. Each container should do one task and do it well. Containers can be linked through networks.

# task-docker

Start by running Docker Desktop.

Check that docker is installed correctly. May need to prefix with `sudo` on Linux or Mac.
```shell
docker run hello-world
```

# task-hi-from-py

Create project folder `bpaml183-docker` and inside it task folder `task-hi-from-py` and change into that directory
```shell
mkdir bpaml183
cd bpaml183
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
WORKDIR /bpaml183
COPY . /bpaml183
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
- build image using Dockerfile in current directory (.) and give it the tag name 'bpaml183-hi-from-py-image'
- run docker container based on image with tag name 'bpaml183-hi-from-py-image'
```shell
cd task-hi-from-py
docker build -t bpaml183-hi-from-py-image .
docker run bpaml183-hi-from-py-image
cd ..
```

Notice how program uses Python 3.11 even if the latest Python installed on your computer is Python 3.10 

Some docker commands
```shell
docker ps  # view running containers
docker ps -a  # view all containers, even those not running
docker rm <container-id>  # Remove previously exited container with id or partial id.
docker run --rm bpaml183-hi-from-py-image  # run docker container and then automatically remove container when finished
docker run --rm -it --entrypoint bash bpaml183-hi-from-py-image # run docker container interactively and replace ENTRYPOINT with bash shell 
docker run --rm -it bpaml183-hi-from-py-image bash # run docker container interactively and replace CMD with bash shell 
docker exec -ti my_container ls  # run command ls in running container with name `my_container`, -t = pseudo-TTY, -i = interactive
docker cp my_container:/bpaml183-container ./bak/  # copy files to or from existing container which doesn't need to be running
docker images  # list available images
docker history my_container  # view how image created
```

# RabbitMQ - Hello World!
This task uses sample code from rabbitmq site

Create and activate virtual environment
```shell
# Mac or Linux
python3 -m venv venv183
source venv183/bin/activate
```
```shell
# Windows
py -m venv venv183
source venv183\Scripts\Activate.bat
```
Install pika third party library into virtual environment
```shell
pip install -U pika
```
or create a file called requirements.txt
```
pika
```
```shell
pip install -r requirements.txt
```

Run rabbitmq AMQP server using the community Docker image
- https://www.rabbitmq.com/download.html

```shell
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management
```

In another shell you can check logs from docker container with name rabbitmq
```shell
docker logs rabbitmq
```

Download the rabbitmq tutorials from https://github.com/rabbitmq/rabbitmq-tutorials/tree/main/python
one at a time into project folder
- https://raw.githubusercontent.com/rabbitmq/rabbitmq-tutorials/main/python/send.py
- https://raw.githubusercontent.com/rabbitmq/rabbitmq-tutorials/main/python/receive.py

While the docker container is running for rabbitmq, run `receive.py` in one shell and then run `send.py` several times in another shell.
```shell
python receive.py
```
```shell
python send.py
python send.py
```
Quit `receive.py` using ctrl-c or ctrl-F2.

Log in to RabbitMW management console http://localhost:15672 user `guest` pass `guest`.

Repeat, send and receive tutorial this time running `send.py` several times first and then running `receive.py`. This time they can be in the same shell.
```shell
python send.py
python send.py
python send.py
python send.py
```
```shell
python receive.py
```
This demonstrates synchronous messaging using pika's BlockingConnection.

# RabbitMQ - Hello World with two receivers

Create modified `send_msg.py` to be able to send any message attached as a command line argument
```python
import sys
import pika
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='', routing_key='hello', body=message.encode('utf-8'))
print(f" [x] Sent {message}")
```
Now set up two receivers running simultaneously in two separate shells
```shell
python receive.py
```
Then send the following seven messages
```shell
python send_msg.py First message..
python send_msg.py Second message.
python send_msg.py Third message......
python send_msg.py Fourth message..
python send_msg.py Fifth message..........
python send_msg.py Sixth message...
python send_msg.py Seventh message..............
```

Now add following three lines to end of `receive.py` callback function to simulate time taken to process message and repeat to see how queue works.
```python
        import time
        time.sleep(body.count(b'.'))
        print(" [x] Done")
```

You can see a problem is that all the slow messages got sent to the same queue.

## Manual acknowledgement
In receive.py change `auto_ack` to `False`. `False` is actually the default.

Add one line to end of `receive.py` callback function to provide the manual acknowledgement.
```python
        ch.basic_ack(delivery_tag=method.delivery_tag)
```

Repeat the experiment. Not much has visibly changed. However, now we can add one more line before basic_consume to tell rabbitmq that workers should not prefetch more than one message

```python
    channel.basic_qos(prefetch_count=1)
```
# RabbitMQ - Workers queue
An important aspect of message delivery is ensuring no data is lost during shutdowns or system problems. Two important settings are delivery mode to ensure each message is persistent and ensure the queue is durable. 

These files are the same as our final example above but include persistence and durability. A new queue is required because once declared, the durability setting can't be changed.
- https://raw.githubusercontent.com/rabbitmq/rabbitmq-tutorials/main/python/worker.py
- https://raw.githubusercontent.com/rabbitmq/rabbitmq-tutorials/main/python/new_task.py

The difference between this and the previous example is the delivery mode. `delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE` and the queue_declare `durable=True`

Difficult to demonstrate durability.

# Pika asynchronously
There is more in-depth sample code in the pika docs https://pika.readthedocs.io/en/stable/intro.html

Interfacing with Pika asynchronously is done by passing in callback methods.

Sample code can be downloaded from https://github.com/pika/pika/tree/main/examples .

For example:
- https://raw.githubusercontent.com/pika/pika/main/examples/asynchronous_publisher_example.py
- https://raw.githubusercontent.com/pika/pika/main/examples/asynchronous_consumer_example.py
