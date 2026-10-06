# Blueprint Chalamandra - SRAP Barrio Edition

Este es un proyecto web ligero y gamificado para el desarrollo personal, enfocado en manejar el caos y encontrar el flow.

## Estructura del Proyecto

```text
api/                  Endpoint provisional de checkout
assets/css/           Estilos
assets/js/            Lógica de la demo
demo/                 Aplicación web pública
docs/                 Oferta y contratos de flujo de pago
tests/                Pruebas de interacción y captura
```

La versión completa no está incluida en el árbol público. El checkout en `api/checkout.js` es provisional y responde `501`; no se procesan pagos ni se emiten autorizaciones Premium.

## Cómo ejecutar

Abre `demo/index.html`, o ejecuta `npm run dev` y visita `http://localhost:8000/demo/`.

`npm test` ejecuta la prueba de interacción. Para ejecutar también la prueba de captura, usa `npm run test:all`. Las pruebas requieren Python 3, Playwright para Python y Chromium.

## Tecnologías

- HTML5
- CSS3 (con Tailwind CSS vía CDN)
- JavaScript (Vanilla)
- API serverless de Vercel (checkout aún no configurado)
