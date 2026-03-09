-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 10-03-2026 a las 00:26:17
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `compiladores`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comandos`
--

CREATE TABLE `comandos` (
  `id` int(11) NOT NULL,
  `conductor_id` int(11) NOT NULL,
  `nickname` varchar(50) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `codigo` text NOT NULL,
  `estado` enum('pendiente','enviado','ejecutado','error') DEFAULT 'pendiente',
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_envio` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `comandos`
--

INSERT INTO `comandos` (`id`, `conductor_id`, `nickname`, `nombre`, `codigo`, `estado`, `fecha_creacion`, `fecha_envio`) VALUES
(1, 5, 'Mar22sal', 'Prueba', 'PROGRAM MiPrograma\nBEGIN\n    avanzar_mts(2);\n    girar(1) + avanzar_vlts(3);\n    rotar(1);\nEND.', 'enviado', '2026-02-26 16:10:28', '2026-02-26 16:14:27'),
(2, 5, 'Mar22sal', 'Prueba', 'PROGRAM RoverDanceShow\nBEGIN\n    avanzar_mts(1);\n    girar(1) + avanzar_vlts(2);\n    girar(-1) + avanzar_vlts(2);\n\n    rotar(1);\n\n    avanzar_ctms(4) + girar(1);\n    avanzar_ctms(4) + girar(1);\n    avanzar_ctms(4) + girar(1);\n    avanzar_ctms(4) + girar(1);\n\n    circulo(30);\n\n    moonwalk(2);\n    caminar(2);\n\n    rotar(-1);\n\nEND.', 'enviado', '2026-02-26 16:14:13', '2026-02-26 16:21:53'),
(3, 5, 'Mar22sal', 'Prueba1', 'PROGRAM RoverDanceShow\nBEGIN\n    avanzar_mts(1);\n    girar(1) + avanzar_vlts(2);\n    girar(-1) + avanzar_vlts(2);\n\n    rotar(1);\n\n    avanzar_ctms(4) + girar(1);\n    avanzar_ctms(4) + girar(1);\n    avanzar_ctms(4) + girar(1);\n    avanzar_ctms(14) + girar(1);\n\n    circulo(30);\n\n    moonwalk(2);\n    caminar(2);\n\n    rotar(-1);\n\nEND.', 'enviado', '2026-02-26 16:43:22', '2026-02-26 19:37:34');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `conductores`
--

