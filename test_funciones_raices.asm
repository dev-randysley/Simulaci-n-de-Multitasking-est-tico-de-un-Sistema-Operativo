Include funciones.asm


CalcularRaices:
push ax
push bx
push cx
push 4
push ax
call Multiplicar
mov dx, ax
pop cx
push cx
push cx
push dx
call Multiplicar
mov dx, ax
pop cx
pop bx
push bx
push cx
push dx
push bx
push bx
call Multiplicar
push ax
call Restar
mov dx, ax
push dx
call RaizCuadrada
mov dx, ax
pop cx
pop bx
pop ax
neg bx
pop bx
push bx
add bx, dx
add ax, ax
push ax
push dx
push ax
push bx
call Dividir
mov cx, ax
pop dx
pop ax
pop bx
neg dx
pop dx
add bx, dx
push cx
cmp bx, 0
jz UltimaDivisionNegativa
push ax
push bx
call Dividir
pop bx
ret
UltimaDivisionNegativa:
neg bx
pop bx
push ax
push bx
call Dividir
neg ax
pop ax
pop bx
ret

Entry_point:
mov ax, 5
mov bx, 10
mov cx, 0
call CalcularRaices
push bx
mov bx, 0
mov cx, 0
pop ax
mov bx, 1
mov cx, 0