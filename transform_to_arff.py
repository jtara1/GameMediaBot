import re
import json
from os.path import join, dirname, abspath, basename
from collections import Counter, OrderedDict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import arff
import click


@click.command()
@click.argument('file')
@click.option('--dont-care-category',
              type=click.STRING,
              default='dont_care')
@click.option('-a',
              type=click.INT,
              default=40,
              help='Number of attributes. Attrs are the most frequent words '
                   'in the text of the target category')
def transform(file, dont_care_category, a):
    """input example
    [ {id: 123, text: "this is text body", category: ["dont_care"]} ]
    output example
    @relation game_media_bot

    @attribute

    :return:
    """
    classes = set()
    file = 'SmiteGame_classified_data.json'
    data = json.load(open(file, 'r'))

    master_vector = Counter()
    dont_care_category = 'dont_care'

    for tweet in data:
        classes.add(tweet['category'][0])
        if tweet['category'][0] != dont_care_category:
            master_vector += get_word_vector(tweet)

    print(master_vector)

    # most common words in the text of the target category
    attrs = [(word, 'INTEGER') for word, _ in master_vector.most_common(a)]
    attrs.append(('class', [value for value in classes]))

    arff_data = {
        'attributes': attrs,
        'data': [],
        'description': '',
        'relation': '{}'.format(dont_care_category)
    }

    for tweet in data:
        word_vector = get_word_vector(tweet)
        tweet_data = [word_vector[attr[0]] for attr in attrs[:-1]]
        tweet_data.append(tweet['category'][0])
        arff_data['data'].append(tweet_data)

    out_file = file.replace('.json', '.arff')
    data = arff.dumps(arff_data)
    with open(out_file, 'w') as f:
        f.write(data)


def get_word_vector(tweet):
    stop_words = stopwords.words('english')
    stop_words += ['!', ':', ',', '-', 'https', '/', '\u2026', "'s", "n't",
                   '#', '.', ';', ')', '(', "'re", '&', '?', '%', '@', "'",
                   '...']

    uri = re.compile(r'(https)?:?//t\.co/.*')

    # remove whitespace characters and put each word in a list
    words = word_tokenize(tweet['text'])

    # make each word lowercase
    words = [word.lower() for word in words]

    words = list(
        filter(
            lambda word: word not in stop_words and not uri.match(word),
            words
        )
    )

    return Counter(words)


if __name__ == '__main__':
    transform()
