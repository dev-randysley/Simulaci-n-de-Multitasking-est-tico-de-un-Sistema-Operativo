Multiplicar:
pop ax
pop cx
pop dx
push ax
mult cx, dx
ret

Dividir:
pop ax
pop cx
pop dx
push ax
div cx, dx
ret

RaizCuadrada:
pop ax
pop cx
push ax
raizCuadrada cx
ret