const assert = require("node:assert/strict");
const test = require("node:test");

const checkout = require("../api/checkout");

function createResponse() {
  return {
    headers: {},
    statusCode: undefined,
    body: undefined,
    setHeader(name, value) {
      this.headers[name] = value;
    },
    status(code) {
      this.statusCode = code;
      return this;
    },
    json(body) {
      this.body = body;
      return this;
    },
  };
}

test("checkout rejects non-POST requests without caching", () => {
  const res = createResponse();

  checkout({ method: "GET" }, res);

  assert.equal(res.statusCode, 405);
  assert.deepEqual(res.body, { error: "METHOD_NOT_ALLOWED" });
  assert.equal(res.headers.Allow, "POST");
  assert.equal(res.headers["Cache-Control"], "no-store");
});

test("checkout reports that payment processing is not configured", () => {
  const res = createResponse();

  checkout({ method: "POST" }, res);

  assert.equal(res.statusCode, 501);
  assert.deepEqual(res.body, {
    ok: false,
    error: "CHECKOUT_NOT_CONFIGURED",
    product_id: "blueprint-srap-barrio",
  });
  assert.equal(res.headers["Cache-Control"], "no-store");
});
