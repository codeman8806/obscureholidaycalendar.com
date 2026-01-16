import fs from "fs";
import path from "path";
import http from "http";
import express from "express";
import Stripe from "stripe";
import { fileURLToPath } from "url";
import {
  Client,
  GatewayIntentBits,
  Partials,
  EmbedBuilder,
  ActivityType,
  ActionRowBuilder,
  ButtonBuilder,
  ButtonStyle,
  PermissionsBitField,
  MessageFlags,
} from "discord.js";
import { commandDefs } from "./commandDefs.js";

const TOKEN = process.env.DISCORD_BOT_TOKEN;
const DAILY_CHANNEL_ID = process.env.DAILY_CHANNEL_ID || process.env.HOLIDAY_CHANNEL_ID || null;
const GUILD_ID = process.env.GUILD_ID || null; // optional: register commands to a single guild for faster propagation

if (!TOKEN) {
  console.error("Missing DISCORD_BOT_TOKEN env var.");
  process.exit(1);
}

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function resolveHolidaysPath() {
  // Option A: keep a copy next to the bot (./holidays.json)
  const local = path.resolve(__dirname, "holidays.json");
  if (fs.existsSync(local)) return local;

  // Fallback: root-level (../holidays.json)
  const root = path.resolve(__dirname, "..", "holidays.json");
  if (fs.existsSync(root)) {
    // If running from /bot and local is missing, copy it locally so Docker/hosted envs can read it
    try {
      fs.copyFileSync(root, local);
      console.log("Copied ../holidays.json into bot/holidays.json for runtime");
      return local;
    } catch (e) {
      console.warn("Failed to copy ../holidays.json into bot/:", e.message);
    }
    return root;
  }

  // Env override: allow explicit path if provided
  const envPath = process.env.HOLIDAYS_PATH;
  if (envPath && fs.existsSync(envPath)) return envPath;

  throw new Error("holidays.json not found. Place it in bot/ or repo root.");
}

const HOLIDAYS_PATH = resolveHolidaysPath();
const APP_URL = "https://www.obscureholidaycalendar.com/app/";
const SITE_URL = "https://www.obscureholidaycalendar.com";
const BOT_INVITE_URL =
  process.env.BOT_INVITE_URL ||
  "https://discord.com/oauth2/authorize?client_id=1447955404142153789&permissions=2684438528&integration_type=0&scope=applications.commands+bot";
const SUPPORT_URL = process.env.SUPPORT_URL || `${SITE_URL}/discord-bot/`;
const SLACK_BOT_URL = process.env.SLACK_BOT_URL || `${SITE_URL}/slack-bot/`;
const TOPGG_VOTE_URL = process.env.TOPGG_VOTE_URL || "https://top.gg/bot/1447955404142153789/vote";
const TOPGG_REVIEW_URL = process.env.TOPGG_REVIEW_URL || "https://top.gg/bot/1447955404142153789#reviews";
const PREMIUM_ROLE_ID = process.env.PREMIUM_ROLE_ID || null; // Discord Server Subscription role id
const CONFIG_PATH = process.env.GUILD_CONFIG_PATH
  ? path.resolve(__dirname, process.env.GUILD_CONFIG_PATH)
  : path.resolve(__dirname, "guild-config.json");
console.log(`GUILD_CONFIG_PATH env: ${process.env.GUILD_CONFIG_PATH || "(not set)"}`);
console.log(`Resolved guild config path: ${CONFIG_PATH}`);
const PREMIUM_PATH = path.resolve(__dirname, "premium.json"); // optional allowlist
const BOT_OWNER_ID = process.env.BOT_OWNER_ID || null;
const TOPGG_TOKEN = process.env.TOPGG_TOKEN || null; // for posting stats to top.gg
function normalizeApiToken(value) {
  if (!value) return null;
  const trimmed = value.trim();
  if (
    (trimmed.startsWith("\"") && trimmed.endsWith("\"")) ||
    (trimmed.startsWith("'") && trimmed.endsWith("'"))
  ) {
    return trimmed.slice(1, -1).trim() || null;
  }
  return trimmed || null;
}

const DISCORDSERVICES_TOKEN = normalizeApiToken(process.env.DISCORDSERVICES_TOKEN); // for posting stats to api.discordservices.net
const TOPGG_POST_INTERVAL_MIN = Number(process.env.TOPGG_POST_INTERVAL_MIN || "30");
const DISCORDSERVICES_POST_INTERVAL_MIN = Number(process.env.DISCORDSERVICES_POST_INTERVAL_MIN || TOPGG_POST_INTERVAL_MIN || "30");
const PORT = process.env.PORT || null; // for Railway/health checks (optional)
const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY || null;
const STRIPE_PRICE_ID_STANDARD = process.env.STRIPE_PRICE_ID_STANDARD || process.env.STRIPE_PRICE_ID || null; // $3.99/month
const STRIPE_PRICE_ID_INTRO = process.env.STRIPE_PRICE_ID_INTRO || null; // $0.99 first month
const STRIPE_LOOKUP_KEY = process.env.STRIPE_LOOKUP_KEY || null; // optional lookup key
const STRIPE_WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET || null;
const STRIPE_SUCCESS_URL = process.env.STRIPE_SUCCESS_URL || `${SITE_URL}/discord-bot/?success=1`;
const STRIPE_CANCEL_URL = process.env.STRIPE_CANCEL_URL || `${SITE_URL}/discord-bot/?canceled=1`;
const STRIPE_PORTAL_RETURN_URL = process.env.STRIPE_PORTAL_RETURN_URL || `${SITE_URL}/discord-bot/`;
const DEFAULT_HOLIDAY_CHOICE = 0; // which holiday of the day to schedule: 0 = first, 1 = second
const DEFAULT_EMBED_COLOR = 0x1c96f3;
const DEFAULT_EMBED_STYLE = "compact";
const DEFAULT_TIMEZONE = "UTC";
const PROMO_VOTE_INTERVAL_MS = 7 * 24 * 60 * 60 * 1000; // once per week per guild
const PROMO_RATE_INTERVAL_MS = 30 * 24 * 60 * 60 * 1000; // once per 30 days per guild
const DEFAULT_STREAK_GOAL = 7;
const FOLLOWUP_DELAY_MIN = Number(process.env.FOLLOWUP_DELAY_MIN || "45");
const DEFAULT_TONE = "default";
const ALLOWED_TONES = new Set(["wholesome", "silly", "nerdy", "historical", "global", "default"]);
const MAX_ANALYTICS_HISTORY = 120;
const FOOD_KEYWORDS = ["pizza", "burger", "chocolate", "cake", "coffee", "tea", "soup", "cheese", "ice cream", "taco", "donut", "bacon", "cookie", "bread", "pasta"];
const RELIGIOUS_KEYWORDS = ["christmas", "easter", "ramadan", "hanukkah", "diwali", "yom kippur", "lent", "ash wednesday", "saint", "holy", "religious"];
const WEIRD_KEYWORDS = ["weird", "absurd", "odd", "quirky", "strange", "silly", "goof", "bizarre", "random", "peculiar"];
const INTERNATIONAL_KEYWORDS = ["international", "world", "global"];
const SAFE_MODE_BLOCKLIST = ["adult", "sex", "drug", "alcohol", "beer", "wine", "weed", "marijuana", "violence", "gambling"];

function readJsonSafe(filePath, fallback) {
  try {
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, "utf8"));
    }
  } catch (e) {
    console.error(`Failed to read ${filePath}:`, e);
  }
  return fallback;
}

function writeJsonSafe(filePath, data) {
  try {
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), "utf8");
  } catch (e) {
    console.error(`Failed to write ${filePath}:`, e);
  }
}

const guildConfig = readJsonSafe(CONFIG_PATH, {});
const premiumAllowlist = readJsonSafe(PREMIUM_PATH, {});
const stripeClient = STRIPE_SECRET_KEY ? new Stripe(STRIPE_SECRET_KEY) : null;
const SITE_BASE = "https://www.obscureholidaycalendar.com/holiday";

function normalizeAllGuildConfigs() {
  let changed = false;
  let updatedGuilds = 0;
  const updatedGuildIds = [];
  Object.keys(guildConfig).forEach((guildId) => {
    const cfg = guildConfig[guildId] || {};
    let updated = false;
    if (!Array.isArray(cfg.channelIds)) {
      cfg.channelIds = [];
      changed = true;
      updated = true;
    }
    if (!cfg.channelSettings) {
      cfg.channelSettings = {};
      changed = true;
      updated = true;
    }
    if (typeof cfg.timezone !== "string") {
      cfg.timezone = DEFAULT_TIMEZONE;
      changed = true;
      updated = true;
    }
    if (!Number.isInteger(cfg.hour)) {
      cfg.hour = 0;
      changed = true;
      updated = true;
    }
    if (typeof cfg.branding !== "boolean") {
      cfg.branding = true;
      changed = true;
      updated = true;
    }
    if (typeof cfg.holidayChoice !== "number") {
      cfg.holidayChoice = DEFAULT_HOLIDAY_CHOICE;
      changed = true;
      updated = true;
    }
    if (typeof cfg.promotionsEnabled !== "boolean") {
      cfg.promotionsEnabled = true;
      changed = true;
      updated = true;
    }
    if (!cfg.lastVotePromptAt) {
      cfg.lastVotePromptAt = 0;
      changed = true;
      updated = true;
    }
    if (!cfg.lastRatePromptAt) {
      cfg.lastRatePromptAt = 0;
      changed = true;
      updated = true;
    }
    if (updated) {
      updatedGuilds += 1;
      updatedGuildIds.push(guildId);
    }
    guildConfig[guildId] = cfg;
  });
  if (changed) {
    writeJsonSafe(CONFIG_PATH, guildConfig);
    console.log(`Normalized guild-config.json on startup (${updatedGuilds} guild(s) updated): ${updatedGuildIds.join(", ")}`);
  }
}

function loadHolidays() {
  const raw = fs.readFileSync(HOLIDAYS_PATH, "utf8");
  const data = JSON.parse(raw);
  return data.holidays || {};
}

const holidaysByDate = loadHolidays();
const allHolidays = Object.values(holidaysByDate).flat();
normalizeAllGuildConfigs();

function isPremium(guild, member) {
  if (!guild) return false;
  // Discord Server Subscription role check on interacting member
  if (PREMIUM_ROLE_ID && member && member.roles && member.roles.cache.has(PREMIUM_ROLE_ID)) return true;
  // Allowlist fallback
  if (premiumAllowlist[guild.id]) return true;
  return false;
}

function isPremiumGuild(guild) {
  if (!guild) return false;
  if (premiumAllowlist[guild.id]) return true;
  if (PREMIUM_ROLE_ID) {
    const role = guild.roles.cache.get(PREMIUM_ROLE_ID);
    if (role && role.members && role.members.size > 0) return true;
  }
  return false;
}

function isOwner(userId) {
  if (!BOT_OWNER_ID) return false;
  return userId === BOT_OWNER_ID;
}

function setPremiumGuild(guildId, enabled) {
  if (!guildId) return;
  if (enabled) premiumAllowlist[guildId] = true;
  else delete premiumAllowlist[guildId];
  writeJsonSafe(PREMIUM_PATH, premiumAllowlist);
}

// Optional tiny HTTP server to satisfy platforms expecting a listening port (e.g., Railway "web" services)
const app = express();

