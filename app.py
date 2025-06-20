from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


def cant_coordinadores(cantidad_personas):
    if cantidad_personas <= 200:
        num_coordinadores = 2
    else:
        num_coordinadores = (cantidad_personas + 99) // 100
    return num_coordinadores


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu', methods=['POST'])
def menu():    
    nombre = request.form['nombre']
    fecha_evento = request.form['fecha']
    cantidad_personas = int(request.form['cantidad'])
    num_coordinadores = cant_coordinadores(cantidad_personas)
    return render_template('menu.html', nombre=nombre, fecha_evento=fecha_evento, cantidad_personas=cantidad_personas, num_coordinadores=num_coordinadores)

@app.route('/datos', methods=['POST'])
def cotizar():
    nombre = request.form['nombre']
    fecha_evento = request.form['fecha']
    cantidad_personas = int(request.form['cantidad'])
    num_coordinadores = cant_coordinadores(cantidad_personas)
   
    df_servicios_base = pd.read_excel('sources/Servicios.xlsx', sheet_name="Base")
    df_servicios_adicionales = pd.read_excel('sources/Servicios.xlsx', sheet_name="Adicionales")
    servicios = list(zip(df_servicios_adicionales['Servicio'], df_servicios_adicionales['Costo']))

# Aquí luego puedes hacer el cálculo de la cotización
    return render_template('/cotizar.html', 
                           nombre=nombre, 
                           fecha=fecha_evento, 
                           cantidad=cantidad_personas, 
                           num_coordinadores=num_coordinadores,
                           servicios=servicios)

@app.route('/resultado', methods=['POST'])
def resultado():
    nombre = request.form.get('nombre')
    fecha_evento = request.form.get('fecha')
    cantidad_personas = int(request.form.get('cantidad', 0))
    num_coordinadores = cant_coordinadores(cantidad_personas)
    servicios_seleccionados = request.form.getlist('servicios')

    
    df_base = pd.read_excel('sources/Servicios.xlsx', sheet_name="Base")
    df_adicionales = pd.read_excel('sources/Servicios.xlsx', sheet_name="Adicionales")
    
    servicios_base = df_base["Servicio"].tolist()
    servicios_seleccionados = request.form.getlist('servicios')

    
    df_seleccionados = df_adicionales[df_adicionales['Servicio'].isin(servicios_seleccionados)]
    servicios = list(zip(df_seleccionados['Servicio'], df_seleccionados['Costo']))


    return render_template('resultado.html',
                           nombre=nombre,
                           fecha=fecha_evento,
                           cantidad=cantidad_personas,
                           num_coordinadores=num_coordinadores,
                           servicios_base=servicios_base,
                           servicios=servicios
)

@app.route('/confirmar_pago', methods=['POST'])
def confirmar_pago():
    nombre = request.form.get('nombre')
    fecha_evento = request.form.get('fecha_evento')
    total_cotizacion = request.form.get('total_cotizacion')
    fecha_pago = request.form.get('fecha_pago')

    return f"Gracias {nombre}, tu fecha de pago preferida es el día {fecha_pago} de cada mes."

@app.route('/wedding_exp', methods=['POST'])
def wedding_exp():
    nombre = request.form.get('nombre')
    fecha_evento_str = request.form.get('fecha')
    total_cotizacion = 28900
    fecha_evento = datetime.strptime(fecha_evento_str, "%Y-%m-%d")

    # Cálculos
    if total_cotizacion > 4900:           
        apartado_fecha = 500
        anticipo = (total_cotizacion  - apartado_fecha) * 0.3
        restante = total_cotizacion - apartado_fecha - anticipo
    
    fecha_pago = request.form.get('fecha_pago', '15')
    dia_pago = int(fecha_pago)
    # Fecha de anticipo
    hoy = datetime.today()
    fecha_anticipo = datetime(hoy.year, hoy.month, 1) + relativedelta(months=1)
    fecha_anticipo = fecha_anticipo.replace(day=dia_pago)

    # Fecha de primera mensualidad
    fecha_primera_mensualidad = fecha_anticipo + relativedelta(months=1)

