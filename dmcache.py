#datamuse-caching
import requests
import json

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

# A helper function that accepts 2 parameters
# and returns a string that uniquely represents the request
# that could be made with this info (url + params)
def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

# The main cache function: it will always return the result for this
# url+params combo. However, it will first look to see if we have already
# cached the result and, if so, return the result from cache.
# If we haven't cached the result, it will get a new one (and cache it)
def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

# Gets data from the datamuse API, using the cache
def get_rhymes_from_datamuse_caching(rhymes_with):
    baseurl = "https://api.datamuse.com/words"
    params_diction = {}
    params_diction["rel_rhy"] = rhymes_with
    return make_request_using_cache(baseurl, params_diction)

# extract just the words from the data structures returned by datamuse
def get_word_list(data_muse_word_list):
    words = []
    for word_dict in data_muse_word_list:
        words.append(word_dict['word'])
    return words

# print up to 'max_rhymes' words that rhyme with 'word'
def print_rhymes(word, max_rhymes=10):
    rhymes = get_word_list(get_rhymes_from_datamuse_caching(word))
    print('Words that rhyme with', word)
    max2print = min(max_rhymes, len(rhymes))
    for i in range(max2print):
        print('\t', rhymes[i])

print_rhymes('blue')
print_rhymes('green')
print_rhymes('purple')
