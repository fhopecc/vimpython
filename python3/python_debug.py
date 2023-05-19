from fhopecc.winman import TEMP
from pathlib import Path
import re

def 套件名稱(f):
    from toml import load
    t = load(f)
    return t['project']['name']

def 打包布署():
    import vim
    import os
    cwd = vim.eval("expand('%:p:h')")
    os.system(f'cd {cwd}')
    os.system('del dist\*')
    os.system('py -m build')
    os.system(r'twine upload dist\*')
    n = 套件名稱(Path(cwd) / 'pyproject.toml') 
    os.system(f'python -m pip install {n} -U')
    os.system(f'python -m pip install {n} -U')

def 至():
    from zhongwen.file import FileLocation
    import vim
    line = vim.eval("getline('.')")
    錯誤位置 = FileLocation(line)
    vim.command(f"e +{錯誤位置.列} {錯誤位置.路徑}")

def find_testfile(f:Path, debug=True):
    '依據路徑推論測試檔位置'
    if not isinstance(f, Path): 
        f = Path(f)

    def 是否為中文檔名(檔名):
        from zhongwen.text import 是否為中文字元
        for c in 檔名:
            if 是否為中文字元(c): return True
        return False
    
    測試檔前綴 = '測試' if 是否為中文檔名(f.name) else 'test_' 

    test = f
    pat = 測試檔前綴
    if m:=re.match(pat, test.name) and test.exists():
        return str(test) 

    test = f.parent.parent / 'tests' / f'{測試檔前綴}{f.name}'
    if test.exists(): return str(test) 

    test = f.parent / f'{測試檔前綴}{f.name}'
    if test.exists(): return str(test) 

    test = f.parent / 'tests' / f'{測試檔前綴}{f.name}'
    if test.exists(): return str(test) 

    test = f.parent.parent / f'{測試檔前綴}{f.name}'
    if test.exists(): return str(test) 
     
    test = f.parent / 'test.py'
    if test.exists(): return str(test) 

    test = f.parent.parent / f'{測試檔前綴}{f.parent.name}.py'
    if test.exists(): return str(test) 
    
    raise FileNotFoundError(f'{f.name}尚無測試檔！')

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

def escape_vim_special_chars(text):
    import vim
    escaped_text = vim.eval('escape("' + text + '", "#")')
    return escaped_text

def 說明():
    import vim
    r = 光標物件()
    if r:
        m = r.docstring()
        m = m.split("\n")
        m = [f"'{_m}'" for _m in m]
        m = ','.join(m)
        m = f"[{m}]"
        # print(f"{m!r}")
        # m = escape_vim_special_chars(m)
        vim.command(f"call popup_atcursor({m}, {{}})")
