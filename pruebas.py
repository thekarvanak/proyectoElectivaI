# from selenium import webdriver
# import time

# driver = webdriver.Firefox()
# driver.get("https://www.instagram.com")

# ... tu código para interactuar con la página ...

# time.sleep(10)  # Pausa durante 10 segundos
# driver.quit()

alpha = 0.05
z = 1.96
e = 0.1
poblacion = 7400

n = (z**2 * 0.5 * 0.5) / (0.1 ** 2)
n_adj = n / (1 + (n-1)/poblacion)

print(f"muestra inicial = {n}")
print(f"muestra ajustada = {n_adj}")