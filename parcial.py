# Juan Camilo Gallo - 240420241054
# Punto 1 Máximo entre 2 numeros
def max_2(a, b):
    if a == b:
        return a
    if a > b:
        return a
    return b


# Punto 2  max_de_tres
def max_de_tres(a, b, c):
    return max(a, b, c)

#     if a > b and a > c:
#         return a
#     if b > a and b > c:
#         return b
#     if c > a and c > b:
#         return c

# Punto 3 longitud cadena
def get_len_cadena(s):
    c = 0
    for _ in s:
        c += 1
    return c


# Punto 4 is caracter
def is_vocal(s):
    vowels = ['a', 'e', 'i', 'o', 'u']
    return s in vowels


# Punto 5 sum y mult
def suma(arr):
    s = 0
    for i in arr:
        s += i
    return s


def mult(arr):
    s = 1
    for i in arr:
        s *= i
    return s


# Punto 6 inversa
def inversa(s):
    return s[::-1]


# Punto 7 es_palindromo
def es_palindromo(s):
    return s == s[::-1]


# Punto 8 superposicion
def superposicion(a, b):
    for i in a:
        for j in b:
            if i == j:
                return True
    return False


# Punto 9 generar_n_caracteres
def generar_n_caracteres(n: int, s: str):
    return s * n


# Punto 10 histograma
def histograma(arr):
    for i in arr:
        print("*" * i)





