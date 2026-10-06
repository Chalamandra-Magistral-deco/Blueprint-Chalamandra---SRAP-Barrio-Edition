# MONEY FLOW — Blueprint Chalamandra SRAP Barrio Edition

## Producto
Blueprint Chalamandra — SRAP Barrio Edition

## Modelo
Demo gratuita → Oferta → Checkout → Pago confirmado → Acceso Premium → Entrega

## Producto gratuito
demo/index.html

## Producto premium
Contenido completo SRAP Barrio Edition

## Regla crítica
La autorización PREMIUM NO debe depender de:
- localStorage
- variables JavaScript manipulables
- initGame('full')
- parámetros enviados únicamente por el navegador
- una URL pública permanente hacia full/index.html

## Estado actual
El acceso premium es client-side y puede ser manipulado.

## Arquitectura objetivo

TRÁFICO
  ↓
DEMO
  ↓
OFERTA
  ↓
CHECKOUT
  ↓
PAGO CONFIRMADO
  ↓
WEBHOOK / VERIFICACIÓN
  ↓
REGISTRO DE COMPRA
  ↓
TOKEN / SESIÓN DE ACCESO
  ↓
PREMIUM
  ↓
ENTREGA

## Pago
Requisito comercial:
Google Pay como método de pago.

Google Pay requiere un procesador/PSP compatible.

## Requisito de seguridad
No publicar el contenido premium como recurso estático accesible sin autorización.

## Métricas
- visitas
- CTA clicks
- checkout iniciado
- pago aprobado
- ingreso bruto
- comisión
- ingreso neto
- acceso premium entregado
- recompra / upsell
