from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    resultado = None

    form_data = {
        "sexo": "hombre",
        "edad": "",
        "peso": "",
        "altura": "",
        "actividad": "1.2",
        "objetivo": "mantener"
    }

    if request.method == "POST":

        sexo = request.form.get("sexo")
        edad = int(request.form.get("edad", 0))
        peso = float(request.form.get("peso", 0))
        altura = float(request.form.get("altura", 0))
        actividad = float(request.form.get("actividad", 1.2))
        objetivo = request.form.get("objetivo", "mantener")

        form_data = {
            "sexo": sexo,
            "edad": edad,
            "peso": peso,
            "altura": altura,
            "actividad": actividad,
            "objetivo": objetivo
        }

        # -----------------------------
        # BMR (Harris-Benedict)
        # -----------------------------

        if sexo == "hombre":
            bmr = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad)
        else:
            bmr = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * edad)

        mantenimiento = bmr * actividad

        objetivos = {
            "mantener": ("Mantener peso", 0),
            "perder_lento": ("Perder grasa lentamente", -300),
            "perder_rapido": ("Perder grasa rápidamente", -500),
            "ganar_limpio": ("Ganar músculo", 250),
            "ganar_agresivo": ("Ganar músculo rápidamente", 500)
        }

        nombre_objetivo, ajuste = objetivos.get(objetivo, objetivos["mantener"])

        calorias = mantenimiento + ajuste

        # -----------------------------
        # MACROS (básico pero útil)
        # -----------------------------

        # Proteína:
        # - 2 g por kg de peso (base fitness)
        proteina = peso * 2

        # Grasas:
        # - 0.8 g por kg
        grasas = peso * 0.8

        # Calorías de macros:
        calorias_proteina = proteina * 4
        calorias_grasa = grasas * 9

        # Carbohidratos = resto
        calorias_restantes = calorias - (calorias_proteina + calorias_grasa)
        carbohidratos = calorias_restantes / 4

        resultado = {
            "bmr": round(bmr),
            "mantenimiento": round(mantenimiento),
            "objetivo": nombre_objetivo,
            "calorias": round(calorias),

            "proteina": round(proteina),
            "grasas": round(grasas),
            "carbohidratos": round(carbohidratos)
        }

    return render_template("index.html", resultado=resultado, form=form_data)


if __name__ == "__main__":
    app.run(debug=True)