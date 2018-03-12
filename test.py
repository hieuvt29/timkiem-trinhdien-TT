from __future__ import print_function, unicode_literals
import requests, json, hashlib

def getPageLinks(title, limit = 100, offset = 0):
    url = "https://vi.wikipedia.org/w/api.php?action=query&format=json&prop=links&titles=" + title + "&utf8=1&plnamespace=0&pllimit=" + str(limit + offset)
    res = requests.get(url)
    resj = json.loads(res.text)
    pages = resj['query']['pages']
    pageID = list(pages.keys())[0]
    pageTitle = pages[pageID]['title']
    links = None
    if "links" in pages[pageID]:
        links = pages[pageID]['links'][offset:]
    return links

def getPageContent(title):
    api = "https://vi.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles="+ title +"&utf8=1&explaintext=1"

    res = requests.get(api)
    res = json.loads(res.text)
    pages = res['query']['pages']
    pageID = list(pages.keys())[0]
    content = None
    if pageID != '-1':
        content = pages[pageID]['extract']
    return pageID, content

def save(pages, num_pages):
    pages = json.dumps(pages, ensure_ascii=False)
    with open(str(num_pages) + "-backup.json", 'w') as f:
        f.write(pages)

def getPagesContent(startPage, limit, offset, maxNumPage):
    pages = {}
    baseTitles = [startPage]
    nextTitles = []
    while True:
        for pageTitle in baseTitles:
            pageID, content = getPageContent(pageTitle)
            print(pageTitle)
            if content and (pageID not in pages):
                pages[pageID] = {"url": "https://vi.wikipedia.org/wiki/" + pageTitle, "content": content, "title": pageTitle, "origin": "Group 10"}
                if (len(pages) % 500) == 0:
                    save(pages, len(pages))
                links = getPageLinks(pageTitle, limit, offset)
                if links:
                    for link in links:
                        if link['title'] not in nextTitles:
                            nextTitles.append(link['title'])

        if len(pages) + len(nextTitles) > maxNumPage:
            nextTitles = nextTitles[:(maxNumPage - len(pages))]
        print("Num page: ", len(pages))
        print("Next title: ", nextTitles)

        if len(nextTitles) == 0:
            break
        else:
            baseTitles = nextTitles
            nextTitles = []

getPagesContent("Giáo dục", 20, 10, 2000)