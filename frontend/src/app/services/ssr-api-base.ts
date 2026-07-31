// Server-side (SSR) API base URL.
//
// When Angular renders on the Node/Express server it cannot use the public
// `environment.apiUrl` (that host may not be reachable from inside the server),
// so it calls the backend directly. In `docker-compose up` the backend is
// reachable as the compose service name `backend:8000`, but in a real
// production SSR deployment there is no such alias — set `SSR_API_URL` in the
// SSR process environment (e.g. `http://127.0.0.1:8000/api`) so server-side
// fetches resolve. Falls back to the compose alias so local dev keeps working.
export function ssrApiBase(): string {
  // Read via globalThis so this compiles without Node type defs (the unit-test
  // tsconfig has none) while still resolving process.env on the SSR server.
  const env = (globalThis as { process?: { env?: Record<string, string | undefined> } }).process
    ?.env;
  const fromEnv = env?.['SSR_API_URL'];
  return fromEnv && fromEnv.trim() ? fromEnv.trim().replace(/\/$/, '') : 'http://backend:8000/api';
}
