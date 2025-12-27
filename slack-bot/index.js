import crypto from "crypto";
import express from "express";
import fs from "fs";
import path from "path";
import Stripe from "stripe";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PORT = process.env.PORT || 8080;
const SLACK_SIGNING_SECRET = (process.env.SLACK_SIGNING_SECRET || "").trim() || null;
const SLACK_APP_NAME = process.env.SLACK_APP_NAME || "ObscureHolidayCalendar";
const SLACK_CLIENT_ID = process.env.SLACK_CLIENT_ID || null;
const SLACK_CLIENT_SECRET = process.env.SLACK_CLIENT_SECRET || null;
const SLACK_OAUTH_SCOPES = process.env.SLACK_OAUTH_SCOPES || "commands,chat:write";
const SLACK_REDIRECT_URI = process.env.SLACK_REDIRECT_URI || null;

const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY || null;
const STRIPE_PRICE_ID_INTRO = process.env.STRIPE_PRICE_ID_INTRO || null;
const STRIPE_PRICE_ID_STANDARD = process.env.STRIPE_PRICE_ID_STANDARD || process.env.STRIPE_PRICE_ID || null;
const STRIPE_WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET || null;
const STRIPE_SUCCESS_URL = process.env.STRIPE_SUCCESS_URL || null;
const STRIPE_CANCEL_URL = process.env.STRIPE_CANCEL_URL || null;
const STRIPE_PORTAL_RETURN_URL = process.env.STRIPE_PORTAL_RETURN_URL || null;

const stripeClient = STRIPE_SECRET_KEY ? new Stripe(STRIPE_SECRET_KEY) : null;

const SITE_URL = process.env.SITE_URL || null;
const SITE_BASE = SITE_URL ? `${SITE_URL}/holiday` : null;
const APP_URL = process.env.APP_URL || (SITE_URL ? `${SITE_URL}/app/` : null);
const SUPPORT_URL = process.env.SLACK_SUPPORT_URL || (SITE_URL ? `${SITE_URL}/slack-bot/` : null);
const TOPGG_VOTE_URL = process.env.SLACK_VOTE_URL || null;
const TOPGG_REVIEW_URL = process.env.SLACK_REVIEW_URL || null;

const CONFIG_PATH = path.resolve(__dirname, "workspace-config.json");
const PREMIUM_PATH = path.resolve(__dirname, "premium.json");
const WORKSPACE_TOKENS_PATH = path.resolve(__dirname, "workspace-tokens.json");

const DEFAULT_TIMEZONE = "UTC";
const DEFAULT_HOUR = 9;
const DEFAULT_HOLIDAY_CHOICE = 0;

function readJsonSafe(filePath, fallback) {
  try {
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, "utf8"));
    }
  } catch (e) {
    console.error(`Failed to read ${filePath}:`, e.message);
  }
  return fallback;
}

function writeJsonSafe(filePath, data) {
  try {
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), "utf8");
  } catch (e) {
    console.error(`Failed to write ${filePath}:`, e.message);
  }
}

const workspaceConfig = readJsonSafe(CONFIG_PATH, {});
const premiumAllowlist = readJsonSafe(PREMIUM_PATH, {});
const workspaceTokens = readJsonSafe(WORKSPACE_TOKENS_PATH, {});

function resolveHolidaysPath() {
  const local = path.resolve(__dirname, "holidays.json");
  if (fs.existsSync(local)) return local;
  const root = path.resolve(__dirname, "..", "holidays.json");
  if (fs.existsSync(root)) return root;
  throw new Error("holidays.json not found. Place it in slack-bot/ or repo root.");
}

function loadHolidays() {
  const raw = fs.readFileSync(resolveHolidaysPath(), "utf8");
  const data = JSON.parse(raw);
  return data.holidays || {};
}

const holidaysByDate = loadHolidays();
const allHolidays = Object.values(holidaysByDate).flat();

