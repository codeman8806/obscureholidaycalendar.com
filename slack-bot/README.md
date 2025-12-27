# Obscure Holiday Slack Bot

## Setup (Railway or any Node 18+ host)

1) Install dependencies:
   - `npm install`

2) Set env vars:
   - `SLACK_BOT_TOKEN=<xoxb_...>`
   - `SLACK_SIGNING_SECRET=<signing_secret>`
   - `SLACK_APP_NAME=ObscureHolidayCalendar` (optional)
   - `PORT=8080` (Railway injects this)
   - Stripe (optional, for premium):
     - `STRIPE_SECRET_KEY=<sk_live_or_test>`
     - `STRIPE_PRICE_ID_INTRO=<price_0_99>`
     - `STRIPE_PRICE_ID_STANDARD=<price_3_99>`
     - `STRIPE_WEBHOOK_SECRET=<whsec_...>`
     - `STRIPE_SUCCESS_URL` / `STRIPE_CANCEL_URL`
     - `STRIPE_PORTAL_RETURN_URL`

3) Slack app config:
   - Slash commands: point to `https://<your-host>/slack/commands`
   - Stripe webhook endpoint: `https://<your-host>/stripe/webhook`
   - Enable Stripe events: `checkout.session.completed`, `invoice.paid`, `customer.subscription.updated`, `customer.subscription.deleted`

## Slash commands
- `/today`
- `/tomorrow`
- `/upcoming [days]`
- `/week [days]`
- `/date MM-DD`
- `/search <query>`
- `/random`
- `/facts [name or MM-DD]`
- `/setup key=value ...`
- `/premium`
- `/upgrade`
- `/manage`
- `/help`
- `/invite`
- `/vote`
- `/rate`
- `/support`
- `/app`

## /setup examples
- `/setup timezone=America/New_York hour=9 promotions=true`
- `/setup holiday_choice=1 skip_weekends=true`

Defaults:
- timezone: `UTC`
- hour: `9`
- holiday_choice: `0` (first holiday)
- skip_weekends: `false`
