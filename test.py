import fuzz
import discover
import requests


def test_delayed(urls):
    treshold = 1.9
    for url in urls:
        r = requests.get(url).elapsed.total_seconds()
        if (fuzz.is_link_validated(url) == True):
            if (r > treshold):
                print(url, "has a delayed response of ", r, ' seconds')
        else:
            continue

def test_valid(urls):
    for url in urls:
        if (fuzz.is_link_validated(url) == False):
            print(url, "has non 200 response code!: ", requests.get(url).status_code, " code")

def test_sensitive_data(urls, sensitive, browser):
    with open(sensitive) as sens:
        read = sens.read()
        sens_content = read.split()
        counter = 0
        # print(sens_content)
    for url in urls:
        if (fuzz.is_link_validated(url) == True):
            for content in sens_content:
                page_text = browser.get(url).soup.get_text()
                # print(page_text)
                if (content in page_text):
                    print("sensitive content exists;", content, " in ",url)
                    counter +=1
        else:
            continue
    if counter == 0: 
        print("No sensitive data found!")


def test(links, sensitive, browser):

    print("\n**CHECKING FOR BAD LINKS (not 200 response code)**\n")
    test_valid(links)

    print("\n**CHECKING FOR DELAYED LINKS**\n")
    test_delayed(links)

    print("\n**CHECKING FOR SENSITIVE DATA**\n")
    test_sensitive_data(links, sensitive, browser)