function normalizeName(text) {
  return (text || "")
    .toLowerCase()
    .replace(/&/g, "and")
    .replace(/['’]/g, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

function buildNameToSlug() {
  const map = {};
  const holidayDir = path.resolve(__dirname, "..", "holiday");
  if (!fs.existsSync(holidayDir)) return map;
  for (const entry of fs.readdirSync(holidayDir)) {
    const page = path.join(holidayDir, entry, "index.html");
    if (!fs.existsSync(page)) continue;
    const html = fs.readFileSync(page, "utf8");
    const h1 = html.match(/<h1[^>]*>(.*?)<\/h1>/s);
    const title = h1 ? h1[1].replace(/<[^>]+>/g, "").trim() : null;
    if (title) map[normalizeName(title)] = entry;
  }
  return map;
}

const nameToSlug = buildNameToSlug();

function findByDate(mmdd) {
  return holidaysByDate[mmdd] || [];
}

function findByName(query) {
  const q = normalizeName(query);
  if (!q) return [];
  return allHolidays.filter((h) => normalizeName(h.name || "").includes(q));
}

function toMMDD(date) {
  const mm = String(date.getUTCMonth() + 1).padStart(2, "0");
  const dd = String(date.getUTCDate()).padStart(2, "0");
  return `${mm}-${dd}`;
}

function parseDateInput(input) {
  if (!input) return null;
  const match = input.trim().match(/^(\d{1,2})[/-](\d{1,2})$/);
  if (!match) return null;
  const mm = String(match[1]).padStart(2, "0");
  const dd = String(match[2]).padStart(2, "0");
  return `${mm}-${dd}`;
}

function holidayUrl(holiday) {
  const slug = nameToSlug[normalizeName(holiday.name || "")];
  if (!SITE_BASE) return SITE_URL || "";
  return slug ? `${SITE_BASE}/${slug}/` : SITE_URL || "";
}

function formatHoliday(holiday, mmdd) {
  if (!holiday) return "No holiday found.";
  const emoji = holiday.emoji ? `${holiday.emoji} ` : "";
  const dateLine = mmdd ? `(${mmdd})` : "";
  const link = holidayUrl(holiday);
  return `${emoji}*${holiday.name || "Holiday"}* ${dateLine}\n${holiday.description || ""}\n${link}`;
}

function isPremiumTeam(teamId) {
  return Boolean(premiumAllowlist[teamId]);
}

function ensureWorkspace(teamId) {
  if (!workspaceConfig[teamId]) {
    workspaceConfig[teamId] = {
      channelId: null,
      timezone: DEFAULT_TIMEZONE,
      hour: DEFAULT_HOUR,
      holidayChoice: DEFAULT_HOLIDAY_CHOICE,
      skipWeekends: false,
      promotionsEnabled: true,
      lastPostedDate: null,
    };
  }
  return workspaceConfig[teamId];
}

function parseSetupArgs(text) {
  const out = {};
  if (!text) return out;
  const parts = text.split(/\s+/);
  for (const part of parts) {
    const [key, rawVal] = part.split("=");
    if (!key || rawVal == null) continue;
    const val = rawVal.trim();
    out[key.toLowerCase()] = val;
  }
  return out;
}

function parseHolidayChoice(text) {
  if (!text) return null;
  const lower = text.toLowerCase();
  if (lower.includes("2") || lower.includes("second")) return 1;
  if (lower.includes("1") || lower.includes("first")) return 0;
  return null;
}

function getLocalParts(timeZone) {
  const now = new Date();
  const fmt = new Intl.DateTimeFormat("en-US", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
  }).formatToParts(now);
  const get = (type) => fmt.find((p) => p.type === type)?.value || "";
  return {
    year: get("year"),
    month: get("month"),
    day: get("day"),
    hour: Number(get("hour")),
    minute: Number(get("minute")),
    ymd: `${get("year")}-${get("month")}-${get("day")}`,
    weekday: new Intl.DateTimeFormat("en-US", { timeZone, weekday: "short" }).format(now),
  };
}

async function slackPostMessage(channel, text) {
  const token = channel.teamId ? workspaceTokens[channel.teamId]?.access_token : null;
  if (!token) return;
  await fetch("https://slack.com/api/chat.postMessage", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json; charset=utf-8",
    },
    body: JSON.stringify({ channel: channel.id || channel, text }),
  });
}

async function handleDailyPosts() {
  for (const [teamId, config] of Object.entries(workspaceConfig)) {
    if (!config.channelId) continue;
    if (!workspaceTokens[teamId]?.access_token) continue;
    const tz = config.timezone || DEFAULT_TIMEZONE;
    const parts = getLocalParts(tz);
    if (config.skipWeekends && (parts.weekday === "Sat" || parts.weekday === "Sun")) continue;
    if (parts.hour !== Number(config.hour) || parts.minute !== 0) continue;
    if (config.lastPostedDate === parts.ymd) continue;

    const mmdd = `${parts.month}-${parts.day}`;
    const hits = findByDate(mmdd);
    if (!hits.length) continue;
    const choice = Math.min(config.holidayChoice || 0, hits.length - 1);
    const holiday = hits[choice];
    const text = formatHoliday(holiday, mmdd);
    await slackPostMessage({ id: config.channelId, teamId }, text);
    config.lastPostedDate = parts.ymd;
    writeJsonSafe(CONFIG_PATH, workspaceConfig);
  }
}

