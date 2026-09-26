import assert from "node:assert/strict";
import { test } from "node:test";
import { describeFailure } from "../generation/errors.ts";
import { createSubmitGuard } from "../generation/submit-guard.ts";

const platformError = (status, body = null) =>
  Object.assign(new Error(`Platform request failed (${status})`), { name: "PlatformError", status, body });

test("platform failures become readable, correctly classified messages", () => {
  assert.match(describeFailure(platformError(401), "submit").error, /rejected your API key/);
  assert.equal(describeFailure(platformError(401), "submit").transient, false);
  assert.match(describeFailure(platformError(402), "submit").error, /credits/);
  assert.equal(describeFailure(platformError(429), "status").transient, true);
  assert.equal(describeFailure(platformError(503), "status").transient, true);
  assert.match(describeFailure(platformError(409), "cancel").error, /can no longer be canceled/);
  assert.equal(describeFailure(platformError(422, { detail: "prompt is too long" }), "submit").error, "prompt is too long");
  assert.equal(
    describeFailure(platformError(422, { detail: [{ loc: ["body", "duration"], msg: "must be 5 or 10" }] }), "submit").error,
    "duration: must be 5 or 10",
  );
  const missing = Object.assign(new Error("x"), { name: "MissingCredentialsError" });
  assert.match(describeFailure(missing, "submit").error, /Connect your Higgsfield API key/);
});

test("a network failure on submit warns instead of inviting a blind retry", () => {
  const failure = describeFailure(new TypeError("fetch failed"), "submit");
  assert.match(failure.error, /Could not confirm/);
  assert.equal(describeFailure(new TypeError("fetch failed"), "status").transient, true);
});

test("the submit guard shares one outcome between duplicate submissions", async () => {
  const guard = createSubmitGuard(1000);
  let calls = 0;
  const run = () => Promise.resolve({ requestId: `r${++calls}` });
  const [a, b] = await Promise.all([guard("same", run), guard("same", run)]);
  assert.equal(calls, 1);
  assert.deepEqual(a, b);
  await guard("different", run);
  assert.equal(calls, 2);
});

test("the submit guard lets the same payload through again after its window", async () => {
  const guard = createSubmitGuard(5);
  let calls = 0;
  const run = () => Promise.resolve(++calls);
  await guard("k", run);
  await new Promise((r) => setTimeout(r, 15));
  await guard("k", run);
  assert.equal(calls, 2);
});
