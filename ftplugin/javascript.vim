" 執行 Javascript
command! MaxWindow normal <c-w>o

func! javascript#run() 
    w!
    let cmd = "cd " . expand("%:p:h") . "&& node " . expand("%:p:t") 
    execute(":R " . cmd)
endfunc
map <buffer> ;e :call javascript#run()<CR>

" 測試腳本
func! javascript#test()
    w!
    MaxWindow
    let cmd = "cmd /c cd " . expand("%:p:h") . "&& npm run test"
    call term_start(cmd)
endfunc
map <buffer> ;t :call javascript#test()<CR>

" 移動
map <buffer> gd :TernDef<cr>
