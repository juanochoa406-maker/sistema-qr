import os
import uuid
import qrcode
import time
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfReader, PdfWriter
import mysql.connector
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True 

def get_db_connection():
    # Reintento para esperar a que MySQL esté listo
    while True:
        try:
            return mysql.connector.connect(
                host='database', 
                user='root', 
                password='rootpassword', 
                database='validacion_qr'
            )
        except mysql.connector.Error:
            time.sleep(2) # Espera 2 segundos y vuelve a intentar

@app.route('/')
def index():
    return redirect(url_for('repositorio'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username, password = request.form.get('username'), request.form.get('password')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM usuarios WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('repositorio'))
        error = "Credenciales incorrectas"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/repositorio')
def repositorio():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM documentos ORDER BY id DESC")
    docs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('repositorio.html', documentos=docs)

@app.route('/cambiar_estado/<int:id>/<nuevo_estado>')
def cambiar_estado(id, nuevo_estado):
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE documentos SET estado = %s WHERE id = %s", (nuevo_estado, id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('repositorio'))

@app.route('/subir', methods=['GET', 'POST'])
def subir():
    if 'user_id' not in session: return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '' or not file.filename.lower().endswith('.pdf'):
            return "Error: Solo se permiten archivos PDF", 400
            
        titulo, tipo, area = request.form['titulo'], request.form['tipo'], request.form['area']
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        folio = str(uuid.uuid4())[:8].upper()
        qr_path = os.path.join(app.config['UPLOAD_FOLDER'], f"qr_{folio}.png")
        qrcode.make(f"http://localhost:5000/validar/{folio}").save(qr_path)
        
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"final_{folio}.pdf")
        temp_pdf = f"temp_{folio}.pdf"
        c = canvas.Canvas(temp_pdf, pagesize=letter)
        c.drawImage(qr_path, 450, 650, width=100, height=100)
        c.save()
        
        reader = PdfReader(filepath)
        writer = PdfWriter()
        qr_reader = PdfReader(temp_pdf)
        page = reader.pages[0]
        page.merge_page(qr_reader.pages[0])
        writer.add_page(page)
        with open(output_path, "wb") as f: writer.write(f)
        if os.path.exists(temp_pdf): os.remove(temp_pdf)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO documentos (titulo, tipo, area_emisora, folio, pdf_original, pdf_con_qr, estado, usuario_id, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, 'Vigente', %s, %s)"
        cursor.execute(query, (titulo, tipo, area, folio, os.path.basename(filepath), os.path.basename(output_path), session['user_id'], datetime.now()))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('repositorio'))
    return render_template('subir.html')

@app.route('/validar/<folio>')
def validar(folio):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM documentos WHERE folio = %s", (folio,))
    doc = cursor.fetchone()
    cursor.close()
    conn.close()
    if not doc: return "<h1>Documento no encontrado</h1>", 404
    return render_template('validar.html', doc=doc)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)