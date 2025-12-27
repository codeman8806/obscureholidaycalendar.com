# Obscure Holiday Discord Bot

Node.js Discord bot that answers holiday questions using `holidays.json`.

## Features
- Slash commands (Discord highlights these):
  - `/today` — today’s holiday
  - `/date MM-DD` — holiday on a specific date (e.g., `12-08`)
  - `/search <query>` — search by name/keywords
  - `/random` — random holiday
  - `/facts <name|MM-DD>` — quick fun facts
  - `/invite` — get the bot invite link
  - `/support` — landing/help link
  - `/app` — app store/site links
  - `/setup` — configure daily posts (premium unlocks time/timezone/branding)
  - `/premium` — check your premium status
  - `/upgrade` — get a Stripe checkout link to upgrade
  - `/tomorrow` — tomorrow’s holiday (premium)
  - `/upcoming` — upcoming holidays (premium)
  - `/grantpremium` — owner only
  - `/installcount` — owner only
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
     - Optional: `BOT_INVITE_URL=https://discord.com/oauth2/authorize?client_id=1447955404142153789&permissions=2684438528&integration_type=0&scope=applications.commands+bot` (defaults to this if unset)  
     - Optional: `DAILY_CHANNEL_ID=<channel_id>` to enable daily auto-post at 00:05.  
     - Optional: `GUILD_ID=<guild_id>` to register slash commands to one guild for instant availability (otherwise they register globally and may take a few minutes).  
     - Optional: `SUPPORT_URL=https://www.obscureholidaycalendar.com/discord-bot/` to point `/support` to your landing page.
     - Optional: `BOT_OWNER_ID=<your_user_id>` for owner-only commands (`/grantpremium`, `/installcount`).
     - Optional: `PREMIUM_ROLE_ID=<role_id>` if using Discord Server Subscriptions for premium.
     - Optional: `TOPGG_TOKEN=<api_token>` to auto-post server counts to top.gg (global commands recommended; interval defaults to 30 min, override with `TOPGG_POST_INTERVAL_MIN`).
    - Optional Stripe (for paid premium):  
      - `STRIPE_SECRET_KEY=<sk_live_or_test>`  
      - `STRIPE_PRICE_ID_INTRO=<price_0_99>`  
      - `STRIPE_PRICE_ID_STANDARD=<price_3_99>`  
      - `STRIPE_WEBHOOK_SECRET=<whsec_...>`  
      - `STRIPE_SUCCESS_URL` / `STRIPE_CANCEL_URL` (defaults to your discord-bot page)  
      - `PORT` (Railway injects this; HTTP server listens here for Stripe/webhook)  
   - Run `npm start`.
3) Invite the bot to your server using the OAuth URL with `bot` scope and at least `Send Messages` / `Embed Links` permissions.

## Hosting tips
- Any Node 18+ host works (Railway/Render/Fly/Heroku-style dyno).  
- Mount/sync `holidays.json` alongside the bot (it reads `../holidays.json`).  
- Keep the bot token secret; use host-level secrets/env vars.
