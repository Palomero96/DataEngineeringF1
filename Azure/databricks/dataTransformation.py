# Databricks notebook source
# Mount the Azure Data Lake Storaged
dbutils.fs.mount(
  source="abfss://formula1data@palomeroformula1data.dfs.core.windows.net", 
  mount_point="/mnt/formula1data",
  extra_configs={
    "fs.azure.account.auth.type": "OAuth",
    "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
    "fs.azure.account.oauth2.client.id": "a8c5f462-4cba-4c43-b82f-042126cfcb39",
    "fs.azure.account.oauth2.client.secret": "",
    "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/748cb327-cfee-46fb-8270-8c081cd60da3/oauth2/token"
  }
)

# COMMAND ----------

# Import the required libraries
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
from pyspark.sql import SparkSession

# Create a Spark session
spark = SparkSession.builder.getOrCreate()

# Set up the MSI credentials
credential = ManagedIdentityCredential()

# Create a SecretClient instance using the MSI credentials
key_vault_url = "https://databricksSecretPalomero.vault.azure.net/"
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

# Get the secret value from the Key Vault
client_id_secret = secret_client.get_secret("client-id")
client_secret_secret = secret_client.get_secret("client-secret")
tenant_id_secret = secret_client.get_secret("tenant-id")

# Get the actual secret values
client_id = client_id_secret.valueB
client_secret = client_secret_secret.value
tenant_id = tenant_id_secret.value

# Mount the Azure Data Lake Storage
dbutils.fs.mount(
  source="abfss://formula1data@palomeroformula1data.dfs.core.windows.net",
  mount_point="/mnt/formula1data",
  extra_configs={
    "fs.azure.account.auth.type": "OAuth",
    "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
    "fs.azure.account.oauth2.client.id": client_id,
    "fs.azure.account.oauth2.client.secret": client_secret,
    "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/748cb327-cfee-46fb-8270-8c081cd60da3/oauth2/token"
  }
)

# COMMAND ----------

dbutils.secrets.get(scope="AzureKeyVault", key="databricksFormulaSecret")

# COMMAND ----------

# MAGIC %fs
# MAGIC ls '/mnt/formula1data'
# MAGIC  

# COMMAND ----------

#Load all files

circuits = spark.read.format("csv").option("header", "true").option("inferSchema","true").load("/mnt/formula1data/raw-data-postgresAll/circuits.csv")
constructor_results = spark.read.format("csv").option("header", "true").option("inferSchema","true").load("/mnt/formula1data/raw-data-postgresAll/constructor_results.csv") 
constructor_standings = spark.read.format("csv").option("header", "true").option("inferSchema","true").load("/mnt/formula1data/raw-data-postgresAll/constructor_standings.csv")
constructor = spark.read.format("csv").option("header", "true").option("inferSchema","true").load("/mnt/formula1data/raw-data-postgresAll/constructors.csv")
driver_standings = spark.read.format("csv").option("header", "true").option("inferSchema","true").load("/mnt/formula1data/raw-data-postgresAll/driver_standings.csv")
drivers = spark.read.format("csv").option("header", "true").option("inferSchema","true").load("/mnt/formula1data/raw-data-postgresAll/drivers.csv")
lap_times = spark.read.format("csv").option("header", "true").option("inferSchema","true").load("/mnt/formula1data/raw-data-postgresAll/lap_times.csv")
pit_stops = spark.read.format("csv").option("header", "true").option("inferSchema","true").load("/mnt/formula1data/raw-data-postgresAll/pit_stops.csv")
qualifying = spark.read.format("csv").option("header", "true").option("inferSchema","true").load("/mnt/formula1data/raw-data-postgresAll/qualifying.csv")
races = spark.read.format("csv").option("header", "true").option("inferSchema","true").load("/mnt/formula1data/raw-data-postgresAll/races.csv")
results = spark.read.format("csv").option("header", "true").option("inferSchema","true").load("/mnt/formula1data/raw-data-postgresAll/results.csv")
seasons = spark.read.format("csv").option("header", "true").option("inferSchema","true").load("/mnt/formula1data/raw-data-postgresAll/seasons.csv")
sprint_results = spark.read.format("csv").option("header", "true").option("inferSchema","true").load("/mnt/formula1data/raw-data-postgresAll/sprint_results.csv")
status = spark.read.format("csv").option("header", "true").option("inferSchema","true").load("/mnt/formula1data/raw-data-postgresAll/status.csv")


