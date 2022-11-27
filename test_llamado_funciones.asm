Include funciones.asm

Entry_point:
mov ax, 10
mov bx, 5

push ax
push bx
call Restar
mov dx, bx