import unittest
from app.models import Comment


class TestComment(unittest.TestCase):
    def setUp(self):
        self.new_comment = Comment(
            id=408765, body='A comment', author_id='Ezekiel Kibiego', post_id=301)

    def tearDown(self):
        Comment.query.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment, Comment))