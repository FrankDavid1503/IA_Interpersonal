# Especificación de Endpoints API REST

## Autenticación
- `POST /api/auth/register` - Registro de nuevos usuarios
- `POST /api/auth/login` - Inicio de sesión y entrega de JWT
- `GET /api/auth/me` - Perfil del usuario autenticado

## Situaciones
- `POST /api/situations` - Crear nueva situación
- `GET /api/situations` - Listar situaciones del usuario
- `GET /api/situations/{id}` - Consultar detalle de situación
- `DELETE /api/situations/{id}` - Eliminar situación

## Análisis e IA
- `POST /api/situations/{id}/analyze` - Generar análisis de IA para una situación
- `GET /api/analyses/{id}` - Consultar resultado de análisis
