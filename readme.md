## Sample Python App Couchbase

The purpose of this app is to quickly setup a Couchbase instance (single node) and demonstrate upserting a document, reading it by key and then querying via a property attribute of the documents. Each document is uniquely defined by a timestamp.

The URL for the server will be ([http://localhost:8091])

1. First run a docker-compose up to setup the Couchbase Environment. Note this uses the .env file for shared values on configuration and running the app.
2. Install the required packages with ```pip install -r requirements.txt```
3. Run ```python ./sample.py```

This will create a document similar to what Wireshark renders on network capture. 

This will perform an upsert with the UTC Timestamp and the src Address as the key, followed by a keylookup from the just inserted record and finally a query using the query service.

Note: You will be required to create the primary index (GSI) in the system in order for the application to support the query function. 
```CREATE PRIMARY INDEX `#primary` ON `sampleData` ``` Otherwise the query will fail.