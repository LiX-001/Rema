# Importing necessary NLTK modules
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

# Other imports
import random
import re
import json
from datetime import datetime
from fuzzywuzzy import fuzz
import pyjokes
import randfacts
import wikipedia
import wolframalpha
from stackapi import StackAPI

wolfram_app_id = "XH5964-PTRJY9XQHX"
stack_overflow_api_key = "gm3f2GloM839EtUdorUT6g(("
conversation_data_file = 'conversation_data.json'

with open(conversation_data_file, 'r') as file:
    conversation_data = json.load(file)

# Apply this code here to initialize NLTK resources
# import nltk
# nltk.download('vader_lexicon')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.download('omw-1.4')

# For simple talking:

# Get synonyms
def synonyms(word):
    synonyms = set()
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            synonym = lemma.name().replace('_', ' ')
            synonyms.add(synonym)
    return synonyms

# Function to preprocess and tokenize text
def preprocess(text):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum()]
    return tokens

# Function to find the most similar pattern
def find_similarity(input_pattern, patterns):
    max_similarity = 0
    matching_pattern = None
    input_tokens = preprocess(input_pattern)
    for pattern in patterns:
        for pattern_input in pattern['input_patterns']:
            pattern_tokens = preprocess(pattern_input)
            pattern_tokens_with_synonyms = set(pattern_tokens)
            for token in pattern_tokens:
                pattern_tokens_with_synonyms.update(synonyms(token))
            common_tokens = set(input_tokens).intersection(pattern_tokens_with_synonyms)
            similarity = len(common_tokens) / (len(input_tokens) + len(pattern_tokens_with_synonyms) - len(common_tokens))
            if similarity > max_similarity:
                max_similarity = similarity
                matching_pattern = pattern
    return matching_pattern

# Functions that don't exist in the original file.
def get_inp(tag):
    patterns = conversation_data['patterns']
    for pattern in patterns:
        if pattern["tag"] == tag:
            return pattern["input_patterns"]
    return None

def talk(input):
    patterns = conversation_data['patterns']
    informations = conversation_data['informations']
    matching_pattern = find_similarity(input.lower(), patterns)
    if matching_pattern:
        out = random.choice(matching_pattern["output_patterns"])
        sub_verb = random.choice(["I am", "Rema is", "I'm"])
        optional_formality = random.choice([", how are you?",", what's up?",", how about you?", ".","!"])
        greeting = random.choice(list(synonyms("hi")))
        farewell = random.choice(list(synonyms("bye")))
        condition = random.choice(["fine","good"] + list(synonyms("joyful")))
        Is = random.choice(informations["is"])
        joke = pyjokes.get_joke('en')
        fact = randfacts.get_fact()
        mid = random.choice(["made","created"] + list(synonyms("built")))
        name = informations["name"]
        creator = str(informations["creator"])
        location = str(informations["location"])
        prefix_a = random.choice(["My name is","I am", "I'm"])
        prefix_b = random.choice(["I was","Rema was"])
        prefix_c = random.choice(["I live","Rema exists","Rema is"])
        joiner = random.choice(["in your","inside your"])
        reply = out.replace("$PREFIX-A",prefix_a).replace("$PREFIX-B",prefix_b).replace("$PREFIX-C",prefix_c).replace("$NAME",name).replace("$FP_SUBJECT+VERB",sub_verb).replace("$GREETING", greeting).replace("$FAREWELL", farewell).replace("$CONDITION", condition).replace("$OPTIONAL_FORMALITY", optional_formality).replace("$IS", Is).replace("$MID", mid).replace("$CREATOR", creator).replace("$JOINER", joiner).replace("$LOCATION", location).replace("$OPTIONAL_LANG", random.choice(('in Python', 'using Python', ''))).replace("$JOKE",  joke).replace("$FACT", fact)
        return reply
    return None

# Fetching informations:

# Function for sentiment recognition.
def feel(query):
    sentiment_analyzer = SentimentIntensityAnalyzer()
    sentiment = sentiment_analyzer.polarity_scores(query)['compound']

    if sentiment == -1.0:
        out = "doleful"
    elif sentiment < 0 and sentiment != -1.0:
        out = "negative"
    elif sentiment == 0:
        out = "neutral"
    elif sentiment > 0 and sentiment != 1.0:
        out = "positive"
    elif sentiment == 1.0:
        out = "exclamatory"
    return random.choice(conversation_data["sentiments"][out])

