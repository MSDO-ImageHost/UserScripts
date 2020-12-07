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
    def test_start_python_container(self):
        root_dir = os.path.dirname(os.path.abspath("README.md"))
        volume_path = root_dir + "/src/test/test_scripts"
        c = Container(volume_path)
        actual = c.container_starter("python", "test.py")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)

    def test_start_java_container(self):
        root_dir = os.path.dirname(os.path.abspath("README.md"))
        volume_path = root_dir + "/src/test/test_scripts"
        c = Container(volume_path)
        actual = c.container_starter("java", "test.java")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual.output)

    def test_start_haskell_container(self):
        root_dir = os.path.dirname(os.path.abspath("README.md"))
        volume_path = root_dir + "/src/test/test_scripts"
        c = Container(volume_path)
        actual = c.container_starter("haskell", "test.hs")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)

    def test_start_javascript_container(self):
        root_dir = os.path.dirname(os.path.abspath("README.md"))
        volume_path = root_dir + "/src/test/test_scripts"
        c = Container(volume_path)
        actual = c.container_starter("javascript", "test.hs")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)


class TestPythonContainer(TestCase):
    def test_python_container(self):
        root_dir = os.path.dirname(os.path.abspath("README.md"))
        volume_path = root_dir + "/src/test/test_scripts"
        c = Container(volume_path)
        actual = c.python_container("test.py")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)


class TestJavaContainer(TestCase):
    def test_java_container(self):
        root_dir = os.path.dirname(os.path.abspath("README.md"))
        volume_path = root_dir + "/src/test/test_scripts"
        c = Container(volume_path)
        actual = c.java_container("test.java")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual.output)


class TestHaskellContainer(TestCase):
    def test_haskell_container(self):
        root_dir = os.path.dirname(os.path.abspath("README.md"))
        volume_path = root_dir + "/src/test/test_scripts"
        c = Container(volume_path)
        actual = c.haskell_container("test.hs")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)


class TestJavascriptContainer(TestCase):
    def test_javascript_container(self):
        root_dir = os.path.dirname(os.path.abspath("README.md"))
        volume_path = root_dir + "/src/test/test_scripts"
        c = Container(volume_path)
        actual = c.javascript_container("test.js")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)
