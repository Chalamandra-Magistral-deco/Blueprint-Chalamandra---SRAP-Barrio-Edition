module.exports = (req, res) => {
  res.setHeader("Cache-Control", "no-store");

  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "METHOD_NOT_ALLOWED" });
  }

  return res.status(501).json({
    ok: false,
    error: "CHECKOUT_NOT_CONFIGURED",
    product_id: "blueprint-srap-barrio",
  });
};
