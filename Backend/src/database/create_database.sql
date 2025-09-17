-- Creación de la tabla de roles si no existe
CREATE TABLE IF NOT EXISTS roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE
);

-- Creación de la tabla de usuarios si no existe
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    contrasena_hash VARCHAR(256) NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_rol INT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Inserción de roles básicos si no existen
INSERT IGNORE INTO roles (nombre_rol) VALUES ('admin');
INSERT IGNORE INTO roles (nombre_rol) VALUES ('estandar');

-- Creación de un índice para acelerar las búsquedas por nombre de usuario
CREATE INDEX IF NOT EXISTS idx_nombre_usuario ON usuarios (nombre_usuario);