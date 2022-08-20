" 執行 Javascript
command! -buffer MaxWindow normal <c-w>o

func! javascript#run() 
    w!
    let term_opt = {"close_cb": "javascript:done"}
    let cmd = "cd " . expand("%:p:h") . "&& node " . expand("%:p:t") 
    MaxWindow
    call term_start(cmd , term_opt)
endfunc
map <buffer> ;e :call javascript#run()<CR>

func! javascript#done(job)
    set filetype=nodetrace
endfunc

" 測試腳本
func! javascript#test()
    w!
    MaxWindow
    let cmd = "cmd /c cd " . expand("%:p:h") . "&& npm run test"
    let term_opt = {"close_cb": "javascript:jest_done"}
    call term_start(cmd, term_opt)
endfunc
func! javascript#jest_done(job)
    set filetype=jest
endfunc
map <buffer> ;t :call javascript#test()<CR>

" 移動
map <buffer> gd :TernDef<cr>
