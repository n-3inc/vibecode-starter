import { Hono } from "hono"
import { cloudflareAccess } from "@hono/cloudflare-access"

const app = new Hono<{ Bindings: Env }>()

if (!import.meta.env.DEV) {
    app.use("*", async (c, next) => {
        if (!c.env.ACCESS_TEAM || !c.env.ACCESS_AUD) {
            return c.json(
                { error: "ACCESS_TEAM and ACCESS_AUD must be configured" },
                500,
            )
        }
        return cloudflareAccess(c.env.ACCESS_TEAM, c.env.ACCESS_AUD)(c, next)
    })
}

app.get("/api/", (c) => c.json({ name: "Cloudflare" }))

export default app
