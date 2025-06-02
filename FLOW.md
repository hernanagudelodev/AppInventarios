Flujo de aplicación

INICIO DE SESIÓN
    ↓
¿Usuario tiene cuenta?
    ├─ NO → [Registro de Usuario] → [Dashboard]
    └─ SÍ → [Login]
                 ↓
        ¿Login exitoso?
            ├─ NO → [Mensaje de error] → [Login]
            └─ SÍ → [Dashboard]

DASHBOARD
    ↓
[Cards resumen]
[Gráfica captaciones 6 meses]
[Pendientes de firma]
    ↓
Menú principal:
    ├─ [Clientes]
    │      ↓
    │   [Listado] ←→ [Buscar/Filtrar/Paginar]
    │      ↓
    │   [Crear]/[Editar]/[Eliminar]/[Detalle]
    │
    ├─ [Propiedades]
    │      ↓
    │   [Listado] ←→ [Buscar/Filtrar/Paginar]
    │      ↓
    │   [Crear]/[Editar]/[Eliminar]/[Detalle]
    │      ↓
    │   [Clientes asociados] ←→ [Agregar relación]/[Eliminar relación]
    │      ↓
    │   [Captaciones] ←→ [Ver/Crear/Editar/Eliminar/Firmar/Enviar PDF]
    │      ↓
    │   [Entregas] ←→ [Crear/Editar/Firmar/Enviar PDF]
    │
    ├─ [Administración]
    │      ├─ [Config Inmobiliaria] (logo, textos contractuales, firma)
    │      ├─ [CRUD ciudades/tipo propiedad]
    │      └─ [CRUD secciones/campos formulario captación]

FLUJO DE CAPTACIÓN
    ↓
[Detalle propiedad]
    ↓
[Crear nueva captación]
    ↓
[Llenar formulario dinámico]
    ↓
[Guardar captación (borrador)]
    ↓
[Firma digital cliente]
    ↓
[Captación firmada]
    ↓
[Enviar PDF por correo]

FLUJO DE ENTREGA
    ↓
[Detalle propiedad]
    ↓
¿Captación firmada existe?
    ├─ NO → [Mostrar mensaje: "No disponible"]
    └─ SÍ → [Crear entrega]
                ↓
        [Seleccionar cliente/relación]
                ↓
        [Agregar ambientes]
                ↓
        [Editar ítems]
                ↓
        [Guardar entrega (borrador)]
                ↓
        [Firma digital cliente]
                ↓
        [Entrega firmada]
                ↓
        [Enviar PDF por correo]

SALIDA / LOGOUT
    ↓
[Logout seguro]
