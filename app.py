from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#Conexion mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudanimes'
mysql = MySQL(app)

#settings de sesion
app.secret_key='mysecretkey'

#Ruta inicial
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT* FROM animes')
    datos = cur.fetchall()

    return render_template('index.html', animes=datos)

#Ruta para de alta de anime
@app.route('/alta_anime', methods=['POST'])
def altacontacto():
    if request.method =='POST' :
        nombre = request.form['nombre']
        est = request.form['estudio']
        ep = request.form['episodios']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO animes (nombre,estudio,episodios) VALUES (%s, %s, %s)', (nombre, est, ep))
        mysql.connection.commit()
        flash('Añadido correctamente')
    return redirect(url_for('index'))

#Ruta para actualizar anime
@app.route('/edit_anime/<id>', methods = ['POST', 'GET'])
def editarcontacto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM animes WHERE id LIKE %s', [id])
    datos = cur.fetchall()
    print(datos[0])
    cur.close()
    return render_template('editar-anime.html', anime=datos[0])

#ruta de actualizar anime
@app.route('/actualizar/<id>', methods=['POST'])
def actualizaranime(id):
    if (request.method == 'POST'):
        nombre = request.form['nombre']
        estudio = request.form['estudio']
        episodios = request.form['episodios']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE animes
            SET nombre=%s, estudio=%s, episodios=%s
            WHERE id=%s
        
        """, (nombre, estudio, episodios, id))
        mysql.connection.commit()
        flash('Anime actualizado')
        return redirect(url_for('index'))

#Ruta de eliminar anime
@app.route('/baja_anime/<string:id>')
def bajacontacto(id):
    #Creamos el cursor
    cur = mysql.connection.cursor()

    #Ejecutamos la consulta
    cur.execute('DELETE FROM animes WHERE id={0}'.format(id))

    #Actualizamos
    mysql.connection.commit()

    #Mensaje de anime borrado
    flash('Anime eliminado')

    #Redireccionamos
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(port=3000, debug=True)
