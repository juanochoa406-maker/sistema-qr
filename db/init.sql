-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL
);

-- Insertar usuario de prueba
INSERT IGNORE INTO usuarios (username, password) VALUES ('admin', 'admin123');

-- Crear tabla de documentos
CREATE TABLE IF NOT EXISTS documentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    area_emisora VARCHAR(100) NOT NULL,
    folio VARCHAR(50) NOT NULL UNIQUE,
    estado VARCHAR(20) DEFAULT 'Vigente', -- Vigente, Revocado, Cancelado
    pdf_original VARCHAR(255),
    pdf_con_qr VARCHAR(255),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);