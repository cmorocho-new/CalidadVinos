from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/')


def calcular_similitud_jaccard(nuevo_vino):
    lista_calculada = []
    with open("winequality-red.csv", "r") as f:
        linea = f.readline()
        while linea:
            linea = f.readline()
            propiedades_vino = linea.split(";")
            set_vino = set(map(float, propiedades_vino[:-1]))
            lista_calculada.append({
                'calidad': propiedades_vino[-1:][0].replace("\n", ""),
                'similitud': len(set_vino.intersection(nuevo_vino)) / len(set_vino.union(nuevo_vino))
            })
    # Retorna los 15 mas similares
    return sorted(lista_calculada, key=lambda item: item['similitud'], reverse=True)[:16]


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/comparacion', methods=['POST'])
def calcular_calidad():
    valores = [float(num) for num in request.form.values() if num]
    return render_template("index.html", lista=calcular_similitud_jaccard(valores))


if __name__ == '__main__':
    app.run()
