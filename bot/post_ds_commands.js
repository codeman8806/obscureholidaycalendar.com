#!/usr/bin/env node
/**
 * Post slash commands to discordservices.net so they show on the bot page.
 *
 * Env vars required:
 *  - DISCORDSERVICES_TOKEN: API token from discordservices.net (Authorization header)
 *  - DISCORD_BOT_ID: your bot user ID (snowflake)
 *
 * Usage:
 *   DISCORDSERVICES_TOKEN=... DISCORD_BOT_ID=... node post_ds_commands.js
 */
import { commandDefs } from "./commandDefs.js";

const token = (process.env.DISCORDSERVICES_TOKEN || "").trim();
const botId = process.env.DISCORD_BOT_ID;

if (!token || !botId) {
  console.error("Missing DISCORDSERVICES_TOKEN or DISCORD_BOT_ID env vars.");
  process.exit(1);
}

async function postCommand(cmd) {
  const category = cmd.options && cmd.options.length ? "Slash" : "Utility";
  const payload = {
    command: `/${cmd.name}`,
    desc: cmd.description || "Slash command",
    category,
  };
  const res = await fetch(`https://api.discordservices.net/bot/${botId}/commands`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bot ${token}`,
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`POST /commands failed for /${cmd.name}: ${res.status} ${res.statusText} ${text || ""}`.trim());
  }
  return true;
}

async function main() {
  let success = 0;
  for (const cmd of commandDefs) {
    try {
      await postCommand(cmd);
      success++;
    } catch (err) {
      console.error(err.message || err);
    }
  }
  console.log(`Posted ${success}/${commandDefs.length} commands to discordservices.net for bot ${botId}`);
}

main().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
