mov ax, 0
mov cx, 1
Ciclo:
add ax, cx
inc cx
cmp cx, 10
jz Ciclo
jmp Fin
Fin: