/**
 * Server-side guard against accidental duplicate generations: the same payload
 * from the same browser within `windowMs` shares the first submission's
 * outcome instead of starting (and paying for) a second job. A failed or
 * ambiguous submission is shared too, so a double-click never retries blindly.
 *
 * In-memory, so it covers one server process; a multi-instance deployment
 * needs a shared store (e.g. Redis) behind the same interface.
 */
export function createSubmitGuard<T>(windowMs = 10_000) {
  const entries = new Map<string, { at: number; outcome: Promise<T> }>()

  return function guard(key: string, run: () => Promise<T>): Promise<T> {
    const now = Date.now()
    for (const [k, entry] of entries)
      if (now - entry.at > windowMs) entries.delete(k)
    const existing = entries.get(key)
    if (existing) return existing.outcome
    const outcome = run()
    entries.set(key, { at: now, outcome })
    return outcome
  }
}