CREATE TABLE `conductores` (
  `id` int(11) NOT NULL,
  `correo` varchar(150) NOT NULL,
  `correo_confirm` varchar(150) DEFAULT NULL,
  `telefono` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nickname` varchar(50) NOT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `rol` enum('administrador','editor','visualizador') DEFAULT 'visualizador',
  `verificado` tinyint(1) DEFAULT 0,
  `token_verificacion` varchar(100) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `creado_en` datetime DEFAULT current_timestamp(),
  `token_recuperacion` varchar(100) DEFAULT NULL,
  `token_recuperacion_exp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `conductores`
--

INSERT INTO `conductores` (`id`, `correo`, `correo_confirm`, `telefono`, `password`, `nickname`, `avatar`, `rol`, `verificado`, `token_verificacion`, `activo`, `creado_en`, `token_recuperacion`, `token_recuperacion_exp`) VALUES
(1, 'gerardo@test.com', NULL, '12345678', '$2b$12$daiAB6YFxDGKslLqYnLiyOqYKacYsd4iJf6DxvGf.73flVzFtkHYa', 'gerardo2026', NULL, 'visualizador', 1, NULL, 1, '2026-02-26 13:38:36', NULL, NULL),
(3, 'gerardo.salazar@loginsolutions.ai', NULL, '59625467', '$2b$12$wgyK9oYvEfhS8/Xuh4hshuSq9Urj1MkZUuRNtCRQEYN4Fgd6abjw.', 'Gerardojr', NULL, 'administrador', 0, 'iOe6-HiTp3wnRmQenyYuHZKTD_VKL7-n0xxGvx02uTM', 1, '2026-02-26 14:14:26', NULL, NULL),
(4, 'gerardo@prueba', NULL, '12345678', '$2b$12$NfoWe/9/wGgmte9BFSOFnexGaxCOWaKFnC3PkParrLidU5ZUhGGxK', 'gerardo22', NULL, 'visualizador', 0, '2eSBImhsGodlfPFvFixA25SwTkxhLM0sHmeTV4xYriE', 1, '2026-02-26 14:58:07', NULL, NULL),
(5, 'marving.salazar2231@gmail.com', NULL, '59625467', '$2b$12$vTjSNKxajx/9iIqv4aitI.y5rhsmjnEF9cPv8KRNj10NQfuWZWeYG', 'Mar22sal', NULL, 'administrador', 1, NULL, 1, '2026-02-26 15:00:54', NULL, NULL),
(6, 'marvin.sinay@loginsolutions.ai', NULL, '55976485', '$2b$12$NiP5ueeTOTpEsfMsD2G.l.f7MSgJtycvQSLMnrpbfyGoHUFzaz2JO', 'Lalo', NULL, 'administrador', 1, NULL, 1, '2026-03-03 17:25:43', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `logs`
--

CREATE TABLE `logs` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `usuario_nombre` varchar(100) NOT NULL,
  `accion` varchar(50) NOT NULL,
  `tabla_afectada` varchar(50) DEFAULT NULL,
  `registro_id` int(11) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `datos_antes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`datos_antes`)),
  `datos_despues` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`datos_despues`)),
  `ip_address` varchar(45) DEFAULT NULL,
  `fecha` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `logs`
--

INSERT INTO `logs` (`id`, `usuario_id`, `usuario_nombre`, `accion`, `tabla_afectada`, `registro_id`, `descripcion`, `datos_antes`, `datos_despues`, `ip_address`, `fecha`) VALUES
(1, 1, 'Juan Admin', 'CREAR', 'usuarios', 4, 'Se creó el usuario \'Marvin Salazar\' con rol \'editor\'', NULL, '{\"nombre\":\"Marvin Salazar\",\"email\":\"marvin.salazar@prueba.com\",\"rol\":\"editor\"}', '::1', '2026-02-26 11:48:23'),
(2, 1, 'gerardo2026', 'LOGIN', NULL, NULL, 'Inicio de sesión desde 127.0.0.1', NULL, NULL, '127.0.0.1', '2026-02-26 13:45:02'),
(3, 1, 'gerardo2026', 'LOGIN', NULL, NULL, 'Inicio de sesión desde 127.0.0.1', NULL, NULL, '127.0.0.1', '2026-02-26 14:07:14'),
(4, 3, 'Gerardojr', 'EDITAR', NULL, NULL, 'Contraseña actualizada por recuperación', NULL, NULL, '127.0.0.1', '2026-02-26 14:48:49'),
(5, 3, 'Gerardojr', 'EDITAR', NULL, NULL, 'Contraseña actualizada por recuperación', NULL, NULL, '127.0.0.1', '2026-02-26 14:53:53'),
(6, 3, 'Gerardojr', 'EDITAR', NULL, NULL, 'Contraseña actualizada por recuperación', NULL, NULL, '127.0.0.1', '2026-02-26 14:56:45'),
(7, 1, 'gerardo2026', 'LOGIN', NULL, NULL, 'Inicio de sesión desde 127.0.0.1', NULL, NULL, '127.0.0.1', '2026-02-26 14:59:19'),
(8, 5, 'Mar22sal', 'LOGIN', NULL, NULL, 'Inicio de sesión desde 127.0.0.1', NULL, NULL, '127.0.0.1', '2026-02-26 15:04:12'),
(9, 5, 'Mar22sal', 'LOGIN', NULL, NULL, 'Inicio de sesión desde 127.0.0.1', NULL, NULL, '127.0.0.1', '2026-02-26 15:45:51'),
(10, 5, 'Mar22sal', 'CREAR', NULL, NULL, 'Creó comando \'Prueba\'', NULL, NULL, '127.0.0.1', '2026-02-26 16:10:28'),
(11, 5, 'Mar22sal', 'CREAR', NULL, NULL, 'Creó comando \'Prueba\'', NULL, NULL, '127.0.0.1', '2026-02-26 16:14:13'),
(12, 5, 'Mar22sal', 'EDITAR', NULL, NULL, 'Envió comando ID 2 al Rover', NULL, NULL, '127.0.0.1', '2026-02-26 16:14:21'),
(13, 5, 'Mar22sal', 'EDITAR', NULL, NULL, 'Envió comando ID 1 al Rover', NULL, NULL, '127.0.0.1', '2026-02-26 16:14:27'),
(14, 5, 'Mar22sal', 'LOGIN', NULL, NULL, 'Inicio de sesión desde 127.0.0.1', NULL, NULL, '127.0.0.1', '2026-02-26 16:21:12'),
(15, 5, 'Mar22sal', 'EDITAR', NULL, NULL, 'Envió comando ID 2 al Rover', NULL, NULL, '127.0.0.1', '2026-02-26 16:21:53'),
(16, 5, 'Mar22sal', 'LOGIN', NULL, NULL, 'Inicio de sesión desde 10.10.1.118', NULL, NULL, '10.10.1.118', '2026-02-26 16:32:29'),
(17, 5, 'Mar22sal', 'CREAR', NULL, NULL, 'Creó comando \'Prueba1\'', NULL, NULL, '10.10.1.118', '2026-02-26 16:43:22'),
(18, 5, 'Mar22sal', 'EDITAR', NULL, NULL, 'Envió comando ID 3 al Rover', NULL, NULL, '10.10.1.118', '2026-02-26 16:43:23'),
(19, 5, 'Mar22sal', 'LOGIN', NULL, NULL, 'Inicio de sesión desde 10.10.1.118', NULL, NULL, '10.10.1.118', '2026-02-26 16:59:41'),
(20, 5, 'Mar22sal', 'LOGIN', NULL, NULL, 'Inicio de sesión desde 127.0.0.1', NULL, NULL, '127.0.0.1', '2026-02-26 19:13:41'),
(21, 5, 'Mar22sal', 'LOGIN', NULL, NULL, 'Inicio de sesión desde 127.0.0.1', NULL, NULL, '127.0.0.1', '2026-02-26 19:24:30'),
(22, 5, 'Mar22sal', 'LOGIN', NULL, NULL, 'Inicio de sesión desde 127.0.0.1', NULL, NULL, '127.0.0.1', '2026-02-26 19:35:18'),
(23, 5, 'Mar22sal', 'LOGIN', NULL, NULL, 'Inicio de sesión desde 127.0.0.1', NULL, NULL, '127.0.0.1', '2026-02-26 19:36:56'),
(24, 5, 'Mar22sal', 'EDITAR', NULL, NULL, 'Envió comando ID 3 al Rover', NULL, NULL, '127.0.0.1', '2026-02-26 19:37:34'),
(25, 6, 'Lalo', 'LOGIN', NULL, NULL, 'Inicio de sesión desde 10.40.0.47', NULL, NULL, '10.40.0.47', '2026-03-03 17:27:56'),
(26, 5, 'Mar22sal', 'LOGIN', NULL, NULL, 'Inicio de sesión desde 10.40.0.11', NULL, NULL, '10.40.0.11', '2026-03-03 17:29:01'),
(27, 5, 'Mar22sal', 'EDITAR', NULL, NULL, 'Cambió rol del usuario ID 6 a \'administrador\'', NULL, NULL, '10.40.0.11', '2026-03-03 17:29:14'),
(28, 6, 'Lalo', 'LOGIN', NULL, NULL, 'Inicio de sesión desde 10.40.0.47', NULL, NULL, '10.40.0.47', '2026-03-03 17:29:52');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permisos`
--

CREATE TABLE `permisos` (
  `id` int(11) NOT NULL,
  `rol` enum('administrador','editor','visualizador') NOT NULL,
  `permiso` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `permisos`
--

INSERT INTO `permisos` (`id`, `rol`, `permiso`) VALUES
(10, 'administrador', 'ver_dashboard'),
(11, 'administrador', 'gestionar_usuarios'),
(12, 'administrador', 'ver_logs'),
(13, 'administrador', 'ver_sesiones'),
(14, 'administrador', 'escribir_comandos'),
(15, 'administrador', 'enviar_comandos'),
(16, 'administrador', 'ver_comandos'),
(17, 'editor', 'escribir_comandos'),
(18, 'editor', 'enviar_comandos'),
(19, 'editor', 'ver_comandos'),
(20, 'visualizador', 'ver_comandos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sesiones`
--

CREATE TABLE `sesiones` (
  `id` int(11) NOT NULL,
  `conductor_id` int(11) NOT NULL,
  `token` varchar(255) NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `fecha_ingreso` datetime DEFAULT current_timestamp(),
  `fecha_salida` datetime DEFAULT NULL,
  `activa` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `sesiones`
--

INSERT INTO `sesiones` (`id`, `conductor_id`, `token`, `ip_address`, `fecha_ingreso`, `fecha_salida`, `activa`) VALUES
(1, 1, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwibmlja25hbWUiOiJnZXJhcmRvMjAyNiIsInJvbCI6InZpc3VhbGl6YWRvciIsImV4cCI6MTc3MjIyMTUwMn0.PtjkHgKnvJFiXjofYFHc_F8OsQ3sqSJggZdP95_qCiA', '127.0.0.1', '2026-02-26 13:45:02', NULL, 1),
(2, 1, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwibmlja25hbWUiOiJnZXJhcmRvMjAyNiIsInJvbCI6InZpc3VhbGl6YWRvciIsImV4cCI6MTc3MjIyMjgzNH0._8swvzeWujzyqsSENsH9OUcMov3Z4kmaSzyS20rvciA', '127.0.0.1', '2026-02-26 14:07:14', '2026-02-26 14:09:39', 0),
(3, 1, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwibmlja25hbWUiOiJnZXJhcmRvMjAyNiIsInJvbCI6InZpc3VhbGl6YWRvciIsImV4cCI6MTc3MjIyNTk1OH0.yy0tOU2S4eW_J41qaJlK0BB6b19h-lVNzCVsDGjO9yY', '127.0.0.1', '2026-02-26 14:59:19', NULL, 1),
(4, 5, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NSwibmlja25hbWUiOiJNYXIyMnNhbCIsInJvbCI6InZpc3VhbGl6YWRvciIsImV4cCI6MTc3MjIyNjI1Mn0.WZa_QZpvCUmWKZFprpGX3TgWyh0w9Vf2OS2Vc-ZUzTo', '127.0.0.1', '2026-02-26 15:04:12', '2026-02-26 15:45:08', 0),
(5, 5, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NSwibmlja25hbWUiOiJNYXIyMnNhbCIsInJvbCI6ImFkbWluaXN0cmFkb3IiLCJleHAiOjE3NzIyMjg3NTF9.5jVtf8reH62v4lCK6Cplouzr2fRWb-zWG-7OMIEpgLM', '127.0.0.1', '2026-02-26 15:45:51', '2026-02-26 16:21:02', 0),
(6, 5, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NSwibmlja25hbWUiOiJNYXIyMnNhbCIsInJvbCI6ImFkbWluaXN0cmFkb3IiLCJleHAiOjE3NzIyMzA4NzJ9.0ZQqkO3RdP9XLrqNJXtk9xMGrXu9sY81Rsa6Y2GXlBw', '127.0.0.1', '2026-02-26 16:21:12', '2026-02-26 19:10:29', 0),
(7, 5, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NSwibmlja25hbWUiOiJNYXIyMnNhbCIsInJvbCI6ImFkbWluaXN0cmFkb3IiLCJleHAiOjE3NzIyMzE1NDl9.YSv00Ke-p-d7aFNmh5rWCiVHPx3cDxVYQoTGPJKtAdE', '10.10.1.118', '2026-02-26 16:32:29', '2026-02-26 16:59:00', 0),
(8, 5, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NSwibmlja25hbWUiOiJNYXIyMnNhbCIsInJvbCI6ImFkbWluaXN0cmFkb3IiLCJleHAiOjE3NzIyMzMxODF9.4nDaBc_lGGq7ZYOjgZXAkN6RtkAydtAoaVpBRvdghg8', '10.10.1.118', '2026-02-26 16:59:41', NULL, 1),
(9, 5, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NSwibmlja25hbWUiOiJNYXIyMnNhbCIsInJvbCI6ImFkbWluaXN0cmFkb3IiLCJleHAiOjE3NzIyNDEyMjF9.sKli9cnc6hhqjn86GY0jftlB9kUCjNRCW7LrD5kq-qo', '127.0.0.1', '2026-02-26 19:13:41', '2026-02-26 19:14:22', 0),
(10, 5, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NSwibmlja25hbWUiOiJNYXIyMnNhbCIsInJvbCI6ImFkbWluaXN0cmFkb3IiLCJleHAiOjE3NzIyNDE4Njl9.mOOXmx3gCJCDGMJA0VNF-6nx-2kepLXExYQfGqneJ1Q', '127.0.0.1', '2026-02-26 19:24:30', '2026-02-26 19:32:26', 0),
(11, 5, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NSwibmlja25hbWUiOiJNYXIyMnNhbCIsInJvbCI6ImFkbWluaXN0cmFkb3IiLCJleHAiOjE3NzIyNDI1MTh9.LOszBb9b2xCWI0EBqxkUbmgnay7PlEPf5IcHW6OoyQQ', '127.0.0.1', '2026-02-26 19:35:18', '2026-02-26 19:36:28', 0),
(12, 5, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NSwibmlja25hbWUiOiJNYXIyMnNhbCIsInJvbCI6ImFkbWluaXN0cmFkb3IiLCJleHAiOjE3NzIyNDI2MTZ9.dRImVDcPJIWFGozW0J1w_5mNithKNdvYuczU_AxUbZA', '127.0.0.1', '2026-02-26 19:36:56', NULL, 1),
(13, 6, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Niwibmlja25hbWUiOiJMYWxvIiwicm9sIjoidmlzdWFsaXphZG9yIiwiZXhwIjoxNzcyNjY2ODc2fQ.t8ukXxJ4fHhRbmGq8qV0bg6Szm_VNjNGDCtopnCbQ_Y', '10.40.0.47', '2026-03-03 17:27:56', '2026-03-03 17:29:44', 0),
(14, 5, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NSwibmlja25hbWUiOiJNYXIyMnNhbCIsInJvbCI6ImFkbWluaXN0cmFkb3IiLCJleHAiOjE3NzI2NjY5NDF9.duIxHGuouuWiFXQ2V6lnXmKC2HQ0_Wb00gATUePHH8k', '10.40.0.11', '2026-03-03 17:29:01', NULL, 1),
(15, 6, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Niwibmlja25hbWUiOiJMYWxvIiwicm9sIjoiYWRtaW5pc3RyYWRvciIsImV4cCI6MTc3MjY2Njk5Mn0.4v3-kdEkMDCeM7iDgGTbnYW2cMzcxUQqYbjeLrK2pSk', '10.40.0.47', '2026-03-03 17:29:52', NULL, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `rol` enum('admin','editor','viewer') DEFAULT 'viewer',
  `activo` tinyint(1) DEFAULT 1,
  `creado_en` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `email`, `rol`, `activo`, `creado_en`) VALUES
(1, 'Juan Admin', 'juan@empresa.com', 'admin', 1, '2026-02-26 10:59:12'),
(2, 'María Editora', 'maria@empresa.com', 'editor', 1, '2026-02-26 10:59:12'),
(3, 'Carlos Viewer', 'carlos@empresa.com', 'viewer', 1, '2026-02-26 10:59:12'),
(4, 'Marvin Salazar', 'marvin.salazar@prueba.com', 'editor', 1, '2026-02-26 11:48:23');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `comandos`
--
ALTER TABLE `comandos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `conductor_id` (`conductor_id`);

--
-- Indices de la tabla `conductores`
--
ALTER TABLE `conductores`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD UNIQUE KEY `nickname` (`nickname`);

--
-- Indices de la tabla `logs`
--
ALTER TABLE `logs`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `sesiones`
--
ALTER TABLE `sesiones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `conductor_id` (`conductor_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `comandos`
--
ALTER TABLE `comandos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `conductores`
--
ALTER TABLE `conductores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `logs`
--
ALTER TABLE `logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT de la tabla `permisos`
--
ALTER TABLE `permisos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `sesiones`
--
ALTER TABLE `sesiones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `comandos`
--
ALTER TABLE `comandos`
  ADD CONSTRAINT `comandos_ibfk_1` FOREIGN KEY (`conductor_id`) REFERENCES `conductores` (`id`);

--
-- Filtros para la tabla `sesiones`
--
ALTER TABLE `sesiones`
  ADD CONSTRAINT `sesiones_ibfk_1` FOREIGN KEY (`conductor_id`) REFERENCES `conductores` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
