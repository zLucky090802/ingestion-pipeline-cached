[Skip to content](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#_top)
# Google Cloud SQL for PostgreSQL - `PostgresDocumentStore` & `PostgresIndexStore` 
> [Cloud SQL](https://cloud.google.com/sql) is a fully managed relational database service that offers high performance, seamless integration, and impressive scalability. It offers MySQL, PostgreSQL, and SQL Server database engines. Extend your database application to build AI-powered experiences leveraging Cloud SQL’s LlamaIndex integrations.
This notebook goes over how to use `Cloud SQL for PostgreSQL` to store documents and indexes with the `PostgresDocumentStore` and `PostgresIndexStore` classes.
Learn more about the package on [GitHub](https://github.com/googleapis/llama-index-cloud-sql-pg-python/).
## Before you begin
[Section titled “Before you begin”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#before-you-begin)
To run this notebook, you will need to do the following:
  * [Create a Google Cloud Project](https://developers.google.com/workspace/guides/create-project)
  * [Enable the Cloud SQL Admin API.](https://console.cloud.google.com/flows/enableapi?apiid=sqladmin.googleapis.com)
  * [Create a Cloud SQL instance.](https://cloud.google.com/sql/docs/postgres/connect-instance-auth-proxy#create-instance)
  * [Create a Cloud SQL database.](https://cloud.google.com/sql/docs/postgres/create-manage-databases)
  * [Add a User to the database.](https://cloud.google.com/sql/docs/postgres/create-manage-users)


### 🦙 Library Installation
[Section titled “🦙 Library Installation”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#-library-installation)
Install the integration library, `llama-index-cloud-sql-pg`, and the library for the embedding service, `llama-index-embeddings-vertex`.

```


%pip install --upgrade --quiet llama-index-cloud-sql-pg llama-index-llms-vertex llama-index


```

**Colab only:** Uncomment the following cell to restart the kernel or use the button to restart the kernel. For Vertex AI Workbench you can restart the terminal using the button on top.

```

# # Automatically restart kernel after installs so that your environment can access the new packages


# import IPython



# app = IPython.Application.instance()


# app.kernel.do_shutdown(True)

```

### 🔐 Authentication
[Section titled “🔐 Authentication”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#-authentication)
Authenticate to Google Cloud as the IAM user logged into this notebook in order to access your Google Cloud Project.
  * If you are using Colab to run this notebook, use the cell below and continue.
  * If you are using Vertex AI Workbench, check out the setup instructions [here](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/setup-env).



```


from google.colab import auth




auth.authenticate_user()

```

### ☁ Set Your Google Cloud Project
[Section titled “☁ Set Your Google Cloud Project”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#-set-your-google-cloud-project)
Set your Google Cloud project so that you can leverage Google Cloud resources within this notebook.
If you don’t know your project ID, try the following:
  * Run `gcloud config list`.
  * Run `gcloud projects list`.
  * See the support page: [Locate the project ID](https://support.google.com/googleapi/answer/7014113).



```

# @markdown Please fill in the value below with your Google Cloud project ID and then run the cell.




PROJECT_ID="my-project-id"# @param {type:"string"}




# Set the project id



!gcloud config set project {PROJECT_ID}


```

## Basic Usage
[Section titled “Basic Usage”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#basic-usage)
### Set Cloud SQL database values
[Section titled “Set Cloud SQL database values”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#set-cloud-sql-database-values)
Find your database values, in the [Cloud SQL Instances page](https://console.cloud.google.com/sql?_ga=2.223735448.2062268965.1707700487-2088871159.1707257687).

```

# @title Set Your Values Here { display-mode: "form" }



REGION="us-central1"# @param {type: "string"}




INSTANCE="my-primary"# @param {type: "string"}




DATABASE="my-database"# @param {type: "string"}




TABLE_NAME="document_store"# @param {type: "string"}




USER="postgres"# @param {type: "string"}




PASSWORD="my-password"# @param {type: "string"}


```

### PostgresEngine Connection Pool
[Section titled “PostgresEngine Connection Pool”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#postgresengine-connection-pool)
One of the requirements and arguments to establish Cloud SQL as a vector store is a `PostgresEngine` object. The `PostgresEngine` configures a connection pool to your Cloud SQL database, enabling successful connections from your application and following industry best practices.
To create a `PostgresEngine` using `PostgresEngine.from_instance()` you need to provide only 4 things:
  1. `project_id` : Project ID of the Google Cloud Project where the Cloud SQL instance is located.
  2. `region` : Region where the Cloud SQL instance is located.
  3. `instance` : The name of the Cloud SQL instance.
  4. `database` : The name of the database to connect to on the Cloud SQL instance.


By default, [IAM database authentication](https://cloud.google.com/sql/docs/postgres/iam-authentication#iam-db-auth) will be used as the method of database authentication. This library uses the IAM principal belonging to the [Application Default Credentials (ADC)](https://cloud.google.com/docs/authentication/application-default-credentials) sourced from the envionment.
For more informatin on IAM database authentication please see:
  * [Configure an instance for IAM database authentication](https://cloud.google.com/sql/docs/postgres/create-edit-iam-instances)
  * [Manage users with IAM database authentication](https://cloud.google.com/sql/docs/postgres/add-manage-iam-users)


Optionally, [built-in database authentication](https://cloud.google.com/sql/docs/postgres/built-in-authentication) using a username and password to access the Cloud SQL database can also be used. Just provide the optional `user` and `password` arguments to `PostgresEngine.from_instance()`:
  * `user` : Database user to use for built-in database authentication and login
  * `password` : Database password to use for built-in database authentication and login.


**Note:** This tutorial demonstrates the async interface. All async methods have corresponding sync methods.

```


from llama_index_cloud_sql_pg import PostgresEngine





engine =await PostgresEngine.afrom_instance(




project_id=PROJECT_ID,




region=REGION,




instance=INSTANCE,




database=DATABASE,




user=USER,




password=PASSWORD,



```

### Initialize a table
[Section titled “Initialize a table”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#initialize-a-table)
The `PostgresDocumentStore` class requires a database table. The `PostgresEngine` engine has a helper method `init_doc_store_table()` that can be used to create a table with the proper schema for you.

```


await engine.ainit_doc_store_table(




table_name=TABLE_NAME,



```

#### Optional Tip: 💡
[Section titled “Optional Tip: 💡”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#optional-tip)
You can also specify a schema name by passing `schema_name` wherever you pass `table_name`.

```


SCHEMA_NAME="my_schema"





await engine.ainit_doc_store_table(




table_name=TABLE_NAME,




schema_name=SCHEMA_NAME,



```

### Initialize a default PostgresDocumentStore
[Section titled “Initialize a default PostgresDocumentStore”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#initialize-a-default-postgresdocumentstore)

```


from llama_index_cloud_sql_pg import PostgresDocumentStore





doc_store =await PostgresDocumentStore.create(




engine=engine,




table_name=TABLE_NAME,




# schema_name=SCHEMA_NAME



```

### Download data
[Section titled “Download data”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#download-data)

```


!mkdir -p 'data/paul_graham/'




!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt'-O 'data/paul_graham/paul_graham_essay.txt'


```

### Load documents
[Section titled “Load documents”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#load-documents)

```


from llama_index.core import SimpleDirectoryReader





documents = SimpleDirectoryReader("./data/paul_graham").load_data()




print("Document ID:", documents[0].doc_id)


```

### Parse into nodes
[Section titled “Parse into nodes”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#parse-into-nodes)

```


from llama_index.core.node_parser import SentenceSplitter





nodes = SentenceSplitter().get_nodes_from_documents(documents)


```

### Set up an IndexStore
[Section titled “Set up an IndexStore”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#set-up-an-indexstore)

```


from llama_index_cloud_sql_pg import PostgresIndexStore






INDEX_TABLE_NAME="index_store"




await engine.ainit_index_store_table(




table_name=INDEX_TABLE_NAME,






index_store =await PostgresIndexStore.create(




engine=engine,




table_name=INDEX_TABLE_NAME,




# schema_name=SCHEMA_NAME



```

### Add to Docstore
[Section titled “Add to Docstore”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#add-to-docstore)

```


from llama_index.core import StorageContext





storage_context = StorageContext.from_defaults(




docstore=doc_store, index_store=index_store





storage_context.docstore.add_documents(nodes)

```

## Use with Indexes
[Section titled “Use with Indexes”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#use-with-indexes)
The Document Store can be used with multiple indexes. Each index uses the same underlying nodes.

```


from llama_index.core import Settings, SimpleKeywordTableIndex, SummaryIndex




from llama_index.llms.vertex import Vertex





Settings.llm = Vertex(model="gemini-1.5-flash", project=PROJECT_ID)




summary_index = SummaryIndex(nodes, storage_context=storage_context)




keyword_table_index = SimpleKeywordTableIndex(




nodes, storage_context=storage_context



```

### Query the index
[Section titled “Query the index”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#query-the-index)

```


query_engine = summary_index.as_query_engine()




response = query_engine.query("What did the author do?")




print(response)


```

## Load existing indexes
[Section titled “Load existing indexes”](https://developers.llamaindex.ai/python/examples/docstore/cloudsqlpgdocstoredemo/#load-existing-indexes)
The Document Store can be used with multiple indexes. Each index uses the same underlying nodes.

```

# note down index IDs



list_id = summary_index.index_id




keyword_id = keyword_table_index.index_id


```


```


from llama_index.core import load_index_from_storage




# re-create storage context



storage_context = StorageContext.from_defaults(




docstore=doc_store, index_store=index_store





# load indices



summary_index = load_index_from_storage(




storage_context=storage_context, index_id=list_id





keyword_table_index = load_index_from_storage(




storage_context=storage_context, index_id=keyword_id



```

  * [ LlamaParse ](https://developers.llamaindex.ai/llamaparse/)
  * [ LiteParse ](https://developers.llamaindex.ai/liteparse/)
  * [ LlamaAgents ](https://developers.llamaindex.ai/python/llamaagents/)
  * [ LlamaIndex Framework ](https://developers.llamaindex.ai/python/framework/)


