import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from launcher.update.update_installer import UpdateInstaller


class UpdateProceedsWithRealFrozenLayoutTests(unittest.TestCase):
    """A frozen Rose ships its Python code (party/, main/, pengu/) inside
    Rose.exe's PYZ archive, never as loose _internal files. The old
    PROTECTED_PARTY_FILES preservation demanded those loose paths, failed
    closed when they were absent, and aborted every update while protecting
    nothing. An update package shaped like dist/Rose must install."""

    def setUp(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        root = Path(temp_dir.name)
        self.install_dir = root / "install"
        self.extracted_root = root / "staged"
        self.updates_root = root / "updates"
        self.zip_path = root / "update.zip"
        self.staging_dir = root / "staging"
        for directory in (self.install_dir, self.extracted_root, self.updates_root):
            directory.mkdir(parents=True)

        # The real package layout: the executable plus _internal data files,
        # with no party/, main/, or pengu/ .py files on disk.
        exe_name = Path(sys.executable).name
        (self.extracted_root / exe_name).write_bytes(b"fake exe")
        internal = self.extracted_root / "_internal"
        internal.mkdir()
        (internal / "assets").mkdir()
        (internal / "assets" / "icon.png").write_bytes(b"png")
        (internal / "Pengu Loader").mkdir()
        (internal / "Pengu Loader" / "plugins").mkdir()

        self.statuses = []

    def install(self):
        with patch("launcher.update.update_installer.subprocess.Popen") as popen:
            ok = UpdateInstaller().install(
                self.extracted_root,
                self.install_dir,
                self.updates_root,
                self.zip_path,
                self.staging_dir,
                self.statuses.append,
            )
        return ok, popen

    def test_the_update_starts_when_no_protected_paths_exist_on_disk(self):
        ok, popen = self.install()

        self.assertTrue(ok, self.statuses)
        self.assertEqual(popen.call_count, 1)
        self.assertFalse(any("aborted" in status.lower() for status in self.statuses), self.statuses)
        self.assertTrue((self.updates_root / "apply_update.bat").is_file())

    def test_missing_persistent_root_files_are_skipped_not_fatal(self):
        # icon.ico, unins000.exe and unins000.dat are absent here; the
        # persistent loops skip them instead of aborting the update.
        ok, _ = self.install()

        self.assertTrue(ok, self.statuses)


if __name__ == "__main__":
    unittest.main()
