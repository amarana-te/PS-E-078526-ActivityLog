import json
from connector import *
from Logs import Logs

# Date & Time
def timestamp():
    date_time_now = datetime.now()
  
    return date_time_now.strftime("%m/%d/%H:%M:%S")



def get_account_groups(headers) -> dict:

    
    aid_list = get_data(headers=headers, endp_url="https://api.thousandeyes.com/v6/account-groups.json")

    aids: dict = {}
    if aid_list["accountGroups"]:

        for aid in aid_list["accountGroups"]:

            aids.update({aid.get("accountGroupName"): aid.get("aid")})


    return aids



def get_logs(headers, window: int, account: str, file_path:str) -> dict:


    aids = get_account_groups(headers=headers)
                                  

    logs_list = get_data(headers=headers, endp_url="https://api.thousandeyes.com/v6/audit/user-events/search.json?window=" + str(window) + "d&aid=" + str(aids.get(account)))


    # los logs traen pagination en algunos casos
    pagination = 1 #lo dejaremos por el momento así para que entre al while

    while pagination == 1:

        for log in logs_list["auditEvents"]:

            log.pop("uid"), log.pop("aid")
            #returnedValue = returnedValue.pop("aid")

            logs = Logs("5d24b10e56d4e549a3942585", 
                    log.get("event"),
                    "ThousandEyes",
                    log)
        
            build_payload(file_path,logs)

        if "next" in logs_list["pages"]: #si hay una next page en esto significa que tenemos que hacer otro query
            
            URL = logs_list["pages"]["next"]
            logs_list = get_data(headers=headers, endp_url=URL)
            

        else:
            #si ya no hay paginas por revisar apagamos el while y sacamos valores para las tablas una vez que ya recopilamos toooda la info de todas las paginas
            pagination = 0


    return logs_list


def build_payload(file_path,logs):

    #para construir una entry del archivo
    d_logs = {"service_id": logs.service_id, "log_type": logs.log_type, "tag": logs.tag, "message": logs.message}
    file_name = file_path
    f = open(file_name, 'a+')  # open file in append mode
    f.write(json.dumps(d_logs)+"\n")
    f.close()

    return 0




############################
#            MAIN
############################

OAuth = "XXXXXX-XXXX-XXXXX-XXXX-XXXXX"
file_path = "home_depot.log"
account = ["Dani's sandbox", "Switching team"]

############################

headers = headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + OAuth,
    }

with open(file_path, 'w'):
    pass


for acc in account:
    get_logs(headers=headers, window=1, account=acc, file_path=file_path)
