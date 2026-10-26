# Contrato técnico — SRAP Autoservicio v1

**Estado:** propuesta técnica; no habilita cobros ni declara el producto listo para producción.  
**Alcance:** preparar un flujo verificable de experiencia SRAP de autoservicio, pago único y entrega protegida, sin reemplazar la metodología ni inventar una puntuación.

## 1. Hallazgos confirmados en el repositorio

La revisión de `main` encontró:

- `demo/index.html` presenta la experiencia SRAP y niveles de una demo.
- `assets/js/script.js` persiste el progreso en `localStorage` mediante la clave `chalamandra_state`. El modo demo bloquea niveles desde el cliente.
- `api/checkout.js` rechaza métodos distintos de POST y devuelve `501 CHECKOUT_NOT_CONFIGURED` para POST.
- `tests/api-checkout.test.js` comprueba ambos comportamientos del endpoint provisional.
- `README.md` declara que el checkout es provisional y que no procesa pagos ni emite autorizaciones Premium.

Estas piezas prueban una demo interactiva, no un diagnóstico calculado de extremo a extremo ni un sistema de autorización de compras. El estado del navegador no debe ser fuente de verdad para conceder Premium.

## 2. Objetivo de v1

Permitir que una persona complete una experiencia guiada SRAP, reciba un resultado descriptivo que corresponda únicamente a reglas documentadas, y —tras un pago verificado— obtenga el entregable premium comprado.

La nomenclatura visible actual de SRAP es:

1. **SCAN:** observar qué está frenando a la persona y nombrar un impulso sin juzgarlo.
2. **RESPIRA:** hacer una pausa breve e identificar el sentimiento raíz.
3. **ALINEA:** paso presente en la demo; el instrumento completo y sus criterios aún deben especificarse.
4. **PAUSA:** figura en la expansión metodológica propuesta; debe comprobarse contra la versión canónica de la metodología antes de venderse como evaluación formal.

**No se fija una puntuación, ponderación, umbral ni afirmación diagnóstica nueva en este contrato.** Hasta que la metodología y las reglas estén documentadas y probadas, el resultado debe llamarse reflexión o resumen de actividad, no una medición validada ni un diagnóstico clínico.

## 3. Separación de responsabilidades

- **Demo pública:** puede ejecutar interacciones educativas, pero no concede derechos de compra.
- **API de checkout:** valida el producto contra una lista permitida del servidor y solicita una sesión al proveedor de pagos.
- **Webhook de pagos:** verifica la firma con el secreto del webhook, verifica el estado de pago y procesa eventos de forma idempotente.
- **Persistencia de órdenes y entregables:** registra órdenes, estado, identificadores del proveedor, versión de producto y referencia al entregable. Debe tener una política de acceso definida.
- **API de acceso/entrega:** devuelve el material únicamente tras verificar la orden y la autorización del usuario o un enlace de acceso firmado, según el mecanismo que se implemente.
- **Generador de informe:** transforma respuestas estructuradas en un entregable; no modifica reglas SRAP por inferencia no aprobada.
- **Panel operativo:** registra conversión, errores, entregas y reembolsos sin volcar respuestas sensibles o secretos en logs.

No se asume que un servicio externo, un proveedor de correo o una base de datos ya estén conectados a este repositorio.

## 4. Contrato de API propuesto

### `POST /api/checkout`

Solicitud mínima:

```json
{
  "product_id": "srap-reflection-report-v1"
}
```

Reglas:

- Solo acepta POST y devuelve `Cache-Control: no-store`.
- Rechaza campos desconocidos o `product_id` que no figure en la lista permitida del servidor.
- El precio, la moneda, el modo de pago y las URLs de retorno vienen de configuración del servidor; nunca del navegador.
- No acepta una URL de retorno arbitraria ni información de tarjeta en el cuerpo.
- Si faltan configuración o proveedor de pagos, responde con error controlado sin intentar cobrar.
- No comunica que el acceso está concedido por el simple retorno del navegador.
- Los errores del proveedor se registran sin exponer claves, cabeceras de autorización o payloads sensibles.

Respuesta de éxito propuesta:

```json
{
  "ok": true,
  "checkout_url": "https://checkout.example/...",
  "session_id": "cs_..."
}
```

Los valores del ejemplo son ilustrativos, no credenciales ni endpoints activos.

### Webhook

El webhook solo acepta eventos firmados. Para este producto de pago único, la concesión requiere un evento compatible con el flujo configurado y una sesión cuyo estado de pago sea efectivamente pagado. Un evento duplicado no debe duplicar órdenes ni entregas. Los eventos fallidos, vencidos, pendientes o sin pagar no conceden acceso.

El nombre exacto del evento, la política de pagos asíncronos y el contrato del proveedor deben implementarse y probarse al elegir el proveedor.

### Acceso / entrega

