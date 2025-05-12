import numpy as np
import matplotlib.pyplot as plt
import bisect

def simular_puerto(N, mostrar_desde, mostrar_hasta, media_descarga, costo_espera, costo_inactividad, fase):
    llegadas = [0, 1, 2, 3, 4, 5]
    prob_llegadas = [0.13, 0.17, 0.15, 0.25, 0.20, 0.10]
    descargas = [1, 2, 3, 4, 5]
    prob_descargas = [0.05, 0.15, 0.50, 0.20, 0.10]

    desv_descarga = 120
    esperando = 0
    barcos_en_espera_total = 0
    dias_muelle_ocupado = 0
    ganancia_total = 0
    ganancia_acumulada = 0

    dias = []
    ganancia_diaria = []
    barcos_espera_diario = []
    muelle_ocupado = []

    llegadas_acum = np.cumsum(prob_llegadas).tolist()
    descargas_acum = np.cumsum(prob_descargas).tolist()

    print(f"\n Simulación de Fase {fase} seleccionada:")
    if fase == 1:
        print("🔹 Fase 1: Llegadas y descargas según distribuciones discretas.")
    else:
        print("🔸 Fase 2: Llegadas Poisson (λ=48) + Capacidad extra con distribución uniforme [0,9]")

    for dia in range(1, N + 1):
        print(f"\n📅 Día {dia}")

        if fase == 1:
            rnd_llegadas = round(np.random.random(), 2)
            llegadas_dia = llegadas[bisect.bisect_left(llegadas_acum, rnd_llegadas)]
            print(f"  🎲 RND Llegadas = {rnd_llegadas:.2f} → Llegadas: {llegadas_dia}")

            rnd_descargas = round(np.random.random(), 2)
            capacidad = descargas[bisect.bisect_left(descargas_acum, rnd_descargas)]
            print(f"  🎲 RND Capacidad = {rnd_descargas:.2f} → Capacidad de descarga: {capacidad}")
        else:
            rnd_llegadas = round(np.random.random(), 2)
            llegadas_dia = np.random.poisson(48)
            print(f"  🎲 RND Llegadas (simulada para mostrar) = {rnd_llegadas:.2f} → Llegadas (Poisson): {llegadas_dia}")
            capacidad_base = np.random.choice(descargas, p=prob_descargas)
            barcos_extra = np.random.randint(0, 10)
            capacidad = capacidad_base + barcos_extra
            print(f"  🔧 Capacidad base: {capacidad_base} + extra: {barcos_extra} → Total: {capacidad}")
            rnd_descargas = "-"

        total_para_descargar = esperando + llegadas_dia
        descargados = min(total_para_descargar, capacidad)
        esperando = total_para_descargar - descargados
        barcos_en_espera_total += esperando

        print(f"  🚢 Total barcos a descargar (esperando + nuevos): {total_para_descargar}")
        print(f"  ⚓ Barcos descargados hoy: {descargados}")
        print(f"  ⛔ Barcos que siguen esperando: {esperando}")

        costo_descarga = 0
        costo_inactivo = 0
        ganancia_dia = 0
        precios_descarga = "-"
        if descargados > 0:
            dias_muelle_ocupado += 1
            muelle_ocupado.append(1)

            print(f"\n  🔁 Descargas:")
            rnds_n1 = np.round(np.random.random(descargados), 2)
            rnds_n1[rnds_n1 == 0] = 1e-10
            rnds_n2 = np.round(np.random.random(descargados), 2)
            z = np.sqrt(-2 * np.log(rnds_n1)) * np.cos(2 * np.pi * rnds_n2)
            valores_descarga = np.round(z * desv_descarga + media_descarga, 2)

            precios = []
            for i, valor in enumerate(valores_descarga):
                print(f"    - Barco {i + 1} → RND = {rnds_n1[i]:.2f} → Precio: ${valor:,.2f}")
                precios.append(f"B{i+1}:${valor:,.2f}")
            precios_descarga = " ".join(precios)
            costo_descarga = np.sum(valores_descarga)
            ganancia_dia = costo_descarga
        else:
            muelle_ocupado.append(0)
            costo_inactivo = costo_inactividad
            ganancia_dia = costo_inactivo

        costo_espera_total = esperando * costo_espera
        ganancia_dia -= costo_espera_total
        ganancia_acumulada += ganancia_dia
        ganancia_total += ganancia_dia

        dias.append(dia)
        ganancia_diaria.append(ganancia_dia)
        barcos_espera_diario.append(esperando)

        print(f"\n  💤 Costo por inactividad: ${costo_inactivo:,.2f}")
        print(f"  🕗 Costo por espera ({esperando} barcos): ${costo_espera_total:,.2f}")
        print(f"  💰 Ganancia neta del día: ${ganancia_dia:,.2f}")
        print(f"  📊 Ganancia acumulada: ${ganancia_acumulada:,.2f}")

        # Mostrar tabla Monte Carlo
        if dia == 1:
            print("\n📋 Tabla de simulación (estilo Monte Carlo):")
            print(f"{'Día':<5} {'RND Lleg':<9} {'Lleg':<6} {'RND Desc':<9} {'Capac.':<8} {'Esperando':<10} "
                  f"{'Descarg.':<10} {'Nuevo Esp.':<12} {'$Descarga':<11} {'$Inact.':<9} {'$Espera':<9} "
                  f"{'$Ganancia':<11} {'$Acumulada':<12} {'Descargas':<30}")

        print(f"{dia:<5} {rnd_llegadas:<9.2f} {llegadas_dia:<6} "
              f"{(f'{rnd_descargas:.2f}' if fase == 1 else '-'): <9} {capacidad:<8} {total_para_descargar:<10} "
              f"{descargados:<10} {esperando:<12} ${costo_descarga:<10.2f} ${costo_inactivo:<8.2f} "
              f"${costo_espera_total:<8.2f} ${ganancia_dia:<10.2f} ${ganancia_acumulada:<11.2f} {precios_descarga}")

    porcentaje_ocupacion = dias_muelle_ocupado / N * 100
    barcos_promedio_en_espera = barcos_en_espera_total / N
    max_esperando = max(barcos_espera_diario)
    ganancia_promedio = ganancia_total / N
    dias_inactivos = N - dias_muelle_ocupado

    print("\n---- RESULTADOS ----")
    print(f"Días simulados: {N}")
    print(f"Porcentaje de ocupación del muelle: {porcentaje_ocupacion:.2f}%")
    print(f"Promedio de barcos en espera: {barcos_promedio_en_espera:.2f}")
    print(f"Ganancia neta total: ${ganancia_total:,.2f}")
    print(f"🔹 Máximo de barcos en espera en un día: {max_esperando}")
    print(f"🔹 Ganancia promedio diaria: ${ganancia_promedio:,.2f}")
    print(f"🔹 Días con muelle inactivo: {dias_inactivos} ({(dias_inactivos / N) * 100:.2f}%)")

    # Gráficos
    fig, ax = plt.subplots(3, 1, figsize=(14, 12), tight_layout=True)

    ax[0].bar(dias, ganancia_diaria)
    ax[0].set_title("Ganancia diaria")
    ax[0].set_xlabel("Día")
    ax[0].set_ylabel("Ganancia ($)")

    ax[1].bar(dias, barcos_espera_diario)
    ax[1].set_title("Cantidad de barcos en espera por día")
    ax[1].set_xlabel("Día")
    ax[1].set_ylabel("Barcos en espera")

    ocupacion_acumulada = np.cumsum(muelle_ocupado) / np.arange(1, N + 1) * 100
    ax[2].bar(dias, ocupacion_acumulada)
    ax[2].set_title("Porcentaje de ocupación acumulado del muelle")
    ax[2].set_xlabel("Día")
    ax[2].set_ylabel("Ocupación (%)")

    nombre_grafico = f"grafico_resultados_fase{fase}.png"
    plt.savefig(nombre_grafico)
    print(f"✅ Gráfico guardado como '{nombre_grafico}'")

# Interfaz consola
if __name__ == "__main__":
    while True:
        try:
            print("Seleccione la fase de simulación:")
            print("1. Fase 1 (original: llegadas y descargas discretas)")
            print("2. Fase 2 (Poisson + descarga uniforme adicional por nuevo muelle)")
            fase = int(input("Fase: "))
            if fase not in [1, 2]:
                raise ValueError()

            N = int(input("Ingrese la cantidad de días a simular (N): "))
            desde = int(input("Ingrese el día desde el que desea mostrar: "))
            hasta = int(input("Ingrese el día hasta el que desea mostrar: "))
            media = 800
            espera = float(input("Ingrese el costo por barco en espera ($1500 defecto): "))
            inactividad = float(input("Ingrese el costo por inactividad del muelle ($-3200 defecto): "))

            if desde < 1 or hasta > N or desde > hasta:
                print("⚠️ Rango de días inválido.")
            else:
                simular_puerto(N, desde, hasta, media, espera, inactividad, fase)

            repetir = input("¿Desea hacer otra simulación? (s/n): ").strip().lower()
            if repetir != 's':
                print("✅ Simulación finalizada.")
                break

        except ValueError:
            print("❌ Entrada inválida. Ingrese solo números válidos.")
