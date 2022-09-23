from pathlib import Path
import unittest
import os, sys
wdir = Path(__file__).parent

class TestPythonDebug(unittest.TestCase):
    def setUp(self):
        test_file = wdir / 'test_file.py'
        test_file.touch()
        self.test_file = test_file
        
    def test_testfile(self):
        from python_debug import testfile
        wdir = Path(__file__).parent

        self.assertEqual(testfile(wdir / r'test_file.py')
                        ,str(wdir / r'test_file.py'))
        
        self.assertEqual(testfile(wdir / 'file.py')
                        ,str(wdir / f'test_file.py' ))

        testpy = wdir / 'test.py'
        testpy.touch()
        self.assertEqual(testfile(wdir / 'file2.py')
                        ,str(wdir / f'test.py'))
        testpy.unlink()
        
        testpython3 = wdir.parent / 'test_python3.py'
        testpython3.touch()
        self.assertEqual(testfile(wdir / 'file2.py')
                        ,str(testpython3))
        testpython3.unlink()

    def tearDown(self):
        self.test_file.unlink()
        
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
