from pathlib import Path
import unittest
import os, sys
wdir = Path(__file__).parent

class TestPythonDebug(unittest.TestCase):
    def setUp(self):
        test_file = wdir / 'test_file.py'
        test_file.touch()
        self.test_file = test_file

        test_file2 = wdir.parent / 'test_file2.py'
        test_file2.touch()
        self.test_file2 = test_file2

    def test_deploy(self):
        from python_debug import 套件名稱
        self.assertEqual(套件名稱(wdir / 'pyproject.toml'), 'zhongwen')

    def test_find_testfile(self):
        from python_debug import find_testfile
        wdir = Path(__file__).parent

        # 檔名前綴為'test_'即為測試檔
        self.assertEqual(find_testfile(wdir / r'test_file.py')
                        ,str(wdir / r'test_file.py'))
        
        # 檔名加上前綴'test_'為其測試檔
        # 在同目錄或父目錄搜尋
        self.assertEqual(find_testfile(wdir / 'file.py')
                        ,str(wdir / f'test_file.py' ))

        self.assertEqual(find_testfile(wdir / 'file2.py')
                        ,str(wdir.parent / f'test_file2.py' ))

        testpy = wdir / 'test.py'
        testpy.touch()
        self.assertEqual(find_testfile(wdir / 'file2.py')
                        ,str(wdir.parent / f'test_file2.py'))
        testpy.unlink()
        
        testpython3 = wdir.parent / 'test_python3.py'
        testpython3.touch()
        self.assertEqual(find_testfile(wdir / 'file3.py')
                        ,str(testpython3))
        testpython3.unlink()

    def tearDown(self):
        self.test_file.unlink()
        self.test_file2.unlink()
        
    # def test_至定義(self):
        # code = '''from stock.tifrs_schema import 科目表
        # w = 科目表()
        # '''
        # from jedi import Script
        # import fhopecc.env as env
        # s = Script(code=code, path='test.py')
        # gs = s.goto(2, 6, follow_imports=True)
        # self.assertGreater(len(gs), 0)
        # self.assertEqual(gs[0].module_path, env.workdir / 'stock' / 'tifrs_schema.py')
    
if __name__ == '__main__':
    unittest.main()
