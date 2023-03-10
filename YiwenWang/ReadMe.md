# Deployment Guide

## 0. AWS S3

We use S3 as the foundmental storage for all the original data, trained model, and part of the codes used for deployment.

* use us-west-2 as the region

## 1. AWS Redshift Cluster

We use Redshift Cluster for the storage of the predicetd network flow data. The front-end will call REST APIs to fetch data from Redshift.

+ use dc2.large * 2 nodes (360$/month estimated).
+ make sure the S3 and Redshift clusters are in the same region (us-west-2 in my case)
+ associate IAM role to this cluster while creating, in my case the roles are for S3 management.
+ modify the public access settings to public accessible (in Actions scroll-down).

## 2. AWS Lambda Funtion & API Gateway

We use Lambda Fuction and API Gateway for fetching data, predicting IoT network flow type, and emulating real-time streaming data.

### 2.1 Real-time Data Fetching

Front-end side use this REST API(GET) for the newest labeled data from the Redshift database, for example, data within 30 seconds.

### 2.2 Historical Data Fetching

Front-end side use this REST API(GET) for the requested historical network data from the Redshift database.

### 2.3 Predict Label

The emulation data streaming process use this REST API to get the predicted label generated by the deployed XGBoost model for one data records, and store it into the Redshift database.

## 3. AWS SageMaker

We use AWS SageMaker for the deployment of our trained model, the current model type is XGBoost.

* Need to use the containerized endpoint offered by aws and load the traine model into it.
* The endpoint offered an API for using model.
