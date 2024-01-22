import os
from tqdm.auto import tqdm

def clear_folders():
    print("Clearing folders")
    folders = ["data_raw", "data_xml", "data_temp", "data_results"]
    for folder in folders:
        if folder in os.listdir(os.getcwd()):
            files = os.listdir(os.path.join(os.getcwd(), folder))
            for file in tqdm(files,total=len(files),desc=f"Clearing {folder}"):
                os.remove(os.path.join(os.getcwd(), folder, file))
            os.rmdir(os.path.join(os.getcwd(), folder))
            print(f"  Folder {folder} cleared")
            print()
        else:
            print(f"Folder {folder} not found")
    print("Folders cleared")
    return None

if __name__=="__main__":
    clear_folders()