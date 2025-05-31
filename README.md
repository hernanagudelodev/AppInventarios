# SaaS Inmobiliario
:construction: Proyecto en construcción :construction:;
Este proyecto es una App de inventarios para inmobiliarias

# Checklist SaaS Inmobiliario – MVP & Roadmap

---

## 🟢 Inmediato (MVP Release)
- [ ] Terminar de revisar todas las **plantillas** para ajustes visuales (web/mobile, tablas, formularios, dashboards, PDFs).
- [ ] Agregar **filtros, búsquedas y paginación** a listados (clientes, propiedades, formularios).
- [ ] **Checklist y flujo de pruebas finales (QA)** para cada funcionalidad antes del release.
- [ ] **Despliegue:** definir opciones de hosting profesional (ej: Render, Railway, DigitalOcean, PythonAnywhere, etc.) y migración de la base de datos.
- [ ] **Pruebas de usuario final** (validación real con usuarios de la inmobiliaria y feedback).

---

## 🟡 Versión 2 y siguientes (Roadmap estratégico)
- [ ] Convertir el sistema en **multi-inmobiliaria**: que cada usuario solo acceda a datos de su inmobiliaria.
- [ ] **Integración con Wasi** (vía API REST para publicar propiedades y sincronizar inventario).
- [ ] **Agente inmobiliario AI**: sugerencias inteligentes, análisis de captación y precios.
- [ ] Afinar o ajustar **visuales avanzados** para dispositivos, navegadores, branding único, customización de colores.
- [ ] **Control de permisos por roles** (administrador, agente, asistente, etc.).
- [ ] **Landing page** comercial para captar nuevos clientes fuera de la inmobiliaria actual.

---



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

