%region sa-east-1
%profile profile_name
%iam_role arn:aws:iam::xxxxxxx:role/GlueServiceRole
%glue_version 3.0
%number_of_workers 2
%worker_type "G.1X"
%idle_timeout 60
%connections my_existing_connection

import sys
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.utils import getResolvedOptions
from awsglue.job import Job
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# using an existing connection, this way there is no need to provide DB credentials
datasource = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",
    connection_options={
        "useConnectionProperties": "True",
        "connectionName": "my_existing_connection",
        "dbtable": "my_table_name"
    },
    transformation_ctx="datasource"
)
print(f"Total records read: {datasource.count()}")
df = datasource.toDF()  # Converting to Spark DataFrame
df_transformed = df.filter(df['campo1'] > 100)  # Example transformation
job.commit()  # Finalizing the job

# connection to read data from S3 where table and database are already configured
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="my_database",
    table_name="my_table_name"
)
datasource.toDF().show()  # Displaying data read from S3

# connection using glueContext, it’s not possible to apply a filter at creation time
datasource = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",
    connection_options={
        "url": "jdbc:mysql://my-db-host:3306/my_database",
        "user": "my_user",
        "password": "my_password",
        "dbtable": "my_table_name"
    },
)
selected_fields = datasource.select_fields(['id', 'campo1', 'campo2'])
selected_fields.toDF().show()  # Displaying selected fields

# connection using Spark (filter can be applied directly)
options = {
    'url': 'jdbc:mysql://my-db-host:3306/my_database',
    'query': "SELECT id, campo1, campo2 FROM my_table_name WHERE campo1 > 100",
    'user': 'my_user',
    'password': 'my_password'
}
df = spark.read.format("jdbc").options(**options).load()
df.createGlobalTempView("my_temp_view")  # Creating a global temporary view
result = spark.sql("SELECT * FROM my_temp_view WHERE campo2 < 50")  # Running an SQL query
result.show()  # Displaying the query result
