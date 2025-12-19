#!/usr/bin/env node
/**
 * Post slash commands to discordbotlist.com so they show on the bot page.
 *
 * Env vars required:
 *  - DBL_TOKEN: API token from discordbotlist.com (header: Authorization: Bot <token>)
 *  - DISCORD_BOT_ID: your bot user ID (snowflake)
 *
 * Usage:
 *   DBL_TOKEN=... DISCORD_BOT_ID=... node post_dbl_commands.js
 */
import { commandDefs } from "./commandDefs.js";

const token = process.env.DBL_TOKEN;
const botId = process.env.DISCORD_BOT_ID;

if (!token || !botId) {
  console.error("Missing DBL_TOKEN or DISCORD_BOT_ID env vars.");
  process.exit(1);
}

async function main() {
  const url = `https://discordbotlist.com/api/v1/bots/${botId}/commands`;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bot ${token}`,
    },
    body: JSON.stringify(commandDefs),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`dbl command post failed: ${res.status} ${text}`);
  }
  console.log(`Posted ${commandDefs.length} commands to discordbotlist.com for bot ${botId}`);
}

main().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
