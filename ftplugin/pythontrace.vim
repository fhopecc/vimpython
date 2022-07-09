" 除錯
py3 from python_debug import 至, ErrorPosition
command! ChangeWindow normal <c-w>w
func! pythontrace#locate()
py3 << EOF
import vim
line = vim.eval("getline('.')")
錯誤位置 = ErrorPosition(line)
vim.command(f"ChangeWindow")
vim.command(f"e +{錯誤位置.行號} {錯誤位置.路徑}")
EOF
endfunc
map <buffer> gf :call pythontrace#locate()<cr>
map <buffer> [[ ?File<cr>gf
map <buffer> ]] /File<cr>gf
