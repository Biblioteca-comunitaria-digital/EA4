Cómo ejecutar el proyecto!!!!

Desde la raíz del proyecto:

LA LLAVE MAGICA DE POO ------- = "python -m src.main" (-m) super importante para que python pueda reconocer la app.

PONER COMO ADMIN UN USUARIO


SQL BASH:

USE gestion_usuarios_db;

SQL BASH:

USE gestion_usuarios_db;
UPDATE usuarios
SET id_rol = (SELECT id_rol FROM roles WHERE nombre_rol = 'admin')
WHERE nombre_usuario = 'nombre_de_usuario_que_quieres_poner_como_admin';
