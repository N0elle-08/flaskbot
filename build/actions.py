'''
This function is responsible for handling user actions as per the given defined intents
'''
import requests
from hdbcli import dbapi
from hana_ml.dataframe import ConnectionContext
from hana_ml import dataframe as df
from settings.base import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_SCHEMA, setup_logger

logger = setup_logger()
class Actions:
    def __init__(self):
        pass

    def db_connection(self):
    # Connect to the SAP HANA database
        # Define your SAP HANA credentials
        
        cc = ConnectionContext(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD)

        return cc
    
    def get_details(self, tab_name):
        """
        Fetch employee details from the connected database.
        """
        cc = self.db_connection()
        schema = DB_SCHEMA
        query = f"SELECT * FROM {schema}.{tab_name}"
        emp_df = df.DataFrame(cc, query)
        # Collect the result as a Pandas DataFrame
        emp_pandas_df = emp_df.collect()

         # Convert the Pandas DataFrame to a list of dictionaries
        result_dict = emp_pandas_df.to_dict(orient='records')

        logger.info(f"Retrieved data from {tab_name}")
        logger.info(result_dict)  # Log the result as a dictionary

        return result_dict 
    def get_emp_details(self, empname):
            """
            Fetch employee details from the connected database.
            """
            cc = self.db_connection()
            schema = DB_SCHEMA
            query = f"SELECT * FROM {schema}.COS_EMPINFO where empname = '{empname}'"
            emp = df.DataFrame(cc, query)
            # Collect the result as a Pandas DataFrame
            emp_rec = emp.collect()

            # Convert the Pandas DataFrame to a list of dictionaries
            result_dict = emp_rec.to_dict()

            logger.info(result_dict)  # Log the result as a dictionary

            return result_dict


    def get_access_token(self):
            """
            Request an access token using OAuth credentials.
            """
            try:
                response = requests.post("https://development-oc58dg9d.authentication.us10.hana.ondemand.com/oauth/token", data={
                    "grant_type": "client_credentials",
                    "client_id": "sb-incident_1-initium_digital-Dev!t264940",
                    "client_secret": "d06eead7-ef8c-4949-87eb-4aadcb8f3325$5lsS50X5nBRyOwT-HpwHAI_gzp5LPLAJwGgbwrUZgFI=",
                })
                response.raise_for_status()
                token_info = response.json()
                return token_info['access_token']
            except Exception as e:
                return None
        
    def create_incident(self, args):
        """
        When User needs to create an incident
        """
        logger.info(f"here")
        
        access_token = self.get_access_token()
        if not access_token:
            logger.info("Failed to obtain access token.")
        else:
            logger.info("Access token retrieved")
        

        url = "https://initium-digital-pvt-ltd-development-oc58dg9d-dev-incident-1-srv.cfapps.us10-001.hana.ondemand.com/browse/Incident"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        emp = self.get_emp_details(args["empname"])
        args["isdraft"] = "0"
        # args["empid"] = str(emp["EMPID"][0])
        # args["emppos"] = str(emp["EMPPOS"][0])
        # args["supid"] = str(emp["SUPID"][0])
        # args["division"] = str(emp["DIVISION"][0])
        # args["dept"] = str(emp["DEPT"][0])
        # args["section"] = str(emp["SECTION"][0])
        # args["empemail"] = str(emp["EMPEMAIL"][0])

        logger.info(args)

        response = requests.post(url, json=args, headers=headers)
        logger.info(response)
        response_json = response.json()
        logger.info(response)
        inci_id = response_json.get("ID")
        incident_id = response_json.get("INCID")
        if response.status_code == 201:
            logger.info(f"status: success, response: {response.json()}")
            return f"Incident created successfully - ID {inci_id}, INCID {incident_id}"
        else:
            logger.info(f"status: error, error: {response.text}")
            return {"status": "error", "error": response.text}

