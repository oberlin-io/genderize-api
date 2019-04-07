# To call http://genderize.io API
# 1000 name per day limit. Check header info for current count. See docs.
# This wrapper written by John Oberlin | github.com/oberljn

import requests as r
import json

# Names list
raw_names = """Caroline
Carrie
Carrie
Cathy"""

raw_names = raw_names.split("\n")

# Dedupe list to not waste API calls
names = []
for n in raw_names:
  if n not in names:
    names.append(n)

print("Names to run: " + str(len(names)))

# Split names list into groups of 10 in an array: [ [a,b,..j], [a,b,..j], [a] ]
name_groups = []
sub = []
limit = 9

for n in names:
  ndx = names.index(n)
  
  if ndx == limit:
    sub.append(n)
    name_groups.append(sub)
    sub = []
    limit += 10
    
  else:
    sub.append(n)
    
    if ndx == len(names) - 1:
      name_groups.append(sub)

# Check array output
#for g in name_groups:
#  print(str(len(g)) + ": " + str(g),)

# Build query URLs
# If names list not dedupes, will causing index error
urls = []

for g in name_groups:
  url = "https://api.genderize.io/?"

  for n in g:
    ndx = g.index(n)

    if ndx < 10:
      query = "name[%s]=%s&" % (ndx, n.replace(" ", "%20"))
      url += query

    else:
      break

  url += "country_id=us"
  urls.append(url)

# Check URL output
#for u in urls:
#  print(u)

# Call API and append to results list
results = []

for u in urls:
  got = r.get(u) #.json()
  got = json.loads(got.text)
  for g in got:
    results.append(g)
  #break                        # for testing

# Print as tab-separated text
for res in results:
  try:
    print(res["name"] + "\t" + res["gender"] + "\t" + str(res["probability"]) )
  except:
    print(res["name"] + "\t" + "Error" + "\t" + "Error")
