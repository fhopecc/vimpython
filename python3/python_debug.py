from lark import Lark, Transformer, Token
from pathlib import Path
from fhopecc.winman import TEMP
import re

TRACE = TEMP / 'error.trace' 
OUTPUT = TEMP / 'output.trace' 

def 清除紀錄檔():
    TRACE.unlink()
    OUTPUT.unlink()

def parse_error_trace(file=TRACE, trans=True):
    trace = file.read_text()
    if len(trace) == 0:
        return []
    tb = traceback_parser().parse(trace)
    if trans:
        tb = TracebackTransformer().transform(tb)
    return tb

def tracebacktoqflist():
    import vim
    # wdir = Path(__file__).parent
    # trace = TRACE.read_text()
    try:
        tbs = parse_error_trace()
        if len(tbs) > 0:
            f = vim.Function('setqflist')
            msg = []
            from itertools import chain
            tbs.reverse()
            msg += list(chain(*[tb.todict() for tb in tbs]))
            msg += [{'text':line} for line in OUTPUT.read_text().splitlines()]
            f(msg)
    except Exception as e: 
        # raise e
        f = vim.Function('setqflist')
        import traceback
        s = traceback.format_exception(e)
        s += TRACE.read_text().splitlines()
        t = OUTPUT.read_text().splitlines()
        f([{'text':line} for line in s+t])
        
def traceback_parser():
    grammar = r'''
traceback: _TH loc+ ERR
loc: (LOC|LOC_SE) ERRCODE*
_TH.2: /Traceback \(most recent call last\):/
LOC.2: /  File "([^"\s]+)", line (\d+), in [^\n]+/
ERRCODE.2: /    [^\n]+/
_L: /[^\n]+/
ERR.2: /[^\n:]+(Error|Exception|NotFound):[^\n]+/
syntaxerror: LOC_SE ERRCODE+ ERR
LOC_SE: /  File "([^"\s]+)", line (\d+)/ //location for SyntaxError
tracebacks: (syntaxerror| traceback | _L)+
start: tracebacks
%import common.INT
%import common.NEWLINE
%ignore NEWLINE
'''
    return Lark(grammar, lexer='basic')

def 定位資訊(loc):
    '解析定位資訊，包含檔案路徑加行號'
    # Token LOC
    pat = r'  File "([^"\s]+)", line (\d+), in [^\n]+'
    if m:=re.match(pat, loc):
        return (m[1],  int(m[2]))
    # Token LOCSE
    pat = r'  File "([^"\s]+)", line (\d+)'
    if m:=re.match(pat, loc):
        return (m[1],  int(m[2]))
    return loc

class Traceback(object):
    def __init__(self, locs, error):
        self.locs = locs
        self.error = error
    def todict(self):
        locs = self.locs
        locs.reverse()
        # print(f'locs:{locs}')
        return [{'filename': fn, 'lnum': lnum, 'text':self.error} 
                for fn, lnum in locs]

class TracebackTransformer(Transformer):
    def start(self, tbs):
        return tbs[0]

    def tracebacks(self, tbs):
        return tbs

    def traceback(self, tks):
        # print(f'locs0:{tks}')
        locs = [定位資訊(t) for t in tks[0:-1]]
        # print(f'locs-1:{tks[-1]}')
        return Traceback(locs, tks[-1].value)

    def syntaxerror(self, tks):
        LOC_SE = tks[0]
        pat = r'  File "([^"\s]+)", line (\d+)'
        if m:=re.match(pat, LOC_SE):
            loc = (m[1], int(m[2])) 
        ERR = tks[-1].value
        return Traceback([loc], ERR)

    def loc(self, tks):
        loc = tks[0].value
        return loc

# IndexError: list index out of range
class ErrorPosition(object):
    def __init__(self, 訊息):
        模式 = r'.*File "(.+.py)", line (\d+).*'
        import re 
        if m:=re.match(模式, 訊息):
            self.路徑 = m[1]
            self.行號 = int(m[2])
            return

        模式 = r'(.*\.py):(\d+):.*'
        if m:=re.match(模式, 訊息):
            self.路徑 = m[1]
            self.行號 = int(m[2])
            return
        
        模式 = r'.*: (.+\.js):.*\((\d+):.+\).*'
        if m:=re.match(模式, 訊息):
            self.路徑 = m[1]
            self.行號 = int(m[2])
            return
        
        模式 = r'.+\((.+\.js):(\d+):.*'
        if m:=re.match(模式, 訊息):
            self.路徑 = m[1]
            self.行號 = int(m[2])
            return

def 至():
    import vim
    line = vim.eval("getline('.')")
    錯誤位置 = ErrorPosition(line)
    #print(f"e +{錯誤位置.行號} {錯誤位置.路徑}")
    vim.command(f"e +{錯誤位置.行號} {錯誤位置.路徑}")

def 測試():
    from pathlib import Path
    路徑 = Path(vim.current.buffer.name)
    import os
    vim.command(f"R {路徑.with_name(f'test_{路徑.name}')}")

def 光標物件():
    '光標處Python物件'
    import vim, jedi
    f = vim.eval("expand('%')")
    c = '\n'.join(vim.current.buffer)
    script = jedi.Script(code=c, path=f)
    _a, l, c, _a, _a = map(lambda s: int(s), vim.eval('getcursorcharpos()'))
    try:
        return script.goto(l, c, follow_imports=True)[0]
    except IndexError: None

def 至定義():
    '至光標處Python物件之定義'
    import vim
    r = 光標物件()
    if r:
        p = r.module_path
        l = r.line
        c = r.column
        vim.command(f"e +{l} {p}")

def 說明():
    import vim
    r = 光標物件()
    if r:
        from fhopecc.winman import TEMP
        docfile = TEMP / '__doc__' 
        docfile.write_text(r.docstring(), encoding='utf8')
        vim.command(f":belowright :split {docfile}")
        vim.command(f"set ft=pydoc")

if __name__ == '__main__':
    import jedi, fhopecc.env
    from pathlib import Path
    f = Path(r'D:\g\110稅務局徵課會計\地價稅\資訊研析\landtax.py')
    script = jedi.Script(path=str(f))
    s = script.goto(35, 13)[0]
    print(s.module_path)