async function createPremiumCheckoutSession({ teamId, userId }) {
  if (
    !stripeClient ||
    !STRIPE_PRICE_ID_INTRO ||
    !STRIPE_PRICE_ID_STANDARD ||
    !STRIPE_SUCCESS_URL ||
    !STRIPE_CANCEL_URL
  )
    return null;
  return stripeClient.checkout.sessions.create({
    mode: "subscription",
    line_items: [{ price: STRIPE_PRICE_ID_INTRO, quantity: 1 }],
    success_url: STRIPE_SUCCESS_URL,
    cancel_url: STRIPE_CANCEL_URL,
    metadata: { team_id: teamId, user_id: userId || "" },
    subscription_data: { metadata: { team_id: teamId, user_id: userId || "" } },
  });
}

function subscriptionNeedsUpgrade(sub) {
  const items = sub.items?.data || [];
  const hasIntro = items.some((item) => item?.price?.id === STRIPE_PRICE_ID_INTRO);
  const hasStandard = items.some((item) => item?.price?.id === STRIPE_PRICE_ID_STANDARD);
  return hasIntro && !hasStandard;
}

async function upgradeSubscriptionToStandard(subId) {
  if (!stripeClient || !STRIPE_PRICE_ID_STANDARD || !STRIPE_PRICE_ID_INTRO) return;
  const sub = await stripeClient.subscriptions.retrieve(subId);
  if (!subscriptionNeedsUpgrade(sub)) return;
  const introItem = sub.items?.data?.find((item) => item?.price?.id === STRIPE_PRICE_ID_INTRO);
  if (!introItem) return;
  await stripeClient.subscriptions.update(subId, {
    items: [{ id: introItem.id, price: STRIPE_PRICE_ID_STANDARD }],
    proration_behavior: "none",
  });
}

async function listSubscriptionsByPrice(priceId) {
  if (!stripeClient || !priceId) return [];
  const subs = [];
  let startingAfter = null;
  while (true) {
    const page = await stripeClient.subscriptions.list({
      status: "active",
      price: priceId,
      limit: 100,
      starting_after: startingAfter || undefined,
    });
    subs.push(...page.data);
    if (!page.has_more) break;
    startingAfter = page.data[page.data.length - 1].id;
  }
  return subs;
}

async function findActiveSubscriptionForTeam(teamId) {
  if (!stripeClient || !teamId) return null;
  let startingAfter = null;
  while (true) {
    const page = await stripeClient.subscriptions.list({
      status: "active",
      limit: 100,
      starting_after: startingAfter || undefined,
    });
    for (const sub of page.data) {
      if (sub.metadata?.team_id === teamId) return sub;
    }
    if (!page.has_more) break;
    startingAfter = page.data[page.data.length - 1].id;
  }
  return null;
}

async function syncPremiumFromStripe() {
  if (!stripeClient || !STRIPE_PRICE_ID_STANDARD) return;
  try {
    const standardSubs = await listSubscriptionsByPrice(STRIPE_PRICE_ID_STANDARD);
    const introSubs = STRIPE_PRICE_ID_INTRO ? await listSubscriptionsByPrice(STRIPE_PRICE_ID_INTRO) : [];
    for (const sub of [...standardSubs, ...introSubs]) {
      const teamId = sub.metadata?.team_id;
      if (teamId) {
        premiumAllowlist[teamId] = true;
      }
    }
    writeJsonSafe(PREMIUM_PATH, premiumAllowlist);
  } catch (err) {
    console.warn("Stripe sync failed:", err.message);
  }
}

function verifySlackSignature(req) {
  if (!SLACK_SIGNING_SECRET) return false;
  const timestamp = req.headers["x-slack-request-timestamp"];
  const signature = req.headers["x-slack-signature"];
  if (!timestamp || !signature) return false;
  const fiveMinutes = 60 * 5;
  const now = Math.floor(Date.now() / 1000);
  if (Math.abs(now - Number(timestamp)) > fiveMinutes) return false;
  const sigBase = `v0:${timestamp}:${req.rawBody || ""}`;
  const hmac = crypto.createHmac("sha256", SLACK_SIGNING_SECRET).update(sigBase).digest("hex");
  const computed = `v0=${hmac}`;
  return crypto.timingSafeEqual(Buffer.from(computed), Buffer.from(signature));
}

