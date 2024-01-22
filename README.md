# Documentation


## FETCH_DATA Class

The `FETCH_DATA` class is designed to automate the process of downloading and extracting .xml.gz files from the National Center for Biotechnology Information (NCBI) PubMed baseline dataset. This documentation provides instructions on how to use the class.

## Requirements

Before using the FETCH_DATA class, ensure you have the following:

Python 3.x installed on your system.
requests, bs4 (BeautifulSoup4), tqdm, and concurrent.futures libraries installed in your Python environment. You can install these with the following command:

```
pip install requests beautifulsoup4 tqdm
```

To start using the FETCH_DATA class, you need to create an instance of the class. Optionally, you can specify the base_url parameter if you want to use a different URL than the default NCBI FTP server.

```python
from fetch_data import FETCH_DATA
```


# Create an instance with the default base_url
```python
fetcher = FETCH_DATA()
```

# Or create an instance with a custom base_url
```python
fetcher = FETCH_DATA(base_url="https://your.custom.url/")
```

# Listing Available Files

To list the .xml.gz files available for download, use the `list_baseline_files method`. This method will prompt you to enter the number of files you wish to download.

```python
# List files and choose how many to download
file_list = fetcher.list_baseline_files()
```

# Downloading Files

To download the files, use the get_raw_data method. This method will prompt you for the number of workers (concurrent downloads) and proceed to download the files.


```
fetcher.get_raw_data()
```

# Extracting Files

After downloading, you can extract the .xml.gz files using the initiate_data_extraction method. This method will also prompt you for the number of workers for parallel extraction.

```python
fetcher.initiate_data_extraction()
```

# Folder Structure

The class automatically manages the folder structure for storing raw data, extracted XML files, temporary files, and result data. The folders are created in the current working directory and are named as follows:

- **data_raw:** Stores the downloaded .xml.gz files.
- **data_xml:** Stores the extracted .xml files.
- **data_temp:** Used for any temporary data handling.
- **data_results:** Intended for storing processed results.

# Important Notes

- Ensure you have a stable internet connection for downloads to prevent incomplete files.

- The class handles basic error checking, such as skipping already downloaded or extracted files.

- The actual processing of .xml files after extraction is not covered by this class and should be implemented separately according to your needs.

By following the above instructions, you should be able to utilize the FETCH_DATA class to automate the fetching and extraction of files from the NCBI PubMed baseline dataset.