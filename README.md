# G6T3 E-Commerce Backend

This is the backend microservice for the G6T3 E-Commerce web application. It provides RESTful APIs for managing products, orders, payments, users, and authentication. These microservices are built with Flask, Spring Boot Java, MongoDB, and other third-party libraries (i.e. Mailgun and Stripe).

## Table of Contents

- [How to Set Up the E-Commerce Microservices with Docker](#how-to-set-up-the-e-commerce-microservices-with-docker)
- [Technical Overview Diagram](#technical-overview-diagram)
- [User Scenario](#user-scenario)
- [Frameworks and Databases Utilised for Backend](#frameworks-and-databases-utilised-for-backend)
- [Stripe, Mailgun and MongoDB account/URI to verify working scenario](#stripe-mailgun-and-mongodb-accounturi-to-verify-working-scenario)
- [FAQ](#faq)
- [Contributors](#contributors)

## How to Set Up the E-Commerce Microservices with Docker

1. Clone our GitHub Repository or download the ZIP file
   `git clone https://github.com/boonyeow/g6t3-ecommerce.git`
2. Open Command Prompt/Terminal and cd to the root folder:
3. Run `docker-compose up --build` to build and start up the microservices
4. Start the frontend through`npm run dev`
   (If you have not already set up the frontend, do follow the README.md guide at `https://github.com/boonyeow/g6t3-ecommerce-fe`

## Technical Overview Diagram

![Technical Overview Diagram](README_files/Technical_Diagram.png)

## User Scenario

### Scenario 1 - User adds a product to cart

![Scenario 1 Diagram](README_files/Scenario_1.png)

### Scenario 2 - User places an order for products

![Scenario 2 Diagram](README_files/Scenario_2.png)

### Scenario 3 - User post reviews on products

![Scenario 3 Diagram](README_files/Scenario_3.png)

## Frameworks and Databases Utilised for Backend

**Services**

- Python Flask
- Spring Boot Java

**Database**

- MongoDB
- PostgreSQL

**Others**

- Stripe Payment API
- RabbitMQ Messaging
- Mailgun API

## Stripe, Mailgun and MongoDB account/URI to verify working scenario

**Stripe** https://dashboard.stripe.com/test/dashboard

- Stripe account: esdg6t3@gmail.com
- Stripe password: ESD-g6t3!@#

**Mailgun** https://app.mailgun.com/mg/dashboard

- Mailgun account: esdg6t3@gmail.com
- Mailgun password: ESD-g6t3!@#

**MongoDB**

- MongoDB URI: `mongodb+srv://esdg6t3:root@esdg6t3.rs7urs2.mongodb.net/test`

## FAQ

**1. I'm getting /init.sh not found when running docker**

- Please make sure the line ending for init.sh is configured to be LF instead of CRLF. See below for a step by step guide to change the file's line ending:

  **STEP 1**:
  ![Step 1 Pic](README_files/Step1.png)

  **STEP 2:**
  ![Step 2 Pic](README_files/Step2.png)

**2. I'm getting 500 INTERNAL SERVER ERROR when logging in**

- If you had stopped the container with docker-compose down, it will remove all containers, networks, volumes, and images created by up. This includes all service users that was previously registered. The data in mongo database will no longer be synchronized with the newly started container.

- Please remove all users from mongodb and re-register the account to solve the error.

## Contributors

- Alvin Ling (alvin.ling.2021@scis.smu.edu.sg)
- Tan Boon Yeow (bytan.2021@scis.smu.edu.sg)
- Sebastian Ong (cpong.2021@scis.smu.edu.sg)
- Kant Kaw Khin (kkkant.2021@scis.smu.edu.sg)
- Ong Ping Yuan (pyong.2021@scis.smu.edu.sg)
- Wong Dehou (dehou.wong.2021@scis.smu.edu.sg)
