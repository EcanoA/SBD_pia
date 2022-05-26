CREATE DATABASE BOLETERIA

USE BOLETERIA

CREATE TABLE Evento(
idEvento INT not null identity (1,1) Primary key,
nombre varchar(80) not null,
idTipoEvento INT not null,
fecha varchar(10) not null,
idLocalidad INT not null
)

CREATE TABLE Zona(
idZona INT not null identity (1,1) PRIMARY KEY,
ZonaNom varchar (50) not null,
)

CREATE TABLE Precio(
idPrecio INT not null identity(1,1) PRIMARY KEY,
idEvento INT not null,
idZona INT not null,
Precio INT not null,
)

CREATE TABLE Localidad(
idLocalidad INT not null identity (1,1) PRIMARY KEY,
Estado varchar(50),
Pais varchar (50),
Ciudad varchar (50),
)

CREATE TABLE TipoEvento(
idTipoEvento INT not null identity (1,1) PRIMARY KEY,
TipoEvento varchar (60) not null,
)

CREATE TABLE Disponibilidad(
idZona INT not null,
idEvento INT not null,
Disponibilidad INT not  null
)

//cambiar los valores en la entrada y reestablecer tabla
CREATE TABLE Lugar(
idLugar INT not null identity (1,1) PRIMARY KEY,
AsientoNum INT not null identity (1,1),
idZona INT not null,
)

CREATE TABLE Boleto(
idEvento INT not null,
idBoleto INT not null PRIMARY KEY identity (1,1),
idComprador INT not null,
idLugar INT not null,
idLocalidad INT not null,
fechapago varchar(10) not null,
)

CREATE TABLE Comprador(
idComprador INT not null identity (1,1) PRIMARY KEY,
Nombre varchar (50) not null,
Apellido varchar (50) not null,
)

CREATE TABLE Factura(
idBoleto INT not null,
idPrecio INT not null,
idComprador INT not null,
idPago INT not null,
)

CREATE TABLE FormaPago(
idPago INT not null identity (1,1) PRIMARY KEY,
TipoPago varchar(50) not null,
)

--Drop table Boleto


--zona de creacion de consultas o para selects generales
SELECT * FROM Evento
SELECT * FROM Disponibilidad
SELECT * FROM Lugar
SELECT * FROM Comprador
SELECT * FROM Boleto
SELECT * FROM Factura
SELECT * FROM FormaPago
SELECT * FROM Localidad
SELECT * FROM Precio
SELECT * FROM TipoEvento
SELECT * FROM Zona


--DATOS
--Precio
insert into Precio(idEvento,idZona,Precio) values(1,1,1200);
insert into Precio(idEvento,idZona,Precio) values(1,2,1159);
insert into Precio(idEvento,idZona,Precio) values(1,3,671);
insert into Precio(idEvento,idZona,Precio) values(1,4,488);
insert into Precio(idEvento,idZona,Precio) values(1,5,851);
--ZONAS
insert into Zona(ZonaNom) values('VIP');
insert into Zona(ZonaNom) values('Preferente');
insert into Zona(ZonaNom) values('Luneta');
insert into Zona(ZonaNom) values('Platea');
insert into Zona(ZonaNom) values('Palco');
--Localidad
insert into Localidad(Estado,Pais,Ciudad) values('Nuevo Leon', 'Mexico', 'Monterrey');
insert into Localidad(Estado,Pais,Ciudad) values('CDMX', 'Mexico', 'CDMX');
insert into Localidad(Estado,Pais,Ciudad) values('Jalisco', 'Mexico', 'Guadalajara');
insert into Localidad(Estado,Pais,Ciudad) values('Texas', 'USA', 'Dallas');
insert into Localidad(Estado,Pais,Ciudad) values('California', 'USA', 'Los Angeles');
--Lugar
insert into Lugar(AsientoNum,idZona) values(1,1);
insert into Lugar(AsientoNum,idZona) values(1,2);
insert into Lugar(AsientoNum,idZona) values(1,3);
insert into Lugar(AsientoNum,idZona) values(1,4);
insert into Lugar(AsientoNum,idZona) values(2,1);
insert into Lugar(AsientoNum,idZona) values(2,2);
insert into Lugar(AsientoNum,idZona) values(2,3);
insert into Lugar(AsientoNum,idZona) values(2,4);
insert into Lugar(AsientoNum,idZona) values(3,1);
insert into Lugar(AsientoNum,idZona) values(3,2);
insert into Lugar(AsientoNum,idZona) values(3,3);
insert into Lugar(AsientoNum,idZona) values(3,4);
insert into Lugar(AsientoNum,idZona) values(4,1);
insert into Lugar(AsientoNum,idZona) values(4,2);
insert into Lugar(AsientoNum,idZona) values(4,3);
insert into Lugar(AsientoNum,idZona) values(4,4);
insert into Lugar(AsientoNum,idZona) values(5,1);
insert into Lugar(AsientoNum,idZona) values(5,2);
insert into Lugar(AsientoNum,idZona) values(5,3);
insert into Lugar(AsientoNum,idZona) values(5,4);
--Comprador
insert into Comprador(Nombre,Apellido) values('Orlando', 'Alvarado');
insert into Comprador(Nombre,Apellido) values('Daniel', 'Espinoza');
insert into Comprador(Nombre,Apellido) values('Alondra', 'Garza');
insert into Comprador(Nombre,Apellido) values('Perla', 'Velat');
--TipoEvento
insert into TipoEvento(TipoEvento) values('Concierto');
insert into TipoEvento(TipoEvento) values('Obra de teatro');
insert into TipoEvento(TipoEvento) values('Evento Privado');
insert into TipoEvento(TipoEvento) values('Graduacion');
--FormaPago 
insert into FormaPago(TipoPago) values('Tarjeta');
insert into FormaPago(TipoPago) values('Paypal');
insert into FormaPago(TipoPago) values('Oxxo');
insert into FormaPago(TipoPago) values('Transferencia');
--Evento
insert into Evento(nombre,idTipoEvento,fecha,idLocalidad) values('Mana', 1, '06/08/2022',1);
insert into Evento(nombre,idTipoEvento,fecha,idLocalidad) values('Harry Styles', 1, '09/10/2022',2);
insert into Evento(nombre,idTipoEvento,fecha,idLocalidad) values('El Cascanueces', 3, '26/12/2022',3);
insert into Evento(nombre,idTipoEvento,fecha,idLocalidad) values('Prueba', 3, '26/12/2020',3);
--Boleto
insert into Boleto(idEvento,idComprador,idLugar,idLocalidad,fechapago) values(1, 1, 9, 1, '03/05/2022');
insert into Boleto(idEvento,idComprador,idLugar,idLocalidad,fechapago) values(1, 2, 15, 1, '22/06/2022');
insert into Boleto(idEvento,idComprador,idLugar,idLocalidad,fechapago) values(2, 3, 18, 4, '15/01/2022');
insert into Boleto(idEvento,idComprador,idLugar,idLocalidad,fechapago) values(3, 4, 10, 5, '21/03/2022');
--Factura
insert into Factura(idBoleto,idPrecio,idComprador,idPago) values(1, 1200, 1, 1);
insert into Factura(idBoleto,idPrecio,idComprador,idPago) values(2, 671, 2, 1);
insert into Factura(idBoleto,idPrecio,idComprador,idPago) values(3, 1159, 3, 2);
insert into Factura(idBoleto,idPrecio,idComprador,idPago) values(4, 1159, 4, 3);
--Disponibilidad
INSERT INTO Disponibilidad(idZona,idEvento,Disponibilidad) values(1,1,10);