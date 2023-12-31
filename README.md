# Distributed Storage Mini Project

## Overview

This project focuses on designing, implementing, and comparing the performance of a distributed storage system with
different redundancy allocation schemes. The implementation is in Python 3, and the system aims to provide a flexible
and scalable solution for distributed storage. The project involves teamwork, covering stages such as specification,
system design, implementation, testing, and measurements.

## Team Members

- Alexander Stæhr Johansen 201905865@post.au.dk
- Henrik Tambo Buhl 201905590@post.au.dk
- Liulihan Kuang 201906612@post.au.dk
- Shivaram Rammohan 202202968@post.au.dk

## Project Structure

The project is organized into two main directories:

1. **Task1**
    - `requirements.txt`: Contains necessary dependencies.
    - `server.py`: Implements the distributed storage system using OOP.
    - `rest_server.py`: Implements a REST API over HTTP for external clients.
    - `docker_deploy.py`: Generate a YAML file for client nodes to be deployed
    - `FileDistribution.py`: Implements the distribution of file fragments across the clients
    - `FileOperations.py`: Handles all the utils required for generating and fragmenting a file
    - `automated_script.py`: Calls the REST API to trigger the deployment and analysis.

2. **Task2**
    - `requirements.txt`: Contains necessary dependencies.
    - `server.py`: Implements the distributed storage system using OOP.
    - `rest_server.py`: Implements a REST API over HTTP for external clients.
    - `docker_deploy.py`: Generate a YAML file for client nodes to be deployed
    - `FileDistribution.py`: Implements the distribution of file fragments across the clients
    - `FileOperations.py`: Handles all the utils required for generating and fragmenting a file
    - `automated_script.py`: Calls the REST API to trigger the deployment and analysis.

## Program Requirements

The project required docker and python to be preinstalled to deploy nodes and perform operations

## Project Description

1. **Task1 and Task2**
    1. For task1 we have a server object that has initializer to get al the parameters for deployment and is considered
       as the lead node to handle all clients communications.
    2. The server also container a cli command that can be utilized for direct access and deployment as needed.
    3. The rest server file handles all the API calls that are needed to expose to the public that API can be posted and
       the results of the operation are returned in JSON format
    4. The automated script will trigger the API to invoke the server to deploy nodes as requested by the user through
       the parameters.

## Project Deployment

The project needs to either be deployed using REST API or via CLI

### REST API Deployement

The REST API deployment ensure to have the requirements.txt outside the TASK directories to be installed

```commandline
   pip3 install -r requirements.txt
```

Next we need to have the server deployed followed by the automation script

```python
   python3 rest_server.py
```
```python
python3 automated_script.py
```

This will trigger API calls required to complete all the tasks as needed and finally generate the ```final_result.json``` file to view all the results

### Server CLI Implementation
The server cli is a standalone tool that can be triggered using command line.

```commandline
usage: server.py [-h] [--repeat REPEAT] [--replicas REPLICAS]
                 [--file_size FILE_SIZE] [--nodes NODES] [--throttle THROTTLE]
                 [--fragments FRAGMENTS] [--operation OPERATION]

Example script with command-line arguments

options:
  -h, --help            show this help message and exit
  --repeat REPEAT       Number of times to repeat the operation
  --replicas REPLICAS   Number of replicas to be generated for the file
  --file_size FILE_SIZE
                        The size of the file in Bytes
  --nodes NODES         Number of Client Nodes to be deployed
  --throttle THROTTLE   To throttle bandwidth
  --fragments FRAGMENTS
                        Number of fragments to be generated per file
  --operation OPERATION
                        Type of operation to be taken place while storing
                        Valid types : random buddy min_copy
```

Example deployment of the script is displayed below:

```python
server.py --repeat 100 --nodes 24 --file_size 100000 --operation random 
```

The server will then finally store all the result in ```result.json``` file