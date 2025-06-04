# SaaS Inmobiliario
:construction: Proyecto en construcción :construction:

Este proyecto es una App de inventarios para inmobiliarias, 100% responsive, robusta y alineada a buenas prácticas Django.

---

## **Checklist SaaS Inmobiliario – MVP & Roadmap**

### 🟢 **Inmediato (MVP Release)**

- [X] Terminar de revisar todas las **plantillas** para ajustes visuales (web/mobile, tablas, formularios, dashboards, PDFs).
- [X] Agregar **filtros, búsquedas y paginación** a listados (clientes, propiedades, formularios).
- [ ] **Checklist y flujo de pruebas finales (QA)** para cada funcionalidad antes del release.
- [ ] **Despliegue:** definir opciones de hosting profesional (ej: Render, Railway, DigitalOcean, PythonAnywhere, etc.) y migración de la base de datos.
- [ ] **Pruebas de usuario final** (validación real con usuarios de la inmobiliaria y feedback).

---

### 🟡 **Versión 2 y siguientes (Roadmap estratégico)**

- [ ] Convertir el sistema en **multi-inmobiliaria**: que cada usuario solo acceda a datos de su inmobiliaria.
- [ ] **Integración con Wasi** (vía API REST para publicar propiedades y sincronizar inventario).
- [ ] **Agente inmobiliario AI**: sugerencias inteligentes, análisis de captación y precios.
- [ ] Afinar o ajustar **visuales avanzados** para dispositivos, navegadores, branding único, customización de colores.
- [ ] **Control de permisos por roles** (administrador, agente, asistente, etc.).
- [ ] **Landing page** comercial para captar nuevos clientes fuera de la inmobiliaria actual.

---

## **Resumen técnico de la aplicación**

### **Objetivo General**
Sistema SaaS para gestión de inventarios inmobiliarios, adaptable a varias inmobiliarias, con generación de documentación profesional, flujos contractuales, firmas digitales y todo el ciclo de vida (captación, entrega, seguimiento).

---

### **Modelos Principales**
- **Propiedad:** Datos completos del inmueble, incluyendo ubicación GPS.
- **Cliente:** Personas o empresas con información de contacto y gestión.
- **PropiedadCliente:** Relación flexible cliente-propiedad con rol (propietario, apoderado, arrendatario), sin duplicidades.
- **FormularioCaptacion:** Relaciona propiedad/cliente, soporta campos fijos y dinámicos, firma digital, textos contractuales y PDF.
- **FormularioEntrega:** Similar a captación, pero solo para arrendatarios, incluye ambientes e ítems, firma digital y PDF.
- **Inmobiliaria:** Branding, firmas, textos contractuales personalizados, datos legales y relación con usuarios.
- **Ambientes e Ítems:** Modelan el inventario detallado de cada inmueble entregado/recibido.

---

### **Flujo de la aplicación**

1. **Inicio de sesión y registro** (Bootstrap, mensajes claros, flujo seguro).
2. **Dashboard**: Cards resumen, gráficos, acciones rápidas.
3. **Propiedades**: CRUD, asignación de clientes (solo propietario/apoderado para captación, solo arrendatario para entrega).
4. **Clientes**: CRUD, edición, visuales responsive.
5. **Captación:**  
   - Solo disponible si hay propietario/apoderado.
   - Formulario dinámico.
   - Firma digital, generación de PDF.
   - Eliminación solo si no está firmado.
6. **Entrega:**  
   - Solo si hay captación firmada y arrendatario.
   - Detalle de ambientes/ítems.
   - Firma digital, generación de PDF.
   - Eliminación solo en estado borrador y por POST.
7. **Firmas:**  
   - Uso de SignaturePad en captación y entrega.
   - Visualización y guardado seguro.
8. **Mapas:**  
   - Selección interactiva en formulario de propiedad, usando Leaflet y geolocalización del navegador.
9. **Mensajes y validaciones:**  
   - Todos los mensajes globales se muestran en el bloque superior (mensajes Django).
   - Validaciones limpias, sin errores de integridad visibles para el usuario.
10. **Visuales:**  
    - 100% Bootstrap 5: tarjetas, tablas, formularios y tablas responsive.
    - Consistencia visual y buena experiencia móvil y escritorio.
11. **Seguridad:**  
    - Todas las eliminaciones y acciones críticas solo por POST y con confirmación.
    - Permisos básicos para evitar acciones indebidas.

---

**¿Siguiente paso?**  
- Ve marcando lo ya completado y agrega pendientes en el checklist para máxima claridad.
- Mantén este README actualizado para nuevos miembros o para presentar el avance del proyecto.
- Revisa el roadmap cada sprint y ajusta prioridades.

---

¡App lista para pruebas reales y próximo despliegue SaaS! 🚀