const app = express();

app.use(
  "/slack/commands",
  express.urlencoded({
    extended: false,
    verify: (req, res, buf) => {
      req.rawBody = buf.toString("utf8");
    },
  })
);

app.use("/stripe/webhook", express.raw({ type: "application/json" }));

app.get("/slack/install", (req, res) => {
  if (!SLACK_CLIENT_ID || !SLACK_REDIRECT_URI) {
    return res.status(400).send("Slack OAuth not configured.");
  }
  const url = new URL("https://slack.com/oauth/v2/authorize");
  url.searchParams.set("client_id", SLACK_CLIENT_ID);
  url.searchParams.set("scope", SLACK_OAUTH_SCOPES);
  url.searchParams.set("redirect_uri", SLACK_REDIRECT_URI);
  return res.redirect(url.toString());
});

app.get("/slack/oauth/callback", async (req, res) => {
  if (!SLACK_CLIENT_ID || !SLACK_CLIENT_SECRET || !SLACK_REDIRECT_URI) {
    return res.status(400).send("Slack OAuth not configured.");
  }
  const code = req.query.code;
  if (!code) return res.status(400).send("Missing code.");
  try {
    const body = new URLSearchParams({
      client_id: SLACK_CLIENT_ID,
      client_secret: SLACK_CLIENT_SECRET,
      code: String(code),
      redirect_uri: SLACK_REDIRECT_URI,
    });
    const resp = await fetch("https://slack.com/api/oauth.v2.access", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });
    const data = await resp.json();
    if (!data.ok) {
      console.warn("Slack OAuth failed:", data.error);
      return res.status(400).send("Slack OAuth failed.");
    }
    const teamId = data.team?.id;
    if (teamId) {
      workspaceTokens[teamId] = {
        access_token: data.access_token,
        bot_user_id: data.bot_user_id,
        team_name: data.team?.name || "",
      };
      writeJsonSafe(WORKSPACE_TOKENS_PATH, workspaceTokens);
      ensureWorkspace(teamId);
      writeJsonSafe(CONFIG_PATH, workspaceConfig);
      console.log(`Slack OAuth installed for team ${teamId}`);
    }
    if (!SITE_URL) return res.status(500).send("SITE_URL not configured.");
    return res.redirect(`${SITE_URL}/slack-bot/installed.html`);
  } catch (err) {
    console.warn("Slack OAuth error:", err.message);
    return res.status(500).send("Slack OAuth error.");
  }
});

