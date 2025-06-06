from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import bisect

app = Flask(__name__)
CORS(app)

@app.route('/simular', methods=['POST'])
def simular():
    data = request.get_json()
    try:
        N = int(data.get('N'))
        desde = int(data.get('desde'))
        hasta = int(data.get('hasta'))
        fase = int(data.get('fase'))
        espera = float(data.get('espera'))
        inactividad = float(data.get('inactividad'))
        prob_llegadas = data.get("prob_llegadas")
        prob_descargas = data.get("prob_descargas")

        if not prob_llegadas or not prob_descargas:
            return jsonify({"error": "Faltan probabilidades de llegada o descarga"}), 400

        if abs(sum(prob_llegadas) - 1.0) > 0.01 or abs(sum(prob_descargas) - 1.0) > 0.01:
            return jsonify({"error": "Las probabilidades deben sumar 1"}), 400

    except Exception as e:
        return jsonify({"error": f"Datos inválidos: {str(e)}"}), 400

    llegadas = list(range(len(prob_llegadas)))
    descargas = list(range(1, len(prob_descargas) + 1))

    desv_descarga = 120
    media_descarga = 800
    esperando = 0
    ganancia_acumulada = 0

    llegadas_acum = [float(x) for x in np.cumsum(prob_llegadas)]
    descargas_acum = [float(x) for x in np.cumsum(prob_descargas)]

    resultados = []

    for dia in range(1, N + 1):
        rnd_lleg = round(float(np.random.random()), 2)
        rnd_desc = round(float(np.random.random()), 2)

        if fase == 1:
            llegadas_dia = llegadas[bisect.bisect_left(llegadas_acum, rnd_lleg)]
            idx = bisect.bisect_left(descargas_acum, rnd_desc)
            idx = min(idx, len(descargas) - 1)
            capacidad = descargas[idx]
        else:
            llegadas_dia = int(np.random.poisson(48))
            capacidad = int(rnd_desc * 9)

        total_para_desc = llegadas_dia + esperando
        descargados = min(capacidad, total_para_desc)
        esperando = total_para_desc - descargados

        precios = []
        costo_descarga = 0
        inactivo = 0

        if descargados > 0:
            for i in range(descargados):
                rnd = round(float(np.random.random()), 2)
                if rnd == 0:
                    rnd = 0.01
                z = np.sqrt(-2 * np.log(rnd)) * np.cos(2 * np.pi * np.random.random())
                precio = round(float(z * desv_descarga + media_descarga), 2)
                precios.append({"barco": i + 1, "rnd": rnd, "precio": precio})
                costo_descarga += precio
        else:
            inactivo = inactividad

        costo_espera = esperando * espera
        ganancia_dia = (costo_descarga if descargados > 0 else inactivo) - costo_espera
        ganancia_acumulada += ganancia_dia

        resultados.append({
            "dia": dia,
            "rnd_lleg": rnd_lleg,
            "llegadas": llegadas_dia,
            "rnd_desc": rnd_desc,
            "capacidad": capacidad,
            "esperando": total_para_desc,
            "descargados": descargados,
            "nuevo_esperando": esperando,
            "costo_descarga": round(costo_descarga, 2),
            "detalle_descarga": precios,
            "inactividad": round(inactivo, 2),
            "espera": round(costo_espera, 2),
            "ganancia_dia": round(ganancia_dia, 2),
            "ganancia_acumulada": round(ganancia_acumulada, 2)
        })

    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)