async function postTopGGStats() {
  if (!TOPGG_TOKEN) return;
  try {
    const serverCount = client.guilds.cache.size;
    const botId = process.env.DISCORDSERVICES_BOT_ID || client.user?.id;
    if (!botId) return;
    const res = await fetch(`https://top.gg/api/bots/${botId}/stats`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: TOPGG_TOKEN,
      },
      body: JSON.stringify({ server_count: serverCount }),
    });
    if (!res.ok) {
      const text = await res.text();
      console.warn(`top.gg stats post failed: ${res.status} ${text}`);
    } else {
      console.log(`Posted stats to top.gg: ${serverCount} servers`);
    }
  } catch (e) {
    console.warn("top.gg stats post failed:", e.message);
  }
}

async function postDiscordServicesStats() {
  if (!DISCORDSERVICES_TOKEN) return;
  try {
    if (!client?.user) return;
    const botId = process.env.DISCORDSERVICES_BOT_ID || client.user.id;
    const serverCount = client.guilds.cache.size;
    const shardCount = Number(process.env.DISCORDSERVICES_SHARDS) || 1;
    const url = `https://api.discordservices.net/bot/${botId}/stats`;
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: DISCORDSERVICES_TOKEN,
      },
      body: JSON.stringify({
        servers: serverCount,
      }),
    });
    if (!res.ok) {
      const text = await res.text();
      console.error(
        "Discord Services stats post failed:",
        res.status,
        res.statusText,
        text
      );
      console.error(
        "Discord Services response headers:",
        Object.fromEntries(res.headers.entries())
      );
    } else {
      console.log(`Posted stats to discordservices.net: ${serverCount} servers`);
    }
  } catch (e) {
    console.warn("discordservices stats post failed:", e.message);
  }
}

function removeChannelFromConfig(guildId, channelId, reason) {
  const config = getGuildConfig(guildId);
  const before = config.channelIds || [];
  config.channelIds = before.filter((id) => id !== channelId);
  if (config.channelSettings && config.channelSettings[channelId]) {
    delete config.channelSettings[channelId];
  }
  saveGuildConfig();
  console.warn(`Removed channel ${channelId} from guild ${guildId} config (${reason}).`);
}

function isMissingAccessError(err) {
  const code = err?.code;
  const status = err?.status;
  return code === 50001 || code === 10003 || status === 403 || status === 404;
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
      expand: ["data.default_payment_method"],
    });
    subs.push(...page.data);
    if (!page.has_more) break;
    startingAfter = page.data[page.data.length - 1].id;
  }
  return subs;
}

function subscriptionHasPremiumPrice(sub) {
  const items = sub.items?.data || [];
  return items.some((item) => {
    const priceId = item?.price?.id;
    return priceId === STRIPE_PRICE_ID_STANDARD || priceId === STRIPE_PRICE_ID_INTRO;
  });
}

async function syncPremiumFromStripe() {
  if (!stripeClient || !STRIPE_PRICE_ID_STANDARD) return;
  try {
    const standardSubs = await listSubscriptionsByPrice(STRIPE_PRICE_ID_STANDARD);
    const introSubs = STRIPE_PRICE_ID_INTRO ? await listSubscriptionsByPrice(STRIPE_PRICE_ID_INTRO) : [];
    const allSubs = new Map();
    for (const sub of [...standardSubs, ...introSubs]) allSubs.set(sub.id, sub);
    let total = 0;
    for (const sub of allSubs.values()) {
      const guildId = sub.metadata?.guild_id || sub.items?.data?.[0]?.price?.metadata?.guild_id;
      if (guildId && subscriptionHasPremiumPrice(sub)) {
        setPremiumGuild(guildId, true);
        total++;
      }
    }
    if (total) console.log(`Synced ${total} premium guild(s) from Stripe.`);
  } catch (err) {
    console.warn("Failed to sync premium from Stripe:", err.message);
  }
}

