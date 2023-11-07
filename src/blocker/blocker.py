"""Main module for blocker."""
import re
from typing import Dict, List

from .sync import Sync
from .base import Base


class Blocker(Base):
    """blocker is a Python package that allows you to check if a given value is in a block list."""

    def _compile_regex(self, value: str) -> re.Pattern:
        """Compiles a regex pattern for a given value.

        Args:
            value (str): The value to compile a regex pattern for.

        Returns:
            re.Pattern: The compiled regex pattern.
        """
        chars_to_escape = r"([.|/^&+%*=!<>?\\()-])"
        r = re.sub(chars_to_escape, r"\\\1", value)
        r = r"\b{}\b".format(r)
        return re.compile(r)

    def _lookup_dnsbl(self, value: str) -> Dict[str, str]:
        """A method to lookup a given value against DNSBLs.

        Args:
            value (str): The IP address to lookup.

        Returns:
            Dict[str, str]: A dict of DNSBLs that the provided IP address is listed in.
        """
        from .dnsbl import DNSBL

        return DNSBL().check(value)

    def lookup(self, value: str or List[str], text_list: bool = False, dns_list: bool = False) -> Dict[str, List[str]]:
        """Lookup is the main method to check if a given value can be identified in block lists.  

        The consumer of this method can toggle the different checks as needed.

        Args:
            value (str): A value to lookup. This is typically going to be a domain, ip address, etc.
            text_list (bool, optional): Whether or not to check text based lists. Defaults to False.
            dns_list (bool, optional): Whether or not to check dns lists. Defaults to False.

        Returns:
            Dict[str, List[str]]: A dictionary of the matched value and the sources it was found in.
        """
        count: int = 0
        return_dict: dict = {}
        if not value:
            self.__logger.critical("No value provided to lookup.")
            raise ValueError("No value provided to lookup.")
        if not isinstance(value, list):
            value = [value]

        if not text_list and not dns_list:
            self.__logger.critical("No lookup type provided.")
            raise ValueError("No lookup type provided.")

        if dns_list:
            self.__logger.debug("Starting to lookup DNSBLs.")
            for lookup_value in value:
                if lookup_value not in return_dict:
                    return_dict[lookup_value] = []
                dns_results = self._lookup_dnsbl(value=lookup_value)
                if dns_results:
                    return_dict[lookup_value].append(dns_results)
            self.__logger.debug("Finished looking up DNSBLs.")

        if text_list:
            self.__logger.debug("Starting to sync external data.")
            sync_data: Dict[str, str] = Sync().get_data()
            if not sync_data:
                self.__logger.critical("No data returned from sync.")
                raise ValueError("No data returned from sync.")
            self.__logger.debug("Finished syncing external data.")

            for blocker in sync_data["data"]:
                for lookup_value in value:
                    if lookup_value not in return_dict:
                        return_dict[lookup_value] = []
                    for url, data in blocker.items():
                        result = self._compile_regex(lookup_value).search(data)
                        if result:
                            count += 1
                            return_dict[lookup_value].append(url)
        return return_dict
