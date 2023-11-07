"""This class is responsible for downloading and syncing data for lookups."""
from datetime import datetime, timedelta
from os import path
from typing import Dict, List

import  requests

from  .base import  Base


class Sync(Base):

    DATA_FILE: str = "text.blocker.yml"
    OUTPUT_FILE: str = "blocker_list.json"
    URL_MAP: Dict[str, bool] = {}

    def __init__(self) -> None:
        self._blocker_lookup_list: List = self.get_yml_data(path.join(Base.DATA_DIRECTORY, Sync.DATA_FILE))

    def _download_threaded_method(self, urls: str or List[str]) -> Dict[str,str]:
        return_list: List[Dict[str, str]] = []
        try:
            with requests.Session() as s:
                if not isinstance(urls, list):
                    urls = [urls]
                for url in urls:
                    try:
                        download = s.get(url)
                    except Exception as e:
                        self.__logger.debug(f"Error trying to download content from '{url}' in threaded method: {e}")
                    if download.status_code != 200:
                        self.__logger.debug(f"Error trying to download content from '{url}' in threaded method.")
                        pass
                    else:
                        try:
                            decoded_content = download.content.decode('utf-8', errors='ignore')
                            self.__logger.info(f"Successfully downloaded content from '{url}' in threaded method.")
                            # print(f"decoded_content is {decoded_content}\n")
                            # input("Press Enter to continue...")
                            self.results["data"].append({url: decoded_content})
                        except Exception as e:
                            self.__logger.debug(f"Error trying to decode content from '{url}' in threaded method: {e}")
                            pass
            return return_list
        except:
            self.__logger.debug(f"Error trying to download content from '{url}' in threaded method.")
            pass

    def sync(self, force: bool = False) -> List:
        """Initiates syncing of external data to the local system.

        Args:
            force (bool, optional): Whether or not to force override based on last updated timestamp. Defaults to False.

        Returns:
            bool: Whether or not the sync was successful.
        """
        self.results: Dict[str, str] = {
            "updated": datetime.now().isoformat(),
            "data": []
        }
        response = self.run_threaded(
            method=self._download_threaded_method,
            list_data=self._blocker_lookup_list["blocks"]
        )
        if not self.save_json_data(self.results, path.join(Base.DATA_DIRECTORY, Sync.OUTPUT_FILE)):
            self.__logger.error("Error trying to save downloaded data to disk.")
            return False
        return self.results

    def get_data(self) -> List:
        """Returns the data from the last sync.

        Returns:
            List: The data from the last sync.
        """
        if not hasattr(self, "results"):
            self.__logger.info("Loading data from disk.")
            self.results = self.get_yml_data(path.join(Base.DATA_DIRECTORY, Sync.OUTPUT_FILE))
            if self.results and "updated" in self.results and "data" in self.results:
                if self.results["updated"] <= (datetime.now() - timedelta(days=1)).isoformat():
                    self.__logger.info("Data is older than 1 day. Syncing.")
                    self.sync()
                return self.results
        return self.results
