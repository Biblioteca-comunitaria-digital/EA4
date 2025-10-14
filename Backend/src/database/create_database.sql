-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS gestion_usuarios_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE gestion_usuarios_db;

-- Tabla de roles 
CREATE TABLE IF NOT EXISTS roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE
);

-- Insertar roles por defecto
INSERT IGNORE INTO roles (nombre_rol) VALUES ('admin'), ('estandar');

-- Tabla de usuarios (existente, con leve ajuste para relación con productos)
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    contrasena_hash VARCHAR(255) NOT NULL,
    id_rol INT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

-- Productos 
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    id_usuario INT NOT NULL,  -- Quién creó el producto (FK a usuarios)
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Datos de prueba para usuarios
INSERT IGNORE INTO usuarios (nombre_usuario, email, contrasena_hash, id_rol) VALUES
('admin', 'admin@example.com', SHA2(CONCAT('admin123', UNHEX(SHA2('una_sal_super_secreta', 256))), 256), 1),
('user1', 'user1@example.com', SHA2(CONCAT('password1', UNHEX(SHA2('una_sal_super_secreta', 256))), 256), 2);

-- NUEVOS DATOS DE PRUEBA: Productos (creados por admin)
INSERT IGNORE INTO productos (nombre, descripcion, precio, id_usuario) VALUES
('Producto 1', 'Descripción del producto 1', 29.99, 1),
('Producto 2', 'Descripción del producto 2', 49.99, 1),
('Servicio A', 'Descripción del servicio A', 99.99, 1),
('Producto 3', 'Descripción del producto 3', 19.99, 1);

-- Consulta de ejemplo con JOIN 
SELECT p.nombre AS producto, p.descripcion, p.precio, u.nombre_usuario AS creador 
FROM productos p 
JOIN usuarios u ON p.id_usuario = u.id_usuario 
ORDER BY p.id_producto;