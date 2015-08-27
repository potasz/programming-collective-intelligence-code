import feedparser
import re

ARS_RSS_FEED_URL='http://feeds.arstechnica.com/arstechnica/index'

# Returns title and dictionary of word counts for an RSS feed
def getwordcounts(url):
  # Parse the feed
  d=feedparser.parse(url)
  titles = {}

  # Loop over all the entries
  for e in d.entries:
    # Extract a list of words
    words=getwords(e.title + ' ' + e.content[0]['value'])
    wc = {}
    for word in words:
      wc.setdefault(word,0)
      wc[word]+=1
    titles[e.feedburner_origlink] = wc
  return titles

def getwords(html):
  # Remove all the HTML tags
  txt=re.compile(r'<[^>]+>').sub('',html)

  # Split words by all non-alpha characters
  words=re.compile(r'[^A-Z^a-z]+').split(txt)

  # Convert to lowercase
  return [word.lower() for word in words if word!='']


apcount={}
wordcounts = getwordcounts(ARS_RSS_FEED_URL)
#print wordcounts
for title,wc in wordcounts.items():
  for word,count in wc.items():
    apcount.setdefault(word,0)
    if count>1: apcount[word]+=1

wordlist=[]
for w,bc in apcount.items():
  frac=float(bc)/len(wordcounts.items())
  if frac>0 and frac<0.1:
    wordlist.append(w)

out=file('ars_data.txt','w')
out.write('Title')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for title,wc in wordcounts.items():
  print title
  out.write(title)
  for word in wordlist:
    if word in wc: out.write('\t%d' % wc[word])
    else: out.write('\t0')
  out.write('\n')