# Último pago
    meses_disponibles = (fecha_evento.year - fecha_primera_mensualidad.year) * 12 + (fecha_evento.month - fecha_primera_mensualidad.month)
    if meses_disponibles > 18:
        fecha_ultimo_pago = fecha_primera_mensualidad + relativedelta(months=18)
    else:
        fecha_ultimo_pago = fecha_evento - relativedelta(months=1)
    fecha_ultimo_pago = fecha_ultimo_pago.replace(day=dia_pago)

    # Sugerencia MSI y mensualidad
    sugerencia_msi = min(18, (fecha_ultimo_pago.year - fecha_anticipo.year) * 12 + (fecha_ultimo_pago.month - fecha_anticipo.month))
    mensualidad = restante / sugerencia_msi if sugerencia_msi > 0 else 0

    return render_template('wedding_exp.html',
        nombre=nombre,
        fecha_evento=fecha_evento_str,
        total_cotizacion=total_cotizacion,
        apartado_fecha=apartado_fecha,
        anticipo=anticipo,
        restante=restante,
        fecha_anticipo=fecha_anticipo.strftime("%Y-%m-%d"),
        fecha_primera_mensualidad=fecha_primera_mensualidad.strftime("%Y-%m-%d"),
        fecha_ultimo_pago=fecha_ultimo_pago.strftime("%Y-%m-%d"),
        sugerencia_msi=sugerencia_msi,
        mensualidad=round(mensualidad, 2),
        fecha_pago=fecha_pago
    )

@app.route('/wedding_dream', methods=['POST'])
def wedding_dream():
    nombre = request.form.get('nombre')
    fecha_evento_str = request.form.get('fecha')
    total_cotizacion = 14900
    fecha_evento = datetime.strptime(fecha_evento_str, "%Y-%m-%d")

    # Cálculos
    if total_cotizacion > 4900:           
        apartado_fecha = 500
        anticipo = (total_cotizacion  - apartado_fecha) * 0.3
        restante = total_cotizacion - apartado_fecha - anticipo
    
    fecha_pago = request.form.get('fecha_pago', '15')
    dia_pago = int(fecha_pago)
    # Fecha de anticipo
    hoy = datetime.today()
    fecha_anticipo = datetime(hoy.year, hoy.month, 1) + relativedelta(months=1)
    fecha_anticipo = fecha_anticipo.replace(day=dia_pago)

    # Fecha de primera mensualidad
    fecha_primera_mensualidad = fecha_anticipo + relativedelta(months=1)

# Último pago
    meses_disponibles = (fecha_evento.year - fecha_primera_mensualidad.year) * 12 + (fecha_evento.month - fecha_primera_mensualidad.month)
    if meses_disponibles > 18:
        fecha_ultimo_pago = fecha_primera_mensualidad + relativedelta(months=18)
    else:
        fecha_ultimo_pago = fecha_evento - relativedelta(months=1)
    fecha_ultimo_pago = fecha_ultimo_pago.replace(day=dia_pago)

    # Sugerencia MSI y mensualidad
    sugerencia_msi = min(18, (fecha_ultimo_pago.year - fecha_anticipo.year) * 12 + (fecha_ultimo_pago.month - fecha_anticipo.month))
    mensualidad = restante / sugerencia_msi if sugerencia_msi > 0 else 0

    return render_template('wedding_dream.html',
        nombre=nombre,
        fecha_evento=fecha_evento_str,
        total_cotizacion=total_cotizacion,
        apartado_fecha=apartado_fecha,
        anticipo=anticipo,
        restante=restante,
        fecha_anticipo=fecha_anticipo.strftime("%Y-%m-%d"),
        fecha_primera_mensualidad=fecha_primera_mensualidad.strftime("%Y-%m-%d"),
        fecha_ultimo_pago=fecha_ultimo_pago.strftime("%Y-%m-%d"),
        sugerencia_msi=sugerencia_msi,
        mensualidad=round(mensualidad, 2),
        fecha_pago=fecha_pago
    )

@app.route('/wedding_day', methods=['POST'])
def wedding_day():
    nombre = request.form.get('nombre')
    fecha_evento_str = request.form.get('fecha')
    total_cotizacion = 9790
    fecha_evento = datetime.strptime(fecha_evento_str, "%Y-%m-%d")

    # Cálculos
    if total_cotizacion > 4900:           
        apartado_fecha = 500
        anticipo = (total_cotizacion  - apartado_fecha) * 0.3
        restante = total_cotizacion - apartado_fecha - anticipo
    
    fecha_pago = request.form.get('fecha_pago', '15')
    dia_pago = int(fecha_pago)
    # Fecha de anticipo
    hoy = datetime.today()
    fecha_anticipo = datetime(hoy.year, hoy.month, 1) + relativedelta(months=1)
    fecha_anticipo = fecha_anticipo.replace(day=dia_pago)

    # Fecha de primera mensualidad
    fecha_primera_mensualidad = fecha_anticipo + relativedelta(months=1)

