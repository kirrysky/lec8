#ny-simple.py
from secrets import *
import requests
from datetime import datetime

now = datetime.now()
sec_since_epoch = now.timestamp()
nyt_key="47ac5d339b324432b83e28d241a1b572"
# gets stories from a particular section of NY times
# on startup, try to load the cache from file
CACHE_FNAME = 'cache_file_name.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def get_stories(section):
    baseurl = 'https://api.nytimes.com/svc/topstories/v2/'
    extendedurl = baseurl + section + '.json'
    params={'api-key': nyt_key}
    #return requests.get(extendedurl, params).json()
    return make_request_using_cache(extendedurl, params)

def get_headlines(nyt_results_dict):
    results = nyt_results_dict['results']
    headlines = []
    for r in results:
        headlines.append(r['title'])
    return headlines



def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        if is_fresh(CACHE_DICTION[unique_ident]): #### THIS IS NEW
            print("Getting cached data...")
            return CACHE_DICTION[unique_ident]
    else:
        pass ## it's a cache miss, fall through to refresh code

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file

    print("Making a request for new data...")
    # Make the request and cache the new data
    resp = requests.get(baseurl, params)
    CACHE_DICTION[unique_ident] = json.loads(resp.text)
    ### THE NEXT LINE IS NEW
    CACHE_DICTION[unique_ident]['cache_timestamp'] = datetime.now().timestamp()
    dumped_json_cache = json.dumps(CACHE_DICTION)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json_cache)
    fw.close() # Close the open file
    return CACHE_DICTION[unique_ident]


MAX_STALENESS = 30 ## 30 seconds--only for lecture demo!
def is_fresh(cache_entry):
    now = datetime.now().timestamp()
    staleness = now - cache_entry['cache_timestamp']
    return staleness < MAX_STALENESS

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

story_list_json = get_stories('science')
headlines = get_headlines(story_list_json)
for h in headlines:
    print(h)
