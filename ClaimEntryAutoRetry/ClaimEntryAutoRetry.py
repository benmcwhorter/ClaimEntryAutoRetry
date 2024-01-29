import utils.Config as c
import pandas as pd
import utils.SQLConnector as s
import PublisherHandler as ph

#setup connection to log server
sql_connector = s.SQLConnector(c.log_server,c.log_db)
with open("payloads_to_retry.sql") as f:
    sql_query = f.read()
connection = sql_connector.get_connection()

#get payloads to retry
print("getting payloads to retry")
all_retry_df = pd.read_sql(sql_query, connection)
list_of_client_retry_df = [group for _, group in all_retry_df.groupby('internal_client_key')]
print(f"payloads found: {len(all_retry_df)} for {len(list_of_client_retry_df)} clients")

#retry payloads, submit batch for each internal_client_key
publisher_handler = ph.PublisherHandler()
response_batchids = []
for client_df in list_of_client_retry_df:
    #send the payloads
    response = publisher_handler.post_data_frame(client_df)
    print(response)

print("done!")