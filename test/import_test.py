import unittest
import jupyter_module_loader

jupyter_module_loader.register(tags=["export"])

import nb.load as x



class TestTemplateFileHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    def test_tagged(self):
        self.assertEqual("tagged",x.tagged())

    def test_untagged(self):
        with self.assertRaises(AttributeError) as context:
            x.untagged

