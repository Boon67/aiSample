import os, datetime, time
from dotenv import load_dotenv
load_dotenv()


# needed for any cluster connection
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
# needed for options -- cluster, timeout, SQL++ (N1QL) query, etc.
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,
                               QueryOptions)

TEXT_GREEN =  '\033[32m' # Green Text
TEXT_YELLOW =  '\033[33m' # Yellow Text
TEXT_BLUE =  '\033[34m' # Blue Text
TEXT_PURPLE =  '\033[35m' # Purple Text
TEXT_WHITE =  '\033[37m' # WHITE Text
END_TEXT = '\033[m' # reset to the defaults
# Update this to your cluster
ADMIN_USERNAME = os.getenv('ADMIN_ID')
ADMIN_PASSWORD = os.getenv('ADMIN_PWD')
BUCKET_NAME =os.getenv('BUCKET_NAME')
SCOPE_NAME =os.getenv('SCOPE_NAME')
COLLECTION_NAME =os.getenv('COLLECTION_NAME')
# User Input ends here.

# Connect options - authentication
auth = PasswordAuthenticator(
    ADMIN_USERNAME,
    ADMIN_PASSWORD,
)

# Get a reference to our cluster
# NOTE: For TLS/SSL connection use 'couchbases://<your-ip-address>' instead
cluster = Cluster('couchbase://localhost', ClusterOptions(auth))

# Wait until the cluster is ready for use.
cluster.wait_until_ready(datetime.timedelta(seconds=5))

# get a reference to our bucket
cb = cluster.bucket(BUCKET_NAME)

cb_coll = cb.scope(SCOPE_NAME).collection(COLLECTION_NAME)

# Get a reference to the default collection, required for older Couchbase server versions
cb_coll_default = cb.default_collection()

# upsert document function


def upsert_document(doc):
    print(TEXT_GREEN, "Upsert CAS:")
    try:
        key = str(doc["id"])
        result = cb_coll.upsert(key, doc)
        print(result.cas, END_TEXT, "\n")
    except Exception as e:
        print(e)

# get document function
def get_record_by_key(key):
    print(TEXT_YELLOW +"Key Retrieval: ")
    try:
        result = cb_coll.get(key)
        print(result.content_as[str], END_TEXT)
    except Exception as e:
        print(e)

# query for new document by callsign
def query_by_property(id, value):
    print("\nQuery Result: ")
    try:
        scope = cb.scope(SCOPE_NAME)
        sql_query = 'SELECT * FROM _default WHERE ' + id + ' = "' + value + '"'
        print(TEXT_BLUE, sql_query, END_TEXT)
        row_iter = scope.query(sql_query)
        for row in row_iter:
            print(TEXT_PURPLE, row, END_TEXT)
    except Exception as e:
        print(e)


document = {
    "id": str(time.time()) + "::" +  "2607:f8b0:4023:1006::bc",
    "time":str(datetime.datetime.utcnow()),
    "src":"2607:f8b0:4023:1006::bc",
    "dest":"2600:1700:158:111f:554:daff:fbe1:6fae",
    "protocol":"TLSv1.2",
    "length":"112",
    "info":"Application Data"
}

upsert_document(document) #Upsert for updating or creating new record
get_record_by_key(document["id"]) #retrieve record by key name (fastest)
query_by_property("src", document["src"]) #retrieve record by query parameter