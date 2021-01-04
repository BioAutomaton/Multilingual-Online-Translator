import argparse

import requests
from bs4 import BeautifulSoup


def translate(request):
    """
    Parse BS4 request for translation and examples and return those items.

    :type request: BeautifulSoup.request
    :return: translation: list, examples: list of tuples
    """
    soup = BeautifulSoup(request.content, 'html.parser')

    translations = soup.find_all('a', {'class': 'translation'})
    examples_src = soup.find_all('div', {'class': 'src'})
    examples_trg = soup.find_all('div', {'class': 'trg'})

    translations = [translation.text.strip() for translation in translations[1:]]
    examples = []
    for i in range(len(examples_src)):
        examples.append((examples_src[i].text.replace('\n', '').strip(),
                         examples_trg[i].text.replace('\n', '').strip()))
    return translations, examples


def print_translation(translations, examples, quantity=5):
    print(f"\n{target_language.capitalize()} translations:")
    for i in range(len(translations) if len(translations) < quantity else quantity):
        print(translations[i])

    print(f"\n{target_language.capitalize()} examples:")
    for i in range(len(examples) if len(examples) < quantity else quantity):
        print(*examples[i], sep='\n')


def write_to_file(file, translations, examples, quantity=5):
    file.write(f"\n{target_language.capitalize()} translations:\n")
    for i in range(len(translations) if len(translations) < quantity else quantity):
        file.write(translations[i] + '\n')

    file.write(f"\n{target_language.capitalize()} examples:\n")
    for i in range(len(examples) if len(examples) < quantity else quantity):
        file.write('\n'.join(examples[i]) + '\n')


SUPPORTED_LANGUAGES = {
    '1': 'arabic',
    '2': 'german',
    '3': 'english',
    '4': 'spanish',
    '5': 'french',
    '6': 'hebrew',
    '7': 'japanese',
    '8': 'dutch',
    '9': 'polish',
    '10': 'portuguese',
    '11': 'romanian',
    '12': 'russian',
    '13': 'turkish'
}
SERVICE_URL = "https://context.reverso.net/translation"
USER_AGENT = "Mozilla/5.0"

parser = argparse.ArgumentParser(description='This program takes exactly 3 arguments.'
                                             'source_language, target_language '
                                             '(optionally all) and a word to translate')
parser.add_argument('source')
parser.add_argument('target')
parser.add_argument('word')

args = parser.parse_args()
source_language = ""
target_languages = []
word = args.word

if args.source in SUPPORTED_LANGUAGES.values():
    source_language = args.source
else:
    print("Sorry, the program doesn't support", args.source)
    exit()



if args.target == "all":
    target_languages = list(SUPPORTED_LANGUAGES.values())
    target_languages.remove(source_language)
elif args.target in SUPPORTED_LANGUAGES.values():
    target_languages = [args.target]
else:
    print("Sorry, the program doesn't support", args.target)
    exit()

for target_language in target_languages:
    url = f"{SERVICE_URL}/{source_language}-{target_language}/{word}"
    r = requests.get(url, headers={'User-Agent': USER_AGENT})
    if r:
        file = open(f'{word}.txt', 'a', encoding='utf-8')
        examples_quantity = 1 if len(target_languages) > 1 else 5
        translations, examples = translate(r)
        print_translation(translations, examples, quantity=examples_quantity)
        write_to_file(file, translations, examples, quantity=examples_quantity)
        file.close()
    elif r.status_code == 404:
        print("Sorry, unable to find", word)
        file.close()
        exit()
    else:
        print("Something wrong with your internet connection")
        file.close()
        exit()
