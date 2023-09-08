# Course Final Project - Cryptocurrency Price Monitoring Application

## Table of Contents
- [Introduction](#introduction)
- [Project Overview](#project-overview)
  - [Database](#database)
  - [Bepa Service](#bepa-service)
  - [Peyk Service](#peyk-service)
- [Deployment](#deployment)
  - [Dockerization](#dockerization)
  - [Kubernetes Deployment](#kubernetes-deployment)
- [Additional Steps](#additional-steps)
- [Scoring](#scoring)

---

## Introduction

Welcome to the repository for your course's final project. This project aims to apply the concepts you've learned during the course by creating a cryptocurrency price monitoring application. The application consists of various components, including a database, "Bepa" service, and "Peyk" service. Additionally, you will package the application using Docker and deploy it with Kubernetes.

## Project Overview

### Database

The database for this program contains two tables:

#### Price Table

- **Coin Name (String)**: The name of the cryptocurrency.
- **Timestamp (Time)**: The timestamp when the price was recorded.
- **Price (Float)**: The price of the cryptocurrency in dollars.

#### Alert Subscription Table

- **Email (String)**: User's email for notifications.
- **Coin Name (Foreign Key, String)**: The desired cryptocurrency.
- **Difference Percentage (Int)**: The percentage change that triggers a notification.

### Bepa Service

The "Bepa" service performs the following tasks:

- Periodically fetches the latest prices of cryptocurrencies from the coinnews service and stores them in the Price Table.
- Calculates the percentage change of each cryptocurrency compared to the last recorded price.
- Sends email alerts to users based on their subscription settings.

### Peyk Service

The "Peyk" service provides users with two endpoints:

- **GetPriceHistory**: Allows users to subscribe to changes in a cryptocurrency's price by specifying their email, the desired cryptocurrency, and the desired percentage change.
- **SubscribeCoin**: Provides the price history of a cryptocurrency based on user requests.

## Deployment

### Dockerization

After developing the database and services, package each component as a Docker image using a Dockerfile. Employ the multistage build technique to create the images in two steps:

1. Build the project and create an executable file.
2. Execute the file within an Alpine container.

### Kubernetes Deployment

Deploy the application with Kubernetes. Each part of the project requires specific Kubernetes resources:

#### General Items

- **ConfigMap**: Contains project configuration information, including server port and database address.
- **Secret**: Contains the database username and password.

#### Database

- **Persistent Volume and Persistent Volume Claim**: Used to maintain database data.
- **Deployment**: Responsible for preparing and executing the database in pod form. You can choose how to create the database.
- **Service**: Enables communication with deployment pods. The deployment should use the username and password defined in the secret and the memory space defined in the Persistent Volume Claim.

#### Bepa Service

- **CronJob**: Runs the Bepa service as a Kubernetes cron job. It executes the image created during the Dockerization step every 3 minutes.

#### Peyk Service

- **Deployment**: Runs the Peyk server as two pods. These pods must have access to the ConfigMap and Secret content to access the database.
- **Service**: Facilitates communication with Peyk service pods.

The Kubernetes resources mentioned here should be created in logical dependency order, meaning you should create resources from right to left and from top to bottom. To create each item, use the `kubectl apply` command.

## Additional Steps

In addition to the core project, there are some additional steps that can earn you extra points:

- **Creation of HPA (Horizontal Pod Autoscaler)**: Implement automatic scaling for Peyk service pods.
- **Replacing Database Deployment with StatefulSet**: Modify your project code to properly utilize a StatefulSet, which includes master and slave components.
- **Helm Chart Implementation**: Create a Helm chart for your project to streamline deployment.
- **Docker Compose**: Implement Docker Compose to automate the creation of project resources and dependencies, build Docker images, and run the application.

## Scoring

In your work report, make sure to address each of the scoring sections mentioned above and provide details on how you implemented them. These additional steps will demonstrate your proficiency in containerization and orchestration technologies, further enhancing your project's quality.

Feel free to consult course materials and documentation as needed during your project development. Good luck with your final project!
