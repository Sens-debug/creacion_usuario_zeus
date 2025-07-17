drop database if exists automat_usuarios_zeus;
create database  automat_usuarios_zeus;
use automat_usuarios_zeus;


create table control_funcion(funcionando bit);

create table personal_asistencial_creado(
    id int AUTO_INCREMENT primary key,
    primer_nombre varchar (30),
    segundo_nombre varchar (30),
    primer_apellido varchar(30),
    segundo_apellido varchar (30),
    documento_identidad varchar(20),
    correo varchar (15),
    telefono varchar (20),
    especialidad varchar(40)
    );

create table usuario_creado(
    id int AUTO_INCREMENT primary key,
    nombre_completo varchar(100),
    documento_identidad varchar(20),
    correo varchar (15),
    usuario varchar(30),
    contraseña_md5 varchar(200),
    contraseña varchar(30)
    );