import json

with open("config.json", 'r') as file:
        config_data = json.load(file)
        environment = config_data["env"]
        print(f"running in {environment}")
        server_config = config_data[environment]
        token_info = server_config["token_info"]

        log_server = server_config["log_server"]
        log_db = server_config["log_db"]
        publisher_url= server_config["publisher_url"]
        token_url = token_info["url"]
        client_id = token_info["client_id"]
        client_secret = token_info["client_secret"]