py3 from python_debug import 至

" 該行如有位置資訊，則至其表示之位置
nnoremap gf <cmd>py3 至()<cr><c-w><c-o>

" 切換至目前編輯檔之目錄
command! Cwd exe 'cd '.expand("%:p:h")   
