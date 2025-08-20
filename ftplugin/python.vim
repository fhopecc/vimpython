py3 from zhongwen.python_dev import find_testfile

command! -buffer ChangeWindow normal <c-w>w
command! -buffer MaxWindow normal <c-w>o

" 查詢名稱說明
nnoremap <buffer> K <Cmd>py3 from zhongwen.python_dev import 說明;說明()<cr>

" 查找函數
map <leader>c :set noimdisable<cr>:Leaderf function<cr>

" 至定義
nnoremap <buffer> gd <Cmd>py3 from zhongwen.python_dev import 至定義;至定義()<CR>

" 執行
func! python#execute()
    w!
    let term_opt = {"close_cb": "python#done"}
    MaxWindow
    call term_start('python '.expand('%'), term_opt)
endfunc

map <buffer> <leader>e :call python#execute()<cr>

" 交談式介面實驗
map <buffer> <leader>i :term ipython

func! python#nextterm()
    let name = bufnr('#')
    return name
endfunc

" 測試
func! python#test()
    w!
    let testfile = py3eval("find_testfile(r'".expand('%')."')")
    let term_opt = {"close_cb": "python#done"}
    MaxWindow
    call term_start('python '.testfile, term_opt)
endfunc
map <buffer> <leader>t :call python#test()<cr>

func! python#done(job)
    set filetype=pythontrace
endfunc

" 效能
func! python#profile()
    w!
    topleft :terminal ++rows=10 cmd /c py -m cProfile -s cumtime %
endfunc
map <buffer> <leader>P :call python#profile()<cr>

" 打包佈署
func! python#deploy()
    w!
    py3 << EOF
import vim
from zhongwen.python_dev import 布署
from pathlib import Path
布署(Path(vim.current.buffer.name))
EOF
endfunc
map <buffer> <leader>D :call python#deploy()<cr>

" 環境設定
map <buffer> <F7> :w!<CR>:belowright :terminal python % --setup<CR>  
