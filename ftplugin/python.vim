" 執行系統命令
" command -nargs=+ R :belowright :terminal ++rows=5 cmd /c <args>

py3 from python_debug import testfile

" 程式碼區塊折疊
set foldmethod=indent
nnoremap <space> za
vnoremap <space> zf
command! ChangeWindow normal <c-w>w
command! MaxWindow normal <c-w>o

" 佈署至 pypi
func! python#deploy()
    w!
    let dir = expand('%:h')
    !py -m build
    !del dist\*
    call term_start('twine upload dist\*')
endfunc
map <buffer> ;d :call python#deploy()<cr>

" 執行
func! python#execute()
    w!
    let term_opt = {"close_cb": "python#done"}
    MaxWindow
    call term_start('python '.expand('%'), term_opt)
endfunc

" 交談式介面實驗
map <buffer> ;i :term ipython

func! python#nextterm()
    let name = bufnr('#')
    return name
endfunc

func! python#done(job)
    set filetype=pythontrace
endfunc

func! python#execute2()
    w!
    let file = expand('%')
     " todo: 檢核檔案是否存在
    py3 from python_debug import TRACE, OUTPUT, 清除紀錄檔
    py3 清除紀錄檔
    call setqflist([], 'r')
    let output = py3eval('str(OUTPUT)')
    let trace = py3eval('str(TRACE)')
    let job = job_start("cmd /c py ".file." >".output." 2>".trace, {"close_cb": "python#done"})
endfunc
map <buffer> ;e :call python#execute()<cr>

function! python#done2(job)
    py3 from python_debug import tracebacktoqflist;tracebacktoqflist()
    if !empty(getqflist())
        cc
    else
        py3 from python_debug import TRACE, OUTPUT
        let output_size =  py3eval('OUTPUT.stat().st_size')
        let error_size =  py3eval('TRACE.stat().st_size')
        if output_size == 0 && error_size == 0
            echom '沒有輸出'
            return
        endif
        let output = py3eval('str(OUTPUT)')
        let trace = py3eval('str(TRACE)')
        let cmd = ':botright :12split '.output
        execute(cmd)
        let cmd = ':read '.trace
        execute(cmd)
        execute(':w')
    endif 
endfunction

" 測試
func! python#test()
    w!
    " let cmd = "topleft :terminal ++rows=10 python "
    let testfile = py3eval("testfile(r'".expand('%')."')")
    let term_opt = {"close_cb": "python#done"}
    MaxWindow
    call term_start('python '.testfile, term_opt)
endfunc
map <buffer> ;t :call python#test()<cr>

func! python#test2()
    w!
    let file = expand("%:h") . "\\test_" . expand("%:t")

    py3 from python_debug import OUTPUT, TRACE
    let output = py3eval('str(OUTPUT)')
    let trace = py3eval('str(TRACE)')
    let cmd = "cmd /c py ".file." >".output." 2>".trace
    let job = job_start(cmd, {"close_cb": "python#done"})
endfunc

" 測試效能
func! python#profile()
    w!
    topleft :terminal ++rows=10 cmd /c py -m cProfile -s time %
endfunc
map <buffer> ;P :call python#profile()<cr>

" 查詢說明
nnoremap <buffer> K <Cmd>py3 from python_debug import 說明;說明()<cr><c-w>w

" 至定義
nnoremap <buffer> gd <Cmd>py3 from python_debug import 至定義;至定義()<CR>

" 環境設定
map <buffer> <F7> :w!<CR>:belowright :terminal python % --setup<CR>  

" 布署 VIM 模組
map <buffer> <expr> <F8> ":cd " . g:wdriver . ":\\" . g:workdir . "\\vimfiles<CR>:w!<CR>:INV d<CR>" 

" 註解--向後相容
map <buffer> ;3 gcc<CR>
