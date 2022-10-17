" 執行系統命令
" command -nargs=+ R :belowright :terminal ++rows=5 cmd /c <args>
py3 from python_debug import find_testfile, 打包布署

" 程式碼區塊折疊
" set foldmethod=indent
" nnoremap <space> za
" vnoremap <space> zf
command! -buffer ChangeWindow normal <c-w>w
command! -buffer MaxWindow normal <c-w>o

" 佈署至 pypi
func! python#deploy()
    w!
    py3 打包布署()
endfunc
map <buffer> <leader>D :call python#deploy()<cr>

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

" 查詢說明
nnoremap <buffer> K <Cmd>py3 from python_debug import 說明;說明()<cr><c-w>w

" 至定義
nnoremap <buffer> gd <Cmd>py3 from python_debug import 至定義;至定義()<CR>

" 環境設定
map <buffer> <F7> :w!<CR>:belowright :terminal python % --setup<CR>  

" 布署 VIM 模組
map <buffer> <expr> <F8> ":cd " . g:wdriver . ":\\" . g:workdir . "\\vimfiles<CR>:w!<CR>:INV d<CR>" 