app.post("/slack/commands", async (req, res) => {
  if (!verifySlackSignature(req)) return res.status(401).send("Invalid signature");
  const { command, text, team_id, user_id, channel_id } = req.body || {};
  const teamId = team_id || "unknown";
  const config = ensureWorkspace(teamId);

  const respond = (message) => res.json({ response_type: "ephemeral", text: message });

  if (!command) return respond("Missing command.");

  const rawCmd = command.replace("/", "");
  const aliasMap = {
    ohsearch: "search",
    ohinvite: "invite",
    ohapp: "app",
  };
  const cmd = aliasMap[rawCmd] || rawCmd;
  const isPremium = isPremiumTeam(teamId);

  if (cmd === "help") {
    return respond(
      [
        "Holiday bot commands:",
        "/today",
        "/today 2 (premium: second holiday)",
        "/tomorrow (premium: add 2 for second holiday)",
        "/week [days] (premium)",
        "/upcoming [days] (premium)",
        "/date MM-DD (premium: add 2 for second holiday)",
        "/search <query> (premium) — or /ohsearch if /search is taken",
        "/random (premium)",
        "/facts [name or MM-DD] (premium)",
        "/setup key=value ...",
        "/premium [refresh]",
        "/upgrade",
        "/manage",
        "/invite — or /ohinvite if /invite is taken",
        "/vote",
        "/rate",
        "/support",
        "/app — or /ohapp if /app is taken",
      ].join("\n")
    );
  }

  if (cmd === "support") return respond(SUPPORT_URL ? `Support: ${SUPPORT_URL}` : "Support link not configured.");
  if (cmd === "app") return respond(APP_URL ? `App: ${APP_URL}` : "App link not configured.");
  if (cmd === "invite") return respond(SUPPORT_URL ? `Invite and setup: ${SUPPORT_URL}` : "Invite link not configured.");
  if (cmd === "vote") return respond(TOPGG_VOTE_URL ? `Vote: ${TOPGG_VOTE_URL}` : "Vote link not configured.");
  if (cmd === "rate") return respond(TOPGG_REVIEW_URL ? `Review: ${TOPGG_REVIEW_URL}` : "Review link not configured.");

  if (cmd === "premium") {
    if (isPremium) {
      return respond("✅ Premium is active for this workspace.");
    }
    const wantsRefresh = (text || "").toLowerCase().includes("refresh");
    if (stripeClient && wantsRefresh) {
      try {
        const sub = await findActiveSubscriptionForTeam(teamId);
        if (sub) {
          premiumAllowlist[teamId] = true;
          writeJsonSafe(PREMIUM_PATH, premiumAllowlist);
          console.log(`Premium refreshed from Stripe for team ${teamId}`);
          return respond("✅ Premium is active for this workspace.");
        }
        console.log(`Premium refresh found no active subscription for team ${teamId}`);
      } catch (e) {
        console.warn(`Premium refresh failed for team ${teamId}:`, e.message);
        // Ignore and fall through to default message.
      }
    }
    return respond("⚠️ Premium not active. Use /upgrade to subscribe.");
  }

  if (cmd === "upgrade") {
    if (!stripeClient || !STRIPE_PRICE_ID_INTRO || !STRIPE_PRICE_ID_STANDARD || !STRIPE_SUCCESS_URL || !STRIPE_CANCEL_URL) {
      return respond("Stripe is not configured.");
    }
    try {
      const session = await createPremiumCheckoutSession({ teamId, userId: user_id });
      return respond(`Upgrade to premium: ${session.url}`);
    } catch (e) {
      return respond("Unable to create checkout session right now.");
    }
  }

  if (cmd === "manage") {
    if (!stripeClient || !STRIPE_PORTAL_RETURN_URL) return respond("Stripe is not configured.");
    try {
      const subs = await stripeClient.subscriptions.list({ status: "active", limit: 100 });
      const sub = subs.data.find((s) => s.metadata?.team_id === teamId);
      const customerId = sub?.customer;
      if (!customerId) return respond("No active subscription found.");
      const portal = await stripeClient.billingPortal.sessions.create({
        customer: customerId,
        return_url: STRIPE_PORTAL_RETURN_URL,
      });
      return respond(`Manage your subscription: ${portal.url}`);
    } catch (e) {
      return respond("Unable to open the billing portal right now.");
    }
  }

  if (cmd === "setup") {
    const args = parseSetupArgs(text || "");
    config.channelId = channel_id;
    if (args.timezone && isPremium) config.timezone = args.timezone;
    if (args.hour && isPremium) config.hour = Math.min(Math.max(Number(args.hour), 0), 23);
    if (args.holiday_choice && isPremium) config.holidayChoice = Number(args.holiday_choice) ? 1 : 0;
    if (args.skip_weekends && isPremium) config.skipWeekends = args.skip_weekends === "true";
    if (args.promotions && isPremium) config.promotionsEnabled = args.promotions === "true";
    writeJsonSafe(CONFIG_PATH, workspaceConfig);
    return respond(
      `Saved. Channel: <#${config.channelId}>, timezone: ${config.timezone}, hour: ${config.hour}, holiday_choice: ${config.holidayChoice}`
    );
  }

  if (cmd === "today") {
    const mmdd = toMMDD(new Date());
    const hits = findByDate(mmdd);
    if (!hits.length) return respond("No holiday found for today.");
    let choice = 0;
    if (isPremium) {
      const requested = parseHolidayChoice(text);
      if (requested !== null) choice = Math.min(requested, hits.length - 1);
      else choice = Math.min(config.holidayChoice || 0, hits.length - 1);
    }
    return respond(formatHoliday(hits[choice], mmdd));
  }

  if (cmd === "tomorrow") {
    if (!isPremium) return respond("Premium required. Use /upgrade.");
    const d = new Date();
    d.setUTCDate(d.getUTCDate() + 1);
    const mmdd = toMMDD(d);
    const hits = findByDate(mmdd);
    if (!hits.length) return respond("No holiday found for tomorrow.");
    let choice = 0;
    const requested = parseHolidayChoice(text);
    if (requested !== null) choice = Math.min(requested, hits.length - 1);
    else choice = Math.min(config.holidayChoice || 0, hits.length - 1);
    return respond(formatHoliday(hits[choice], mmdd));
  }

  if (cmd === "date") {
    if (!isPremium) return respond("Premium required. Use /upgrade.");
    const mmdd = parseDateInput(text);
    if (!mmdd) return respond("Use MM-DD (e.g., 12-25).");
    const hits = findByDate(mmdd);
    if (!hits.length) return respond(`No holidays found on ${mmdd}.`);
    let choice = 0;
    const requested = parseHolidayChoice(text);
    if (requested !== null) choice = Math.min(requested, hits.length - 1);
    else choice = Math.min(config.holidayChoice || 0, hits.length - 1);
    return respond(formatHoliday(hits[choice], mmdd));
  }

  if (cmd === "search") {
    if (!isPremium) return respond("Premium required. Use /upgrade.");
    if (!text) return respond("Provide a search query.");
    const hits = findByName(text).slice(0, 5);
    if (!hits.length) return respond("No matches found.");
    const lines = hits.map((h) => `• ${h.emoji || ""} ${h.name} — ${holidayUrl(h)}`);
    return respond(lines.join("\n"));
  }

  if (cmd === "random") {
    if (!isPremium) return respond("Premium required. Use /upgrade.");
    const pick = allHolidays[Math.floor(Math.random() * allHolidays.length)];
    return respond(formatHoliday(pick));
  }

  if (cmd === "facts") {
    if (!isPremium) return respond("Premium required. Use /upgrade.");
    let holiday = null;
    const parsed = parseDateInput(text || "");
    if (parsed) holiday = findByDate(parsed)[0];
    if (!holiday && text) holiday = findByName(text)[0];
    if (!holiday) holiday = findByDate(toMMDD(new Date()))[0];
    if (!holiday) return respond("No facts found.");
    const facts = Array.isArray(holiday.funFacts) ? holiday.funFacts.slice(0, 5) : [];
    if (!facts.length) return respond("No facts found.");
    const lines = facts.map((f) => `• ${f}`);
    return respond(`*${holiday.name}* fun facts:\n${lines.join("\n")}`);
  }

  if (cmd === "week" || cmd === "upcoming") {
    if (!isPremium) return respond("Premium required. Use /upgrade.");
    const days = Math.min(Math.max(Number(text || "7"), 3), 30);
    const list = [];
    const now = new Date();
    for (let i = 0; i < days; i++) {
      const d = new Date(now);
      d.setUTCDate(now.getUTCDate() + i);
      const mmdd = toMMDD(d);
      const hits = findByDate(mmdd);
      if (hits.length) list.push({ mmdd, holiday: hits[0] });
    }
    if (!list.length) return respond("No upcoming holidays found.");
    const lines = list.slice(0, 10).map(({ mmdd, holiday }) => `• ${mmdd} — ${holiday.emoji || ""} ${holiday.name}`);
    return respond(lines.join("\n"));
  }

  return respond(`Unknown command: ${cmd}`);
});

