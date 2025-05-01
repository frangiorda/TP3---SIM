import numpy as np
import matplotlib
matplotlib.use("TkAgg")  # Esto soluciona el problema en PyCharm
import matplotlib.pyplot as plt

def simular_puerto(N, mostrar_desde, mostrar_hasta):
    llegadas = [0, 1, 2, 3, 4, 5]
    prob_llegadas = [0.13, 0.17, 0.15, 0.25, 0.20, 0.10]
    descargas = [1, 2, 3, 4, 5]
    prob_descargas = [0.05, 0.15, 0.50, 0.20, 0.10]

    media_descarga = 800
    desv_descarga = 120
    costo_espera = 1500
    costo_inactividad = -3200

    esperando = 0
    barcos_en_espera_total = 0
    dias_muelle_ocupado = 0
    ganancia_total = 0

    dias = []
    ganancia_diaria = []
    barcos_espera_diario = []
    muelle_ocupado = []

    print(f"{'Día':<5}{'Llegadas':<10}{'Capacidad':<10}{'Esperando':<10}"
          f"{'Descargados':<12}{'Esperan Nuevo':<15}{'Ganancia Día':<15}")

    for dia in range(1, N + 1):
        llegadas_dia = np.random.choice(llegadas, p=prob_llegadas)
        total_para_descargar = esperando + llegadas_dia
        capacidad = np.random.choice(descargas, p=prob_descargas)
        descargados = min(total_para_descargar, capacidad)
        esperando = total_para_descargar - descargados
        barcos_en_espera_total += esperando

        if descargados > 0:
            dias_muelle_ocupado += 1
            ingresos = np.sum(np.random.normal(loc=media_descarga, scale=desv_descarga, size=descargados))
            ganancia_dia = ingresos
            muelle_ocupado.append(1)
        else:
            ganancia_dia = costo_inactividad
            muelle_ocupado.append(0)

        ganancia_dia -= esperando * costo_espera
        ganancia_total += ganancia_dia

        dias.append(dia)
        ganancia_diaria.append(ganancia_dia)
        barcos_espera_diario.append(esperando)

        if mostrar_desde <= dia <= mostrar_hasta or dia == N:
            print(f"{dia:<5}{llegadas_dia:<10}{capacidad:<10}{total_para_descargar:<10}"
                  f"{descargados:<12}{esperando:<15}${ganancia_dia:,.2f}")

    porcentaje_ocupacion = dias_muelle_ocupado / N * 100
    barcos_promedio_en_espera = barcos_en_espera_total / N

    print("\n---- RESULTADOS ----")
    print(f"Días simulados: {N}")
    print(f"Porcentaje de ocupación del muelle: {porcentaje_ocupacion:.2f}%")
    print(f"Promedio de barcos en espera: {barcos_promedio_en_espera:.2f}")
    print(f"Ganancia neta total: ${ganancia_total:,.2f}")

    # Graficar métricas en barras
    fig, ax = plt.subplots(3, 1, figsize=(14, 12), tight_layout=True)

    ax[0].bar(dias, ganancia_diaria, color='skyblue')
    ax[0].set_title("Ganancia diaria")
    ax[0].set_xlabel("Día")
    ax[0].set_ylabel("Ganancia ($)")

    ax[1].bar(dias, barcos_espera_diario, color='orange')
    ax[1].set_title("Cantidad de barcos en espera por día")
    ax[1].set_xlabel("Día")
    ax[1].set_ylabel("Barcos en espera")

    ocupacion_acumulada = np.cumsum(muelle_ocupado) / np.arange(1, N+1) * 100
    ax[2].bar(dias, ocupacion_acumulada, color='green')
    ax[2].set_title("Porcentaje de ocupación acumulado del muelle")
    ax[2].set_xlabel("Día")
    ax[2].set_ylabel("Ocupación (%)")

    plt.show()


# Ejecutar desde consola
if __name__ == "__main__":
    try:
        N = int(input("Ingrese la cantidad de días a simular (N): "))
        desde = int(input("Ingrese el día desde el que desea mostrar: "))
        hasta = int(input("Ingrese el día hasta el que desea mostrar: "))

        if desde < 1 or hasta > N or desde > hasta:
            print("⚠️ Rango de días inválido.")
        else:
            simular_puerto(N, desde, hasta)

    except ValueError:
        print("❌ Entrada inválida. Ingrese solo números enteros.")
