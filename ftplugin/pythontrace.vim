" 除錯
py3 from zhongwen.file import FileLocation
command! ChangeWindow normal <c-w>w
func! pythontrace#locate()
py3 << EOF
import vim
line = vim.eval("getline('.')")
錯誤位置 = FileLocation(line)
vim.command(f"ChangeWindow")
try:
    vim.command(f"e +{錯誤位置.列} {錯誤位置.路徑}")
except AttributeError:
    vim.command(f"e {錯誤位置.路徑}")
EOF
endfunc
map <buffer> gf :call pythontrace#locate()<cr>
map <buffer> [[ ?File<cr>gf
map <buffer> ]] /File<cr>gf
