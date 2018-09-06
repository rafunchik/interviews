from unittest import TestCase
from io import StringIO
from unittest import mock
from hashtags.main import print_hashtags


class TestPrintHashtags(TestCase):

    def test_print_hashtags(self):
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            print_hashtags('../testdocs', 3)
            self.assertIn("us 87", fake_out.getvalue())
            self.assertIn("doc6.txt: We entered through no fences or discernible security, and once we did, we found "
                          "ourselves in a building with open first-floor windows and padlocks that many of us would "
                          "not use to secure our own luggage.", fake_out.getvalue())
            self.assertIn("doc1.txt: Each of us, in our own lives, will have to accept responsibility - for instilling "
                          "an ethic of achievement in our children, for adapting to a more competitive economy, for "
                          "strengthening our communities, and sharing some measure of sacrifice.", fake_out.getvalue())
            self.assertIn("iraq 63", fake_out.getvalue())
            self.assertIn("doc2.txt: Let us keep that promise - that American promise - and in the words of Scripture "
                          "hold firmly, without wavering, to the hope that we confess.", fake_out.getvalue())


