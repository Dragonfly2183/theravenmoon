"use server"

import { createHash } from "node:crypto"
import { cookies } from "next/headers"

import { getModel, parseSettings } from "./catalog"
import type { GenerationPlane } from "./catalog/types"
import {
  MissingCredentialsError,
  PLATFORM_KEY_COOKIE,
  PLATFORM_KEY_COOKIE_OPTIONS,
  decodeCredentials,
  encodeCredentials,
  parseCredentialInput,
  platformBaseUrl,
} from "./credentials"
import { DEVICE_COOKIE } from "./device"
import { describeFailure } from "./errors"
import type { ActionResult } from "./errors"
import { createPlatformClient } from "./platform"
import type { QueuedGeneration, StatusResult } from "./platform"
import { createSubmitGuard } from "./submit-guard"
import { toPlatform } from "./to-platform"

const submitGuard = createSubmitGuard<QueuedGeneration>()

export async function savePlatformCredentials(
  data: unknown
): Promise<ActionResult<object>> {
  let apiKey: string
  try {
    apiKey = parseCredentialInput(data).apiKey
  } catch (caught) {
    return {
      ok: false,
      error: caught instanceof Error ? caught.message : "Enter an API key",
      transient: false,
    }
  }
  const jar = await cookies()
  jar.set(
    PLATFORM_KEY_COOKIE,
    encodeCredentials(apiKey),
    PLATFORM_KEY_COOKIE_OPTIONS
  )
  return { ok: true }
}

export async function clearPlatformCredentials() {
  const jar = await cookies()
  jar.set(PLATFORM_KEY_COOKIE, "", {
    ...PLATFORM_KEY_COOKIE_OPTIONS,
    maxAge: 0,
  })
}

export async function hasPlatformCredentials() {
  return (await readStoredCredentials()) !== null
}

/** Submits once. Never retried here: after an ambiguous failure the job may
    already exist, and a second POST would start (and bill) another one. */
export async function submitGeneration(
  plane: GenerationPlane
): Promise<ActionResult<{ queued: QueuedGeneration }>> {
  try {
    const model = getModel(plane.model)
    const parsed: GenerationPlane = {
      ...plane,
      settings: parseSettings(model, plane.settings),
    }
    const { path, body } = toPlatform(parsed)
    const credentials = await readCredentials()
    const device = (await cookies()).get(DEVICE_COOKIE)?.value ?? ""
    const key = createHash("sha256")
      .update(JSON.stringify([device, credentials.apiKey, path, body]))
      .digest("hex")
    const queued = await submitGuard(key, () =>
      createPlatformClient(credentials).submit(path, body)
    )
    return { ok: true, queued }
  } catch (caught) {
    return { ok: false, ...describeFailure(caught, "submit") }
  }
}

/** Every request in flight, answered in one round trip. Next dispatches server
    actions one at a time per client, so a poll per run would queue ahead of the
    next submit — the fan-out belongs on this side of the call, where it is
    genuinely parallel. */
export async function getGenerationStatuses(
  data: unknown
): Promise<ActionResult<{ results: StatusResult[] }>> {
  try {
    const requestIds = parseRequestIds(data)
    const client = createPlatformClient(await readCredentials())
    const results = await Promise.all(
      requestIds.map(async (requestId): Promise<StatusResult> => {
        try {
          return { requestId, status: await client.status(requestId) }
        } catch (caught) {
          return { requestId, ...describeFailure(caught, "status") }
        }
      })
    )
    return { ok: true, results }
  } catch (caught) {
    return { ok: false, ...describeFailure(caught, "status") }
  }
}

/** Cancel must reach the platform; stopping the poll alone leaves the job running. */
export async function cancelGeneration(
  data: unknown
): Promise<ActionResult<object>> {
  try {
    const [requestId] = parseRequestIds(data)
    await createPlatformClient(await readCredentials()).cancel(requestId!)
    return { ok: true }
  } catch (caught) {
    return { ok: false, ...describeFailure(caught, "cancel") }
  }
}

async function readStoredCredentials() {
  const jar = await cookies()
  return decodeCredentials(jar.get(PLATFORM_KEY_COOKIE)?.value)
}

async function readCredentials() {
  const stored = await readStoredCredentials()
  if (!stored) throw new MissingCredentialsError()
  return { ...stored, baseUrl: platformBaseUrl() }
}

function parseRequestIds(data: unknown): string[] {
  const payload = asObject(data, "Invalid status payload")
  const requestIds = payload.requestIds
  if (!Array.isArray(requestIds) || requestIds.length === 0) {
    throw new Error("Invalid request ids")
  }
  return requestIds.map((requestId) => {
    if (typeof requestId !== "string" || !requestId)
      throw new Error("Invalid request id")
    return requestId
  })
}

function asObject(data: unknown, message: string): Record<string, unknown> {
  if (data === null || typeof data !== "object" || Array.isArray(data))
    throw new Error(message)
  return data as Record<string, unknown>
}
