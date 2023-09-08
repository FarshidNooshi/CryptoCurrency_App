# Cryptocurrency Price Monitoring Application

This repository contains the source code and documentation for the final project of the Cloud Computing course. The project is an application that monitors cryptocurrency prices, sends alerts to users, and provides historical price data.

## Introduction

In this project, we have implemented various cloud computing concepts, including cloud services, containerization with Docker and Kubernetes, and big data processing with Apache Spark and Apache Hadoop. The application is designed to monitor and alert users about cryptocurrency price changes.

## Project Components

### Database

The database consists of two tables:
- **Price Table**: Stores the price of specific cryptocurrencies at specific times.
    - Coin Name (String)
    - Timestamp (Time)
    - Price (Float)
- **Alert Subscription Table**: Allows users to subscribe to price change alerts for specific cryptocurrencies.
    - Email (String)
    - Coin Name (Foreign Key, String)
    - Difference Percentage (Int)

### Bepa Service

The Bepa service performs the following tasks:
- Periodically fetches the latest cryptocurrency prices from the coinnews service and stores them in the Price Table.
- Calculates the percentage change in cryptocurrency prices and sends email alerts to subscribed users.

### Peyk Service

The Peyk service provides two endpoints:
- **GetPriceHistory**: Allows users to subscribe to price change alerts for specific cryptocurrencies by specifying their email, the desired cryptocurrency, and the percentage of desired changes.
- **SubscribeCoin**: Retrieves the price history of a specific cryptocurrency.

## Deployment Steps

### 1. Program Development

Develop the database, Bepa, and Peyk services, including the appearance side of the application using your chosen language and framework.

### 2. Package the Application using Docker

Create Docker images for each component using multi-stage builds:
- Use a Dockerfile to build each component's image.
- The first stage should build the project and create an executable file.
- The second stage should execute the file in an Alpine container.

### 3. Deploy the Program with Kubernetes

Deploy the application components in Kubernetes:
- Create a ConfigMap containing project configuration information.
- Create a Secret containing the database credentials.
- Set up a Persistent Volume and a Persistent Volume Claim for the database.
- Deploy the database using a Deployment and expose it with a Service.
- Schedule the Bepa service as a Kubernetes CronJob to run every 3 minutes.
- Deploy the Peyk service with a Deployment and a corresponding Service.

### 4. Additional Tasks

Consider completing the following optional tasks for extra points:
- Implement Horizontal Pod Autoscaling (HPA) for the Peyk service for automatic scaling of courier service pods.
- Replace the database Deployment with a StatefulSet and modify your project code accordingly.
- Implement a Helm chart for easier deployment and management.
- Create a Docker Compose file to automate resource creation and project building and running.

## Work Report

In your work report, make sure to include details and documentation for each of the project components and deployment steps. Explain any additional tasks you have completed for bonus points.

For further assistance or questions, refer to the course materials or contact the instructor.

Happy coding!
