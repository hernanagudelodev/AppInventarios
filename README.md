# SaaS Inmobiliario
:construction: Proyecto en construcción :construction:;
Este proyecto es una App de inventarios para inmobiliarias

# Brief Técnico – SaaS Inmobiliario

## Objetivo General
Sistema SaaS para gestión de inventarios inmobiliarios, con flujos legales, contractuales y de firma digital, adaptable a varias inmobiliarias y con generación de documentación profesional.

---

## Modelos Principales

### Propiedad / Cliente / PropiedadCliente
- Propiedad y Cliente desacoplados.
- Relación PropiedadCliente, con tipo de relación (dueño, apoderado, arrendatario). Constraint único.

### Formularios
- **FormularioCaptacion:** Relacionado a PropiedadCliente, con campos fijos y dinámicos, firma digital, tipo (venta/renta), y textos contractuales diferenciados.
- **FormularioEntrega:** Igual de flexible, con ambientes, ítems, firma, textos contractuales.
- Ambos permiten generación de PDFs legales y envío por email.

### Inmobiliaria (en `account`)
- Nombre, logo, textos contractuales por tipo de formulario, firma digitalizada, responsable autorizado (nombre, cédula).
- Relacionada a cada usuario vía Profile.

---

## Funcionalidad y Flujo

- CRUD de propiedades y clientes, con gestión de relaciones Propiedad-Cliente (tipo obligatorio).
- Captación y entrega solo permitidas con flujos y permisos coherentes (ej: no se puede entregar sin captación firmada).
- Formularios con campos dinámicos configurables y firma digital con canvas.
- PDFs de resumen (captación y entrega) con branding, textos legales, firmas de ambas partes, fechas en letras y números.
- Documentación contractual clara y lista para auditoría.

---

## Arquitectura
- Multi-inmobiliaria (escalable), desacoplada por apps.
- ModelForm para campos fijos + lógica para campos dinámicos.
- Contexto de inmobiliaria por usuario autenticado.
- Listo para SaaS y futuras integraciones.

---