# COMMAND ----------



# COMMAND ----------

circuits.show()
# Convert column types to double
circuits = circuits.withColumn("alt", circuits["alt"].cast("integer"))
circuits.printSchema()

# COMMAND ----------

from pyspark.sql.functions import expr
constructor_standings.show()
constructor_standings = constructor_standings.withColumn("wins", expr("CASE WHEN wins > 0 THEN true ELSE false END"))
constructor_standings = constructor_standings.select("constructorStandingsId","raceId","constructorId","points","position","wins")
constructor_standings.printSchema()

# COMMAND ----------

constructor.show()
constructor = constructor.select("constructorId","constructorRef","nationality")

# COMMAND ----------

driver_standings.show()
driver_standings = driver_standings.withColumn("wins", expr("CASE WHEN wins > 0 THEN true ELSE false END"))
driver_standings = driver_standings.select("driverStandingsId","raceId","driverId","points","position","wins")
driver_standings.printSchema()

# COMMAND ----------

drivers.show()
drivers = drivers.select("driverId","driverRef","code","forename","surname","dob","nationality")
drivers = drivers.withColumnRenamed("dob", "birthDate")
drivers.printSchema()

# COMMAND ----------

lap_times.show()
lap_times.printSchema()

# COMMAND ----------

pit_stops.show()
pit_stops = pit_stops.drop("milliseconds")
pit_stops.printSchema()

# COMMAND ----------

qualifying.show()
qualifying.printSchema()

# COMMAND ----------

races.show()
races = races.select("raceId","year","circuitId","date","time")
races.printSchema()

# COMMAND ----------

results.show()
results = results.drop("number","positionText","positionOrder","milliseconds")
results.printSchema()

# COMMAND ----------

sprint_results.show()
sprint_results = sprint_results.drop("number","positionText","positionOrder","milliseconds")
sprint_results.printSchema()

# COMMAND ----------

seasons.show()
seasons.printSchema()
status.show()
status.printSchema()

# COMMAND ----------

circuits.write.format("csv").option("header", "true").mode("overwrite").save("/mnt/formula1data/transformed-data/circuits.csv")
constructor_results.write.format("csv").option("header", "true").mode("overwrite").save("/mnt/formula1data/transformed-data/constructor_results.csv") 
constructor_standings.write.format("csv").option("header", "true").mode("overwrite").save("/mnt/formula1data/transformed-data/constructor_standings.csv")
constructor.write.format("csv").option("header", "true").mode("overwrite").save("/mnt/formula1data/transformed-data/constructors.csv")
driver_standings.write.format("csv").option("header", "true").mode("overwrite").save("/mnt/formula1data/transformed-data/driver_standings.csv")
drivers.write.format("csv").option("header", "true").mode("overwrite").save("/mnt/formula1data/transformed-data/drivers.csv")
lap_times.write.format("csv").option("header", "true").mode("overwrite").save("/mnt/formula1data/transformed-data/lap_times.csv")
pit_stops.write.format("csv").option("header", "true").mode("overwrite").save("/mnt/formula1data/transformed-data/pit_stops.csv")
qualifying.write.format("csv").option("header", "true").mode("overwrite").save("/mnt/formula1data/transformed-data/qualifying.csv")
races.write.format("csv").option("header", "true").mode("overwrite").save("/mnt/formula1data/transformed-data/races.csv")
results.write.format("csv").option("header", "true").mode("overwrite").save("/mnt/formula1data/transformed-data/results.csv")
seasons.write.format("csv").option("header", "true").mode("overwrite").save("/mnt/formula1data/transformed-data/seasons.csv")
sprint_results.write.format("csv").option("header", "true").mode("overwrite").save("/mnt/formula1data/transformed-data/sprint_results.csv")
status.write.format("csv").option("header", "true").mode("overwrite").save("/mnt/formula1data/transformed-data/status.csv")
