# docker run --rm -it -p 80:80 andymeneely/swen331fuzzer
import mechanicalsoup
import argparse
import requests
from urllib.parse import urljoin, urlparse
import discover
import test

#running fuzzer with dvwa
def open_dvwa(url):
    """
    PART 0: OLD CODE
    """

    #connect to the dvwa website 
    browser = mechanicalsoup.StatefulBrowser(user_agent='MechanicalSoup')
    browser.open("{}setup.php".format(url))

    browser.select_form('form[action="#"]')
    #submit the form
    browser.submit_selected()

    browser.open(url)
    browser.select_form('form[action="login.php"]')
    #get the form information 
        #browser.form.print_summary()
    
    browser['username'] = 'admin'
    browser['password'] = 'password'
    browser.submit_selected()

    browser.open('{}security.php'.format(url))

    browser.select_form('form[action="#"]')
    browser['security'] = 'low'
    browser.submit_selected()

    page = browser.page
    print(page)
    # discover_links(url, links_found, custom)
       


def is_link_validated(url):
    """
        Check to see if the url is valid 
    """
    r = requests.get(url)
    if (r.status_code == 200):
        return True
    return False

def is_external(url, new_url):
    """
        Check to see if a given url is external 
    """
    url_domain = urlparse(url).netloc
    new_url_domain = urlparse(new_url).netloc

    if (url_domain != new_url_domain):
        return True
    return False


def parse_url(url):
    """
        Take a URL and parse it. 
        If the url has a parameter, return that URL with the parameters else, 
        simply return the orginal url 
    """
    split_url = url.split('?')
    parsed_url = list()
    if (len(split_url) > 1):
        base_url = split_url[0]
        parameters = split_url[1]
        parsed_url.append(base_url)
        parsed_url.append(parameters)
    else: 
        parsed_url.append(url)

    return parsed_url

def print_parsing(links_found):
    """
        Print parsed urls
    """
    for link in links_found:
        if parse_url(link) == None:
            continue
        else:
            print(parse_url(link))

def main():

    #get the arguments via command line
    parser = argparse.ArgumentParser(description='Get url')
    sub_parser = parser.add_subparsers(dest='command', help="the different commands you can run!")
    # parser.add_argument('discover', help="enter discover by default")
    # parser.add_argument('url', help="the site url")
    # parser.add_argument('--custom', help="enter 'dvwa' when testing dvwa")
    # parser.add_argument('--words', help="enter the common word file name: ex. common_word.txt")
    # parser.add_argument('--sensitive', help="enter the sensitive words file name: ex. sensitive.txt")

    discover_parser = sub_parser.add_parser('discover', help="running fuzzer for discovering")
    discover_parser.add_argument('url', help="the site url")
    discover_parser.add_argument('--custom', help="enter 'dvwa' when testing dvwa")
    discover_parser.add_argument('--words', help="enter the common word file name: ex. common_word.txt")
    discover_parser.set_defaults(func=discover.discover)


    test_parser = sub_parser.add_parser('test', help='running fuzzer for test')
    test_parser.add_argument('url', help="the site url")
    test_parser.add_argument('--custom', help="enter 'dvwa' when testing dvwa")
    test_parser.add_argument('--words', help="enter the common word file name: ex. common_word.txt")
    test_parser.add_argument('--sensitive', help="enter the sensitive words file name: ex. sensitive.txt")
    test_parser.set_defaults(func=test.test)


    args = parser.parse_args()

    url = args.url
    links_found = set()
    guessed_pages = set()

    if (args.command == 'discover'):
        discover.discover(url, links_found, guessed_pages, args.custom, args.words)
    else:
        browser = mechanicalsoup.StatefulBrowser(user_agent='MechanicalSoup')
        discovered = discover.discover_links(url, links_found, browser)
        
        if (args.words != None):
            discovered = discover.page_guess(url, args.words, guessed_pages, browser)

        test.test(discovered, args.sensitive, browser)


if __name__ == '__main__':
    main()
