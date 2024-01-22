import requests
from tqdm.auto import tqdm
import bs4
import re
import os
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
import gzip
import shutil

base_url = "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/"


class FETCH_DATA:
    def __init__(self, base_url:str = base_url):
        self.base_url = base_url
        self.wd  = os.getcwd()
        #check if data folder exists

        self.data_raw_folder = self.path_to_folder("data_raw")
        self.data_xml_folder = self.path_to_folder( "data_xml")
        self.data_temp_folder = self.path_to_folder("data_temp")
        self.data_results_folder = self.path_to_folder("data_results")
        self.item_list = self.list_baseline_files()
        self.nw = self. number_of_workers()
        self.download = self.get_raw_data()
        self.download_file = self.extract_data()
        

    def number_of_workers(self):
         number_worker = input("define number of workers (default = 1):")
         return int(number_worker) if number_worker.isdigit() else 1

    def path_to_folder(self, folder_name:str):
        if folder_name not in os.listdir(os.getcwd()):
            os.mkdir(folder_name)
        return os.path.join(os.getcwd(), folder_name)
    
    def list_baseline_files(self):    
        base_url = self.base_url
        base_page = requests.get(base_url)
        base_soup = bs4.BeautifulSoup(base_page.text, "html.parser")
        list_items = base_soup.find_all("a", href=re.compile(r"\.xml\.gz$"))
        print(f"From the fpt server {len(list_items)} fileswill be obtained")
        print("")
        num_files = int(input("how many files do you want to download? (0->all):"))
        num_files = int(num_files) if num_files.isdigit() and int(num_files) != 0 else len(list_items)
        return list_items[:num_files]
    
    def download_file(self,item):
        url = r"https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/"+item["href"]
        file_name = url.split("/")[-1]
        file_path = os.path.join(self.data_raw_folder, file_name)
        if file_name not in os.listdir(self.data_raw_folder):
            print(f"Downloading {file_name}")
            file_data = requests.get(url)
            with open(file_path, "wb") as f:
                f.write(file_data.content)
            return f"Downloaded {file_name}"
        else:
            return f"Already downloaded {file_name}"
    
    def get_raw_data(self):
        # Assuming `list_items` is a list of dictionaries with "href" keys
        # Assuming `data_folder` is the path to your data folder

        # Create a progress bar
        pbar = tqdm(desc="Downloading", total=len(self.item_list), position=0, leave=True)

        # Setup ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Using list comprehension to create a list of futures
            futures = [executor.submit(self.download_file, item) for item in self.item_list]
            # As each future completes, update the progress bar
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                pbar.desc = future.result()
                pbar.update(1)
        pbar.close()
        print("Download complete")
        return True
    
    def extract_file(self,file):
        # Specify the file paths
        gz_file_path = file
        filename = os.path.basename(gz_file_path)
        xml_file = filename.replace('.gz', '')  # Removing the .gz extension
        xml_file_path = self.data_xml_folder + xml_file

        if xml_file in os.listdir(self.data_xml_folder):
            return f"{xml_file_path} already exists."
        else:
            # Use gzip to open the file in read mode ('rb') and shutil to copy the file object to a new file
            with gzip.open(gz_file_path, 'rb') as f_in:
                with open(xml_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            return f"Extracted {xml_file_path}"
    
    def extract_data(self):
        gzip_file = [file for file in os.listdir(self.data_raw_folder) if file.endswith(".gz")]
        with ProcessPoolExecutor() as executor:
            # Prepare the paths for the gzip files
            gzip_file_paths = [os.path.join(self.data_raw_folder, file) for file in gzip_file]
            # Start the progress bar
            pbar = tqdm(total=len(gzip_file_paths), desc="Extracting files")
            # Submit tasks to the executor
            futures = {executor.submit(self.extract_file, gz_file_path): gz_file_path for gz_file_path in gzip_file_paths}
            # As each future completes, update the progress bar
            for future in concurrent.futures.as_completed(futures):
                pbar.update(1)
            pbar.close()
        print("File extraction complete")
        return True