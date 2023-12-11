import numpy as np
import matplotlib.pyplot as plt


#Variables para cambiar
fila_unica = False #CAMBIAR ACA PARA HACER MULTIFILA
n_clientes = 200  # Número de clientes
n_cajas = 3  # Número de cajas
media_llegadas = 5  # Media para la distribución de Poisson
media_productos = 10  # Media para la distribución normal de productos
desviacion_productos = 3  # Desviación estándar para la distribución normal de productos
p_prob_efectivo = 0.4  # Probabilidad de pagar en efectivo
tiempo_efectivo = 2  # Tiempo de pago en efectivo (en minutos)
tiempo_otro_medio = 70 / 60  # Tiempo de pago en otro medio (en minutos)


#Variables para almacenar datos

tiempo_liberacion_cajas = [0] * n_cajas #minuto en que se va a liberar
tiempo_uso_cajas = [0] * n_cajas

tiempos_llegadas = np.random.poisson(media_llegadas, n_clientes)
tiempos_llegadas[0] = 0
tiempos_llegadas = np.cumsum(tiempos_llegadas)

tiempo_compra_clientes = [0] * n_clientes
tiempo_espera_clientes = [0] * n_clientes

#variables multifila
fila_caja = [0] * n_cajas
salieron = [False] * n_clientes
caja_cliente = [0] * n_clientes


for i in range(n_clientes):
    tiempo_actual = tiempos_llegadas[i]

    if not fila_unica:
        for j in range(i):
            if( tiempo_compra_clientes[j] + tiempo_espera_clientes[j]  + tiempos_llegadas[j] < tiempo_actual):
                caja = caja_cliente[j]
                if not salieron[j]:
                    fila_caja[caja] -= 1
                    salieron[j] = True
                    #print("cliente " + str(j+1) + " se va de la caja " + str(caja+1) + " en el min " + str(tiempo_compra_clientes[j] + tiempo_espera_clientes[j]  + tiempos_llegadas[j]))

    #print("Cliente " + str(i+1) + " llega en el min " + str(tiempo_actual))
    p_pago_efectivo = np.random.rand()
    if p_pago_efectivo <= p_prob_efectivo:
        tiempo_pago = tiempo_efectivo
    else:
        tiempo_pago = tiempo_otro_medio
    
    productos = max(1, round(np.random.normal(media_productos, desviacion_productos)))
    tiempo_compra_clientes[i] = productos + tiempo_pago
   #print("Tarda " + str(tiempo_compra_clientes[i]) + " comprando")
    #Elige la caja que se va a liberar antes

    #Si se va a liberar antes del tiempo actual, coloco el valor en 0 para que escoja la mas cercana
    for caja in range(n_cajas):
        if(tiempo_liberacion_cajas[caja] < tiempo_actual):
            tiempo_liberacion_cajas[caja] = 0
    
    #if not fila_unica:
       # print("Fila cajas: " + str(fila_caja))

    #elige la caja que se libera antes
    if(fila_unica):
        caja_elegida = tiempo_liberacion_cajas.index(min(tiempo_liberacion_cajas))
    else:
        caja_elegida = fila_caja.index(min(fila_caja))
        fila_caja[caja_elegida] += 1

    #print("va a la caja " + str(caja_elegida+1))
    caja_cliente[i] = caja_elegida

    #el tiempo que espera es el de liberacion de su caja - el que llego
    tiempo_espera_clientes[i] =  max(0, tiempo_liberacion_cajas[caja_elegida] - tiempos_llegadas[i])
   # print("la caja se libera en " + str(tiempo_liberacion_cajas[caja_elegida]))

    #se libera en el tiempo actual + lo que espera + el que va a tardar comprando
    tiempo_liberacion_cajas[caja_elegida] = tiempo_actual + tiempo_compra_clientes[i] + tiempo_espera_clientes[i]
    #al tiempo de uso total le suma el tiempo de compra
    tiempo_uso_cajas[caja_elegida] += tiempo_compra_clientes[i]

tiempo_actual = max(tiempo_liberacion_cajas)



print("********************************************************")

#3) Valor medio y desviación estándar para el tiempo de uso de cada caja
tiempo_medio_uso_cajas = np.mean(tiempo_uso_cajas)
desviacion_caja = np.std(tiempo_uso_cajas)


print(f'Valor medio de tiempo de uso: {tiempo_medio_uso_cajas:.2f} m')
print(f'Desviacion estandar de tiempo de uso: {desviacion_caja:.2f} m')
print("********************************************************")



#4) Valor medio y desviación estándar de tiempo de espera en la fila de cada cliente
tiempo_medio_espera = np.mean(tiempo_espera_clientes)
desviacion_espera = np.std(tiempo_espera_clientes)

print(f'Valor medio de tiempo de espera: {tiempo_medio_espera:.2f} m')
print(f'Desviacion estandar de tiempo de espera: {desviacion_espera:.2f} m')
print("********************************************************")


#5) Tiempo libre de cada caja disponible
for caja in range(n_cajas):
    tiempo_libre_caja = tiempo_actual - tiempo_uso_cajas[caja]
    print(f'Tiempo libre de Caja {caja+1}: {tiempo_libre_caja:.2f} m')
print("********************************************************")


print("Tiempo final")
print(tiempo_actual)
print("********************************************************")


# Grafico de tiempo de uso de cada caja
plt.figure(figsize=(10, 6))
for caja in range(n_cajas):
     tiempo_total_caja = tiempo_uso_cajas[caja]
     plt.bar(caja + 1, tiempo_uso_cajas[caja], label=f'Caja {caja+1}')
     
     plt.text(caja + 1, tiempo_total_caja + 5, f'{tiempo_total_caja:.2f} m', ha='center', va='bottom')

plt.xticks(np.arange(1, n_cajas + 1, 1))
plt.xlabel('Caja')
plt.ylabel('Tiempo de uso total (minutos)')
plt.legend()
plt.show()


# Grafico del tiempo de espera de los clientes
ancho_barras = 0.8 
plt.figure(figsize=(12, 6))  

bars = plt.bar(np.arange(1, n_clientes + 1), tiempo_espera_clientes, width=ancho_barras, align='center')
plt.xlabel('Cliente')
plt.ylabel('Tiempo de espera en la fila (minutos)')
plt.title('Tiempo de espera de cada cliente en la fila')

for bar, tiempo_espera in zip(bars, tiempo_espera_clientes):
    if tiempo_espera > 0:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{tiempo_espera:.2f} m', ha='center', va='bottom')

plt.xticks(np.arange(1, n_clientes + 1, 1))
plt.show()


plt.hist(tiempo_espera_clientes)
plt.title('Tiempos de espera')
plt.xlabel('Valor')
plt.ylabel('Frecuencia')

plt.show()

