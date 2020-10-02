from stackapi import StackAPI
import datetime
import random
import enum
from bs4 import BeautifulSoup
import random

StackOverflowApi = StackAPI('stackoverflow')
StackOverflowApi.page_size = 50
StackOverflowApi.max_pages = 1

class SelectionStrategy(enum.Enum):
    VOTES = enum.auto()
    RANDOM = enum.auto()

    @staticmethod
    def from_str(name: str) -> 'SelectionStrategy':
        return getattr(SelectionStrategy, name.strip().upper())


def find(keyword, selection_strategy=SelectionStrategy.VOTES, safety_date=None):
    # TODO use the selection strategy to order answers
    question_options = {
        'order': 'desc',
        'sort': 'relevance',
        'q': keyword,
        'nottagged': 'python-2.x',
        'tagged': ['python', 'sorting'],
        'filter': '!b93xdWqUwqOO7m'
    }
    answer_options = {
        'order': 'desc',
        'sort': 'votes',
        'filter': '-XG6tqDiasfBQHS1'
    }
    if safety_date:
        question_options['todate'] = safety_date
        answer_options['todate'] = safety_date

    question_search = { 'has_more': True }
    answer_search = { 'has_more': True }

    question_page = 1
    while question_search.get('has_more', False):
        question_search = StackOverflowApi.fetch('search/advanced', page=question_page, **question_options)
        question_page = question_search['page']+1

        ids = [ item['question_id'] for item in question_search['items'] if item['is_answered'] ]

        answer_page = 1
        while answer_search.get('has_more', False):
            answer_search = StackOverflowApi.fetch('questions/{ids}/answers', ids=ids, page=answer_page, **answer_options)
            answer_page = answer_search['page']+1

            if selection_strategy is SelectionStrategy.RANDOM:
                random.shuffle(answer_search['items'])

            for answer in answer_search['items']:
                if safety_date:
                    edit_date = datetime.datetime.fromtimestamp(answer.get('last_edit_date', 0))
                    if edit_date > safety_date:
                        continue
                soup = BeautifulSoup(answer['body'], features="lxml")
                for pre in soup.find_all('pre'):
                    for code in pre.findChildren('code'):
                        yield code.text
