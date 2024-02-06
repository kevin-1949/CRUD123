from flask import Flask 
from flask import request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

# aqui va el codigo

def conectar(vhost, vuser, vpass, vdb):
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset='utf8mb4')
    return conn


@app.route('/')
def consulta_general():
    try:
        conn = conectar('localhost', 'root', '1234', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM baul """)
        datos.fetcha11()
        data=[]

        for row in datos:
            dato = {'id_baul' : row[0], 'Plataforma' : row[1], 'usuario' : row[2], 'clave' : row[3]}
            data.append(dato)

        cur.close()
        conn.close()

        return jsonify({'baul' : dato, 'Mensaje' : 'Baul de contraseñas.'}) 

    except Exception as ex:
        return jsonify({'Mensaje' : 'Error'})


@app.route('/consulta_individual/<codigo>', methods=['GET'])
def consulta_individual(codigo):
    try:
        conn = conectar('localhost', 'root', '1234', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM baul where id_baul='{0}' """.format(codigo))
        datos = cur.fetchone()
        cur.close()
        conn.close()
        if datos != None:
            dato = {'id_baul' : datos[0], 'Plataforma' : datos[1], 'usuario' : datos[2], 'clave' : datos[3]}
            return jsonify({'baul' : dato, 'Mensaje' : 'Registro encontrado.'})
        else:
            return jsonify({'Mensaje' : 'Registro no encontrado.'})

    except Exception as ex:
        return jsonify({'Mensaje' : 'Error'})
    
@app.route('/registro/', methods=['POST'])
def registro():
    try:
        conn = conectar('localhost', 'root', '1234', 'gestor_contrasena')
        cur = conn.cursor()
        x = cur.execute(""" INSERT INTO baul (plataforma, usuario, clave) values('{0}', '{1}', '{2}')""".format(request.json['plataforma'], request.json['usuario'], request.json['clave']))
        conn.commit # para confirmar la insercion de la informacion
        cur.close()
        conn.close()
        return jsonify({'mensaje' : 'Registro agregado'})    
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje' : 'Error'})

@app.route('/eliminar/<codigo>', methods=['DELETE'])
def eliminar(codigo):
    try:
        conn = conectar('localhost', 'root', '1234', 'gestor_contrasena')
        cur = conn.cursor()
        x = cur.execute(""" DELETE FROM baul where id_baul='{0}' """.format(codigo))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'Mensaje' : 'Eliminado'})
    except Exception as ex:
        print(ex)
        return jsonify({'Mensaje' : 'Error'})

@app.route('/actualizar/<codigo>', methods=['PUT'])
def actualizar(codigo):
    try:
        conn = conectar('localhost', 'root', '1234', 'gestor_contrasena')
        cur = conn.cursor()
        x = cur.execute(""" UPDATE baul set plataforma = '{0}', usuario = '{1}', clave = '{2}' where id_baul={3} """.format(request.json['plataforma'], request.json['usuario'], request.json['clave'], codigo))
        conn.commit # para confirmar la insercion de la informacion
        cur.close()
        conn.close()
        return jsonify({'mensaje' : 'Registro actualizado'})    
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje' : 'Error'})


# aqui va el codigo

if __name__ == '__main__':
    app.run(debug=True)