/**
 * Turns platform failures into messages a person can act on. Server actions
 * return these instead of throwing: a production build replaces a thrown
 * server-action error with an opaque digest, so the message would be lost.
 */

export type PlatformPhase = "submit" | "status" | "cancel"

export type Failure = {
  error: string
  /** Worth asking again later (rate limit, outage, network). */
  transient: boolean
}

export type ActionResult<T> = ({ ok: true } & T) | ({ ok: false } & Failure)

export function describeFailure(
  caught: unknown,
  phase: PlatformPhase
): Failure {
  if (caught instanceof Error && caught.name === "MissingCredentialsError")
    return {
      error: "Connect your Higgsfield API key in the sidebar.",
      transient: false,
    }

  const status = statusOf(caught)
  if (status === undefined) {
    if (caught instanceof TypeError)
      return {
        error:
          phase === "submit"
            ? "Could not confirm that Higgsfield received this request. Check All Generations before generating again."
            : "Could not reach Higgsfield. Retrying shortly.",
        transient: true,
      }
    return {
      error: caught instanceof Error ? caught.message : String(caught),
      transient: false,
    }
  }

  const detail = detailOf(caught)
  if (status === 401)
    return {
      error:
        "Higgsfield rejected your API key. Use the key button in the sidebar to replace it.",
      transient: false,
    }
  if (status === 402)
    return {
      error:
        "Your Higgsfield account does not have enough credits for this generation.",
      transient: false,
    }
  if (status === 403)
    return {
      error: `Higgsfield refused this request (403). Check that your API key is active and can use this model.${detail ? ` ${detail}` : ""}`,
      transient: false,
    }
  if (status === 404)
    return {
      error:
        phase === "submit"
          ? "Higgsfield could not find this model endpoint."
          : "Higgsfield no longer knows this request.",
      transient: false,
    }
  if (status === 409 && phase === "cancel")
    return {
      error:
        "This generation has already started and can no longer be canceled.",
      transient: false,
    }
  if (status === 429)
    return {
      error: "Higgsfield rate limit reached. Wait a moment and try again.",
      transient: true,
    }
  if (status >= 500)
    return {
      error: `Higgsfield is having trouble right now (${status}). Try again shortly.`,
      transient: true,
    }
  return {
    error: detail ?? `Higgsfield rejected the request (${status}).`,
    transient: false,
  }
}

function statusOf(caught: unknown): number | undefined {
  if (caught === null || typeof caught !== "object") return undefined
  const status = (caught as { status?: unknown }).status
  return typeof status === "number" ? status : undefined
}

/** `detail` may be a string or a validation list ({ msg, loc }[]). */
function detailOf(caught: unknown): string | undefined {
  if (caught === null || typeof caught !== "object") return undefined
  const body = (caught as { body?: unknown }).body
  if (body === null || typeof body !== "object") return undefined
  const detail = (body as { detail?: unknown }).detail
  if (typeof detail === "string" && detail) return detail
  if (Array.isArray(detail)) {
    const parts = detail.flatMap((item) => {
      if (item === null || typeof item !== "object") return []
      const { msg, loc } = item as { msg?: unknown; loc?: unknown }
      if (typeof msg !== "string") return []
      const field = Array.isArray(loc) ? loc.filter((l) => l !== "body") : []
      return [field.length ? `${field.join(".")}: ${msg}` : msg]
    })
    if (parts.length) return parts.join("; ")
  }
  return undefined
}
