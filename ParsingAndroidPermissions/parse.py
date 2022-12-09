import pandas as pd
import sys


# Fuction to read raw data
def loadData(filepath = None):
    try:
        raw_data = ""

        with open(filepath, 'r') as f:
            raw_data = f.read().split('\n')
        
        return raw_data

    except:
        return None


# Function to group together each permission's information
def combineAPILines(raw_data):
    group_raw_data = []

    for line_id in range(len(raw_data)):
        if("END" in raw_data[line_id]):break

        current_block = []
        
        
        if raw_data[line_id].isupper():
            current_block.append(raw_data[line_id])
            
            line_id = line_id + 1

            while(not raw_data[line_id].isupper()):
                if(not raw_data[line_id] == ""):
                    current_block.append(raw_data[line_id])
                
                line_id = line_id + 1
            
        if current_block != []:
            group_raw_data.append(current_block)

    return group_raw_data


# Function preserves 4 things: name, API level, protection level, and constant value
def pruneExtraInfo(grouped_raw_data):
    refined_data = []

    for group in grouped_raw_data:

        name = None
        api_level = None
        prot_level = None
        prot_level_id = 0
        constant_val = None
        
        private_permission = False
        level_defined = False


        name = group[0]
        api_level = group[1].split(" ")[4]
        constant_val = group[-1].split("\"")[1]

        if "Not for use by third-party applications." in group:
            private_permission = True


        for line in group:
            
            if ("Protection level:" in line):
                level_defined = True
                break
            prot_level_id = prot_level_id + 1
        
        if (not private_permission) and (not level_defined):
            prot_level = "NA"
        
        elif(level_defined):
            prot_level = group[prot_level_id].split(" ")[2]

        else:
            prot_level = "Not for use by third-party applications."


        refined_data.append([name, api_level, prot_level, constant_val])

    return refined_data
        

def createDataframe(refined_data):
    return pd.DataFrame(refined_data, columns=["Name", "API Level", "Protection Level", "Constant Value"])


def writeToCSV(df, outputPath):
    df.to_csv(outputPath, index=False)


def main(filepath):
    raw_data = loadData(filepath)

    if raw_data == None:
        raise Exception("Error reading file")

    df = createDataframe(pruneExtraInfo(combineAPILines(raw_data)))

    writeToCSV(df, "/home/s33khan/Documents/android_perm_prot_levels/files/permissions.csv")
    








if __name__ == "__main__":
    try:
        main("/home/s33khan/Documents/android_perm_prot_levels/files/raw.txt")
    
    except KeyboardInterrupt:
        print(f'\nUnexpected Error: {KeyboardInterrupt}.\nShutting Down...')
        
        sys.exit(0)