CREATE DATABASE IF NOT EXISTS validacion_qr;
USE validacion_qr;

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Insertar usuario de prueba
INSERT IGNORE INTO usuarios (id, username, password) VALUES (1, 'admin', 'admin123');

-- Crear tabla de documentos
CREATE TABLE IF NOT EXISTS documentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255),
    tipo VARCHAR(100),
    area_emisora VARCHAR(100),
    folio VARCHAR(50),
    pdf_original VARCHAR(255),
    pdf_con_qr VARCHAR(255),
    estado VARCHAR(50),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    usuario_id INT
);