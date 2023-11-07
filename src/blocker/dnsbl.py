"""Used to identify if a domain or IP address is listed on a DNS Blocklist."""
import socket
import time
from os import path
from threading import Thread
from typing import List

from .base import Base


class DNSBL(Base):

    DATA_FILE: str = "dns.spam.yml"
    __dns_spam_list = []
    __spam_list: List[str] = []
    __threads = []

    def __init__(self) -> None:
        """Fetches the DNS block list data from the YAML file.
        """
        self.__dns_spam_list = self.get_yml_data(path.join(Base.DATA_DIRECTORY, self.DATA_FILE))

    def _reverse_ip_address(self, ip: str) -> str:
        """Returns the provided IPv4 address in reverse order.

        Args:
            ip (str): An IPv4 address.

        Returns:
            str: An IPv4 address in reverse order.
        """
        if len(ip) <= 1:
            return ip
        l = ip.split('.')
        return '.'.join(l[::-1])

    def _reverse_pointer(self, ip: str) -> str:
        """Returns the reverse DNS pointer name for the IPv6 address.

        This implements the method described in RFC3596 2.5.

        Args:
            ip (str): An IPv6 address.

        Returns:
            str: A reverse DNS pointer name for the IPv6 address.
        """
        reverse_chars = self.exploded[::-1].replace(':', '')
        return '.'.join(reverse_chars)

    def _check_dns_blacklist(self, ip: str, server: str) -> None:
        try:
            url = '{ip}.{server}'.format(ip=ip, server=server)
            res = socket.gethostbyname(url)
            self.__spam_list.append(server)
        except socket.gaierror:
            self.__logger.debug(f"DNSBL: {url} is not listed.")
            pass

    def _check_dns_blacklists(self, ip: str, servers: List[str]) -> None:
        """Checks a given IP address against a list of DNS block lists.

        Args:
            ip (str): _description_
        """
        for server in servers:
            t = Thread(target=self._check_dns_blacklist, args=(ip,server,))
            t.start()
            time.sleep(0.1)
            self.__threads.append(t)

    def is_valid_ipv4_address(self, address):
        try:
            socket.inet_pton(socket.AF_INET, address)
        except AttributeError:  # no inet_pton here, sorry
            try:
                socket.inet_aton(address)
            except socket.error:
                return False
            return address.count('.') == 3
        except socket.error:  # not a valid address
            return False
        return True

    def is_valid_ipv6_address(self, address):
        try:
            socket.inet_pton(socket.AF_INET6, address)
        except socket.error:  # not a valid address
            return False
        return True

    def check(self, value: str) -> dict:
        """The main method to check if a given value can be identified in DNS block lists.

        Args:
            value (str): A value to lookup. This is typically going to be a ip address.

        Returns:
            dict: A dictionary of the matched value and the sources it was found in.
        """
        ip: str = None
        try:
            if self.is_valid_ipv4_address(value):
                ip = self._reverse_ip_address(value)
            elif self.is_valid_ipv6_address(value):
                ip = self._reverse_pointer(value)
            else:
                ip = self._reverse_ip_address(socket.gethostbyname(value))
        except Exception as e:
            self.__logger.warning(f"Error trying to check DNSBL: {e}")
        if ip:
            self._check_dns_blacklists(
                ip=ip,
                servers=self.__dns_spam_list['servers']
            )
            while len(self.__threads) > 0:
                new_threads = []
                for t in self.__threads:
                    try:
                        if t and t.isAlive():
                            new_threads.append(t)
                    except:
                        # python 3.9 changed to is_alive()
                        if t and t.is_alive():
                            new_threads.append(t)
                self.__threads = new_threads
                time.sleep(1)
        return {
            'matched_on': ip,
            'sources': self.__spam_list
        }