El navegador no puede autorizarse modificando `localStorage`, parámetros de URL o variables JavaScript. Un resultado premium debe entregarse desde un endpoint que verifique la orden o una credencial de acceso firmada y revocable. La página de retorno de checkout es informativa; no sustituye la verificación de pago.

## 5. Modelo de datos mínimo a diseñar antes del cobro real

La implementación deberá persistir, como mínimo:

- **orders:** identificador interno, proveedor, sesión/orden del proveedor única, producto y versión, estado del pago, fecha de creación y fecha de actualización.
- **payment_events:** identificador del evento del proveedor único, tipo, estado de procesamiento, fecha y resultado técnico no sensible.
- **deliverables:** orden asociada, tipo, referencia privada al resultado, estado de entrega y fecha.
- **assessment_runs** (si se recopilan respuestas): identificador aleatorio, versión de metodología/reglas, entradas necesarias, resultado reproducible y política de retención.

Los estados de pago y de entrega son distintos: un cobro confirmado con entrega fallida debe quedar visible para reintento o soporte, no fingir una entrega exitosa. El motor no debe guardar datos personales innecesarios. La política de borrado, exportación y acceso se definirá antes de aceptar respuestas reales.

## 6. Seguridad y privacidad no negociables

- Secretos solo en variables de servidor; nunca en archivos estáticos ni variables que se publiquen al cliente.
- Verificación criptográfica de firma del webhook y validación de esquema.
- Lista permitida de productos y precios configurada exclusivamente en el servidor.
- Idempotencia para sesión de pago, evento y entrega.
- Sin autorización premium basada solo en HTML, JavaScript o `localStorage`.
- Sin registro de datos de tarjeta ni secretos de proveedor en la aplicación.
- Enlace de entrega limitado, revocable y con vencimiento o autenticación de cuenta.
- Consentimiento y política de privacidad claros antes de almacenar respuestas.
- No presentar la experiencia como diagnóstico médico o evaluación validada sin evidencia y autorización de la metodología.
- No habilitar cobros mientras falte una ruta funcional de acceso, soporte y reembolso.

## 7. Pruebas de aceptación para habilitar el cobro

### Checkout
- GET y otros métodos no permitidos responden 405.
- Configuración incompleta responde de forma controlada y no crea una sesión.
- SKU desconocido, precio enviado desde el cliente, campos inesperados o retorno arbitrario se rechazan.
- Los errores del proveedor no filtran secretos.
- Solo una solicitud válida genera una sesión con el producto/precio configurado.

### Webhook y autorización
- Una firma incorrecta se rechaza.
- Una sesión pendiente, cancelada o sin pagar no concede Premium.
- Un evento válido de pago confirmado crea o actualiza la orden y es idempotente.
- El mismo evento enviado varias veces genera una sola concesión y una sola entrega lógica.
- Una orden de otra persona o una referencia manipulada no permite consultar el entregable.
- Reembolso y disputa se reflejan en el estado de autorización conforme a la política aprobada.

### Entrega y experiencia
- Existe una prueba de extremo a extremo en entorno de test: completar actividad → checkout de prueba → evento verificado → orden persistida → entregable disponible.
- Se comprueba la recuperación de una entrega fallida y se puede identificar la transacción sin exponer contenido privado.
- Se confirma que la demo pública sigue funcionando y que el pago no altera su estado local.
- Build y pruebas existentes pasan sin regresiones.

## 8. Decisiones necesarias antes de activar el producto

1. **Entregable exacto:** informe de reflexión descargable, acceso a niveles premium u otro producto. No mezclar estos productos en una misma clave de compra.
2. **Método de precio:** importe, moneda, impuestos, reembolsos y términos comerciales.
3. **Proveedor de pago y entorno:** test y producción separados.
4. **Persistencia y acceso:** elegir una base de datos y definir autenticación o mecanismo de enlace seguro.
5. **Entrega:** canal, formato, tratamiento de fallos y soporte.
6. **Contenido y metodología:** especificar el instrumento SRAP, entradas, reglas, limitaciones y pruebas reproducibles.
7. **Privacidad:** datos a recoger, consentimiento, retención y eliminación.

## 9. Secuencia de implementación

- **Fase A — especificación:** cerrar entregable, reglas SRAP, precio y política de datos.
- **Fase B — persistencia y autorización:** implementar órdenes y entregables privados; probar los controles de acceso.
- **Fase C — pagos en test:** crear checkout, validar webhook firmado e idempotencia.
- **Fase D — entrega:** construir el entregable y reparar/reintentar fallos.
- **Fase E — pruebas de extremo a extremo:** verificar flujo completo y regresiones.
- **Fase F — producción:** configurar secretos y webhook en el proveedor, verificar monitorización y soporte, y habilitar ventas solo después de superar los criterios.

**Estado de este PR:** solo especificación. No se habilitan cobros, no se publican secretos, no se concede acceso Premium y no se modifican archivos existentes.
