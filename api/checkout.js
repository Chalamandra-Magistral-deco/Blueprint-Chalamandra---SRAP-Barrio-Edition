module.exports = (req, res) => {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "METHOD_NOT_ALLOWED" });
  }

  return res.status(501).json({
    ok: false,
    error: "CHECKOUT_NOT_CONFIGURED",
    product_id: "blueprint-srap-barrio"
  });
};
