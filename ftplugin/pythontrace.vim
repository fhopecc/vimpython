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
endfunc
map <buffer> gf :call pythontrace#locate()<cr>

