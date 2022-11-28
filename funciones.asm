Multiplicar:
pop cx
pop ax
pop bx
push cx
mov cx, 0
mov dx, 0
cmp cx, bx
jz CicloMultiplicar
mov ax, 0
ret
CicloMultiplicar:
inc cx
add dx, ax
cmp cx, bx
jz CicloMultiplicar
mov ax, dx
ret

Restar:
pop ax
pop bx
pop cx
push ax
neg cx
pop cx
add bx, cx
mov ax, bx
ret

Dividir:
pop cx
pop ax
pop bx
push cx
cmp ax, 1
jz Fin
mov cx, 0
mov dx, 0
CicloDividir:
inc cx
add dx, bx
cmp dx, ax
jz CicloDividir
mov ax, cx
Fin:
ret


RaizCuadrada:
pop cx
pop ax
push cx
mov bx, 0
CicloRaizCuadrada:
inc bx
push ax
push bx
push bx
push bx
call Multiplicar
mov dx, ax
pop bx
pop ax
cmp dx, ax
jz CicloRaizCuadrada
cmp ax, dx
jz CalcularResultadosRaizCuadrada
mov ax, bx
ret
CalcularResultadosRaizCuadrada:
dec bx
mov ax, bx
ret
