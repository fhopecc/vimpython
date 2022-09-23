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
    n = 套件名稱(Path(cwd).parent / 'pyproject.toml') 
    os.system(f'python -m pip install {n} -U')

def 至():
    from zhongwen.file import FileLocation
    import vim
    line = vim.eval("getline('.')")
    錯誤位置 = FileLocation(line)
    vim.command(f"e +{錯誤位置.列} {錯誤位置.路徑}")

def testfile(f:Path, debug=True):
    '依據路徑推論測試檔位置'
    if not isinstance(f, Path): 
        f = Path(f)

    test = f.parent / f'test_{f.name}'
    if test.exists(): return str(test) 
     
    pat = r'test_'
    if m:=re.match(pat, f.name):
        test = f
    if test.exists(): return str(test) 

    test = f.parent / 'test.py'
    if test.exists(): return str(test) 

    test = f.parent.parent / f'test_{f.parent.name}.py'
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

def 說明():
    import vim
    r = 光標物件()
    if r:
        docfile = TEMP / '__doc__' 
        docfile.write_text(r.docstring(), encoding='utf8')
        vim.command(f":belowright :split {docfile}")
        vim.command(f"set ft=pydoc")
