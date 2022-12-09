import sys, os, json
import pandas as pd


TOP_DIR = "/home/s33khan/Documents/newnew/ParsingAndroidPermissions"
FILES_DIR = "files/"
API_DIRs = []
API_TO_PERMISSION = {}


def main():

    df = pd.read_csv(os.path.join(TOP_DIR, FILES_DIR, "permissions_to_protection.csv"))
    print(df.head())

    location_permissions = None
    with open(os.path.join(TOP_DIR, FILES_DIR, "notification", "permission_map.json"), 'r') as f:
        location_permissions = json.load(f)

    # print(type(location_permissions))


    api_list = []
    permissions_list = []
    protection_levels = []
    for api, permissions in location_permissions.items():
        curr_api = api
        curr_permissions = permissions["permissions"]
        curr_protection_level = []

        for permission in curr_permissions:
            if "EXCEPTION" in permission:
                continue
            splitted = permission.split(".")[-1]
            
            if not (df.loc[df["Name"] == splitted].empty):
                curr_protection_level.append(df.loc[df["Name"] == splitted].iloc[0]["Protection Level"])

        api_list.append(curr_api)
        permissions_list.append(curr_permissions)
        protection_levels.append(curr_protection_level)

    output_df = pd.DataFrame({
        "API NAME": api_list,
        "Permissions": permissions_list,
        "Protection Levels": protection_levels
    })

    output_df.to_csv(os.path.join(TOP_DIR, FILES_DIR, "notification", "protection_map.csv"), index=False)

if __name__ == "__main__":
    try:
        main()
    
    except KeyboardInterrupt:
        print(f'\nUnexpected Error: {KeyboardInterrupt}.\nShutting Down...')
        
        sys.exit(0)