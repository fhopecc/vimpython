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

        # 中文檔名其測試檔檔名為其檔名前綴【測試】
        test_file = wdir / '測試中文檔.py'
        test_file.touch()
        self.assertEqual(find_testfile(wdir / r'中文檔.py')
                        ,str(wdir / r'測試中文檔.py'))
        test_file.unlink()

        # 檔名前綴為'test_'即為測試檔
        self.assertEqual(find_testfile(wdir / r'test_file.py')
                        ,str(wdir / r'test_file.py'))
        
        # 拉丁文檔名加上前綴'test_'為其測試檔
        # 在同目錄搜尋
        self.assertEqual(find_testfile(wdir / 'file.py')
                        ,str(wdir / f'test_file.py' ))

        # 在父目錄搜尋
        self.assertEqual(find_testfile(wdir / 'file2.py')
                        ,str(wdir.parent / f'test_file2.py' ))

        # 在父目錄搜尋格式為測試前綴目錄名之測試檔
        testpython3 = wdir.parent / 'test_python3.py'
        testpython3.touch()
        self.assertEqual(find_testfile(wdir / 'file3.py')
                        ,str(testpython3))
        testpython3.unlink()


        # test.py 為第二順位測試檔
        testpy = wdir / 'test.py'
        testpy.touch()
        self.assertEqual(find_testfile(wdir / 'file2.py')
                        ,str(wdir.parent / f'test_file2.py'))
        testpy.unlink()
        
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
