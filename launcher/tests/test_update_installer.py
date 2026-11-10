import tempfile
import unittest
from pathlib import Path

from launcher.update.update_installer import PROTECTED_PARTY_FILES, UpdateInstaller


class ProtectedPartyUpdateTests(unittest.TestCase):
	def test_preserve_paths_replaces_staged_private_files_and_directories(self):
		with tempfile.TemporaryDirectory() as temp_dir:
			root = Path(temp_dir)
			install_dir = root / "install"
			extracted_root = root / "staged"
			install_dir.mkdir()
			extracted_root.mkdir()

			for relative_name in PROTECTED_PARTY_FILES:
				source = install_dir / relative_name
				target = extracted_root / relative_name
				if relative_name.endswith(("party", "ROSE-PartyMode")):
					source.mkdir(parents=True)
					target.mkdir(parents=True)
					(source / "private.txt").write_text("private", encoding="utf-8")
					(target / "upstream.txt").write_text("upstream", encoding="utf-8")
				else:
					source.parent.mkdir(parents=True, exist_ok=True)
					target.parent.mkdir(parents=True, exist_ok=True)
					source.write_text("private", encoding="utf-8")
					target.write_text("upstream", encoding="utf-8")

			ok = UpdateInstaller._preserve_paths(
				install_dir,
				extracted_root,
				PROTECTED_PARTY_FILES,
				lambda _: None,
			)

			self.assertTrue(ok)
			self.assertEqual((extracted_root / "_internal/party/private.txt").read_text(encoding="utf-8"), "private")
			self.assertEqual(
				(extracted_root / "_internal/Pengu Loader/plugins/ROSE-PartyMode/private.txt").read_text(encoding="utf-8"),
				"private",
			)
			self.assertEqual(
				(extracted_root / "_internal/main/__init__.py").read_text(encoding="utf-8"),
				"private",
			)

	def test_preserve_paths_fails_if_a_private_path_is_missing(self):
		with tempfile.TemporaryDirectory() as temp_dir:
			root = Path(temp_dir)
			install_dir = root / "install"
			extracted_root = root / "staged"
			install_dir.mkdir()
			extracted_root.mkdir()

			self.assertFalse(
				UpdateInstaller._preserve_paths(
					install_dir,
					extracted_root,
					("party",),
					lambda _: None,
				)
			)


if __name__ == "__main__":
	unittest.main()
