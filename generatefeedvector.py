#!/usr/bin/python

import feedparser
import re

def getwordcounts(url):
    print 'Getting word counts for feed URL %s' % url
    # Parse the feed
    data = feedparser.parse(url)
    wc = {}

    # Loop over all the entries
    for entry in data.entries:
        # print '    Examining entry %s' % entry
        if 'summary' in entry: summary = entry.summary
        else: summary = entry.description

        # Extract a list of words
        if not hasattr(entry, 'title'):
            print 'Entry does not have a title'
            setattr(entry, 'title', 'DEFAULT TITLE')
        else:
            print('Entry has a title')

        words = getwords(entry.title + ' ' + summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1

    return data.feed.title, wc

def getwords(html):
    # Remove all the HTML tags
    txt = re.compile(r'<[^>]+>').sub('', html)

    # Split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    # Convert to lower case
    return [word.lower() for word in words if word != '']

apcount = {}
wordcounts = {}
feedlist = []
for feedurl in file('feedlist.txt'):
    feedlist.append(feedurl)
    title, wc = getwordcounts(feedurl)
    wordcounts[title] = wc
    for word, count in wc.items():
        apcount.setdefault(word, 0)
        if count > 1:
            apcount[word] += 1

    wordlist = []
    for w, bc in apcount.items():
        frac = float(bc) / len(feedlist)
        if frac > 0.1 and frac < 0.5: wordlist.append(w)

    out = file('blogdata.txt', 'w')
    out.write('Blog')
    for word in wordlist:
        out.write('\t%s' % word)
    out.write('\n')
    for blog, wc in wordcounts.items():
        # Deal with unicode outside the ASCII range
        blog = blog.encode('ascii', 'ignore')
        out.write(blog)
        for word in wordlist:
            if word in wc:
                out.write('\t%d' % wc[word])
            else:
                out.write('\t0')
        out.write('\n')
