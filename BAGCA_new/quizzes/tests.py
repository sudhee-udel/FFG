from django.test import TestCase
from quizzes.email_helpers import get_formatted_message

class SmokeTest(TestCase):

    def test_formatted_message(self):
        post_data = {}
        post_data['question_8'] = u'15'
        post_data['question_7'] = u'20'
        post_data['question_6'] = u'23'
        post_data['OP'] = u'SUBMIT'

        message_list, correct, count, = get_formatted_message(post_data, [])

        self.assertEqual(message_list, [])