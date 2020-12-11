import os
import unittest
from fortic.fortinet import FortiClient
from unittest.mock import patch


class MyTestCase(unittest.TestCase):

    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    def test_detect_binary_ProgramFiles(self, mock_isdir, mock_isfile, mock_exists):
        expected = os.path.join("C:\\Program Files\\Fortinet\\SslvpnClient", "FortiSSLVPNclient.exe")
        mock_exists.side_effect = lambda path: os.path.normpath(path) == os.path.normpath(expected)
        mock_isfile.side_effect = lambda file: False
        mock_isdir.side_effect = lambda dir: False

        fortinet = FortiClient(None)

        print("Actual: " + fortinet.bin)
        print("Expected: " + expected)
        assert fortinet.bin == expected

    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    def test_detect_binary_ProgramFilesX86(self, mock_isdir, mock_isfile, mock_exists):
        expected = os.path.join("C:\\Program Files (x86)\\Fortinet\\SslvpnClient", "FortiSSLVPNclient.exe")
        mock_exists.side_effect = lambda path: os.path.normpath(path) == os.path.normpath(expected)
        mock_isfile.side_effect = lambda file: False
        mock_isdir.side_effect = lambda dir: False

        fortinet = FortiClient(None)

        print("Actual: " + fortinet.bin)
        print("Expected: " + expected)
        assert fortinet.bin == expected

    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    def test_detect_binary_given_path(self, mock_isdir, mock_isfile, mock_exists):
        expected_dir = "c:\\my\\custom\\path"
        expected = os.path.join(expected_dir, "FortiSSLVPNclient.exe")
        mock_exists.side_effect = lambda path: path is not None and os.path.normpath(path) == os.path.normpath(expected)
        mock_isfile.side_effect = lambda file: False
        mock_isdir.side_effect = lambda dir: os.path.normpath(dir) == os.path.normpath(expected_dir)

        fortinet = FortiClient(expected_dir)

        print("Actual: " + fortinet.bin)
        print("Expected: " + expected)
        assert fortinet.bin == expected

    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    def test_detect_binary_given_file(self, mock_isdir, mock_isfile, mock_exists):
        expected = os.path.join("c:\\my\\custom\\path", "FortiSSLVPNclient.exe")
        mock_exists.side_effect = lambda path: path is not None and os.path.normpath(path) == os.path.normpath(expected)
        mock_isfile.side_effect = lambda file: os.path.normpath(file) == os.path.normpath(expected)
        mock_isdir.side_effect = lambda dir: False

        fortinet = FortiClient(expected)

        print("Actual: " + fortinet.bin)
        print("Expected: " + expected)
        assert fortinet.bin == expected

    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    @patch('shutil.which')
    def test_detect_binary_given_environment_variable(self, mock_which, mock_isdir, mock_isfile, mock_exists):
        expected = "c:\\path\\FortiSSLVPNclient.exe"
        mock_exists.side_effect = lambda path: path is not None and os.path.normpath(path) == os.path.normpath(expected)
        mock_isfile.side_effect = lambda file: False
        mock_isdir.side_effect = lambda dir: False
        mock_which.side_effect = lambda path: expected

        fortinet = FortiClient(None)

        print("Actual: " + fortinet.bin)
        print("Expected: " + expected)
        assert fortinet.bin == expected


if __name__ == '__main__':
    unittest.main()