# Wikipedia Search
def search(query):
    terms = conversation_data["error-handling"]["search"]
    try:
        out = wikipedia.summary(query, sentences=10)
    except Exception as e:
        out = "I " + random.choice(terms["inability"]) + ' ' + random.choice(terms["verbs"]) + ' ' + random.choice(terms["connectors"]) + ' ' + random.choice(terms["indicators"]).replace('$QUERY', '"' + query + '"') + '.'
    return out

# WolframAlpha (Maths solver)
def solve(query):
    terms = conversation_data["error-handling"]["solve"]
    try:
        client = wolframalpha.Client(wolfram_app_id)
        res = client.query(query)
        solution = next(res.results).text
    except Exception as e:
        solution = "$CONJ" + "I " + random.choice(terms["inability"]) + ' ' + random.choice(terms["verbs"]) + ' ' + random.choice(terms["indicators"]).replace('$QUERY', '"' + query + '"') + '.'
    return solution

# Stack overflow
def stack(query):
    terms = conversation_data["error-handling"]["search"]
    try:
        stack_api = StackAPI('stackoverflow', key=stack_overflow_api_key)
        questions = stack_api.fetch('search', intitle=query)
        filtered_results = []
        for result in questions['items']:
            similarity = fuzz.ratio(query, result['title'])
            if similarity > 60:
                filtered_results.append(result)
        answer = random.choice(("If its an issue with coding, you might find solution on - ", "If you're facing issues with code the this should help... - ",
                            "Is that a code issue? Try this - ", "This maybe what you're looking for - ")) + filtered_results[0]['link']
    except Exception as e:
        answer = "$CONJ" + "I " + random.choice(terms["inability"]) + ' ' + random.choice(terms["verbs"]) + ' ' + random.choice(terms["connectors"]) + ' ' + random.choice(terms["indicators"]).replace('$QUERY', '"' + query + '"') + '.'
    return answer

# Main function
def Rema(query, mode):
    tokens = word_tokenize(query)
    tagged_tokens = pos_tag(tokens)
    sentiment = None
    for word, pos in tagged_tokens:
        if pos == 'JJ':
            sentiment = feel(query)
            break
    
    responses = []

    if mode == "manual":
        reply = talk(query)
        if reply:
            responses.append(reply)
    elif mode == "conversation":
        # Expressions to match requests
        solve_synonyms = [syn for word in ["solve", "simplify", "maths", "answer", "what is"] for syn in synonyms(word)]
        solve_pattern = re.compile(r'(?:' + '|'.join(solve_synonyms) + r'|what is|whats) (.+)')
        search_synonyms = [syn for word in ["search", "reffering to", "about","who is", "what is"] for syn in synonyms(word)]
        search_pattern = re.compile(r'(?:' + '|'.join(search_synonyms) + r'|what is(?: about)?|whats(?: about)?|who is(?: about)?|whos(?: about)?) (.+)')
        stackoverflow_synonyms = [syn for word in ["stackoverflow", "coding", "programming", "fix", "error", "resolve", "debug"] for syn in synonyms(word)]
        stackoverflow_pattern = re.compile(r'(?:' + '|'.join(stackoverflow_synonyms) + r'|how to) (.+)')
        
        if bool(solve_pattern.match(query)):
            to_solve = solve_pattern.search(query).groups()[-1]
            solution = solve(to_solve)
            if solution:
                responses.append(solution)
        elif bool(search_pattern.match(query)):
            to_search = search_pattern.search(query).groups()[-1]
            result = search(to_search)
            if result:
                responses.append(result)
        elif bool(stackoverflow_pattern.match(query)):
            to_fix = stackoverflow_pattern.search(query).groups()[-1]
            result = stack(to_fix)
            if result:
                responses.append(result)
        else:
            reply = talk(query)
            if reply:
                responses.append(reply)

    if sentiment:
        responses.append(sentiment)
    out = ' '.join(responses)
    return out if out else random.choice(("I did not catch that...","I am not smart enough to get that.","I is very sorry I not understand that.", "There was an error."))

# Example usage
i = Rema("about Narendra Modi", "conversation")
print(i)