# Último pago
    meses_disponibles = (fecha_evento.year - fecha_primera_mensualidad.year) * 12 + (fecha_evento.month - fecha_primera_mensualidad.month)
    if meses_disponibles > 18:
        fecha_ultimo_pago = fecha_primera_mensualidad + relativedelta(months=18)
    else:
        fecha_ultimo_pago = fecha_evento - relativedelta(months=1)
    fecha_ultimo_pago = fecha_ultimo_pago.replace(day=dia_pago)

    # Sugerencia MSI y mensualidad
    sugerencia_msi = min(18, (fecha_ultimo_pago.year - fecha_anticipo.year) * 12 + (fecha_ultimo_pago.month - fecha_anticipo.month))
    mensualidad = restante / sugerencia_msi if sugerencia_msi > 0 else 0

    return render_template('wedding_day.html',
        nombre=nombre,
        fecha_evento=fecha_evento_str,
        total_cotizacion=total_cotizacion,
        apartado_fecha=apartado_fecha,
        anticipo=anticipo,
        restante=restante,
        fecha_anticipo=fecha_anticipo.strftime("%Y-%m-%d"),
        fecha_primera_mensualidad=fecha_primera_mensualidad.strftime("%Y-%m-%d"),
        fecha_ultimo_pago=fecha_ultimo_pago.strftime("%Y-%m-%d"),
        sugerencia_msi=sugerencia_msi,
        mensualidad=round(mensualidad, 2),
        fecha_pago=fecha_pago
    )

@app.route('/pagos', methods=['POST'])
def pagos():
    nombre = request.form.get('nombre')
    fecha_evento_str = request.form.get('fecha_evento')
    total_cotizacion = float(request.form.get('total_cotizacion'))
    fecha_evento = datetime.strptime(fecha_evento_str, "%Y-%m-%d")

    # Cálculos
    if total_cotizacion == 4900:
       apartado_fecha = 0
       anticipo = (total_cotizacion  - apartado_fecha) * 0.5
       restante = total_cotizacion - apartado_fecha - anticipo
    if total_cotizacion > 4900:           
        apartado_fecha = 500
        anticipo = (total_cotizacion  - apartado_fecha) * 0.3
        restante = total_cotizacion - apartado_fecha - anticipo
    
    fecha_pago = request.form.get('fecha_pago', '15')
    dia_pago = int(fecha_pago)
    # Fecha de anticipo
    hoy = datetime.today()
    fecha_anticipo = datetime(hoy.year, hoy.month, 1) + relativedelta(months=1)
    fecha_anticipo = fecha_anticipo.replace(day=dia_pago)

    # Fecha de primera mensualidad
    fecha_primera_mensualidad = fecha_anticipo + relativedelta(months=1)

# Último pago
    meses_disponibles = (fecha_evento.year - fecha_primera_mensualidad.year) * 12 + (fecha_evento.month - fecha_primera_mensualidad.month)
    if meses_disponibles > 18:
        fecha_ultimo_pago = fecha_primera_mensualidad + relativedelta(months=18)
    else:
        fecha_ultimo_pago = fecha_evento - relativedelta(months=1)
    fecha_ultimo_pago = fecha_ultimo_pago.replace(day=dia_pago)

    # Sugerencia MSI y mensualidad
    sugerencia_msi = min(18, (fecha_ultimo_pago.year - fecha_anticipo.year) * 12 + (fecha_ultimo_pago.month - fecha_anticipo.month))
    mensualidad = restante / sugerencia_msi if sugerencia_msi > 0 else 0

    return render_template('pagos.html',
        nombre=nombre,
        fecha_evento=fecha_evento_str,
        total_cotizacion=total_cotizacion,
        apartado_fecha=apartado_fecha,
        anticipo=anticipo,
        restante=restante,
        fecha_anticipo=fecha_anticipo.strftime("%Y-%m-%d"),
        fecha_primera_mensualidad=fecha_primera_mensualidad.strftime("%Y-%m-%d"),
        fecha_ultimo_pago=fecha_ultimo_pago.strftime("%Y-%m-%d"),
        sugerencia_msi=sugerencia_msi,
        mensualidad=round(mensualidad, 2),
        fecha_pago=fecha_pago
    )


if __name__ == '__main__':
    #app.run(debug=True)
    #app.run(host='0.0.0.0', port=5000, debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

