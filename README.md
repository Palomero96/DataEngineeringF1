# DataEngineeringF1
The goal of this project is to use my theorical knowledge to practice and gain some experience in the data engineering field. I have no work experience as a Data Engineer but I would like to develop my career in this path. Despite of having no experience, I have used some of the tools that are used in the role.

For this project I will be using the following tech stack:
- A Raspeberry Pi to host the PostgreSQL
- PostgreSQL
- Python
- Azure Flexible PostgreSQL
- Docker
- Azure DataLake
- Azure DataFactory
- Azure Databricks

I will be using a Formula 1 dataset that you can find here: https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020

## Table of contents
- [DataEngineeringF1](#dataengineeringf1)
  - [Table of contents](#table-of-contents)
  - [Data Model ](#data-model-)
  - [PostgreSQL ](#postgresql-)
    - [Native](#native)
    - [Docker](#docker)
  - [Load and Extraction in PostgreSQL ](#load-and-extraction-in-postgresql-)
  - [Load to Azure PostgreSQL ](#load-to-azure-postgresql-)
  - [Load Data to Azure Datalake ](#load-data-to-azure-datalake-)
  - [Data Transformation in Azure Databricks ](#data-transformation-in-azure-databricks-)

## Data Model <a name="datamodel"></a>
The first thing I did was analyze the csv files, in order to know how the data is organized. In each .csv file there is different information. I used this files as a guide to design the tables and their columns.

DBdiagram.io is the tool that I choose to write my Data Model. With this tool I was able to export my Data Model as a PNG as you will see further down in this document and as a SQL file. Under the folder 1.DataModel you can find the Data Model in SQL language with all the definitions. The path to this file is: /1.DataModel/F1DataModel.sql

Here you have an image of the Data Model:

![alt](/img/F1DataModel.png)


## PostgreSQL <a name="PostgreSQL"></a>
I installed PostgreSQL using two different methods: native and Docker. As a Database Administrator, I am used to install PostgreSQL using native installation but I am have not used Docker and I wanted to learn Docker basics.
### Native
My PostgreSQL server is going to be a RaspberryPi with RaspOS. 
In order to install the software we need to run this command in a terminal:

`sudo apt-get -y install postgresql`

After installing the software and define PATH variable with PostgreSQL Binaries, we need to init and start the instance. In order to do so we need to run this two commands:

```
initdb DATADIRECTORYPATH
pg_ctl start
```

Optionally we can test if everithing has been installed and created correctly with this command to connect to the database:

`psql`

The next step is to configure pg_hba.conf file so that we can connect from outside the RaspberryPi.
We need to add this line in order to connect to PostgreSQL server where the IP is the client IP:

`host                database  user  address     auth-method  [auth-options]`

Optionally we can test if the connection is accepted from the client using, for example, PgAdmin.

### Docker
I used this command to install Docker:
`sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`

The next step is running a postgres image:
Getting the PostgreSQL image: `docker pull postgres`

Running the image: `docker run --name pgsql-dev-f1 -e POSTGRES_PASSWORD=yourpassword -p 5432:5432 -d postgres`

I also installed Docker Compose to test it. I installed this packages:
`sudo apt-get install libffi-dev libssl-dev python3-dev python3 python3-pip docker-compose`

To run a container with Docker Compose you need to create a yml file and exec this command: `docker-compose -f postgresCompose.yml start`
You can find postgresCompose.yml file under "/2.PostgreSQL/B_Docker"


Here are some usefull docker commands:
```
docker ps -a 
docker start CONTAINERNAME
docker stop CONTAINERNAME
docker rm CONTAINERNAME
```


## Load and Extraction in PostgreSQL <a name="loadextraction"></a>
I have the develop a Python file to load data to PostgreSQL. I read data from all csv files and create a table in the database for each csv file.
I have used these libraries:
- psycopg2
- pandas
- sqlalchemy

You fill find this Python file under "/3.LoadandExtractionPostgreSQL/LoadData.py"

To extract data I have used different backups formats with PgAdmin tool. You can find these backups on "/3.LoadandExtractionPostgreSQL"

## Load to Azure PostgreSQL <a name="loadtoazure"></a>
I have created a Azure Flexible PostgreSQL Server to save all the data that I am going to load to Azure. To load this data I am going to use the same python file as before but changing the connection parameters.

You fill find this modified Python file under "/4.LoadtoAzurePostgreSQL/LoadDataAzurePostgres.py"


## Load Data to Azure Datalake <a name="loadtodatalake"></a>
First of all, I created a Storage account to save all the data that I am going to load to Azure. To load this data I will be using two different methods: using the same python file as before and using DataFactory to extract data from raw file.

Source data will be on this Github repository under "/data" or in Azure Flexible PostgreSQL

In order to extract this data I have try two different methods. 

- The first method is a pipeline with a copy activity for each csv file in Github. This is not ideal because you need to define one Linked Service for each, two dataframes for each csv file and the most important part is that it is not dynamic. If you add a new csv file you will have to define a new Linked Service and two more dataframes for each csv file.
- The second method is a better solution that solves the problem of adding new Linked Services and Dataframes. Here I define a linked generic Service (Azure Flexible PostgreSQL) and two generic dataframes (source and output). Then, I have created a pipeline where I do this steps: 
  - Activity 1: List all tables in Azure Flexible PostgreSQL Database 
  - Activity 2: For each table copy data to csv file on Azure Storage account

You fill find all Data Factory objects definitions under "/5.LoadDatatoDatalake/datafactory"
  
## Data Transformation in Azure Databricks <a name="datatransformation"></a>
Extra
