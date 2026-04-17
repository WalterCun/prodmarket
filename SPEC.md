# ProdMarket - Especificación del Proyecto

## 1. Overview

**Nombre:** ProdMarket  
**Tipo:** Marketplace agrícola (OTA-style)  
**Descripción:** Plataforma que conecta productores agrícolas, ganaderos y pescadores directamente con transportistas y consumidores finales, eliminando intermediarios.  
**Modelo de negocio:** Comisión 20% por cada venta completada.

## 2. Objetivos del Negocio

- Unir productores → transportistas → consumidores finales
- Eliminar intermediarios para precios justos
- Venta mayorista y minorista
- Comisiones del 20% por transacción

## 3. Usuarios y Roles

### Productor
- Registra productos (agricultura, ganadería, pesca)
- Define precios, cantidad disponible
- Recibe pedidos
- Cobra por ventas (menos comisión)

### Transportista
- Ve productos disponibles en zonas
- Transporte propio
- Recoge del campo y entrega al consumidor
- Gana por servicio de transporte

### Consumidor Final
- Explora productos disponibles
- Compra directo del productor
- Recibe en ubicación definida

### Administrador
- Dashboard de gestión
- Reportes de ventas
- Gestión de usuarios
- Configuración de comisiones

## 4. Funcionalidades Core

### 4.1 Autenticación
- Login/Registro por email
- Roles: Productor, Transportista, Consumidor, Admin
- JWT tokens

### 4.2 Módulo Productor
- Registro de producto (fotos, precio, cantidad, categoría)
- Dashboard de ventas
- Gestión de pedidos
- Historial de transacciones

### 4.3 Módulo Transportista
- Explorador de productos por zona
- Registro de vehículo/capacidad
- Historial de entregas
- Ganancias por transporte

### 4.4 Módulo Consumidor
- Catálogo de productos
- Carrito de compras
- Métodos de pago (stub)
- Historial de pedidos

### 4.5 Módulo Admin
- Dashboard analytics
- Gestión de usuarios
- Reportes de comisiones
- Configuración de plataforma

## 5. Tech Stack

- **Backend:** Django + Django Ninja (API REST)
- **Frontend Admin:** React + Vite + TypeScript
- **Frontend Público:** Django Templates (server-side render)
- **DB:** PostgreSQL (producción) / SQLite (dev)
- **Styling:** Tailwind CSS

## 6. Estructura del Proyecto

```
prodmarket/
├── backend/          # Django project
│   ├── products/      # App productos
│   ├── orders/        # App pedidos
│   ├── users/        # App usuarios
│   └── api/          # Django Ninja endpoints
├── frontend/         # React dashboard
└── docker-compose.yml
```

## 7. Fases

### Fase 1: MVP
- Autenticación básica
- CRUD productos
- Carrito y checkout (stub)
- Dashboard admin básico

### Fase 2: Enhanced
- Zonas y geolocalización
- Sistema de transportistas
- Notificaciones
- Pagos reales

### Fase 3: Scale
- App móvil
- Chat en tiempo real
- Analytics avanzado

## 8. consideraciones

- Monolito inicial para velocidad
- Separar después si crece
- MVP en ~2-3 semanas