async function createPremiumCheckoutSession({ guildId, userId, customerEmail }) {
  if (!stripeClient || !STRIPE_PRICE_ID_STANDARD || !STRIPE_PRICE_ID_INTRO) return null;
  const metadata = { guild_id: guildId, user_id: userId || "" };
  return stripeClient.checkout.sessions.create({
    mode: "subscription",
    customer_email: customerEmail || undefined,
    line_items: [{ price: STRIPE_PRICE_ID_INTRO, quantity: 1 }],
    success_url: STRIPE_SUCCESS_URL,
    cancel_url: STRIPE_CANCEL_URL,
    metadata,
    subscription_data: {
      metadata,
    },
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

// Stripe Checkout session creation
app.post("/create-checkout-session", express.json(), async (req, res) => {
  if (!stripeClient) return res.status(400).json({ error: "Stripe not configured" });
  try {
    const { guild_id, user_id } = req.body || {};
    if (!guild_id) return res.status(400).json({ error: "Missing guild_id" });
    if (!STRIPE_PRICE_ID_INTRO || !STRIPE_PRICE_ID_STANDARD) {
      return res.status(400).json({ error: "Missing Stripe price IDs" });
    }
    const session = await createPremiumCheckoutSession({
      guildId: guild_id,
      userId: user_id,
    });
    return res.json({ url: session.url });
  } catch (err) {
    console.error("Stripe checkout error:", err);
    return res.status(500).json({ error: "Stripe checkout failed" });
  }
});

// Stripe webhook
app.post(
  "/webhook",
  express.raw({ type: "application/json" }),
  async (req, res) => {
    if (!stripeClient || !STRIPE_WEBHOOK_SECRET) return res.status(400).send("Stripe not configured");
    const sig = req.headers["stripe-signature"];
    let event;
    try {
      event = stripeClient.webhooks.constructEvent(req.body, sig, STRIPE_WEBHOOK_SECRET);
    } catch (err) {
      console.warn("Webhook signature verification failed:", err.message);
      return res.status(400).send(`Webhook Error: ${err.message}`);
    }

    if (event.type === "checkout.session.completed") {
      const session = event.data.object;
      const guildId = session.metadata?.guild_id;
      if (guildId) {
        setPremiumGuild(guildId, true);
        console.log(`Premium granted via Stripe for guild ${guildId}`);
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
    if (event.type === "customer.subscription.deleted" || event.type === "customer.subscription.updated") {
      const sub = event.data.object;
      const guildId = sub.metadata?.guild_id;
      if (guildId) {
        const status = sub.status;
        if (status && (status === "canceled" || status === "unpaid" || status === "incomplete_expired")) {
          setPremiumGuild(guildId, false);
          console.log(`Premium revoked via Stripe for guild ${guildId} (status ${status})`);
        }
      }
    }

    res.json({ received: true });
  }
);
function getGuildConfig(guildId) {
  if (!guildConfig[guildId]) {
    guildConfig[guildId] = {
      channelIds: [],
      timezone: DEFAULT_TIMEZONE,
      hour: 0, // 00:00 UTC-ish
      branding: true,
      channelSettings: {},
      streakCount: 0,
      streakBest: 0,
      streakLastAckDate: "",
      streakRoleId: null,
      streakRoleGoal: DEFAULT_STREAK_GOAL,
      tone: DEFAULT_TONE,
      analytics: { channels: {}, holidays: {}, history: [] },
      filters: {
        noFood: false,
        noReligious: false,
        onlyWeird: false,
        onlyInternational: false,
        safeMode: false,
        blacklist: [],
      },
      surprise: {
        enabled: true,
        monthKey: "",
        days: [],
      },
      lore: {
        anniversary: "",
        keywords: [],
        customs: [],
      },
    };
  }
  if (!Array.isArray(guildConfig[guildId].channelIds)) {
    guildConfig[guildId].channelIds = [];
  }
  // Backfill new fields
  if (!guildConfig[guildId].channelSettings) {
    guildConfig[guildId].channelSettings = {};
  }
  guildConfig[guildId].timezone = normalizeTimezone(guildConfig[guildId].timezone || DEFAULT_TIMEZONE);
  if (typeof guildConfig[guildId].holidayChoice !== "number") {
    guildConfig[guildId].holidayChoice = DEFAULT_HOLIDAY_CHOICE;
  }
  if (typeof guildConfig[guildId].streakCount !== "number") {
    guildConfig[guildId].streakCount = 0;
  }
  if (typeof guildConfig[guildId].streakBest !== "number") {
    guildConfig[guildId].streakBest = 0;
  }
  if (typeof guildConfig[guildId].streakLastAckDate !== "string") {
    guildConfig[guildId].streakLastAckDate = "";
  }
  if (typeof guildConfig[guildId].streakRoleId !== "string") {
    guildConfig[guildId].streakRoleId = null;
  }
  if (typeof guildConfig[guildId].tone !== "string") {
    guildConfig[guildId].tone = DEFAULT_TONE;
  }
  if (!ALLOWED_TONES.has(guildConfig[guildId].tone)) {
    guildConfig[guildId].tone = DEFAULT_TONE;
  }
  if (!guildConfig[guildId].analytics) {
    guildConfig[guildId].analytics = { channels: {}, holidays: {}, history: [] };
  }
  if (!guildConfig[guildId].analytics.channels) guildConfig[guildId].analytics.channels = {};
  if (!guildConfig[guildId].analytics.holidays) guildConfig[guildId].analytics.holidays = {};
  if (!Array.isArray(guildConfig[guildId].analytics.history)) guildConfig[guildId].analytics.history = [];
  if (!guildConfig[guildId].filters) {
    guildConfig[guildId].filters = {
      noFood: false,
      noReligious: false,
      onlyWeird: false,
      onlyInternational: false,
      safeMode: false,
      blacklist: [],
    };
  }
  if (!Array.isArray(guildConfig[guildId].filters.blacklist)) {
    guildConfig[guildId].filters.blacklist = [];
  }
  if (!guildConfig[guildId].surprise) {
    guildConfig[guildId].surprise = { enabled: true, monthKey: "", days: [] };
  }
  if (typeof guildConfig[guildId].surprise.enabled !== "boolean") {
    guildConfig[guildId].surprise.enabled = true;
  }
  if (!Array.isArray(guildConfig[guildId].surprise.days)) guildConfig[guildId].surprise.days = [];
  if (!guildConfig[guildId].lore) {
    guildConfig[guildId].lore = { anniversary: "", keywords: [], customs: [] };
  }
  if (!Array.isArray(guildConfig[guildId].lore.keywords)) guildConfig[guildId].lore.keywords = [];
  if (!Array.isArray(guildConfig[guildId].lore.customs)) guildConfig[guildId].lore.customs = [];
  if (!guildConfig[guildId].streakRoleGoal || typeof guildConfig[guildId].streakRoleGoal !== "number") {
    guildConfig[guildId].streakRoleGoal = DEFAULT_STREAK_GOAL;
  }
  if (typeof guildConfig[guildId].promotionsEnabled !== "boolean") {
    guildConfig[guildId].promotionsEnabled = true;
  }
  if (!guildConfig[guildId].lastVotePromptAt) {
    guildConfig[guildId].lastVotePromptAt = 0;
  }
  if (!guildConfig[guildId].lastRatePromptAt) {
    guildConfig[guildId].lastRatePromptAt = 0;
  }
  return guildConfig[guildId];
}

function saveGuildConfig() {
  writeJsonSafe(CONFIG_PATH, guildConfig);
  const guildCount = Object.keys(guildConfig).length;
  const channelCount = Object.values(guildConfig).reduce((sum, cfg) => sum + ((cfg.channelIds || []).length), 0);
  console.log(`Saved guild config to ${CONFIG_PATH} (${guildCount} guilds, ${channelCount} channel(s)).`);
}

function formatSetupLog(config, channelId) {
  const channelSettings = config.channelSettings?.[channelId] || {};
  const channelIds = config.channelIds || [];
  const tz = channelSettings.timezone || config.timezone || DEFAULT_TIMEZONE;
  const hour = Number.isInteger(channelSettings.hour) ? channelSettings.hour : config.hour || 0;
  const branding = channelSettings.branding ?? config.branding ?? true;
  const holidayChoice = Number.isInteger(channelSettings.holidayChoice) ? channelSettings.holidayChoice : config.holidayChoice;
  const tone = config.tone || DEFAULT_TONE;
  const promotionsEnabled = config.promotionsEnabled !== false;
  const payload = {
    channels: channelIds,
    timezone: tz,
    hour,
    branding,
    holidayChoice,
    tone,
    streakRoleId: config.streakRoleId || null,
    streakRoleGoal: config.streakRoleGoal || DEFAULT_STREAK_GOAL,
    roleId: channelSettings.roleId || null,
    quiet: channelSettings.quiet || false,
    style: channelSettings.style || DEFAULT_EMBED_STYLE,
    color: channelSettings.color || null,
    skipWeekends: channelSettings.skipWeekends || false,
    promotionsEnabled,
  };
  return JSON.stringify(payload);
}

function isValidTimezone(tz) {
  if (!tz || typeof tz !== "string") return false;
  try {
    new Date().toLocaleString("en-US", { timeZone: tz });
    return true;
  } catch {
    return false;
  }
}

function normalizeTimezone(tz) {
  return isValidTimezone(tz) ? tz : DEFAULT_TIMEZONE;
}

function getChannelConfig(guildId, channelId) {
  const base = getGuildConfig(guildId);
  const channelSettings = base.channelSettings?.[channelId] || {};
  return {
    channelId,
    timezone: normalizeTimezone(channelSettings.timezone || base.timezone || DEFAULT_TIMEZONE),
    hour: Number.isInteger(channelSettings.hour) ? channelSettings.hour : base.hour || 0,
    branding: channelSettings.branding ?? base.branding ?? true,
    holidayChoice: Number.isInteger(channelSettings.holidayChoice) ? channelSettings.holidayChoice : base.holidayChoice || 0,
    roleId: channelSettings.roleId || null,
    quiet: channelSettings.quiet || false,
    style: channelSettings.style || DEFAULT_EMBED_STYLE,
    color: channelSettings.color || null,
    skipWeekends: channelSettings.skipWeekends || false,
    lastPostMessageId: channelSettings.lastPostMessageId || null,
    lastPostDateKey: channelSettings.lastPostDateKey || "",
    tone: base.tone || DEFAULT_TONE,
  };
}

function normalizeTone(tone) {
  if (!tone) return DEFAULT_TONE;
  return ALLOWED_TONES.has(tone) ? tone : DEFAULT_TONE;
}

function applyToneToDescription(desc, tone) {
  if (!desc) return desc;
  switch (tone) {
    case "wholesome":
      return `A gentle, feel-good moment today. ${desc}`;
    case "silly":
      return `Leaning into the playful side today. ${desc}`;
    case "nerdy":
      return `Quick knowledge drop for today. ${desc}`;
    case "historical":
      return `A nod to history and context today. ${desc}`;
    case "global":
      return `A global perspective for today. ${desc}`;
    default:
      return desc;
  }
}

function pickHolidayForTone(hits, tone, fallbackIndex) {
  if (!hits || !hits.length) return null;
  if (hits.length === 1) return hits[0];
  const normalized = normalizeTone(tone);
  const candidates = hits.map((h) => {
    const name = (h.name || "").toLowerCase();
    const desc = (h.description || "").toLowerCase();
    let score = 0;
    if (normalized === "global") {
      if (name.includes("international") || name.includes("world") || desc.includes("global")) score += 2;
    }
    if (normalized === "historical") {
      if (desc.includes("history") || desc.includes("historical") || desc.includes("founded")) score += 2;
    }
    if (normalized === "nerdy") {
      if (desc.includes("science") || desc.includes("technology") || desc.includes("math")) score += 2;
    }
    if (normalized === "silly") {
      if (name.includes("fun") || name.includes("silly") || name.includes("weird")) score += 1;
    }
    if (normalized === "wholesome") {
      if (desc.includes("community") || desc.includes("kind") || desc.includes("care")) score += 1;
    }
    return { score, holiday: h };
  });
  candidates.sort((a, b) => b.score - a.score);
  if (candidates[0].score > 0) return candidates[0].holiday;
  return hits[Math.min(Math.max(fallbackIndex || 0, 0), hits.length - 1)];
}

function pickRandomItem(items) {
  if (!items || !items.length) return null;
  return items[Math.floor(Math.random() * items.length)];
}

function normalizeFilterList(value) {
  if (!value) return [];
  return value
    .split(",")
    .map((item) => item.trim().toLowerCase())
    .filter(Boolean);
}

function hasActiveFilters(filters) {
  if (!filters) return false;
  return (
    filters.noFood ||
    filters.noReligious ||
    filters.onlyWeird ||
    filters.onlyInternational ||
    filters.safeMode ||
    (filters.blacklist && filters.blacklist.length > 0)
  );
}

function matchesKeyword(text, keywords) {
  return keywords.some((kw) => text.includes(kw));
}

function filterHoliday(holiday, filters) {
  if (!filters) return true;
  const text = `${holiday.name || ""} ${holiday.description || ""}`.toLowerCase();
  if (filters.onlyInternational && !matchesKeyword(text, INTERNATIONAL_KEYWORDS)) return false;
  if (filters.onlyWeird && !matchesKeyword(text, WEIRD_KEYWORDS)) return false;
  if (filters.noFood && matchesKeyword(text, FOOD_KEYWORDS)) return false;
  if (filters.noReligious && matchesKeyword(text, RELIGIOUS_KEYWORDS)) return false;
  if (filters.safeMode && matchesKeyword(text, SAFE_MODE_BLOCKLIST)) return false;
  if (filters.blacklist && filters.blacklist.length && matchesKeyword(text, filters.blacklist)) return false;
  return true;
}

function applyHolidayFilters(hits, filters) {
  return (hits || []).filter((h) => filterHoliday(h, filters));
}

function isWeirdHoliday(holiday) {
  const text = `${holiday.name || ""} ${holiday.description || ""}`.toLowerCase();
  return matchesKeyword(text, WEIRD_KEYWORDS);
}

function buildMonthKey(dateKey) {
  return dateKey.slice(0, 7);
}

function pickSurpriseDays(monthKey, count) {
  const [yearStr, monthStr] = monthKey.split("-");
  const year = Number(yearStr);
  const month = Number(monthStr);
  const daysInMonth = new Date(Date.UTC(year, month, 0)).getUTCDate();
  const picks = new Set();
  while (picks.size < count && picks.size < daysInMonth) {
    picks.add(Math.floor(Math.random() * daysInMonth) + 1);
  }
  return [...picks]
    .sort((a, b) => a - b)
    .map((day) => `${monthKey}-${String(day).padStart(2, "0")}`);
}

function maybePickWildcardHoliday(config, dateKey) {
  if (!config.surprise?.enabled) return null;
  const monthKey = buildMonthKey(dateKey);
  if (config.surprise.monthKey !== monthKey || !config.surprise.days.length) {
    const count = Math.random() < 0.5 ? 1 : 2;
    config.surprise.monthKey = monthKey;
    config.surprise.days = pickSurpriseDays(monthKey, count);
    saveGuildConfig();
  }
  if (!config.surprise.days.includes(dateKey)) return null;

  const filtered = applyHolidayFilters(allHolidays, config.filters);
  if (!filtered.length && hasActiveFilters(config.filters)) return null;
  const pool = filtered.length ? filtered : allHolidays;
  const weirdPool = pool.filter(isWeirdHoliday);
  return pickRandomItem(weirdPool.length ? weirdPool : pool);
}

function buildLoreLines(config, dateKey) {
  const lines = [];
  const lore = config.lore || {};
  if (lore.anniversary && lore.anniversary === dateKey.slice(5)) {
    lines.push("🎉 Server anniversary today!");
  }
  if (Array.isArray(lore.customs)) {
    const customsToday = lore.customs.filter((c) => c.date === dateKey.slice(5));
    for (const c of customsToday) {
      lines.push(`Server lore: ${c.name}${c.description ? ` — ${c.description}` : ""}`);
    }
  }
  if (Array.isArray(lore.keywords) && lore.keywords.length && Math.random() < 0.25) {
    const keyword = pickRandomItem(lore.keywords);
    if (keyword) lines.push(`Server lore: This feels like a good day for ${keyword}.`);
  }
  return lines;
}

function recordPostAnalytics(config, channelId, dateKey, hour, holiday) {
  const analytics = config.analytics || { channels: {}, holidays: {}, history: [] };
  if (!analytics.channels) analytics.channels = {};
  if (!analytics.holidays) analytics.holidays = {};
  if (!Array.isArray(analytics.history)) analytics.history = [];

  const channelStats = analytics.channels[channelId] || { posts: 0, reactions: 0 };
  channelStats.posts += 1;
  analytics.channels[channelId] = channelStats;

  const slug = holiday.slug || slugify(holiday.name || "holiday");
  const holidayStats = analytics.holidays[slug] || { name: holiday.name || slug, reactions: 0 };
  analytics.holidays[slug] = holidayStats;

  analytics.history.push({
    dateKey,
    channelId,
    slug,
    name: holiday.name || slug,
    reactions: 0,
    hour,
  });
  if (analytics.history.length > MAX_ANALYTICS_HISTORY) {
    analytics.history = analytics.history.slice(-MAX_ANALYTICS_HISTORY);
  }
  config.analytics = analytics;
}

function recordReactionAnalytics(config, channelId, dateKey) {
  const analytics = config.analytics;
  if (!analytics) return;
  if (!analytics.channels) analytics.channels = {};
  if (!analytics.holidays) analytics.holidays = {};
  if (!Array.isArray(analytics.history)) analytics.history = [];

  const channelStats = analytics.channels[channelId] || { posts: 0, reactions: 0 };
  channelStats.reactions += 1;
  analytics.channels[channelId] = channelStats;

  const settings = config.channelSettings?.[channelId] || {};
  const slug = settings.lastPostSlug;
  const name = settings.lastPostName || slug;
  if (slug) {
    const holidayStats = analytics.holidays[slug] || { name: name || slug, reactions: 0 };
    holidayStats.reactions += 1;
    analytics.holidays[slug] = holidayStats;
  }

  for (let i = analytics.history.length - 1; i >= 0; i -= 1) {
    const entry = analytics.history[i];
    if (entry.channelId === channelId && entry.dateKey === dateKey) {
      entry.reactions += 1;
      break;
    }
  }
  config.analytics = analytics;
}

function buildMicroPrompt(holiday, tone) {
  const name = holiday?.name || "today’s holiday";
  const emoji = holiday?.emoji ? `${holiday.emoji} ` : "";
  const normalized = normalizeTone(tone);
  const prompts = {
    wholesome: [
      `${emoji}Share a kind or uplifting way to mark ${name}.`,
      `${emoji}What’s a small, feel-good way to celebrate ${name}?`,
    ],
    silly: [
      `${emoji}Drop your silliest idea for celebrating ${name}.`,
      `${emoji}What’s the most ridiculous way to mark ${name}?`,
    ],
    nerdy: [
      `${emoji}Share a nerdy fact or stat about ${name}.`,
      `${emoji}What’s a technical or behind-the-scenes angle on ${name}?`,
    ],
    historical: [
      `${emoji}Know a historical tidbit related to ${name}?`,
      `${emoji}What’s the origin story behind ${name}?`,
    ],
    global: [
      `${emoji}How is ${name} observed around the world?`,
      `${emoji}Share a cultural tradition tied to ${name}.`,
    ],
    default: [
      `${emoji}React if you’ve celebrated ${name} before.`,
      `${emoji}What’s your go-to way to mark ${name}?`,
      `${emoji}Reply with a quick fact or memory about ${name}.`,
      `${emoji}If you had a 10-minute celebration for ${name}, what would you do?`,
      `${emoji}Drop a themed emoji if ${name} fits your vibe today.`,
    ],
  };
  const pool = prompts[normalized] || prompts.default;
  return pickRandomItem(pool);
}

async function scheduleDidYouKnow(channel, messageId, holiday) {
  const fact = pickRandomItem(holiday?.funFacts || []);
  if (!fact) return;
  const delayMs = Math.max(5, FOLLOWUP_DELAY_MIN) * 60 * 1000;
  setTimeout(async () => {
    try {
      const msg = messageId ? await channel.messages.fetch(messageId) : null;
      const content = `Did you know? ${fact}`;
      if (msg) {
        await msg.reply({ content, allowedMentions: { repliedUser: false } });
      } else {
        await channel.send({ content });
      }
    } catch (e) {
      console.warn("Did-you-know follow-up failed:", e.message);
    }
  }, delayMs);
}

function getDateKey(date, timeZone) {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(date);
}

function previousDateKey(dateKey) {
  const [year, month, day] = dateKey.split("-").map((n) => Number(n));
  const date = new Date(Date.UTC(year, month - 1, day - 1));
  return date.toISOString().slice(0, 10);
}

async function maybeAssignStreakRole(guild, member, roleId) {
  if (!roleId || !guild || !member) return;
  const role = guild.roles.cache.get(roleId);
  if (!role) return;
  const me = guild.members.me;
  if (!me) return;
  if (!me.permissions.has(PermissionsBitField.Flags.ManageRoles)) return;
  if (role.position >= me.roles.highest.position) return;
  if (member.roles.cache.has(roleId)) return;
  try {
    await member.roles.add(roleId);
  } catch (e) {
    console.warn("Failed to assign streak role:", e.message);
  }
}

async function recordGuildStreak(guildId, channelId, userId) {
  const config = getGuildConfig(guildId);
  const channelSettings = config.channelSettings?.[channelId] || {};
  const dateKey = channelSettings.lastPostDateKey || getDateKey(new Date(), channelSettings.timezone || DEFAULT_TIMEZONE);
  if (!dateKey) return;
  if (config.streakLastAckDate === dateKey) return;

  const expectedPrev = previousDateKey(dateKey);
  if (config.streakLastAckDate === expectedPrev) {
    config.streakCount = Math.max(1, (config.streakCount || 0) + 1);
  } else {
    config.streakCount = 1;
  }
  config.streakLastAckDate = dateKey;
  if (config.streakCount > (config.streakBest || 0)) config.streakBest = config.streakCount;
  saveGuildConfig();

  const guild = client.guilds.cache.get(guildId);
  if (!guild) return;
  if (!isPremiumGuild(guild)) return;
  if (!config.streakRoleId || config.streakCount < (config.streakRoleGoal || DEFAULT_STREAK_GOAL)) return;

  try {
    const member = await guild.members.fetch(userId);
    await maybeAssignStreakRole(guild, member, config.streakRoleId);
  } catch (e) {
    console.warn("Failed to grant streak role:", e.message);
  }
}

function slugify(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
}

function canShowVotePrompt(guildId) {
  const cfg = getGuildConfig(guildId);
  if (cfg.promotionsEnabled === false) return false;
  const last = Number(cfg.lastVotePromptAt || 0);
  return Date.now() - last >= PROMO_VOTE_INTERVAL_MS;
}

function canShowRatePrompt(guildId) {
  const cfg = getGuildConfig(guildId);
  if (cfg.promotionsEnabled === false) return false;
  const last = Number(cfg.lastRatePromptAt || 0);
  return Date.now() - last >= PROMO_RATE_INTERVAL_MS;
}

function markVotePrompt(guildId) {
  const cfg = getGuildConfig(guildId);
  cfg.lastVotePromptAt = Date.now();
  saveGuildConfig();
}

function markRatePrompt(guildId) {
  const cfg = getGuildConfig(guildId);
  cfg.lastRatePromptAt = Date.now();
  saveGuildConfig();
}

function buildPromoComponents(guildId, opts = {}) {
  const rows = [];
  const noteParts = [];
  const includeRate = !!opts.includeRate;
  const cfg = getGuildConfig(guildId);
  if (cfg.promotionsEnabled === false) return { rows, note: "" };
  const forceVote = !!opts.forceVote;
  const voteOk = forceVote || canShowVotePrompt(guildId);
  const rateOk = includeRate && canShowRatePrompt(guildId);

  if (!voteOk && !rateOk) return { rows, note: "" };

  const row = new ActionRowBuilder();
  if (voteOk) {
    row.addComponents(new ButtonBuilder().setLabel("Vote on top.gg").setStyle(ButtonStyle.Link).setURL(TOPGG_VOTE_URL));
    noteParts.push("Optional: support the bot with a quick vote.");
    if (!forceVote) markVotePrompt(guildId);
  }
  if (rateOk) {
    row.addComponents(new ButtonBuilder().setLabel("Leave a review").setStyle(ButtonStyle.Link).setURL(TOPGG_REVIEW_URL));
    noteParts.push("Reviews help discovery—thanks!");
    markRatePrompt(guildId);
  }
  if (row.components.length) rows.push(row);
  return { rows, note: noteParts.join(" ") };
}

function pad(num) {
  return String(num).padStart(2, "0");
}

const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
function prettyDate(mmdd) {
  const [mm, dd] = mmdd.split("-").map((n) => Number(n));
  const month = monthNames[mm - 1] || "??";
  return `${month} ${dd}`;
}

function parseDate(input) {
  if (!input) return null;
  const cleaned = input.trim().replace(/\//g, "-");
  const match = cleaned.match(/^(\d{1,2})-(\d{1,2})$/);
  if (!match) return null;
  const mm = Number(match[1]);
  const dd = Number(match[2]);
  if (mm < 1 || mm > 12 || dd < 1 || dd > 31) return null;
  return `${pad(mm)}-${pad(dd)}`;
}

function findByDate(mmdd) {
  return holidaysByDate[mmdd] || [];
}

function findByName(query) {
  const q = query.toLowerCase();
  const scored = [];
  for (const h of allHolidays) {
    const name = h.name || "";
    const l = name.toLowerCase();
    if (l.includes(q)) {
      scored.push({ score: q.length / l.length, item: h });
      continue;
    }
    const words = q.split(/\s+/).filter(Boolean);
    const hits = words.reduce((acc, w) => acc + (l.includes(w) ? 1 : 0), 0);
    if (hits > 0) scored.push({ score: hits / words.length, item: h });
  }
  return scored
    .sort((a, b) => b.score - a.score)
    .map((s) => s.item)
    .slice(0, 5);
}

function pickRandom() {
  return allHolidays[Math.floor(Math.random() * allHolidays.length)];
}

function holidaysForRange(startDate, days) {
  const list = [];
  for (let i = 0; i < days; i++) {
    const d = new Date(startDate);
    d.setDate(startDate.getDate() + i);
    const mmdd = `${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
    const hits = findByDate(mmdd);
    if (hits.length) list.push({ date: mmdd, holiday: hits[0] });
  }
  return list;
}

function buildEmbed(h, options = {}) {
  const name = h.name || "Holiday";
  const emoji = h.emoji || "";
  const date = h.date || "??-??";
  const fullDesc = h.description || "";
  const style = options.style || DEFAULT_EMBED_STYLE;
  const rawDesc = style === "rich" ? fullDesc.slice(0, 1200) : fullDesc.slice(0, 500);
  const desc = applyToneToDescription(rawDesc, normalizeTone(options.tone));
  const facts = Array.isArray(h.funFacts)
    ? h.funFacts.slice(0, style === "rich" ? 5 : 3)
    : [];
  const slug = h.slug || slugify(name);
  const url = `${SITE_BASE}/${slug}/`;
  const showBranding = options.branding !== false; // default true
  const color = options.color || DEFAULT_EMBED_COLOR;

  const embed = new EmbedBuilder()
    .setTitle(`${emoji ? emoji + " " : ""}${name}`)
    .setURL(url)
    .setDescription(desc || "Learn more on the site.")
    .addFields([{ name: "Date", value: prettyDate(date), inline: true }])
    .setColor(color);

  if (showBranding) {
    embed.setFooter({ text: "Powered by ObscureHolidayCalendar.com" });
  }

  if (facts.length) {
    embed.addFields([{ name: "Fun facts", value: facts.map((f) => `• ${f}`).join("\n") }]);
  }

  return embed;
}

function buildButtons(h) {
  const name = h.name || "Holiday";
  const slug = h.slug || slugify(name);
  const url = `${SITE_BASE}/${slug}/`;
  return [
    new ActionRowBuilder().addComponents(
      new ButtonBuilder().setLabel("View on Website").setStyle(ButtonStyle.Link).setURL(url),
      new ButtonBuilder().setLabel("Get the App").setStyle(ButtonStyle.Link).setURL(APP_URL),
      new ButtonBuilder().setLabel("Invite the Bot").setStyle(ButtonStyle.Link).setURL(BOT_INVITE_URL)
    ),
  ];
}

async function handleToday(interaction) {
  const now = new Date();
  const mmdd = `${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  const hits = findByDate(mmdd);
  if (!hits.length) return interaction.reply({ content: "No holiday found for today.", flags: MessageFlags.Ephemeral });
  const premium = isPremium(interaction.guild, interaction.member);
  const config = getGuildConfig(interaction.guild.id);
  const filtered = premium ? applyHolidayFilters(hits, config.filters) : hits;
  if (!filtered.length) {
    return interaction.reply({ content: "No holiday found for today with current filters.", flags: MessageFlags.Ephemeral });
  }
  const requested = interaction.options.getInteger("holiday_choice");
  let choice = 0;
  if (premium) {
    if (Number.isInteger(requested)) {
      choice = Math.min(Math.max(requested, 0), filtered.length - 1);
    } else {
      choice = Math.min(config.holidayChoice || 0, filtered.length - 1);
    }
  } else {
    choice = 0; // free tier: first holiday only
  }
  const pick = pickHolidayForTone(filtered, config.tone, choice) || filtered[choice] || filtered[0];
  const baseComponents = buildButtons(pick);
  const { rows: promoRows, note: promoNote } = buildPromoComponents(interaction.guild.id, { includeRate: false, forceVote: true });
  return interaction.reply({
    content: promoNote || undefined,
    embeds: [buildEmbed(pick, { branding: !premium || config.branding, tone: config.tone })],
    components: [...baseComponents, ...promoRows],
  });
}

async function handleHelp(interaction) {
  const level = interaction.options.getString("level") || "full";
  if (level === "brief") {
    return interaction.reply({
      content: [
        "ObscureHolidayBot quick help",
        "/today, /tomorrow, /upcoming, /week, /streak",
        "/setup, /analytics, /lore (premium/admin)",
        "/premium, /upgrade, /manage",
        "/help full — full command list",
      ].join("\n"),
      flags: MessageFlags.Ephemeral,
    });
  }
  return interaction.reply({
    content: [
      "ObscureHolidayBot help (slash commands)",
      "",
      "Basics (free)",
      "/today — today’s holiday",
      "/tomorrow — tomorrow’s holiday",
      "/upcoming [days] — upcoming holidays (max 30)",
      "/week [days] — 7-day digest (3–14)",
      "/fact [name|MM-DD] — one fun fact (free)",
      "/streak — show the server streak",
      "",
      "Premium content",
      "/date MM-DD — holiday on a date",
      "/search <query> — find matching holidays",
      "/random — surprise me",
      "/facts [name|MM-DD] — fun facts (multiple)",
      "",
      "Setup & admin",
      "/setup — configure daily posts",
      "  free: channel",
      "  premium: timezone, hour, branding, holiday_choice, role_mention, quiet, promotions, embed_style, embed_color, skip_weekends",
      "  premium extras: tone, streak_role, streak_goal, filters, blacklist, surprise_days",
      "/analytics — engagement analytics (premium, admin)",
      "/lore — server lore (premium, admin)",
      "",
      "Account & support",
      "/premium — check premium status",
      "/upgrade — start premium checkout",
      "/manage — manage billing",
      "/vote — vote on top.gg",
      "/rate — leave a review on top.gg",
      "/support — help/landing page",
      "/invite — invite the bot",
      "/app — mobile app links",
      "/slack — Slack bot link",
      "",
      "Tips",
      "Daily posts use the bot’s role permissions in that channel.",
      "Streaks increment when someone reacts to the daily post; the first reaction per day counts.",
      "If streak roles or analytics aren’t working, check Manage Roles + Read Message History.",
    ].join("\n"),
    flags: MessageFlags.Ephemeral,
  });
}

async function handleVote(interaction) {
  return interaction.reply({
    content: "Thanks for supporting the bot on top.gg!",
    components: [
      new ActionRowBuilder().addComponents(
        new ButtonBuilder().setLabel("Vote on top.gg").setStyle(ButtonStyle.Link).setURL(TOPGG_VOTE_URL),
        new ButtonBuilder().setLabel("Leave a review").setStyle(ButtonStyle.Link).setURL(TOPGG_REVIEW_URL)
      ),
    ],
    flags: MessageFlags.Ephemeral,
  });
}

async function handleRate(interaction) {
  return interaction.reply({
    content: "If you’re enjoying ObscureHolidayBot, a quick review helps a ton.",
    components: [
      new ActionRowBuilder().addComponents(
        new ButtonBuilder().setLabel("Review on top.gg").setStyle(ButtonStyle.Link).setURL(TOPGG_REVIEW_URL),
        new ButtonBuilder().setLabel("Vote").setStyle(ButtonStyle.Link).setURL(TOPGG_VOTE_URL)
      ),
    ],
    flags: MessageFlags.Ephemeral,
  });
}

async function handleDate(interaction) {
  if (!isPremium(interaction.guild, interaction.member)) {
    return interaction.reply({ content: "Premium only. Upgrade with /upgrade to use /date.", flags: MessageFlags.Ephemeral });
  }
  const input = interaction.options.getString("date", true);
  const parsed = parseDate(input);
  if (!parsed) return interaction.reply({ content: "Please provide a date as MM-DD or MM/DD (example: 07-04).", flags: MessageFlags.Ephemeral });
  const config = getGuildConfig(interaction.guild.id);
  const hits = applyHolidayFilters(findByDate(parsed), config.filters);
  if (!hits.length) return interaction.reply({ content: `No holidays found on ${parsed} with current filters.`, flags: MessageFlags.Ephemeral });
  return interaction.reply({ embeds: [buildEmbed(hits[0], { branding: config.branding, tone: config.tone })], components: buildButtons(hits[0]) });
}

async function handleSearch(interaction) {
  if (!isPremium(interaction.guild, interaction.member)) {
    return interaction.reply({ content: "Premium only. Upgrade with /upgrade to use /search.", flags: MessageFlags.Ephemeral });
  }
  const query = interaction.options.getString("query", true);
  const config = getGuildConfig(interaction.guild.id);
  const matches = applyHolidayFilters(findByName(query), config.filters);
  if (!matches.length) return interaction.reply({ content: "No match. Try a simpler phrase.", flags: MessageFlags.Ephemeral });
  const embeds = matches.slice(0, 3).map((h) => buildEmbed(h, { branding: config.branding, tone: config.tone }));
  return interaction.reply({ embeds, components: buildButtons(matches[0]) });
}

async function handleRandom(interaction) {
  if (!isPremium(interaction.guild, interaction.member)) {
    return interaction.reply({ content: "Premium only. Upgrade with /upgrade to use /random.", flags: MessageFlags.Ephemeral });
  }
  const config = getGuildConfig(interaction.guild.id);
  const filtered = applyHolidayFilters(allHolidays, config.filters);
  const h = pickRandomItem(filtered.length ? filtered : allHolidays);
  return interaction.reply({ embeds: [buildEmbed(h, { branding: config.branding, tone: config.tone })], components: buildButtons(h) });
}

async function handleWeek(interaction) {
  const days = Math.max(3, Math.min(interaction.options.getInteger("days") || 7, 14));
  const now = new Date();
  const items = holidaysForRange(now, days);
  if (!items.length) return interaction.reply({ content: "No upcoming holidays found.", flags: MessageFlags.Ephemeral });
  const embed = new EmbedBuilder()
    .setTitle(`Next ${days} days of holidays`)
    .setColor(DEFAULT_EMBED_COLOR);
  const fields = items.slice(0, 10).map(({ date, holiday }) => ({
    name: `${holiday.emoji ? holiday.emoji + " " : ""}${holiday.name}`,
    value: prettyDate(date),
    inline: true,
  }));
  embed.addFields(fields);
  embed.setFooter({ text: "Powered by ObscureHolidayCalendar.com" });
  const { rows: promoRows, note: promoNote } = buildPromoComponents(interaction.guild.id, { includeRate: true });
  return interaction.reply({ content: promoNote || undefined, embeds: [embed], components: promoRows });
}

async function handleSetup(interaction) {
  if (!interaction.guild) {
    return interaction.reply({ content: "This command can only be used in a server.", flags: MessageFlags.Ephemeral });
  }
  const guildId = interaction.guild.id;
  const config = getGuildConfig(guildId);
  console.log(`Setup invoked for guild ${guildId} (config path: ${CONFIG_PATH}).`);
  const channel = interaction.options.getChannel("channel", true);
  const tz = interaction.options.getString("timezone");
  const hour = interaction.options.getInteger("hour");
  const brandingOpt = interaction.options.getBoolean("branding");
  const holidayChoice = interaction.options.getInteger("holiday_choice");
  const role = interaction.options.getRole("role_mention");
  const quiet = interaction.options.getBoolean("quiet");
  const embedStyle = interaction.options.getString("embed_style");
  const embedColor = interaction.options.getString("embed_color");
  const skipWeekends = interaction.options.getBoolean("skip_weekends");
  const tone = interaction.options.getString("tone");
  const filterNoFood = interaction.options.getBoolean("filter_no_food");
  const filterNoReligious = interaction.options.getBoolean("filter_no_religious");
  const filterOnlyWeird = interaction.options.getBoolean("filter_only_weird");
  const filterOnlyInternational = interaction.options.getBoolean("filter_only_international");
  const filterSafeMode = interaction.options.getBoolean("filter_safe_mode");
  const filterBlacklist = interaction.options.getString("filter_blacklist");
  const surpriseDays = interaction.options.getBoolean("surprise_days");
  const streakRole = interaction.options.getRole("streak_role");
  const streakGoal = interaction.options.getInteger("streak_goal");
  const promotionsEnabled = interaction.options.getBoolean("promotions");
  const premium = isPremium(interaction.guild, interaction.member);

  if (!channel.isTextBased()) {
    return interaction.reply({ content: "Please pick a text channel.", flags: MessageFlags.Ephemeral });
  }

  if (!premium) {
    config.channelIds = [channel.id];
    config.timezone = DEFAULT_TIMEZONE;
    config.hour = 0;
    config.branding = true;
    config.holidayChoice = DEFAULT_HOLIDAY_CHOICE;
    if (typeof promotionsEnabled === "boolean") config.promotionsEnabled = promotionsEnabled;
    saveGuildConfig();
    console.log(`Setup saved for guild ${guildId}: ${formatSetupLog(config, channel.id)}`);
    scheduleForChannel(guildId, channel.id);
    return interaction.reply({
      content: [
        `Daily posts set to <#${channel.id}> at 00:00 UTC.`,
        `Promotions: ${config.promotionsEnabled === false ? "off" : "on (weekly vote / monthly review)"}`,
        "Premium unlocks timezone/hour/branding toggles.",
      ].join("\n"),
      flags: MessageFlags.Ephemeral,
    });
  }

  // Premium path: allow multiple channels, timezone/hour, branding toggle, holiday choice, role mention, quiet, style, color, skip weekends
  if (!config.channelIds.includes(channel.id)) {
    config.channelIds.push(channel.id);
  }
  if (!config.channelSettings) config.channelSettings = {};
  const ch = config.channelSettings[channel.id] || {};
  if (tone) config.tone = normalizeTone(tone);
  if (typeof filterNoFood === "boolean") config.filters.noFood = filterNoFood;
  if (typeof filterNoReligious === "boolean") config.filters.noReligious = filterNoReligious;
  if (typeof filterOnlyWeird === "boolean") config.filters.onlyWeird = filterOnlyWeird;
  if (typeof filterOnlyInternational === "boolean") config.filters.onlyInternational = filterOnlyInternational;
  if (typeof filterSafeMode === "boolean") config.filters.safeMode = filterSafeMode;
  if (typeof filterBlacklist === "string") config.filters.blacklist = normalizeFilterList(filterBlacklist);
  if (typeof surpriseDays === "boolean") config.surprise.enabled = surpriseDays;
  if (tz) {
    if (!isValidTimezone(tz)) {
      return interaction.reply({ content: "Timezone not recognized. Please use an IANA timezone like America/New_York.", flags: MessageFlags.Ephemeral });
    }
    ch.timezone = tz;
  }
  if (Number.isInteger(hour)) ch.hour = Math.max(0, Math.min(hour, 23));
  if (typeof brandingOpt === "boolean") ch.branding = brandingOpt;
  if (Number.isInteger(holidayChoice)) ch.holidayChoice = Math.min(Math.max(holidayChoice, 0), 1);
  if (role) ch.roleId = role.id;
  if (typeof quiet === "boolean") ch.quiet = quiet;
  if (typeof promotionsEnabled === "boolean") config.promotionsEnabled = promotionsEnabled;
  if (embedStyle) ch.style = embedStyle;
  if (embedColor && /^#?[0-9a-fA-F]{6}$/.test(embedColor)) {
    ch.color = Number.parseInt(embedColor.replace("#", ""), 16);
  }
  if (typeof skipWeekends === "boolean") ch.skipWeekends = skipWeekends;
  if (streakRole) config.streakRoleId = streakRole.id;
  if (Number.isInteger(streakGoal) && streakGoal > 0) config.streakRoleGoal = streakGoal;
  config.channelSettings[channel.id] = ch;

  saveGuildConfig();
  console.log(`Setup saved for guild ${guildId}: ${formatSetupLog(config, channel.id)}`);
  scheduleForChannel(guildId, channel.id);

  return interaction.reply({
    content: [
      `Daily posts set to ${config.channelIds.map((c) => `<#${c}>`).join(", ")}`,
      `Time: ${(ch.hour ?? config.hour)}:00 in ${ch.timezone || config.timezone}`,
      `Branding: ${ch.branding === false ? "off" : "on"}`,
      `Holiday pick: ${ch.holidayChoice === 1 ? "Holiday #2 (second of the day)" : "Holiday #1 (first of the day)"}`,
      role ? `Role ping: <@&${role.id}>` : "Role ping: none",
      `Tone: ${config.tone || DEFAULT_TONE}`,
      `Surprise days: ${config.surprise.enabled ? "on" : "off"}`,
      `Filters: ${[
        config.filters.noFood ? "no food" : null,
        config.filters.noReligious ? "no religious" : null,
        config.filters.onlyWeird ? "only weird" : null,
        config.filters.onlyInternational ? "only international" : null,
        config.filters.safeMode ? "safe mode" : null,
      ]
        .filter(Boolean)
        .join(", ") || "none"}`,
      config.filters.blacklist.length ? `Blacklist: ${config.filters.blacklist.join(", ")}` : "Blacklist: none",
      config.streakRoleId ? `Streak role: <@&${config.streakRoleId}> (goal ${config.streakRoleGoal} days)` : "Streak role: none",
      `Quiet mode: ${ch.quiet ? "on" : "off"}`,
      `Skip weekends: ${ch.skipWeekends ? "yes" : "no"}`,
      `Promotions: ${config.promotionsEnabled === false ? "off" : "on (weekly vote / monthly review)"}`,
    ].join("\n"),
    flags: MessageFlags.Ephemeral,
  });
}

async function handleFacts(interaction) {
  if (!isPremium(interaction.guild, interaction.member)) {
    return interaction.reply({ content: "Premium only. Upgrade with /upgrade to use /facts.", flags: MessageFlags.Ephemeral });
  }
  const target = interaction.options.getString("name_or_date", false) || "today";
  let holiday = null;
  const asDate = parseDate(target);
  if (asDate) {
    holiday = (findByDate(asDate)[0]) || null;
  } else if (target === "today") {
    const now = new Date();
    const mmdd = `${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
    holiday = (findByDate(mmdd)[0]) || null;
  } else {
    holiday = findByName(target)[0] || null;
  }

  if (!holiday) return interaction.reply({ content: "Couldn't find fun facts for that. Try 12-25 or \"bacon\".", flags: MessageFlags.Ephemeral });
  const facts = Array.isArray(holiday.funFacts) ? holiday.funFacts.slice(0, 5) : [];
  if (!facts.length) return interaction.reply({ content: "No fun facts on file for that one.", flags: MessageFlags.Ephemeral });
  const embed = new EmbedBuilder()
    .setTitle(`${holiday.emoji ? holiday.emoji + " " : ""}${holiday.name || "Holiday"} — fun facts`)
    .setDescription(facts.map((f) => `• ${f}`).join("\n"))
    .setColor(0xff7a3c);
  const premium = isPremium(interaction.guild, interaction.member);
  if (!premium || getGuildConfig(interaction.guild.id).branding) {
    embed.setFooter({ text: "Powered by ObscureHolidayCalendar.com" });
  }
  return interaction.reply({ embeds: [embed], components: buildButtons(holiday) });
}

async function handleFact(interaction) {
  const target = interaction.options.getString("name_or_date", false) || "today";
  let holiday = null;
  const asDate = parseDate(target);
  if (asDate) {
    holiday = (findByDate(asDate)[0]) || null;
  } else if (target === "today") {
    const now = new Date();
    const mmdd = `${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
    holiday = (findByDate(mmdd)[0]) || null;
  } else {
    holiday = findByName(target)[0] || null;
  }

  if (!holiday) return interaction.reply({ content: "Couldn't find a fact for that. Try 12-25 or \"bacon\".", flags: MessageFlags.Ephemeral });
  const facts = Array.isArray(holiday.funFacts) ? holiday.funFacts : [];
  const fact = pickRandomItem(facts);
  if (!fact) return interaction.reply({ content: "No fun facts on file for that one.", flags: MessageFlags.Ephemeral });
  const embed = new EmbedBuilder()
    .setTitle(`${holiday.emoji ? holiday.emoji + " " : ""}${holiday.name || "Holiday"} — fun fact`)
    .setDescription(fact)
    .setColor(0xff7a3c);
  const premium = isPremium(interaction.guild, interaction.member);
  if (!premium || getGuildConfig(interaction.guild.id).branding) {
    embed.setFooter({ text: "Powered by ObscureHolidayCalendar.com" });
  }
  return interaction.reply({ embeds: [embed], components: buildButtons(holiday) });
}

async function handleStreak(interaction) {
  const config = getGuildConfig(interaction.guild.id);
  const count = config.streakCount || 0;
  const best = config.streakBest || 0;
  const lastAck = config.streakLastAckDate || "never";
  return interaction.reply({
    content: [
      `🔥 Server streak: ${count} day${count === 1 ? "" : "s"} (best ${best})`,
      `Last acknowledged: ${lastAck}`,
      "Streaks count when someone reacts to the daily post. The first reaction per day counts; missed days reset the streak.",
    ].join("\n"),
    flags: MessageFlags.Ephemeral,
  });
}

async function handleTomorrow(interaction) {
  const now = new Date();
  const tomorrow = new Date(now);
  tomorrow.setDate(now.getDate() + 1);
  const mmdd = `${pad(tomorrow.getMonth() + 1)}-${pad(tomorrow.getDate())}`;
  const hits = findByDate(mmdd);
  if (!hits.length) return interaction.reply({ content: "No holiday found for tomorrow.", flags: MessageFlags.Ephemeral });
  const config = getGuildConfig(interaction.guild.id);
  return interaction.reply({ embeds: [buildEmbed(hits[0], { branding: config.branding })], components: buildButtons(hits[0]) });
}

async function handleUpcoming(interaction) {
  const days = Math.max(1, Math.min(interaction.options.getInteger("days") || 7, 30));
  const now = new Date();
  const items = holidaysForRange(now, days);
  if (!items.length) return interaction.reply({ content: "No upcoming holidays found.", flags: MessageFlags.Ephemeral });
  const fields = items.slice(0, 5).map(({ date, holiday }) => ({
    name: `${holiday.emoji ? holiday.emoji + " " : ""}${holiday.name}`,
    value: prettyDate(date),
    inline: true,
  }));
  const config = getGuildConfig(interaction.guild.id);
  const embed = new EmbedBuilder()
    .setTitle("Upcoming holidays")
    .addFields(fields)
    .setColor(0x1c96f3);
  if (config.branding !== false) {
    embed.setFooter({ text: "Powered by ObscureHolidayCalendar.com" });
  }
  return interaction.reply({ embeds: [embed], components: buildButtons(items[0].holiday) });
}

async function handlePremiumStatus(interaction) {
  const premium = isPremium(interaction.guild, interaction.member);
  const config = getGuildConfig(interaction.guild.id);
  const benefits = [
    "✅ Multiple daily channels",
    "✅ Custom timezone & hour",
    "✅ Premium commands: /date, /search, /random, /facts",
    "✅ Branding toggle",
    "✅ Pick which of the day’s holidays to auto-post",
    "✅ Per-channel role pings & quiet mode",
    "✅ Rich/compact embeds, custom color",
    "✅ Skip-weekends scheduling",
    "✅ Streak role rewards",
    "✅ Mood/tone selector",
    "✅ Holiday filters & server lore",
  ];

  if (premium) {
    const lines = [
      "✅ Premium is active for this server.",
      `Daily channel(s): ${config.channelIds.length ? config.channelIds.map((c) => `<#${c}>`).join(", ") : "not set"}`,
      `Timezone: ${config.timezone} @ ${config.hour}:00`,
      `Branding: ${config.branding === false ? "off" : "on"}`,
      `Holiday pick: ${config.holidayChoice === 1 ? "second of the day" : "first of the day"}`,
      "Premium perks:",
      ...benefits,
    ];
    return interaction.reply({ content: lines.join("\n"), flags: MessageFlags.Ephemeral });
  }

  // Not premium: offer upgrade
  let upgradeUrl = SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/";
  if (stripeClient && STRIPE_PRICE_ID_STANDARD && STRIPE_PRICE_ID_INTRO) {
    try {
      const session = await createPremiumCheckoutSession({
        guildId: interaction.guildId,
        userId: interaction.user.id,
      });
      if (session.url) upgradeUrl = session.url;
    } catch (err) {
      console.error("Stripe checkout error (premium status):", err);
    }
  }

  const lines = [
    "⚠️ Premium not active.",
    "Intro offer: $0.99 for your first month, then $3.99/month. Cancel anytime.",
    "Premium unlocks:",
    ...benefits,
  ];

  return interaction.reply({
    content: lines.join("\n"),
    flags: MessageFlags.Ephemeral,
    components: [
      new ActionRowBuilder().addComponents(
        new ButtonBuilder().setLabel("Upgrade to Premium").setStyle(ButtonStyle.Link).setURL(upgradeUrl),
        new ButtonBuilder().setLabel("Support / Info").setStyle(ButtonStyle.Link).setURL(SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/")
      ),
    ],
  });
}

async function handleAnalytics(interaction) {
  if (!interaction.guild) {
    return interaction.reply({ content: "This command can only be used in a server.", flags: MessageFlags.Ephemeral });
  }
  const premium = isPremium(interaction.guild, interaction.member);
  if (!premium) {
    return interaction.reply({ content: "Premium only. Upgrade with /upgrade to use /analytics.", flags: MessageFlags.Ephemeral });
  }
  if (!interaction.memberPermissions?.has(PermissionsBitField.Flags.ManageGuild)) {
    return interaction.reply({ content: "Admins only (Manage Server).", flags: MessageFlags.Ephemeral });
  }

  const config = getGuildConfig(interaction.guild.id);
  const analytics = config.analytics || { channels: {}, holidays: {}, history: [] };
  const history = Array.isArray(analytics.history) ? analytics.history : [];

  const last7 = history.slice(-7);
  const prev7 = history.slice(-14, -7);
  const sum = (arr) => arr.reduce((acc, item) => acc + (item.reactions || 0), 0);
  const last7Total = sum(last7);
  const prev7Total = sum(prev7);
  const trend = prev7Total > 0 ? Math.round(((last7Total - prev7Total) / prev7Total) * 100) : null;

  const channelEntries = Object.entries(analytics.channels || {})
    .map(([channelId, stats]) => ({
      channelId,
      posts: stats.posts || 0,
      reactions: stats.reactions || 0,
      avg: stats.posts ? stats.reactions / stats.posts : 0,
    }))
    .sort((a, b) => b.avg - a.avg);

  const holidayEntries = Object.entries(analytics.holidays || {})
    .map(([slug, stats]) => ({
      slug,
      name: stats.name || slug,
      reactions: stats.reactions || 0,
    }))
    .sort((a, b) => b.reactions - a.reactions)
    .slice(0, 3);

  const hourBuckets = {};
  for (const entry of history) {
    const hour = entry.hour ?? null;
    if (hour === null) continue;
    if (!hourBuckets[hour]) hourBuckets[hour] = { reactions: 0, posts: 0 };
    hourBuckets[hour].reactions += entry.reactions || 0;
    hourBuckets[hour].posts += 1;
  }
  const bestHour = Object.entries(hourBuckets)
    .map(([hour, stats]) => ({
      hour: Number(hour),
      avg: stats.posts ? stats.reactions / stats.posts : 0,
    }))
    .sort((a, b) => b.avg - a.avg)[0];

  const embed = new EmbedBuilder()
    .setTitle("Server Engagement Analytics")
    .setColor(DEFAULT_EMBED_COLOR)
    .setFooter({ text: "Powered by ObscureHolidayCalendar.com" });

  embed.addFields([
    {
      name: "Best posting time",
      value: bestHour ? `${bestHour.hour}:00 (avg ${bestHour.avg.toFixed(1)} reactions/post)` : "Not enough data yet",
    },
    {
      name: "Top holidays by reactions",
      value: holidayEntries.length
        ? holidayEntries.map((h) => `${h.name} (${h.reactions})`).join("\n")
        : "Not enough data yet",
    },
    {
      name: "Top channels",
      value: channelEntries.length
        ? channelEntries
            .slice(0, 3)
            .map((c) => `<#${c.channelId}> — ${c.avg.toFixed(1)} avg (${c.reactions} reactions / ${c.posts} posts)`)
            .join("\n")
        : "Not enough data yet",
    },
    {
      name: "Engagement trend",
      value:
        trend === null
          ? "Not enough data yet"
          : `${trend >= 0 ? "▲" : "▼"} ${Math.abs(trend)}% vs previous 7 days (${last7Total} vs ${prev7Total})`,
    },
  ]);

  if (last7Total === 0 && history.length >= 7) {
    embed.addFields([{ name: "Channel health", value: "📉 Quiet week detected. Try a more playful tone tomorrow." }]);
  } else if (trend !== null && trend < -20) {
    embed.addFields([{ name: "Channel health", value: "📉 Engagement is down this week. Try a fun holiday tomorrow?" }]);
  }

  return interaction.reply({ embeds: [embed], flags: MessageFlags.Ephemeral });
}

async function handleLore(interaction) {
  if (!interaction.guild) {
    return interaction.reply({ content: "This command can only be used in a server.", flags: MessageFlags.Ephemeral });
  }
  const premium = isPremium(interaction.guild, interaction.member);
  if (!premium) {
    return interaction.reply({ content: "Premium only. Upgrade with /upgrade to use /lore.", flags: MessageFlags.Ephemeral });
  }
  if (!interaction.memberPermissions?.has(PermissionsBitField.Flags.ManageGuild)) {
    return interaction.reply({ content: "Admins only (Manage Server).", flags: MessageFlags.Ephemeral });
  }

  const action = interaction.options.getString("action", true);
  const value = interaction.options.getString("value");
  const dateInput = interaction.options.getString("date");
  const description = interaction.options.getString("description");
  const config = getGuildConfig(interaction.guild.id);
  const lore = config.lore;

  if (action === "set_anniversary") {
    const parsed = parseDate(dateInput || "");
    if (!parsed) return interaction.reply({ content: "Provide a date as MM-DD for the anniversary.", flags: MessageFlags.Ephemeral });
    lore.anniversary = parsed;
    saveGuildConfig();
    return interaction.reply({ content: `Server anniversary set to ${parsed}.`, flags: MessageFlags.Ephemeral });
  }

  if (action === "add_keyword") {
    if (!value) return interaction.reply({ content: "Provide a keyword or phrase.", flags: MessageFlags.Ephemeral });
    const clean = value.trim();
    if (!clean) return interaction.reply({ content: "Provide a keyword or phrase.", flags: MessageFlags.Ephemeral });
    if (!lore.keywords.includes(clean)) lore.keywords.push(clean);
    saveGuildConfig();
    return interaction.reply({ content: `Added lore keyword: ${clean}`, flags: MessageFlags.Ephemeral });
  }

  if (action === "remove_keyword") {
    if (!value) return interaction.reply({ content: "Provide a keyword to remove.", flags: MessageFlags.Ephemeral });
    lore.keywords = lore.keywords.filter((k) => k.toLowerCase() !== value.toLowerCase());
    saveGuildConfig();
    return interaction.reply({ content: `Removed lore keyword: ${value}`, flags: MessageFlags.Ephemeral });
  }

  if (action === "add_custom") {
    if (!value) return interaction.reply({ content: "Provide a custom holiday name.", flags: MessageFlags.Ephemeral });
    const parsed = parseDate(dateInput || "");
    if (!parsed) return interaction.reply({ content: "Provide a date as MM-DD for the custom holiday.", flags: MessageFlags.Ephemeral });
    lore.customs = lore.customs.filter((c) => c.name.toLowerCase() !== value.toLowerCase());
    lore.customs.push({ name: value.trim(), date: parsed, description: description?.trim() || "" });
    saveGuildConfig();
    return interaction.reply({ content: `Added custom holiday: ${value} (${parsed}).`, flags: MessageFlags.Ephemeral });
  }

  if (action === "remove_custom") {
    if (!value) return interaction.reply({ content: "Provide a custom holiday name to remove.", flags: MessageFlags.Ephemeral });
    lore.customs = lore.customs.filter((c) => c.name.toLowerCase() !== value.toLowerCase());
    saveGuildConfig();
    return interaction.reply({ content: `Removed custom holiday: ${value}`, flags: MessageFlags.Ephemeral });
  }

  if (action === "list") {
    const lines = [
      lore.anniversary ? `Anniversary: ${lore.anniversary}` : "Anniversary: not set",
      lore.keywords.length ? `Keywords: ${lore.keywords.join(", ")}` : "Keywords: none",
      lore.customs.length
        ? `Custom holidays: ${lore.customs.map((c) => `${c.name} (${c.date})`).join(", ")}`
        : "Custom holidays: none",
    ];
    return interaction.reply({ content: lines.join("\n"), flags: MessageFlags.Ephemeral });
  }

  return interaction.reply({ content: "Unknown lore action.", flags: MessageFlags.Ephemeral });
}

async function handleUpgrade(interaction) {
  if (!stripeClient || !STRIPE_PRICE_ID_STANDARD || !STRIPE_PRICE_ID_INTRO) {
    return interaction.reply({ content: "Stripe is not configured. Try again later.", flags: MessageFlags.Ephemeral });
  }
  const guildId = interaction.guildId;
  const userId = interaction.user.id;
  try {
    const session = await createPremiumCheckoutSession({ guildId, userId });
    return interaction.reply({
      content: `Upgrade to premium using Stripe Checkout: ${session.url}`,
      flags: MessageFlags.Ephemeral,
    });
  } catch (err) {
    console.error("Stripe checkout error:", err);
    return interaction.reply({ content: "Unable to create checkout session right now.", flags: MessageFlags.Ephemeral });
  }
}

async function handleManage(interaction) {
  if (!stripeClient) return interaction.reply({ content: "Stripe is not configured.", flags: MessageFlags.Ephemeral });
  const premium = isPremium(interaction.guild, interaction.member);
  if (!premium) {
    return interaction.reply({ content: "This server is not premium yet. Use /upgrade to start a subscription.", flags: MessageFlags.Ephemeral });
  }
  // Find the customer for this guild by looking up active subscriptions with matching metadata
  let customerId = null;
  try {
    let startingAfter = null;
    while (true) {
      const subs = await stripeClient.subscriptions.list({
        status: "active",
        limit: 100,
        starting_after: startingAfter || undefined,
      });
      for (const sub of subs.data) {
        const gid = sub.metadata?.guild_id || sub.items?.data?.[0]?.metadata?.guild_id;
        if (gid === interaction.guildId && subscriptionHasPremiumPrice(sub)) {
          customerId = sub.customer;
          break;
        }
      }
      if (customerId || !subs.has_more) break;
      startingAfter = subs.data[subs.data.length - 1].id;
    }
  } catch (err) {
    console.error("Stripe lookup error:", err);
  }

  try {
    const session = await stripeClient.billingPortal.sessions.create({
      customer: customerId || undefined,
      return_url: STRIPE_PORTAL_RETURN_URL,
    });
    if (session.url) {
      return interaction.reply({ content: `Manage your subscription here: ${session.url}`, flags: MessageFlags.Ephemeral });
    }
  } catch (err) {
    console.error("Stripe portal error:", err);
  }
  return interaction.reply({ content: "Unable to open the billing portal right now. If you just subscribed, give it a minute and try again.", flags: MessageFlags.Ephemeral });
}

async function handleGrantPremium(interaction) {
  if (!isOwner(interaction.user.id)) {
    return interaction.reply({ content: "Owner-only command.", flags: MessageFlags.Ephemeral });
  }
  const serverId = interaction.options.getString("server_id", true);
  const enabled = interaction.options.getBoolean("enabled");
  const flag = typeof enabled === "boolean" ? enabled : true;
  if (flag) {
    premiumAllowlist[serverId] = true;
  } else {
    delete premiumAllowlist[serverId];
  }
  writeJsonSafe(PREMIUM_PATH, premiumAllowlist);
  return interaction.reply({ content: `Premium ${flag ? "granted to" : "revoked from"} ${serverId}.`, flags: MessageFlags.Ephemeral });
}

async function handleInstallCount(interaction) {
  if (!isOwner(interaction.user.id)) {
    return interaction.reply({ content: "Owner-only command.", flags: MessageFlags.Ephemeral });
  }
  const count = client.guilds.cache.size;
  return interaction.reply({ content: `I am currently in ${count} server(s).`, flags: MessageFlags.Ephemeral });
}

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessageReactions,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.GuildMembers,
  ],
  partials: [Partials.Message, Partials.Channel, Partials.Reaction],
});

client.once("clientReady", async () => {
  console.log(`Bot logged in as ${client.user.tag}`);

  // Presence / status
  client.user.setPresence({
    activities: [{ name: "obscure holidays", type: ActivityType.Watching }],
    status: "online",
  });

  // Register slash commands
  try {
    if (GUILD_ID) {
      const guild = await client.guilds.fetch(GUILD_ID);
      await guild.commands.set(commandDefs);
      console.log(`Registered slash commands for guild ${guild.name}`);
    } else {
      await client.application.commands.set(commandDefs);
      console.log("Registered global slash commands (may take a few minutes to propagate).");
    }
  } catch (err) {
    console.error("Failed to register commands:", err);
  }

  // Sync premium allowlist from Stripe on startup
  await syncPremiumFromStripe();

  // Schedule daily auto-post
  scheduleDailyPost();

  // Post stats to top.gg now and on interval
  postTopGGStats();
  if (TOPGG_TOKEN && TOPGG_POST_INTERVAL_MIN > 0) {
    setInterval(postTopGGStats, TOPGG_POST_INTERVAL_MIN * 60 * 1000);
  }

  // Post stats to discordservices.net now and on interval
  postDiscordServicesStats();
  if (DISCORDSERVICES_TOKEN && DISCORDSERVICES_POST_INTERVAL_MIN > 0) {
    setInterval(postDiscordServicesStats, DISCORDSERVICES_POST_INTERVAL_MIN * 60 * 1000);
  }
});

client.on("interactionCreate", async (interaction) => {
  if (!interaction.isChatInputCommand()) return;
  try {
    switch (interaction.commandName) {
      case "today":
        return handleToday(interaction);
      case "date":
        return handleDate(interaction);
      case "search":
        return handleSearch(interaction);
      case "random":
        return handleRandom(interaction);
      case "vote":
        return handleVote(interaction);
      case "rate":
        return handleRate(interaction);
      case "facts":
        return handleFacts(interaction);
      case "fact":
        return handleFact(interaction);
      case "streak":
        return handleStreak(interaction);
      case "setup":
        return handleSetup(interaction);
      case "premium":
        return handlePremiumStatus(interaction);
      case "analytics":
        return handleAnalytics(interaction);
      case "lore":
        return handleLore(interaction);
      case "week":
        return handleWeek(interaction);
      case "upgrade":
        return handleUpgrade(interaction);
      case "manage":
        return handleManage(interaction);
      case "tomorrow":
        return handleTomorrow(interaction);
      case "upcoming":
        return handleUpcoming(interaction);
      case "grantpremium":
        return handleGrantPremium(interaction);
      case "installcount":
        return handleInstallCount(interaction);
      case "invite":
        return interaction.reply({
          content: "Invite the bot to your server:",
          components: [
            new ActionRowBuilder().addComponents(
              new ButtonBuilder().setLabel("Invite the Bot").setStyle(ButtonStyle.Link).setURL(BOT_INVITE_URL),
              new ButtonBuilder().setLabel("Get the App").setStyle(ButtonStyle.Link).setURL(APP_URL)
            ),
          ],
        });
      case "support":
        return interaction.reply({
          content: "Need help? Visit our landing page:",
          components: [
            new ActionRowBuilder().addComponents(
              new ButtonBuilder().setLabel("Support / Landing").setStyle(ButtonStyle.Link).setURL(SUPPORT_URL),
              new ButtonBuilder().setLabel("Invite the Bot").setStyle(ButtonStyle.Link).setURL(BOT_INVITE_URL)
            ),
          ],
          flags: MessageFlags.Ephemeral,
        });
      case "app":
        return interaction.reply({
          content: "Get the Obscure Holiday Calendar app:",
          components: [
            new ActionRowBuilder().addComponents(
              new ButtonBuilder().setLabel("Get the App").setStyle(ButtonStyle.Link).setURL(APP_URL),
              new ButtonBuilder().setLabel("View Website").setStyle(ButtonStyle.Link).setURL(SITE_URL)
            ),
          ],
          flags: MessageFlags.Ephemeral,
        });
      case "slack":
        return interaction.reply({
          content: "We also have a Slack bot for daily holiday posts:",
          components: [
            new ActionRowBuilder().addComponents(
              new ButtonBuilder().setLabel("Slack Bot Info").setStyle(ButtonStyle.Link).setURL(SLACK_BOT_URL)
            ),
          ],
          flags: MessageFlags.Ephemeral,
        });
      case "help":
        return handleHelp(interaction);
      default:
        return interaction.reply({ content: "Unknown command.", flags: MessageFlags.Ephemeral });
    }
  } catch (err) {
    console.error(err);
    if (interaction.replied || interaction.deferred) {
      return interaction.followUp({ content: "Something went wrong handling that request.", flags: MessageFlags.Ephemeral });
    }
    return interaction.reply({ content: "Something went wrong handling that request.", flags: MessageFlags.Ephemeral });
  }
});

client.on("messageReactionAdd", async (reaction, user) => {
  if (user.bot) return;
  try {
    if (reaction.partial) await reaction.fetch();
    const message = reaction.message;
    if (!message || !message.guild) return;
    const guildId = message.guild.id;
    const channelId = message.channel.id;
    const config = getGuildConfig(guildId);
    const channelSettings = config.channelSettings?.[channelId];
    if (!channelSettings || !channelSettings.lastPostMessageId) return;
    if (channelSettings.lastPostMessageId !== message.id) return;
    recordReactionAnalytics(config, channelId, channelSettings.lastPostDateKey || "");
    saveGuildConfig();
    await recordGuildStreak(guildId, channelId, user.id);
  } catch (e) {
    console.warn("Streak reaction handler failed:", e.message);
  }
});

client.on("guildCreate", async (guild) => {
  postTopGGStats();
  try {
    const owner = await guild.fetchOwner();
    if (!owner?.user) return;
    await owner.user.send(
      [
        "Thanks for adding Obscure Holiday Calendar!",
        "Run /setup to pick a daily-post channel.",
        "Try /today for a quick holiday card.",
        "Premium: /upgrade to subscribe, /manage to cancel anytime.",
      ].join("\n")
    );
  } catch (err) {
    console.warn("Owner welcome DM failed:", err.message);
  }
});

client.on("guildDelete", () => {
  postTopGGStats();
});

function scheduleDailyPost() {
  console.log("Scheduling daily posts per guild config...");
  const guildIds = Object.keys(guildConfig);
  if (!guildIds.length) {
    console.log("No guild configs found for scheduling.");
    return;
  }
  let scheduledCount = 0;
  guildIds.forEach((guildId) => {
    const cfg = getGuildConfig(guildId);
    (cfg.channelIds || []).forEach((chId) => {
      scheduleForChannel(guildId, chId);
      scheduledCount += 1;
    });
  });
  if (!scheduledCount) {
    console.log("No channels configured for scheduling.");
    return;
  }
  console.log(`Scheduled ${scheduledCount} channel(s) across ${guildIds.length} guild(s).`);
}

const guildTimers = new Map(); // key `${guildId}:${channelId}` -> timer

function nextRunTimestamp(config) {
  const tz = config.timezone || "UTC";
  const hour = Number.isInteger(config.hour) ? config.hour : 0;
  const now = new Date();
  const nowTz = new Date(now.toLocaleString("en-US", { timeZone: tz }));
  const next = new Date(nowTz);
  next.setHours(hour, 0, 0, 0);
  if (next <= nowTz) next.setDate(next.getDate() + 1);
  // Convert back to UTC timestamp
  const offset = next.getTime() - nowTz.getTime();
  return now.getTime() + offset;
}

function scheduleForChannel(guildId, channelId) {
  const config = getGuildConfig(guildId);
  if (!config.channelIds || !config.channelIds.includes(channelId)) return;
  const channelConfig = getChannelConfig(guildId, channelId);
  const runAt = nextRunTimestamp(channelConfig);
  const delay = Math.max(1000, runAt - Date.now());
  const key = `${guildId}:${channelId}`;
  if (guildTimers.has(key)) clearTimeout(guildTimers.get(key));
  const timer = setTimeout(async () => {
    try {
      await postTodayForChannel(guildId, channelId);
    } catch (e) {
      console.error(`Daily post failed for guild ${guildId} channel ${channelId}:`, e);
    } finally {
      scheduleForChannel(guildId, channelId);
    }
  }, delay);
  guildTimers.set(key, timer);
  console.log(`Scheduled ${guildId}#${channelId} in ${Math.round(delay / 1000 / 60)} minutes (${channelConfig.timezone} @ ${channelConfig.hour}:00)`);
}

async function postTodayForChannel(guildId, channelId) {
  const config = getGuildConfig(guildId);
  if (!config.channelIds || !config.channelIds.includes(channelId)) return;
  const channelSettings = getChannelConfig(guildId, channelId);
  if (channelSettings.skipWeekends) {
    const day = new Date().getDay();
    if (day === 0 || day === 6) return; // Sunday or Saturday
  }
  let channel;
  try {
    channel = await client.channels.fetch(channelId);
  } catch (err) {
    if (isMissingAccessError(err)) {
      removeChannelFromConfig(guildId, channelId, `fetch failed: ${err?.code || err?.status || "unknown"}`);
      return;
    }
    throw err;
  }
  if (!channel || !channel.isTextBased()) return;

  const now = new Date();
  const mmdd = `${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  const hits = findByDate(mmdd);
  const dateKey = getDateKey(now, channelSettings.timezone);
  const wildcardHoliday = premium ? maybePickWildcardHoliday(config, dateKey) : null;
  const filteredHits = applyHolidayFilters(hits, config.filters);
  if (!hits.length) {
    return channel.send("No holiday found for today. Check back tomorrow!");
  }
  if (!filteredHits.length) {
    return channel.send("No holiday found for today with current filters.");
  }

  const premium = isPremiumGuild(channel.guild);
  const branding = !premium || channelSettings.branding;
  const choice = Math.min(channelSettings.holidayChoice || 0, filteredHits.length - 1);
  const pick =
    wildcardHoliday ||
    pickHolidayForTone(filteredHits, channelSettings.tone, choice) ||
    filteredHits[choice] ||
    filteredHits[0];
  const topNames = wildcardHoliday ? pick.name : filteredHits.slice(0, 2).map((h) => h.name).join(" and ");
  const todayEmbed = buildEmbed(pick, {
    branding,
    style: channelSettings.style,
    color: channelSettings.color || undefined,
    tone: channelSettings.tone,
  });

  // Coming up tomorrow teaser
  const tomorrow = new Date(now);
  tomorrow.setDate(now.getDate() + 1);
  const tmm = `${pad(tomorrow.getMonth() + 1)}-${pad(tomorrow.getDate())}`;
  const nextHits = applyHolidayFilters(findByDate(tmm), config.filters);
  const teaser = wildcardHoliday ? "" : nextHits.length ? `Up next: ${nextHits[0].name} (${prettyDate(tmm)})` : "";

  const mention = channelSettings.quiet ? "" : channelSettings.roleId ? `<@&${channelSettings.roleId}> ` : "";

  const { rows: promoRows, note: promoNote } = buildPromoComponents(guildId, { includeRate: true, forceVote: true });
  const components = [...buildButtons(pick), ...promoRows];
  const streakLine = config.streakCount ? `\n🔥 Server streak: ${config.streakCount} day${config.streakCount === 1 ? "" : "s"}` : "";
  const wildcardLine = wildcardHoliday ? "\n🪄 Wildcard Day: surprise pick" : "";
  const promptLine = buildMicroPrompt(pick, channelSettings.tone);
  const loreLines = buildLoreLines(config, getDateKey(now, channelSettings.timezone));
  try {
    const sent = await channel.send({
      content: `${mention}🎉 Today’s holidays: ${topNames}${wildcardLine}${teaser ? `\n${teaser}` : ""}${streakLine}${loreLines.length ? `\n\n${loreLines.join("\n")}` : ""}${promptLine ? `\n\n${promptLine}` : ""}${promoNote ? `\n\n${promoNote}` : ""}`,
      embeds: [todayEmbed],
      components,
    });
    console.log(`Daily post sent for guild ${guildId} channel ${channelId}.`);
    const postDateKey = dateKey;
    const settings = config.channelSettings?.[channelId] || {};
    settings.lastPostMessageId = sent?.id || null;
    settings.lastPostDateKey = postDateKey;
    settings.lastPostSlug = pick.slug || slugify(pick.name || "holiday");
    settings.lastPostName = pick.name || settings.lastPostSlug;
    config.channelSettings[channelId] = settings;
    recordPostAnalytics(config, channelId, postDateKey, channelSettings.hour, pick);
    saveGuildConfig();
    scheduleDidYouKnow(channel, sent?.id || null, pick);
  } catch (err) {
    if (isMissingAccessError(err)) {
      removeChannelFromConfig(guildId, channelId, `send failed: ${err?.code || err?.status || "unknown"}`);
      return;
    }
    throw err;
  }
}

// Start HTTP server (Stripe + health)
const listenPort = PORT || 8080;
http.createServer(app).listen(listenPort, () => {
  console.log(`HTTP server listening on ${listenPort}`);
});

client.login(TOKEN);
