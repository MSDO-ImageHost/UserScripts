import os
from unittest import TestCase

import docker.types

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

    def test_prune_networks(self):
        client = docker.from_env()
        ipam_pool = docker.types.IPAMPool(subnet='120.42.0.0/16', iprange='120.42.0.0/8')
        ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
        client.networks.create("test_network", ipam=ipam_config)
        c = Container(self.volume_path)
        actual = c.prune_networks("test_network")
        expected = 1
        self.assertEqual(expected, actual)

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
        expected = b"python: can't open file '//mnt/src/notAfile.notAtype': [Errno 2] No such fil"b'e or directory\n'
        self.assertEqual(expected, actual)

    def test_python_container_restrict_internet_access(self):
        c = Container(self.volume_path)
        actual = c.python_container("webaccess.py")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)

    def test_java_container(self):
        c = Container(self.volume_path)
        actual = c.java_container("test.java")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)

    def test_java_container_invalid_file(self):
        c = Container(self.volume_path)
        actual = c.java_container("notAfile.notAtype")
        expected = b"error: Class names, 'notAfile.notAtype', are only accepted if annotation pro"b'cessing is explicitly requested\n1 error\n'
        self.assertEqual(expected, actual)

    def test_haskell_container(self):
        c = Container(self.volume_path)
        actual = c.haskell_container("test.hs")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)

    def test_haskell_container_invalid_file(self):
        c = Container(self.volume_path)
        actual = c.haskell_container("notAfile.notAtype")
        expected = (b"Warning: ignoring unrecognised input `mnt/src/notAfile.notAtype'\n\nmnt/sr"b"c/notAfile.notAtype:1:53:\n    Not in scope: `main'\n    Perhaps you meant"b" `min' (imported from Prelude)\n")
        self.assertEqual(expected, actual)

    def test_javascript_container(self):
        c = Container(self.volume_path)
        actual = c.javascript_container("test.js")
        expected = b'Hello, World!\n'
        self.assertEqual(expected, actual)

    def test_javascript_container_invalid_file(self):
        c = Container(self.volume_path)
        actual = c.javascript_container("notAfile.notAtype")
        expected = (b'node:internal/modules/cjs/loader:922\n  throw err;\n  ^\n\nError: Cannot fin'b"d module '/mnt/src/notAfile.notAtype'\n    at Function.Module._resolveFil"b'ename (node:internal/modules/cjs/loader:919:15)\n    at Function.Module._'b'load (node:internal/modules/cjs/loader:763:27)\n    at Function.executeUs'b'erEntryPoint [as runMain] (node:internal/modules/run_main:76:12)\n    at 'b"node:internal/main/run_main_module:17:47 {\n  code: 'MODULE_NOT_FOUND',\n "b' requireStack: []\n}\n')
        self.assertEqual(expected, actual)
