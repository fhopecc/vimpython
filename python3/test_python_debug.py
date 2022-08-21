import unittest
import os, sys

from pathlib import Path
wdir = Path(__file__).parent

class TestPythonDebug(unittest.TestCase):

    def test_testfile(self):
        from python_debug import testfile
        self.assertEqual(testfile(wdir / r'test_file.py')
                        ,str(wdir / r'test_file.py'))
        
        self.assertEqual(testfile(wdir / 'file.py')
                        ,str(wdir / r'test_file.py'))

        self.assertEqual(testfile(wdir / 'file2.py')
                        ,str(wdir.parent / f'test_{wdir.name}.py' ))


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
    
    def test_parser(self):
        # self.assertEqual('a', 'q')
        from python_debug import traceback_parser, TracebackTransformer
        from python_debug import parse_error_trace
        from pathlib import Path

        parser = traceback_parser()
        wdir = Path(__file__).parent

        errortrace = wdir / 'error1.trace'
        tb = parse_error_trace(errortrace, trans=False)
        # print(tb.pretty())
        self.assertEqual(len(tb.children[0].children), 1)

        testfile2 = wdir / 'error2.trace'
        tb = parse_error_trace(testfile2, trans=False)
        # print(tb.pretty())
        self.assertEqual(len(tb.children[0].children), 1)
        testfile = wdir / 'test.trace'
        tb = parser.parse(testfile.read_text())
        # print(tb.pretty())
        tb = TracebackTransformer().transform(tb)
        # print(tb.locs)
        self.assertEqual(len(tb), 2)
        self.assertEqual(len(tb[0].locs), 3)
        self.assertEqual(tb[0].error[:17], ('FileNotFoundError'))
        self.assertEqual(len(tb[1].locs), 8)
        self.assertEqual(tb[1].error[:21], ('xbrl.TaxonomyNotFound'))
        self.assertEqual(tb[0].todict()[0]['text'][:17], 'FileNotFoundError')
        self.assertEqual(tb[0].locs, 
            [(r"C:\Python\Python310\lib\site-packages\pandas\io\common.py", 798)
            ,(r"C:\Python\Python310\lib\site-packages\pandas\io\pickle.py", 187)
            ,(r"D:\g\fhopecc\cache.py", 30)
            ])

        testfile3 = wdir / 'error3.trace'
        tb = parser.parse(testfile3.read_text())
        # print('error3:')
        # print(tb.pretty())
        tb = TracebackTransformer().transform(tb)
        self.assertEqual(tb[0].locs[2], (r"D:\g\stock\tifrs.py", 52))

        testfile4 = wdir / 'error4.trace'
        tb = parser.parse(testfile4.read_text())
        # print('error4:')
        # print(tb.pretty())
        tb = TracebackTransformer().transform(tb)
        self.assertEqual(tb[1].locs[2], (r"D:\g\fhopecc\cache.py", 32))
        tbs = parse_error_trace(testfile4)
        self.assertEqual(len(tbs), 2)
 
        testfile5 = wdir / 'error5.trace'
        tb = parser.parse(testfile5.read_text())
        # print('error5:')
        # print(tb.pretty())
        tb = TracebackTransformer().transform(tb)
        self.assertEqual(tb[0].locs[0], (r"d:\g\110稅務局徵課會計\地價稅\資訊研析\landtax.py"
                                        ,166))
 
        testfile6 = wdir / 'error6.trace'
        tb = parser.parse(testfile6.read_text())
        # print('error6:')
        # print(tb.pretty())
        tb = TracebackTransformer().transform(tb)
        self.assertEqual(tb[0].locs[0], 
                (r'd:\hlao\8.總決算\110年度\初稿\參考資料\環保基金\參考資料文稿自動產製.py', 8))

        errortrace = wdir / 'error7.trace'
        tb = parse_error_trace(errortrace, trans=False)
        # print('error7:')
        # print(tb.pretty())
        tb = parse_error_trace(errortrace)
        self.assertEqual(len(tb[0].locs), 25)

        errortrace = wdir / 'error8.trace'
        tb = parse_error_trace(errortrace, trans=False)
        print('error8:')
        print(tb.pretty())
        tb = parse_error_trace(errortrace)
        self.assertEqual(len(tb[0].locs), 2)
        self.assertEqual(tb[0].locs[0][0], 'd:\\g\\fhopecc\\test_chinese.py')
        self.assertEqual(tb[0].locs[1][1], 14)

if __name__ == '__main__':
    unittest.main()
