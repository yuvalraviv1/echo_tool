import unittest
from echo_tool import echo_tool

class TestEchoTool(unittest.TestCase):
    def test_echo_tool(self):
        self.assertEqual(echo_tool("test"), "t e s t")
        self.assertEqual(echo_tool("123"), "1 2 3")
        self.assertEqual(echo_tool(""), "")
        self.assertEqual(echo_tool("test string"), "t e s t   s t r i n g")

if __name__ == '__main__':
    unittest.main()