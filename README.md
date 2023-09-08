# Cryptocurrency Price Monitoring Application

This repository contains the source code and configuration files for a cryptocurrency price monitoring application developed as part of the Cloud Computing final course project. The application is designed to monitor and notify users about changes in cryptocurrency prices. It is divided into several components, including a database, the "Bepa" service, and the "Peyk" service, all of which are containerized using Docker and deployed on Kubernetes. Below, we provide an overview of each component and the steps to set up and deploy the application.

## Table of Contents
1. [Introduction](#introduction)
2. [Components](#components)
    - [Database](#database)
    - [Bepa Service](#bepa-service)
    - [Peyk Service](#peyk-service)
3. [System Design](#system-design)
    - [Overview](#overview)
4. [Dockerization](#dockerization)
5. [Deployment with Kubernetes](#deployment-with-kubernetes)
    - [General Items](#general-items)
    - [Database](#database-deployment)
    - [Bepa Service](#bepa-service-deployment)
    - [Peyk Service](#peyk-service-deployment)
6. [Additional Steps](#additional-steps)
    - [Horizontal Pod Autoscaling (HPA)](#horizontal-pod-autoscaling)
    - [StatefulSet for Database](#statefulset-for-database)
    - [Helm Chart](#helm-chart)
    - [Docker Compose](#docker-compose)
7. [Contributors](#contributors)
8. [License](#license)



---

## Introduction

In this project, we have implemented various cloud computing concepts, including cloud services, containerization with Docker and Kubernetes, and big data processing. The application's main objective is to monitor and notify users about cryptocurrency price changes.

## Components

### Database

The database consists of two tables:

1. **Price table**: Stores the price of specific cryptocurrencies in dollars at specific timestamps.

   | Coin Name (String) | Timestamp (Time) | Price (Float) |
   |--------------------|-------------------|---------------|

2. **Alert subscription table**: Allows users to subscribe to price change alerts for specific cryptocurrencies. Each row contains the user's email, the desired cryptocurrency, and the percentage change trigger.

   | Email (String) | Coin Name (Foreign Key, String) | Difference Percentage (Int) |
   |-----------------|---------------------------------|-----------------------------|


### Bepa Service

The "Bepa" service is responsible for two main tasks:
1. Fetches the latest cryptocurrency prices from the coinnews service and updates the Price Table in the database.
2. Sends price change alerts to users by calculating the percentage change of cryptocurrencies and checking for activated alerts in the Alert Subscription Table. Emails are used for user notifications.

### Peyk Service

The "Peyk" service provides two endpoints:
1. `GetPriceHistory`: Allows users to subscribe to cryptocurrency price change alerts by specifying their email, the cryptocurrency name, and the desired percentage change.
2. `SubscribeCoin`: Retrieves the price history of a specified cryptocurrency.

## System Design
### Overview

Provide a high-level overview of the system's architecture and how different components interact with each other. You can use diagrams, such as architecture diagrams or flowcharts, to visualize the system's design.
![System Architecture](/images/image.png)

## Dockerization

To containerize the application components, we use Docker with a multi-stage build technique. Each component is packaged into a Docker image, ensuring efficient deployment across various environments.

## Deployment with Kubernetes

We deploy the application on Kubernetes, utilizing various resources and configurations for each component.

### General Items

- **ConfigMap**: Contains project configuration information, including server port and database address.
- **Secret**: Stores the database username and password securely.

### Database Deployment

- **Persistent Volume (PV) and Persistent Volume Claim (PVC)**: Ensures data persistence for the database.
- **Deployment**: Manages the database pods and uses the secrets for authentication.
- **Service**: Enables communication with the database pods.

### Bepa Service Deployment

- **CronJob**: Runs the "Bepa" service image at regular intervals (e.g., every 3 minutes).

### Peyk Service Deployment

- **Deployment**: Manages the "Peyk" service pods and accesses the ConfigMap and Secret for database connectivity.
- **Service**: Facilitates communication with "Peyk" service pods.

## Additional Steps

In addition to the core project requirements, we have considered these optional steps to enhance the application:

### Horizontal Pod Autoscaling (HPA)

We have implemented HPA to automatically scale the "Peyk" service pods based on resource utilization or custom metrics.

### StatefulSet for Database

We have replaced the database Deployment with StatefulSets for managing the database pods, allowing for more advanced database management features.

### Helm Chart

We have created a Helm chart to simplify the deployment of your application, making it easier to manage Kubernetes resources.

### Docker Compose

We have implemented a Docker Compose configuration for local development, automating the setup of all required resources and dependencies.

# Contributors
* [Farshid Nooshi](https://FarshidNooshi.GitHub.io)
* [Mehdi Nemati](https://github.com/mohammadmahdi255)

# License

This project is licensed under the MIT License - see the LICENSE.md file for details.
