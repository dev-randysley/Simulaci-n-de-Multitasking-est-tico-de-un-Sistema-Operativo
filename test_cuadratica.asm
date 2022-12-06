Include funciones.asm

Entry_point:
int 2
int 2
int 2
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
push ax
push -4
call MultiplicarNegativos
mov dx, ax
push dx
call MultiplicarNegativos
mov dx, ax
pop bx
push dx
push bx
push bx
call VerificarNegativoCuadrado
call Multiplicar
pop bx
pop dx
add ax, dx
push bx
push ax
call RaizCuadrada
mov dx, ax
pop bx
push dx
neg bx
push dx
neg bx
call Restar
pop cx
pop dx
add cx, dx
push ax
push cx 
pop ax
pop bx
pop cx
push ax
push bx
push cx
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
call DividirNegativos
pop bx
pop cx
push ax
push cx
push bx
call DividirNegativos
push ax
pop ax
pop bx
mov cx, 0
mov dx, 0
int 1






