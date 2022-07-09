" 除錯
map <buffer> [[ ?File<cr>
map <buffer> ]] /File<cr>
py3 from python_debug import 至 
func! pythonoutput#locate()
    py3 至()     
" nnoremap gf <cmd>py3 from fhopecc.python_debug import 至;至()<cr><c-w><c-o>
endfunc
map <buffer> gf pythonoutput#locate()


