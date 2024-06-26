# MarketMind

## Project Overview
MarketMind is an advanced analytics platform designed to transform e-commerce with real-time data insights, personalized product recommendations, and consumer sentiment analysis. Powered by AI and machine learning, MarketMind offers a conversational interface for intuitive user queries, allowing businesses to understand market trends and customer behavior better. The platform's cloud-based structure ensures scalability and reliability, enabling businesses of all sizes to access powerful big data tools. By integrating user chat histories and analyzing customer reviews, MarketMind delivers a tailored shopping experience and actionable insights, empowering businesses to make informed decisions and enhance customer satisfaction.

## Project Resources
[![Google Codelabs](https://img.shields.io/badge/-Google%20Codelabs-blue?style=for-the-badge)](https://codelabs-preview.appspot.com/?file_id=1jgCXONoiZ2SUPDW-pyuGT_dZhfNW3Q1h9VHunhrVhK4#0)
[![Demo Video](https://img.shields.io/badge/-Demo%20Video-red?style=for-the-badge)](https://www.youtube.com/watch?v=WFkK3tz0280)
[![Application](https://img.shields.io/badge/-Application-yellow?style=for-the-badge)](http://52.14.6.11:8501/)

## Tech Stack
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Amazon AWS](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-4B8BBE?style=for-the-badge&logo=python&logoColor=yellow)
![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-00A7E1?style=for-the-badge&logo=apache-airflow&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-6558F5?style=for-the-badge&logo=pinecone&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-purple?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-0db7ed?style=for-the-badge&logo=docker&logoColor=white)
![Amazon S3](https://img.shields.io/badge/Amazon_S3-F7CA18?style=for-the-badge&logo=amazon-s3&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2D9CDB?style=for-the-badge&logo=pydantic&logoColor=white)

## Architecture Diagram
![image](https://github.com/BigDataIA-Spring2024-Sec1-Team8/final-project-proposal/assets/114782541/8d90aa23-27e9-48d7-86b2-763036d65b23)
The "MarketMind" system architecture integrates a Streamlit-based frontend with a FastAPI and Snowflake backend, hosted on AWS to ensure robust scalability. This intelligent e-commerce analytics platform features a chatbot interface for user engagement, handles queries for customized product recommendations, and utilizes OpenAI for content enhancement and data summarization. Automated processes for data extraction, cleaning, and embedding convert raw e-commerce information into accessible and informative insights.

### Customer Query Pipeline:
![image](https://github.com/BigDataIA-Spring2024-Sec1-Team8/final-project-proposal/assets/114782541/dc45d4d2-c635-4cc2-be95-7d5a56181774)
The MarketMind platform creates a seamless interaction flow, beginning with user queries through a chatbot and ending with personalized responses. The backend refines these inputs, using machine learning to categorize and embed them for accurate product matching. OpenAI models add further context and depth to the information. The final customized results are presented via a Streamlit user interface, providing an engaging and informative shopping experience.

### Data Processing Pipeline
![image](https://github.com/BigDataIA-Spring2024-Sec1-Team8/final-project-proposal/assets/114782541/350ef92f-a813-4d72-a92b-c49c75034696)

The Data Processing Layer for the MarketMind project ingests raw e-commerce data, meticulously cleansing and condensing product information and reviews from Amazon's vast datasets. Relevant details are summarized and embedded into a vector space, making them amenable for advanced analytics. These processed assets, including both text and images, are then stored in Snowflake, a cloud data warehouse that supports the platform's scalable, data-driven functionalities. This streamlined pipeline ensures the integrity and utility of data that feeds into the MarketMind user experience.

### Run the application

Clone the project repository:
https://github.com/BigDataIA-Spring2024-Sec1-Team8/MarketMind.git

Navigate to the project directory:

cd MarketMind

Create a .env file and add the following environment variables:
```
SNOWFLAKE_USER=xxxx
SNOWFLAKE_PASSWORD=xxxx
SNOWFLAKE_ACCOUNT=xxxx
SNOWFLAKE_WAREHOUSE=xxxx
SNOWFLAKE_SCHEMA=xxxx
SNOWFLAKE_ROLE=xxxx
SNOWFLAKE_DATABASE=xxxx
sasl_username=xxxx
sasl_password=xxxx
bootstrap_servers=xxxx
AWS_ACCESS_KEY_ID = xxxx
AWS_SECRET_ACCESS_KEY = xxxx
pinecone_key = xxxx
openai_key = xxxx
gemini_key=xxxx
JWT_SECRET=xxxx
```

You can download the dataset from data source in addition to existing one https://jmcauley.ucsd.edu/data/amazon_v2/index.html, please place the downloaded file in the resources folder .
/Web-Service/Backend/resources

Run Docker compose build for initializing and running the containers for Airflow and Web App.

```
cd Web-Service

docker-compose build
```

Run Docker compose for initializing and running the containers for Airflow, Frontend and Backend.

```
docker-compose up
```

Now the application is up and running. Now navigate to below link to check the application in the web browser.

0.0.0.0:8501

```
cd ETL
docker-compose build
docker-compose up
```
Also, once all the Airflow containers are healthy then navigate to the port 8080 i.e. 0.0.0.0:8080

## Project Structure

<img width="227" alt="Screenshot 2024-04-25 at 12 57 53 PM" src="https://github.com/BigDataIA-Spring2024-Sec1-Team8/MarketMind/assets/114782541/c5d3f2f3-4b1b-44eb-83ef-cfbde33762ac">

## Contributions
| Name                     | Share  |
|--------------------------|--------|
| Sai Durga Mahesh Bandaru | 33.3%  |
| Sri Poojitha Mandali     | 33.3%  |
| Shivani Gulgani          | 33.3%  |

WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK
