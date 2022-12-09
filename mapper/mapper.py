import sys, os, json


TOP_DIR = "/home/s33khan/Documents/newnew/mapping_location"
FILES_DIR = "files/"
INPUT_DIR = "input/"
OUTPUT_DIR = "output/"
API_DIRs = []
TARGET_JSON = "api_actions.json"
API_TO_PERMISSION = {}


# Fills the API directory names corresponding to a service
def fillAPIDirList(servicename):
    global API_DIRs
    API_DIRs = []
    API_DIRs = os.listdir(os.path.join(TOP_DIR, FILES_DIR, INPUT_DIR, servicename))


# Given a service and api, the function extracts the permission list
def parseAPIPermissionsList(servicename, apidir):
    apiname = apidir.split(".")[-1]
    contents = None

    print(os.path.join(TOP_DIR, FILES_DIR, INPUT_DIR, servicename, apidir, TARGET_JSON))

    with open(os.path.join(TOP_DIR, FILES_DIR, INPUT_DIR, servicename, apidir, TARGET_JSON)) as f:
        contents = json.load(f)

    size_of_iter = len(contents[servicename][apiname]["ordered_iterations"]) + 1
    iter_val = -1
    permissions_list = None

    while (permissions_list is None) or (permissions_list == []):

        permissions_list = None

        if abs(iter_val) == size_of_iter:
            permissions_list = []
            break

        elif "data" in contents[servicename][apiname]["ordered_iterations"][iter_val]:
            if "permissions" in contents[servicename][apiname]["ordered_iterations"][iter_val]["data"]:
                permissions_list = contents[servicename][apiname]["ordered_iterations"][iter_val]["data"]["permissions"]

        else:
            permissions_list = None

        if (not(permissions_list is None)) and permissions_list != []:
            break_loop = True

            for permission in permissions_list:
                if "EXCEPTION" in permission:

                    break_loop = False
                    break

            if break_loop:
                break

        iter_val = iter_val -1
    

    return permissions_list


def outputToJSONFile(json_str, servicename, filename):
    with open(os.path.join(TOP_DIR, FILES_DIR, OUTPUT_DIR, servicename, filename), 'w') as f:
        f.write(json_str)



def main():
    global API_DIRs, API_TO_PERMISSION, TOP_DIR

    TOP_DIR = os.getcwd()

    service_list = ["location", "telephony.registry", "notification"]

    for service in service_list:


        fillAPIDirList(service)

        print(API_DIRs)

        for apidir in API_DIRs:

            API_TO_PERMISSION[apidir] = {"permissions": parseAPIPermissionsList(service, apidir)}


        outputToJSONFile(json.dumps(API_TO_PERMISSION, indent=4), service, "permission_map.json")

        API_TO_PERMISSION = {}


    print("Done...")



if __name__ == "__main__":
    try:
        print("Starting...")
        main()
    
    except KeyboardInterrupt:
        print(f'\nUnexpected Error: {KeyboardInterrupt}.\nShutting Down...')
        
        sys.exit(0)