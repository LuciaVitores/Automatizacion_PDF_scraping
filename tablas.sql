drop table if exists Pacientes, Diagnostico, Mutaciones, Patogenicas, Informacion

CREATE TABLE Pacientes ( 
	PRIMARY KEY(N_Chip, NHC),
	N_Chip INT NOT NULL,   
	N_Paciente INT NOT NULL,
	NHC INT NOT NULL, 
	Fecha_informe DATE NOT NULL, 
	N_Biopsia INT NOT NULL,
	Biopsia_solida char(3) NOT NULL
);

select * from Pacientes;

CREATE TABLE Diagnostico ( 
	PRIMARY KEY(N_Chip, NHC),
	N_Chip INT NOT NULL,   
	NHC INT NOT NULL,
	Texto_diagnostico text NOT NULL,
	N_Diagnostico INT NOT NULL
);

select * from Diagnostico;

CREATE TABLE Mutaciones (
	PRIMARY KEY(N_Chip, NHC),
	N_Chip INT NOT NULL,   
	NHC INT NOT NULL,
	Mutaciones_detectadas char (50) NOT NULL,
	Número_mutacion_especifica char (50) NOT NULL, 
	Total_mutaciones char (50) NOT NULL,
	Porcentaje_frecuencia_alelica char (50) NOT NULL,
	Fusiones_ID char (50) NOT NULL
);

select * from Mutaciones;

CREATE TABLE Patogenicas(
	PRIMARY KEY(N_Chip, NHC),
	N_Chip INT NOT NULL,   
	NHC INT NOT NULL,
	Genes_patogenicos char (50) NOT NULL,
	Número_mutacion_especifica char (50) NOT NULL, 
	Porcentaje_frecuencia_alelica char (50) NOT NULL, 
	Total_mutaciones char (50) NOT NULL
);

select * from Patogenicas;


CREATE TABLE Informacion(
	PRIMARY KEY(N_Chip, NHC),
	N_Chip INT NOT NULL,   
	NHC INT NOT NULL,
	Ensayos_clinicos INT NOT NULL,
	SI/NO_ensayos BOOLEAN NOT NULL, 
	Farmaco_aprobado INT NOT NULL, 
	SI/NO_farmaco BOOLEAN NOT NULL

);

select * from Informacion
