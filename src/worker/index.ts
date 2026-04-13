import { Hono } from "hono"
import { cloudflareAccess } from "@hono/cloudflare-access"

const app = new Hono<{ Bindings: Env }>()

if (!import.meta.env.DEV) {
    app.use("*", async (c, next) =>
        cloudflareAccess(c.env.ACCESS_TEAM, c.env.ACCESS_AUD)(c, next),
    )
}

app.get("/api/", (c) => c.json({ name: "Cloudflare" }))

export default app
