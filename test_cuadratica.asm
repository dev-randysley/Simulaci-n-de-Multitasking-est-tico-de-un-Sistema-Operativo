Include funciones.asm

Entry_point:
mov ax, 1
mov bx, 6
mov cx, 8
call CalcularRaices
push bx
mov bx, 0
mov cx, 0
pop ax
mov bx, 1
mov cx, 0

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
push dx
neg bx
pop bx
push bx
add bx, dx
pop cx
neg dx
pop dx
add dx, cx
pop cx
push bx
push dx
push ax
push 2
call Multiplicar
push ax
pop ax
pop bx
pop cx
push ax
push bx
push ax
push cx
call Dividir
pop bx
pop cx
push ax
push cx
neg bx
call Dividir
neg ax
pop ax
pop bx
mov cx, 0
mov dx, 0
Int1 -> para escribir en la memoria de video las raices
Int1






