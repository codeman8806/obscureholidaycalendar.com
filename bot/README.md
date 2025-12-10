# Obscure Holiday Discord Bot

Node.js Discord bot that answers holiday questions using `holidays.json`.

## Features
- Slash commands (Discord highlights these):
  - `/today` — today’s holiday
  - `/date MM-DD` — holiday on a specific date (e.g., `12-08`)
  - `/search <query>` — search by name/keywords
  - `/random` — random holiday
  - `/facts <name|MM-DD>` — quick fun facts
  - `/help` — list commands
- Presence/status set on startup (“Watching obscure holidays”).
- Optional daily auto-post to a channel at 00:05 (local time).

## Setup
1) Create a Discord application + bot at https://discord.com/developers/applications  
   - Enable **Message Content Intent** is NOT required for slash commands.  
   - Copy the bot token.
2) In this `bot/` folder:  
   - `npm install`  
   - Set env:  
     - `DISCORD_BOT_TOKEN=your_token_here`  
     - Optional: `DAILY_CHANNEL_ID=<channel_id>` to enable daily auto-post at 00:05.  
     - Optional: `GUILD_ID=<guild_id>` to register slash commands to one guild for instant availability (otherwise they register globally and may take a few minutes).  
   - Run `npm start`.
3) Invite the bot to your server using the OAuth URL with `bot` scope and at least `Send Messages` / `Embed Links` permissions.

## Hosting tips
- Any Node 18+ host works (Railway/Render/Fly/Heroku-style dyno).  
- Mount/sync `holidays.json` alongside the bot (it reads `../holidays.json`).  
- Keep the bot token secret; use host-level secrets/env vars.
