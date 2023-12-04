import requests
from urllib.parse import urlparse
import os


def download_file(url: str, destination_folder: str) -> str:
    """
    Downloads a file from the given URL and saves it to the specified destination folder.
    Returns the path to the downloaded file.

    :param url: The URL of the file to download.
    :param destination_folder: The local folder where the file should be saved.
    :return: The path to the downloaded file.
    """
    try:
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        destination_path = os.path.join(destination_folder, filename)

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(destination_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return destination_path
    except requests.RequestException as e:
        print(f"Error occurred while downloading the file: {e}")
        return ""
    except IOError as e:
        print(f"Error occurred while writing the file to disk: {e}")
        return ""
