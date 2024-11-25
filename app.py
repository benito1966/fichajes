from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from base_de_datos import inicializar_bd, agregar_empleado, obtener_empleados, registrar_fichaje, obtener_fichajes, \
    autenticar_empleado
from generar_informe import generar_pdf

app = Flask(__name__)
app.secret_key = "clave_secreta"
inicializar_bd()

@app.route("/")
def index():
    empleados = obtener_empleados()
    return render_template("index.html", empleados=empleados)

@app.route("/fichar", methods=["GET", "POST"])
def fichar():
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]
        tipo = request.form["tipo"]

        # Autenticar al empleado
        empleado_id = autenticar_empleado(usuario, clave)
        if empleado_id:
            try:
                registrar_fichaje(empleado_id, tipo)
                flash("Fichaje registrado con éxito.")
            except ValueError as e:
                flash(str(e))  # Error en la validación
        else:
            flash("Usuario o clave incorrectos.")
        return redirect(url_for("index"))

    return render_template("fichar.html")


@app.route("/empleados", methods=["GET", "POST"])
def empleados():
    if request.method == "POST":
        nombre = request.form["nombre"]
        usuario = request.form["usuario"]
        clave = request.form["clave"]
        agregar_empleado(nombre, usuario, clave)
        flash("Empleado agregado con éxito.")
        return redirect(url_for("empleados"))
    empleados = obtener_empleados()
    return render_template("empleados.html", empleados=empleados)

@app.route("/informe", methods=["GET", "POST"])
def informe():
    empleados = obtener_empleados()
    if request.method == "POST":
        empleado_id = request.form.get("empleado_id")
        mes = request.form.get("mes")
        ruta_pdf = generar_pdf(empleado_id, mes)
        return send_file(ruta_pdf, as_attachment=True)
    return render_template("informe.html", empleados=empleados)

#if __name__ == "__main__":
 #   app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

