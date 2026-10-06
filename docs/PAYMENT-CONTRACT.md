# PAYMENT CONTRACT
# Blueprint Chalamandra — SRAP Barrio Edition

## Proveedor candidato

dLocal

## Método principal

Google Pay

## Moneda objetivo

MXN

## Flujo

1. Usuario entra a Demo.
2. Usuario alcanza el CTA comercial.
3. Usuario inicia checkout.
4. Google Pay genera el token.
5. Frontend envía el token al backend.
6. Backend procesa el pago con el PSP.
7. PSP confirma el pago.
8. Backend registra la compra.
9. Backend genera autorización Premium.
10. Usuario recibe acceso Premium.

## Regla crítica

El navegador NUNCA decide que una compra fue exitosa.

Nunca usar como prueba de pago:

- localStorage
- sessionStorage
- initGame('full')
- gameMode
- unlockedLevels
- query parameters
- una URL pública /full/

## Estados de orden

CREATED
PENDING
APPROVED
REJECTED
CANCELLED
REFUNDED

## Identidad mínima de una orden

order_id
product_id
amount
currency
customer_email
provider
provider_payment_id
status
created_at
updated_at

## Producto inicial

blueprint-srap-barrio

## Acceso

Una compra APPROVED genera autorización Premium.

Una orden REJECTED / CANCELLED / REFUNDED NO genera acceso Premium.

## Webhook

La confirmación server-side del proveedor es la fuente de verdad para el estado final de la compra.

## Seguridad

No almacenar credenciales del proveedor en Git.

No almacenar secretos en JavaScript del navegador.

No confiar en datos enviados únicamente por el cliente.

## Producción

Antes de activar cobros reales:

- validar onboarding comercial
- validar KYC
- validar cuenta bancaria / liquidación
- validar métodos disponibles para México
- validar Google Pay en la cuenta merchant
- probar sandbox
- probar webhook
- probar pago aprobado
- probar pago rechazado
- probar reembolso
- probar revocación de acceso
