import mechanicalsoup
from urllib.parse import urljoin, urlparse
import fuzz

def discover(url, links_found, guessed_pages, custom, words):
    """
    Fuzzer part1: Discover 
    """
    if custom != None:
        if (custom == "dvwa"):
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
            #print("\n\n",browser.page,"\n\n\n")
    else:
        browser = mechanicalsoup.StatefulBrowser(user_agent='MechanicalSoup')

    discovered = discover_links(url, links_found, browser)
    
    print("\n***DISCOVERING LINKS AT {}***\n".format(url))
    print_discover(url, links_found, browser)

    if (words != None):
        print('\n***LINKS SUCCESSFULLY FOUND THROUGH GUESSING***\n')
        print_guessed_pages(url, words, links_found, guessed_pages ,browser)
        discovered = page_guess(url, words, guessed_pages, browser)
    else:
        print("\n***NO WORDS WERE GIVEN TO GUESS***\n")

    print("\n***PARSED URL***\n")
    fuzz.print_parsing(discovered)

    validated_links = valid_links(url, discovered)
    # print(validated_links)
    print('\n***INPUTS FOUND***\n')
    # print_find_inputs(validated_links, browser)
    find_inputs(validated_links, browser)

    print('\n***COOKIES***\n')
    get_cookies(browser)
    




def discover_links(url, links_found, browser):
    """
    Find every possible link in a page, crawl to them and return a set of valid links 
    """
    browser.open(url)
    current_url = url

    links = browser.page.select('a')
    for link in links:
        link_url = link.get('href')
        new_url = urljoin(current_url, link_url)

        if (new_url not in links_found):
            links_found.add(new_url)
            if (fuzz.is_link_validated(new_url) and not fuzz.is_external(url, new_url) and not ("logout" in new_url) and not ("login" in new_url) ):
                    discover_links(new_url, links_found, browser)
            else:
                continue
        else:
            break
        
    return links_found


def print_discover(url, links_found, browser):
    """
    Print each discovered link in a new line
    """
    for link in discover_links(url, links_found, browser):
        print(link)



def page_guess(url, filename, guessed_pages, browser):
    """
    Read a common_word file and try to guess pages; return a set of guessed pages 
    """
    with open (filename) as file:
        read = file.read()
        common_words = read.split()
    with open('ending.txt') as ending:
        read_end = ending.read()
        endings = read_end.split()

    discovered = discover_links(url, guessed_pages, browser)
    for word in common_words:
        for end in endings:
            possible_link = word + end
            possible_url = urljoin(url,possible_link)
            if (fuzz.is_link_validated(possible_url) and possible_url not in discovered):
                guessed_pages.add(possible_url)
                discover_links(possible_url,guessed_pages, browser)
            else: 
                continue
    
    return guessed_pages

def print_guessed_pages(url, filename, links_found, guessed_pages, browser):
    """
    Print sucessfully guessed pages
    """
    pages = page_guess(url, filename, guessed_pages, browser)
    already_discovered = discover_links(url, links_found, browser)
    valid_guess = set()
    for page in pages: 
        if page not in already_discovered:
            valid_guess.add(page)
        else:
            continue

    
    if valid_guess != None:
        for valid in valid_guess:
            print(valid)
    else:
        print("No guesses could be made :(")


def find_inputs(valid_l, browser):
    """
    Find and print all the inputs from each link
    """
    inputs = []
    title = "No Title"
    # forms_found = set()
    for link in valid_l:
        browser.open(link)
        if browser.page != None:
            # finding all the forms that uses input tag
            inputs = browser.page.find_all('input')
            for input in inputs:
                if input != None and input.get('type') != 'submit' and input.get('type') != 'button':
                    if (browser.page.find('h1') != None):
                        title = browser.page.find('h1').text
                
                    # forms_found.add(input)
                    print("Page:",title,
                            "\n**Name:",input.get('name'),
                            "\n**Value:",input.get('value'),'\n')

        else:
            continue

    # return forms_found


def valid_links(url, links_found):
    """
    Out of all the links, just get the ones that are valid with response 200 (no logout) and not externals
    """
    validated_links = set()
    for link in links_found:
        if (fuzz.is_link_validated(link) and not fuzz.is_external(url, link) and not ("logout" in link)):
            validated_links.add(link)
        else:
            continue
    return validated_links

def get_links_not_extr(url, links_found):
    not_extr = set()
    # links_found = discover_links
    for link in links_found:
        if ((fuzz.is_external(url, link) == False) and not ("logout" in link)):
            not_extr.add(link)
        else:
            continue
    return not_extr

def get_cookies(browser):
    """
    Find and print the cookies from browser
    """
    cookies = browser.get_cookiejar()
    if len(cookies) == 0:
        print("No cookies found\n")
    for cookie in cookies: 
        if cookie == None:
            continue
        print("Cookie:\n","\n**Name:",cookie.name,
                            "\n**Value:",cookie.value,'\n')