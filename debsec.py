import io
import sys
import typing as t

import lxml
import lxml.cssselect
import requests

Url = str
Content = str
Update = str
Updates = t.Iterable[Update]
DsaNumber = int
Dsa = str


class ConnectionError(Exception):
    pass


class DsaDoesNotExit(Exception):
    pass


def recent_url() -> Url:
    return "https://lists.debian.org/debian-security-announce/recent"


def clean_update(update: Update) -> Update:
    prefix = "[SECURITY] [DSA "
    words = "".join(update[len(prefix):].split("]")).split(" ")
    words[0] = words[0].split("-")[0]
    return " ".join(words)


def update_from_element(element) -> Update:
    return clean_update(element.text)


def updates(content: Content) -> Updates:
    parser = lxml.etree.HTMLParser()
    root = lxml.etree.parse(io.StringIO(content), parser)
    path = lxml.cssselect.CSSSelector("ul > li > strong > a").path
    return map(update_from_element, root.xpath(path))


def dsa_url(dsa_number: DsaNumber, updates: Updates) -> Url:
    """Raises DsaDoesNotExit"""
    prefix = "{} ".format(dsa_number)
    for i, update in enumerate(updates):
        if update.startswith(prefix):
            break
    else:
        raise DsaDoesNotExit
    id_ = str(i).zfill(5)
    return ("https://lists.debian.org/debian-security-announce/2019/msg{}.html"
            .format(id_))


def dsa(content: Content) -> Dsa:
    gpg_msg = (content.split("-----BEGIN PGP SIGNED MESSAGE-----\n")
               [1]
               .split("-----BEGIN PGP SIGNATURE-----")
               [0])
    return (gpg_msg.split(
        "- -------------------------------------------------------------------------")[2]
        [2:])


def get_content(url: Url) -> Content:
    """Raises ConnectionError"""
    try:
        return requests.get(url).content.decode()
    except requests.ConnectionError:
        raise ConnectionError


def print_updates(updates: Updates) -> None:
    for update in updates:
        print(update)


def get_updates() -> Updates:
    return updates(get_content(recent_url()))


def get_dsa_number(dsa_number: DsaNumber) -> Url:
    return dsa_url(dsa_number, get_updates())


def main() -> None:
    print_updates(get_updates())


def main_dsa(dsa_number: DsaNumber) -> None:
    print(dsa(get_content(get_dsa_number(dsa_number))))


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0:
        try:
            main()
        except ConnectionError:
            print("Connection error")

    if len(args) == 1:
        try:
            dsa_number = int(args[0])
            main_dsa(dsa_number)
        except ValueError:
            print("Invalid number")
        except ConnectionError:
            print("Connection error")
        except DsaDoesNotExit:
            print("DSA does not exist")

    if len(args) > 1:
        print("Usage: {} [dsa_number]".format(sys.argv[0]))
