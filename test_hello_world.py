import unittest
from io import StringIO
from unittest.mock import patch

from hello_world import hello_world

class TestHelloWorld(unittest.TestCase):
    def test_hello_world_output(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            hello_world()
            self.assertEqual(fake_out.getvalue().strip(), 'hello world')

if __name__ == '__main__':
    unittest.main()
