from flask import Flask, request, render_template
import pickle
import numpy as np


# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Carga el modelo entrenado desde el archivo
with open('checkpoints/modelo_entrenado_AB.pkl', 'rb') as file:
    model = pickle.load(file)

# Rutas de la aplicación
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

def ValuePredictor (to_predict_list):
    to_predict = np.array (to_predict_list). reshape(1, 5)
    loaded_model = pickle. load(open ("checkpoints/modelo_entrenado_AB.pkl","rb"))
    result = loaded_model.predict (to_predict)
    return result[0]

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())

        try:
            to_predict_list = list(map(int, to_predict_list))
            result = ValuePredictor(to_predict_list)
            if int(result) == 0:
                prediction = 'Gana la ronda'
            elif int(result) == 1:
                prediction = 'Pierde la ronda'
            else:
                prediction = f'{int(result)} no-definida'

            message = f"El resultado de la predicción es: {prediction}"
        except ValueError:
            message = 'Error en el formato de los datos'

        return render_template("resultado.html", message=message)

# Ejecuta la aplicación Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)