app.post("/stripe/webhook", async (req, res) => {
  if (!stripeClient || !STRIPE_WEBHOOK_SECRET) return res.status(400).send("Stripe not configured");
  const sig = req.headers["stripe-signature"];
  let event;
  try {
    event = stripeClient.webhooks.constructEvent(req.body, sig, STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }
  if (event.type === "checkout.session.completed") {
    const session = event.data.object;
    const teamId = session.metadata?.team_id;
    if (teamId) {
      premiumAllowlist[teamId] = true;
      writeJsonSafe(PREMIUM_PATH, premiumAllowlist);
      console.log(`Premium granted via Stripe for team ${teamId}`);
    }
  }
  if (event.type === "invoice.paid") {
    const invoice = event.data.object;
    const subId = invoice.subscription;
    if (subId && STRIPE_PRICE_ID_INTRO && STRIPE_PRICE_ID_STANDARD) {
      try {
        await upgradeSubscriptionToStandard(subId);
      } catch (err) {
        console.warn("Stripe subscription upgrade failed:", err.message);
      }
    }
  }
  res.json({ received: true });
});

app.get("/health", (req, res) => res.send("ok"));

app.listen(PORT, async () => {
  if (stripeClient) await syncPremiumFromStripe();
  setInterval(handleDailyPosts, 60 * 1000);
  console.log(`${SLACK_APP_NAME} Slack bot running on ${PORT}`);
});
