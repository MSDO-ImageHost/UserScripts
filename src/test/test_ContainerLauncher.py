import os
from unittest import TestCase
from ..main.ContainerLauncher import split_name_and_type
from ..main.ContainerLauncher import Container


class TestSplitNameAndType(TestCase):
    def test_one_dot(self):
        input_string = "filename.filetype"
        expected = "filename"
        actual = split_name_and_type(input_string)
        self.assertEqual(expected, actual)

    def test_two_dots(self):
        input_string = "file.name.filetype"
        expected = "file.name"
        actual = split_name_and_type(input_string)
        self.assertEqual(expected, actual)


class TestStartContainer(TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.abspath("README.md"))
        self.volume_path = root_dir + "/src/test/test_scripts"

    def test_container_starter_python(self):
        c = Container(self.volume_path)
        actual = c.container_starter("python", "test.py")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)

    def test_container_starter_java(self):
        c = Container(self.volume_path)
        actual = c.container_starter("java", "test.java")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)

    def test_container_starter_haskell(self):
        c = Container(self.volume_path)
        actual = c.container_starter("haskell", "test.hs")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)

    def test_container_starter_javascript(self):
        c = Container(self.volume_path)
        actual = c.container_starter("javascript", "test.js")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)

    def test_container_starter_invalid_Language(self):
        c = Container(self.volume_path)
        actual = c.container_starter("something that isn't a language", "test.js")
        expected = "Invalid Language"
        self.assertEqual(expected, actual)

    def test_python_container(self):
        c = Container(self.volume_path)
        actual = c.python_container("test.py")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)

    def test_python_container_invalid_file(self):
        c = Container(self.volume_path)
        actual = c.python_container("notAfile.notAtype")
        expected = "File error"
        self.assertEqual(expected, actual)

    def test_java_container(self):
        c = Container(self.volume_path)
        actual = c.java_container("test.java")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)

    def test_java_container_invalid_file(self):
        c = Container(self.volume_path)
        actual = c.java_container("notAfile.notAtype")
        expected = "File error"
        self.assertEqual(expected, actual)

    def test_haskell_container(self):
        c = Container(self.volume_path)
        actual = c.haskell_container("test.hs")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)

    def test_haskell_container_invalid_file(self):
        c = Container(self.volume_path)
        actual = c.haskell_container("notAfile.notAtype")
        expected = "File error"
        self.assertEqual(expected, actual)

    def test_javascript_container(self):
        c = Container(self.volume_path)
        actual = c.javascript_container("test.js")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)

    def test_javascript_container_invalid_file(self):
        c = Container(self.volume_path)
        actual = c.javascript_container("notAfile.notAtype")
        expected = "File error"
        self.assertEqual(expected, actual)
