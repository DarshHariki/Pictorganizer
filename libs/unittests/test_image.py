from libs import image
import unittest

class test_image(unittest.TestCase):
    def setUp(self):
        self.path1 = "filename.ftype"
        self.path2 = "dir1/filename.ftype"
        self.path3 = "dir2/dir1/filename.ftype"
        self.path4 = "dir1/dir2/"
    def test_image_file_1(self):
        image_file_1 = image.image_file(self.path1)
        assert image_file_1.dirname() == ""

        image_file_2 = image.image_file(self.path2)
        assert image_file_2.dirname() == "dir1"

        image_file_3 = image.image_file(self.path3)
        assert image_file_3.dirname() == "dir2/dir1"

        image_file_4 = image.image_file(self.path4)
        assert image_file_4.dirname() == "dir1/dir2"
    def test_image_file_2(self):
        image_file_1 = image.image_file(self.path1)
        assert image_file_1.filename() == "filename.ftype"

        image_file_2 = image.image_file(self.path2)
        assert image_file_2.filename() == "filename.ftype"

        image_file_3 = image.image_file(self.path3)
        assert image_file_3.filename() == "filename.ftype"

        image_file_4 = image.image_file(self.path4)
        assert image_file_4.filename() == ""

if __name__ == '__main__':
    unittest.main()
