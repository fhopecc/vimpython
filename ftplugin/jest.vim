py3 from zhongwen.file import FileLocation
command! -buffer ChangeWindow normal <c-w>w
func! jest#locate()
py3 << EOF
import vim
line = vim.eval("getline('.')")
錯誤位置 = FileLocation(line)
vim.command(f"ChangeWindow")
vim.command(f"e +{錯誤位置.列} {錯誤位置.路徑}")
EOF
endfunc
map <buffer> gf :call jest#locate()<cr>
map <buffer> [[ ?(.*\.js:\d\+:\d\+)<cr>gf
map <buffer> ]] /(.*\.js:\d\+:\d\+)<cr>gf
