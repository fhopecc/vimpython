" 除錯
map <buffer> [[ ?File<cr>
map <buffer> ]] /File<cr>
py3 from python_debug import 至, ErrorPosition
func! pythontrace#locate()
py3 << EOF
import vim
line = vim.eval("getline('.')")
錯誤位置 = ErrorPosition(line)
vim.command(f"e +{錯誤位置.行號} {錯誤位置.路徑}")
EOF
" echom "test"
endfunc

" File "d:\github\zhongwen\test_zhongwen.py", line 29, in test_number
"
map <buffer> gf pythontrace#locate()

