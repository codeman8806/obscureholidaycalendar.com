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
const BOTLIST_TOKEN = normalizeApiToken(process.env.BOTLIST_TOKEN); // for posting stats to botlist.me
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
function formatDiscordServicesAuth(token) {
  if (!token) return null;
  if (/^(bot|bearer)\s+/i.test(token)) return token;
  return `Bot ${token}`;
}
const TOPGG_POST_INTERVAL_MIN = Number(process.env.TOPGG_POST_INTERVAL_MIN || "30");
const DISCORDSERVICES_POST_INTERVAL_MIN = Number(process.env.DISCORDSERVICES_POST_INTERVAL_MIN || TOPGG_POST_INTERVAL_MIN || "30");
const BOTLIST_POST_INTERVAL_MIN = Number(process.env.BOTLIST_POST_INTERVAL_MIN || TOPGG_POST_INTERVAL_MIN || "30");
const PORT = process.env.PORT || null; // for Railway/health checks (optional)
const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY || null;
const STRIPE_PRICE_ID_STANDARD = process.env.STRIPE_PRICE_ID_STANDARD || process.env.STRIPE_PRICE_ID || null; // $3.99/month
const STRIPE_PRICE_ID_INTRO = process.env.STRIPE_PRICE_ID_INTRO || null; // $0.99 first month
const STRIPE_PRICE_ID_TRIAL = process.env.STRIPE_PRICE_ID_TRIAL || null; // optional trial price override
const STRIPE_TRIAL_DAYS = Number(process.env.STRIPE_TRIAL_DAYS || "7");
const TRIAL_DAYS = Number.isFinite(STRIPE_TRIAL_DAYS) && STRIPE_TRIAL_DAYS > 0 ? STRIPE_TRIAL_DAYS : 7;
const TRIAL_DURATION_MS = TRIAL_DAYS * 24 * 60 * 60 * 1000;
const STRIPE_PORTAL_URL = process.env.STRIPE_PORTAL_URL || null;
const STRIPE_LOOKUP_KEY = process.env.STRIPE_LOOKUP_KEY || null; // optional lookup key
const STRIPE_WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET || null;
const STRIPE_SUCCESS_URL = process.env.STRIPE_SUCCESS_URL || `${SITE_URL}/discord-bot/?success=1`;
const STRIPE_CANCEL_URL = process.env.STRIPE_CANCEL_URL || `${SITE_URL}/discord-bot/?canceled=1`;
const STRIPE_PORTAL_RETURN_URL = process.env.STRIPE_PORTAL_RETURN_URL || `${SITE_URL}/discord-bot/`;
const PUBLIC_BASE_URL = process.env.PUBLIC_BASE_URL || null;
const DEFAULT_HOLIDAY_CHOICE = 0; // which holiday of the day to schedule: 0 = first, 1 = second
const DEFAULT_EMBED_COLOR = 0x1c96f3;
const DEFAULT_EMBED_STYLE = "compact";
const DEFAULT_TIMEZONE = "UTC";
const PROMO_VOTE_INTERVAL_MS = 7 * 24 * 60 * 60 * 1000; // once per week per guild
const PROMO_RATE_INTERVAL_MS = 30 * 24 * 60 * 60 * 1000; // once per 30 days per guild
const PREMIUM_PROMO_INTERVAL_MS = 7 * 24 * 60 * 60 * 1000; // once per 7 days per guild
const SHARE_PROMO_INTERVAL_MS = 14 * 24 * 60 * 60 * 1000; // once per 14 days per guild
const ACTIVATION_REMINDER_DELAY_MS = 24 * 60 * 60 * 1000; // 24h after join if setup incomplete
const ACTIVATION_SWEEP_INTERVAL_MS = 30 * 60 * 1000; // every 30 minutes
const WEEKLY_RECAP_INTERVAL_MS = 6 * 60 * 60 * 1000; // check every 6 hours
const DEFAULT_STREAK_GOAL = 7;
const FOLLOWUP_DELAY_MIN = Number(process.env.FOLLOWUP_DELAY_MIN || "45");
const DEFAULT_TONE = "default";
const ALLOWED_TONES = new Set(["wholesome", "silly", "nerdy", "historical", "global", "default"]);
const MAX_ANALYTICS_HISTORY = 120;
const MAX_EVENT_HISTORY = 200;
const FOOD_KEYWORDS = ["pizza", "burger", "chocolate", "cake", "coffee", "tea", "soup", "cheese", "ice cream", "taco", "donut", "bacon", "cookie", "bread", "pasta"];
const RELIGIOUS_KEYWORDS = ["christmas", "easter", "ramadan", "hanukkah", "diwali", "yom kippur", "lent", "ash wednesday", "saint", "holy", "religious"];
const WEIRD_KEYWORDS = ["weird", "absurd", "odd", "quirky", "strange", "silly", "goof", "bizarre", "random", "peculiar"];
const INTERNATIONAL_KEYWORDS = ["international", "world", "global"];
const SAFE_MODE_BLOCKLIST = ["adult", "sex", "drug", "alcohol", "beer", "wine", "weed", "marijuana", "violence", "gambling"];
const CATEGORY_KEYWORDS = {
  food: FOOD_KEYWORDS,
  religious: RELIGIOUS_KEYWORDS,
  weird: WEIRD_KEYWORDS,
  international: INTERNATIONAL_KEYWORDS,
  seasonal: ["spring", "summer", "autumn", "fall", "winter", "solstice", "equinox", "harvest", "halloween", "valentine", "new year"],
  nature: ["earth", "ocean", "sea", "river", "forest", "tree", "garden", "green", "climate", "environment", "conservation", "animal", "pet", "dog", "cat", "bird", "wildlife"],
  health: ["health", "wellness", "fitness", "exercise", "mental", "awareness", "cancer", "heart", "diabetes", "blood", "safety", "prevention"],
  tech: ["tech", "technology", "science", "engineering", "math", "computer", "internet", "coding", "programming", "robot", "space"],
  arts: ["art", "music", "dance", "theater", "poetry", "book", "literature", "film", "movie", "photography", "design"],
  community: ["community", "friend", "family", "volunteer", "charity", "kindness", "gratitude", "teacher", "nurse", "service"],
};
const ALL_CATEGORIES = [...Object.keys(CATEGORY_KEYWORDS), "general"];
const SENSITIVE_KEYWORDS = [...SAFE_MODE_BLOCKLIST, "weapon", "gun", "war", "suicide", "death", "crime", "abuse"];

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
    return true;
  } catch (e) {
    console.error(`Failed to write ${filePath}:`, e);
    return false;
  }
}

const guildConfig = readJsonSafe(CONFIG_PATH, {});
const premiumAllowlist = readJsonSafe(PREMIUM_PATH, {});
const stripeClient = STRIPE_SECRET_KEY ? new Stripe(STRIPE_SECRET_KEY) : null;
const SITE_BASE = "https://www.obscureholidaycalendar.com/holiday";

function getPlanStatus(config, now = Date.now()) {
  if (config?.isPremium) return "premium";
  const endsAt = Number(config?.trialEndsAt || 0);
  if (endsAt > 0 && now < endsAt) return "trial";
  return "free";
}

function effectivePremium(config, now = Date.now(), guildId = null) {
  if (!config) return false;
  if (config.isPremium) return true;
  const endsAt = Number(config.trialEndsAt || 0);
  if (endsAt > 0 && now < endsAt) return true;
  if (endsAt > 0 && now >= endsAt) {
    config.trialStartedAt = 0;
    config.trialEndsAt = 0;
    if (guildId) saveGuildConfig();
  }
  return false;
}

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
    if (!("allowedCategories" in cfg)) {
      cfg.allowedCategories = null;
      changed = true;
      updated = true;
    }
    if (typeof cfg.excludeSensitive !== "boolean") {
      cfg.excludeSensitive = false;
      changed = true;
      updated = true;
    }
    if (!cfg.trialStartedAt) {
      cfg.trialStartedAt = 0;
      changed = true;
      updated = true;
    }
    if (!cfg.trialEndsAt) {
      cfg.trialEndsAt = 0;
      changed = true;
      updated = true;
    }
    if (!cfg.trialRedeemedAt) {
      cfg.trialRedeemedAt = 0;
      changed = true;
      updated = true;
    }
    if (!cfg.featureAnnouncementSentAt) {
      cfg.featureAnnouncementSentAt = 0;
      changed = true;
      updated = true;
    }
    if (!cfg.trialReminderSentAt) {
      cfg.trialReminderSentAt = 0;
      changed = true;
      updated = true;
    }
    if (typeof cfg.trialReminderPending !== "boolean") {
      cfg.trialReminderPending = false;
      changed = true;
      updated = true;
    }
    if (!cfg.trialReminderSentAt) {
      cfg.trialReminderSentAt = 0;
      changed = true;
      updated = true;
    }
    if (!Array.isArray(cfg.blockedHolidayIds)) {
      cfg.blockedHolidayIds = [];
      changed = true;
      updated = true;
    }
    if (!Array.isArray(cfg.forcedHolidayIds)) {
      cfg.forcedHolidayIds = [];
      changed = true;
      updated = true;
    }
    if (typeof cfg.upsellWeekKey !== "string") {
      cfg.upsellWeekKey = "";
      changed = true;
      updated = true;
    }
    if (!Number.isInteger(cfg.upsellWeekCount)) {
      cfg.upsellWeekCount = 0;
      changed = true;
      updated = true;
    }
    if (typeof cfg.isPremium !== "boolean") {
      cfg.isPremium = !!premiumAllowlist[guildId];
      changed = true;
      updated = true;
    }
    if (typeof cfg.onboardingDmSent !== "boolean") {
      cfg.onboardingDmSent = false;
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
    if (!cfg.lastPremiumPromptAt) {
      cfg.lastPremiumPromptAt = 0;
      changed = true;
      updated = true;
    }
    if (!cfg.lastSharePromptAt) {
      cfg.lastSharePromptAt = 0;
      changed = true;
      updated = true;
    }
    if (!cfg.lastWeeklyRecapAt) {
      cfg.lastWeeklyRecapAt = 0;
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
  const holidays = data.holidays || {};
  Object.values(holidays).forEach((items) => {
    if (!Array.isArray(items)) return;
    items.forEach((holiday) => {
      ensureHolidayMeta(holiday);
    });
  });
  return holidays;
}

const holidaysByDate = loadHolidays();
const allHolidays = Object.values(holidaysByDate).flat();
normalizeAllGuildConfigs();

function isPremium(guild, member) {
  if (!guild) return false;
  const config = getGuildConfig(guild.id);
  if (effectivePremium(config, Date.now(), guild.id)) return true;
  // Discord Server Subscription role check on interacting member
  if (PREMIUM_ROLE_ID && member && member.roles && member.roles.cache.has(PREMIUM_ROLE_ID)) return true;
  // Allowlist fallback
  if (premiumAllowlist[guild.id]) return true;
  return false;
}

function isPremiumGuild(guild) {
  if (!guild) return false;
  const config = getGuildConfig(guild.id);
  if (effectivePremium(config, Date.now(), guild.id)) return true;
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
  const config = getGuildConfig(guildId);
  config.isPremium = !!enabled;
  saveGuildConfig();
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
    const authHeader = formatDiscordServicesAuth(DISCORDSERVICES_TOKEN);
    const payload = {
      servers: serverCount,
      guilds: serverCount,
      server_count: serverCount,
      shards: shardCount,
      shard_count: shardCount,
    };
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: authHeader,
      },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const text = await res.text();
      console.error(
        "Discord Services stats post failed:",
        res.status,
        text,
        `url=${url}`,
        `payload=${JSON.stringify(payload)}`
      );
    } else {
      console.log(`Posted stats to discordservices.net: ${serverCount} servers (${shardCount} shards)`);
    }
  } catch (e) {
    console.warn("discordservices stats post failed:", e.message);
  }
}

async function postBotListStats() {
  if (!BOTLIST_TOKEN) return;
  try {
    const serverCount = client.guilds.cache.size;
    const botId = process.env.BOTLIST_BOT_ID || client.user?.id;
    if (!botId) return;
    const shardCount = Number(process.env.BOTLIST_SHARDS || process.env.DISCORDSERVICES_SHARDS || "1");
    const res = await fetch(`https://api.botlist.me/api/v1/bots/${botId}/stats`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        authorization: BOTLIST_TOKEN,
      },
      body: JSON.stringify({ server_count: serverCount, shard_count: shardCount }),
    });
    if (!res.ok) {
      const text = await res.text();
      console.warn(`botlist.me stats post failed: ${res.status} ${text}`);
    } else {
      console.log(`Posted stats to botlist.me: ${serverCount} servers`);
    }
  } catch (e) {
    console.warn("botlist.me stats post failed:", e.message);
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

async function createTrialCheckoutSession({ guildId, userId, customerEmail }) {
  const priceId = STRIPE_PRICE_ID_TRIAL || STRIPE_PRICE_ID_STANDARD;
  if (!stripeClient || !priceId || !TRIAL_DAYS) return null;
  const metadata = { guild_id: guildId, user_id: userId || "", trial: "true" };
  return stripeClient.checkout.sessions.create({
    mode: "subscription",
    customer_email: customerEmail || undefined,
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: STRIPE_SUCCESS_URL,
    cancel_url: STRIPE_CANCEL_URL,
    metadata,
    subscription_data: {
      metadata,
      trial_period_days: TRIAL_DAYS,
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

app.get("/start-trial", async (req, res) => {
  const guildId = req.query.guild_id;
  const userId = req.query.user_id;
  if (!guildId) return res.status(400).send("Missing guild_id");
  const result = await startTrialAndGetCheckoutUrl(String(guildId), userId ? String(userId) : "");
  if (!result.ok) {
    return res.redirect(SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/");
  }
  if (result.url) return res.redirect(result.url);
  return res.redirect(SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/");
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
        const isTrialSession = session.metadata?.trial === "true";
        if (isTrialSession) {
          const config = getGuildConfig(guildId);
          if (!config.trialRedeemedAt) startTrialForConfig(config, guildId, session.metadata?.user_id || "");
          console.log(`Trial started via Stripe for guild ${guildId}`);
        } else {
          setPremiumGuild(guildId, true);
          const config = getGuildConfig(guildId);
          recordEvent(config, "upgrade_completed", { guildId, userId: session.metadata?.user_id || "" });
          saveGuildConfig();
          console.log(`Premium granted via Stripe for guild ${guildId}`);
        }
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
      analytics: { channels: {}, holidays: {}, history: [], events: [] },
      allowedCategories: null,
      excludeSensitive: false,
      trialStartedAt: 0,
      trialEndsAt: 0,
      trialRedeemedAt: 0,
      isPremium: false,
      onboardingDmSent: false,
      featureAnnouncementSentAt: 0,
      trialReminderSentAt: 0,
      trialReminderPending: false,
      blockedHolidayIds: [],
      forcedHolidayIds: [],
      upsellWeekKey: "",
      upsellWeekCount: 0,
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
      promotionsEnabled: true,
      lastVotePromptAt: 0,
      lastRatePromptAt: 0,
      lastPremiumPromptAt: 0,
      lastSharePromptAt: 0,
      lastWeeklyRecapAt: 0,
      lastDailyPostAt: 0,
      lastDailyPostStatus: null,
      lastDailyPostAttempts: [],
      firstSeenAt: Date.now(),
      activationReminderDueAt: Date.now() + ACTIVATION_REMINDER_DELAY_MS,
      activationReminderSentAt: 0,
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
  if (!Array.isArray(guildConfig[guildId].analytics.events)) guildConfig[guildId].analytics.events = [];
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
  if (!("allowedCategories" in guildConfig[guildId])) {
    guildConfig[guildId].allowedCategories = null;
  }
  if (Array.isArray(guildConfig[guildId].allowedCategories)) {
    guildConfig[guildId].allowedCategories = guildConfig[guildId].allowedCategories
      .map((cat) => String(cat).toLowerCase())
      .filter((cat) => ALL_CATEGORIES.includes(cat));
  }
  if (typeof guildConfig[guildId].excludeSensitive !== "boolean") {
    guildConfig[guildId].excludeSensitive = false;
  }
  if (!guildConfig[guildId].trialStartedAt) {
    guildConfig[guildId].trialStartedAt = 0;
  }
  if (!guildConfig[guildId].trialEndsAt) {
    guildConfig[guildId].trialEndsAt = 0;
  }
  if (!guildConfig[guildId].trialRedeemedAt) {
    guildConfig[guildId].trialRedeemedAt = 0;
  }
  if (!guildConfig[guildId].featureAnnouncementSentAt) {
    guildConfig[guildId].featureAnnouncementSentAt = 0;
  }
  if (!guildConfig[guildId].trialReminderSentAt) {
    guildConfig[guildId].trialReminderSentAt = 0;
  }
  if (typeof guildConfig[guildId].trialReminderPending !== "boolean") {
    guildConfig[guildId].trialReminderPending = false;
  }
  if (typeof guildConfig[guildId].isPremium !== "boolean") {
    guildConfig[guildId].isPremium = !!premiumAllowlist[guildId];
  }
  if (typeof guildConfig[guildId].onboardingDmSent !== "boolean") {
    guildConfig[guildId].onboardingDmSent = false;
  }
  if (!Array.isArray(guildConfig[guildId].blockedHolidayIds)) {
    guildConfig[guildId].blockedHolidayIds = [];
  }
  if (!Array.isArray(guildConfig[guildId].forcedHolidayIds)) {
    guildConfig[guildId].forcedHolidayIds = [];
  }
  if (typeof guildConfig[guildId].upsellWeekKey !== "string") {
    guildConfig[guildId].upsellWeekKey = "";
  }
  if (!Number.isInteger(guildConfig[guildId].upsellWeekCount)) {
    guildConfig[guildId].upsellWeekCount = 0;
  }
  guildConfig[guildId].blockedHolidayIds = guildConfig[guildId].blockedHolidayIds.map((id) => String(id).toLowerCase());
  guildConfig[guildId].forcedHolidayIds = guildConfig[guildId].forcedHolidayIds.map((id) => String(id).toLowerCase());
  if (!guildConfig[guildId].lastVotePromptAt) {
    guildConfig[guildId].lastVotePromptAt = 0;
  }
  if (!guildConfig[guildId].lastRatePromptAt) {
    guildConfig[guildId].lastRatePromptAt = 0;
  }
  if (!guildConfig[guildId].lastPremiumPromptAt) {
    guildConfig[guildId].lastPremiumPromptAt = 0;
  }
  if (!guildConfig[guildId].lastSharePromptAt) {
    guildConfig[guildId].lastSharePromptAt = 0;
  }
  if (!guildConfig[guildId].lastWeeklyRecapAt) {
    guildConfig[guildId].lastWeeklyRecapAt = 0;
  }
  if (!Number.isFinite(Number(guildConfig[guildId].lastDailyPostAt || 0))) {
    guildConfig[guildId].lastDailyPostAt = 0;
  }
  if (!guildConfig[guildId].lastDailyPostStatus || typeof guildConfig[guildId].lastDailyPostStatus !== "object") {
    guildConfig[guildId].lastDailyPostStatus = null;
  }
  if (!Array.isArray(guildConfig[guildId].lastDailyPostAttempts)) {
    guildConfig[guildId].lastDailyPostAttempts = [];
  }
  guildConfig[guildId].lastDailyPostAttempts = guildConfig[guildId].lastDailyPostAttempts
    .filter((attempt) => attempt && Number.isFinite(Number(attempt.at)))
    .slice(-100);
  if (!Number.isFinite(Number(guildConfig[guildId].firstSeenAt || 0))) {
    guildConfig[guildId].firstSeenAt = Date.now();
  }
  if (!Number.isFinite(Number(guildConfig[guildId].activationReminderDueAt || 0))) {
    guildConfig[guildId].activationReminderDueAt = Number(guildConfig[guildId].firstSeenAt || Date.now()) + ACTIVATION_REMINDER_DELAY_MS;
  }
  if (!Number.isFinite(Number(guildConfig[guildId].activationReminderSentAt || 0))) {
    guildConfig[guildId].activationReminderSentAt = 0;
  }
  if (!guildConfig[guildId].featureAnnouncementSentAt) {
    guildConfig[guildId].featureAnnouncementSentAt = 0;
  }
  if (!guildConfig[guildId].trialReminderSentAt) {
    guildConfig[guildId].trialReminderSentAt = 0;
  }
  return guildConfig[guildId];
}

function saveGuildConfig() {
  const ok = writeJsonSafe(CONFIG_PATH, guildConfig);
  const guildCount = Object.keys(guildConfig).length;
  const channelCount = Object.values(guildConfig).reduce((sum, cfg) => sum + ((cfg.channelIds || []).length), 0);
  if (ok) console.log(`Saved guild config to ${CONFIG_PATH} (${guildCount} guilds, ${channelCount} channel(s)).`);
  return ok;
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

function normalizeCategoryList(value) {
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

function hasActiveCategoryFilters(config) {
  if (!config) return false;
  if (config.allowedCategories === null || typeof config.allowedCategories === "undefined") {
    return !!config.excludeSensitive;
  }
  return true;
}

function hasActiveOverrides(config) {
  if (!config) return false;
  return (
    hasActiveFilters(config.filters) ||
    hasActiveCategoryFilters(config) ||
    (config.blockedHolidayIds && config.blockedHolidayIds.length > 0) ||
    (config.forcedHolidayIds && config.forcedHolidayIds.length > 0)
  );
}

function weekKeyFromDate(date) {
  const start = new Date(Date.UTC(date.getUTCFullYear(), 0, 1));
  const day = Math.floor((date - start) / (24 * 60 * 60 * 1000));
  const week = Math.floor((day + start.getUTCDay()) / 7) + 1;
  return `${date.getUTCFullYear()}-W${String(week).padStart(2, "0")}`;
}

function shouldShowUpsell(config, date, hiddenCount) {
  if (!config || hiddenCount < 1) return false;
  const weekKey = weekKeyFromDate(date);
  if (config.upsellWeekKey !== weekKey) {
    config.upsellWeekKey = weekKey;
    config.upsellWeekCount = 0;
  }
  const maxPerWeek = hiddenCount >= 2 ? 3 : 1;
  return (config.upsellWeekCount || 0) < maxPerWeek;
}

function matchesKeyword(text, keywords) {
  return keywords.some((kw) => text.includes(kw));
}

function holidayText(holiday) {
  return `${holiday.name || ""} ${holiday.description || ""}`.toLowerCase();
}

function holidayId(holiday) {
  if (!holiday) return "";
  return String(holiday.id || holiday.slug || slugify(holiday.name || "holiday")).toLowerCase();
}

function resolveHolidayByIdOrName(input) {
  if (!input) return null;
  const needle = String(input).trim().toLowerCase();
  const direct = allHolidays.find((holiday) => holidayId(holiday) === needle);
  if (direct) return direct;
  const matches = findByName(needle);
  return matches.length ? matches[0] : null;
}

function computeHolidayCategories(holiday) {
  const text = holidayText(holiday);
  const categories = [];
  for (const [category, keywords] of Object.entries(CATEGORY_KEYWORDS)) {
    if (matchesKeyword(text, keywords)) categories.push(category);
  }
  if (!categories.length) categories.push("general");
  return categories;
}

function isSensitiveHoliday(holiday) {
  const text = holidayText(holiday);
  return matchesKeyword(text, SENSITIVE_KEYWORDS);
}

function ensureHolidayMeta(holiday) {
  if (!Array.isArray(holiday.categories) || !holiday.categories.length) {
    holiday.categories = computeHolidayCategories(holiday);
  }
  if (typeof holiday.is_sensitive !== "boolean") {
    holiday.is_sensitive = isSensitiveHoliday(holiday);
  }
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

function applyCategoryFilters(hits, config) {
  if (!config) return hits || [];
  const allowed = config.allowedCategories;
  const excludeSensitive = !!config.excludeSensitive;
  return (hits || []).filter((holiday) => {
    ensureHolidayMeta(holiday);
    if (excludeSensitive && holiday.is_sensitive) return false;
    if (allowed === null || typeof allowed === "undefined") return true;
    if (!Array.isArray(allowed) || !allowed.length) return false;
    const categories = (holiday.categories || []).map((c) => c.toLowerCase());
    return categories.some((c) => allowed.includes(c));
  });
}

function applyServerFilters(hits, config) {
  if (!config) return hits || [];
  const blockedIds = new Set((config.blockedHolidayIds || []).map((id) => String(id).toLowerCase()));
  const forcedIds = new Set((config.forcedHolidayIds || []).map((id) => String(id).toLowerCase()));
  if (forcedIds.size) {
    return (hits || []).filter((holiday) => {
      const id = holidayId(holiday);
      if (!id || blockedIds.has(id)) return false;
      return forcedIds.has(id);
    });
  }
  const keywordFiltered = applyHolidayFilters(hits, config.filters);
  const categoryFiltered = applyCategoryFilters(keywordFiltered, config);
  if (!blockedIds.size) return categoryFiltered;
  return categoryFiltered.filter((holiday) => {
    const id = holidayId(holiday);
    return !id || !blockedIds.has(id);
  });
}

function summarizeFilterReasons(hits, filtered, config) {
  if (!config) return null;
  const total = hits.length;
  const kept = filtered.length;
  const removed = total - kept;
  if (!removed) return null;
  const blockedIds = new Set((config.blockedHolidayIds || []).map((id) => String(id).toLowerCase()));
  const forcedIds = new Set((config.forcedHolidayIds || []).map((id) => String(id).toLowerCase()));
  const reasons = {};
  for (const holiday of hits) {
    const id = holidayId(holiday);
    const removedByForced = forcedIds.size && !forcedIds.has(id);
    if (removedByForced) {
      reasons.not_forced = (reasons.not_forced || 0) + 1;
      continue;
    }
    if (blockedIds.has(id)) {
      reasons.blocked = (reasons.blocked || 0) + 1;
      continue;
    }
    if (!filterHoliday(holiday, config.filters)) {
      reasons.keyword_filter = (reasons.keyword_filter || 0) + 1;
      continue;
    }
    ensureHolidayMeta(holiday);
    if (config.excludeSensitive && holiday.is_sensitive) {
      reasons.sensitive = (reasons.sensitive || 0) + 1;
      continue;
    }
    const allowed = config.allowedCategories;
    if (allowed !== null && typeof allowed !== "undefined") {
      const categories = (holiday.categories || []).map((c) => c.toLowerCase());
      if (!categories.some((c) => allowed.includes(c))) {
        reasons.category = (reasons.category || 0) + 1;
        continue;
      }
    }
  }
  return { total, kept, removed, reasons };
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

  const filtered = applyServerFilters(allHolidays, config);
  if (!filtered.length && hasActiveOverrides(config)) return null;
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

function recordEvent(config, event, meta = {}) {
  if (!config) return { ok: false, error: "missing_config" };
  try {
    if (!config.analytics) config.analytics = { channels: {}, holidays: {}, history: [], events: [] };
    if (!Array.isArray(config.analytics.events)) config.analytics.events = [];
    const planStatus = getPlanStatus(config);
    const at = Date.now();
    const eventId = `${at}_${Math.random().toString(36).slice(2, 8)}`;
    config.analytics.events.push({ id: eventId, event, at, meta: { planStatus, ...meta } });
    if (config.analytics.events.length > MAX_EVENT_HISTORY) {
      config.analytics.events = config.analytics.events.slice(-MAX_EVENT_HISTORY);
    }
    return { ok: true, eventId, at };
  } catch (err) {
    console.error("recordEvent failed:", err?.stack || err?.message || err);
    return { ok: false, error: err?.message || "record_event_failed" };
  }
}

function markDailyPostAttempt(config, attempt) {
  if (!config || !attempt) return;
  const at = Number(attempt.at || Date.now());
  const merged = {
    at,
    guildId: String(attempt.guildId || ""),
    channelId: String(attempt.channelId || ""),
    status: String(attempt.status || "unknown"),
    reason: String(attempt.reason || ""),
    planStatus: String(attempt.planStatus || getPlanStatus(config)),
  };
  config.lastDailyPostAt = at;
  config.lastDailyPostStatus = {
    at,
    status: merged.status,
    reason: merged.reason,
    guildId: merged.guildId,
    channelId: merged.channelId,
    planStatus: merged.planStatus,
  };
  if (!Array.isArray(config.lastDailyPostAttempts)) config.lastDailyPostAttempts = [];
  config.lastDailyPostAttempts.push(merged);
  if (config.lastDailyPostAttempts.length > 100) {
    config.lastDailyPostAttempts = config.lastDailyPostAttempts.slice(-100);
  }
}

function getEventTimestamp(event) {
  const createdAt = Number(event?.createdAt);
  if (Number.isFinite(createdAt) && createdAt > 0) return createdAt;
  const ts = Number(event?.ts);
  if (Number.isFinite(ts) && ts > 0) return ts;
  const at = Number(event?.at);
  if (Number.isFinite(at) && at > 0) return at;
  return 0;
}

function queryAnalyticsEventsInRange(startMs, endMs) {
  const events = [];
  for (const [guildId, config] of Object.entries(guildConfig)) {
    const rows = Array.isArray(config?.analytics?.events) ? config.analytics.events : [];
    for (const row of rows) {
      const at = getEventTimestamp(row);
      if (!at || at < startMs || at > endMs) continue;
      events.push({ guildId, at, event: row?.event || "", meta: row?.meta || {}, id: row?.id || null });
    }
  }
  events.sort((a, b) => a.at - b.at);
  return events;
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

function canShowPremiumPrompt(guildId) {
  const cfg = getGuildConfig(guildId);
  if (cfg.promotionsEnabled === false) return false;
  const last = Number(cfg.lastPremiumPromptAt || 0);
  return Date.now() - last >= PREMIUM_PROMO_INTERVAL_MS;
}

function markPremiumPrompt(guildId) {
  const cfg = getGuildConfig(guildId);
  cfg.lastPremiumPromptAt = Date.now();
  saveGuildConfig();
}

function canShowSharePrompt(guildId) {
  const cfg = getGuildConfig(guildId);
  if (cfg.promotionsEnabled === false) return false;
  const last = Number(cfg.lastSharePromptAt || 0);
  return Date.now() - last >= SHARE_PROMO_INTERVAL_MS;
}

function markSharePrompt(guildId) {
  const cfg = getGuildConfig(guildId);
  cfg.lastSharePromptAt = Date.now();
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

async function getUpgradeUrlForInteraction(interaction) {
  let upgradeUrl = SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/";
  if (stripeClient && STRIPE_PRICE_ID_STANDARD && STRIPE_PRICE_ID_INTRO) {
    try {
      const session = await createPremiumCheckoutSession({
        guildId: interaction.guildId,
        userId: interaction.user.id,
      });
      if (session?.url) upgradeUrl = session.url;
    } catch (err) {
      console.error("Stripe checkout error (upgrade url):", err);
    }
  }
  return upgradeUrl;
}

function buildTrialStartUrl(guildId, userId) {
  if (!PUBLIC_BASE_URL) return null;
  const base = PUBLIC_BASE_URL.replace(/\/+$/, "");
  return `${base}/start-trial?guild_id=${guildId}&user_id=${userId || ""}`;
}

function startTrialForConfig(config, guildId, userId) {
  if (!config || config.trialRedeemedAt) return false;
  const now = Date.now();
  config.trialRedeemedAt = now;
  config.trialStartedAt = now;
  config.trialEndsAt = now + TRIAL_DURATION_MS;
  recordEvent(config, "trial_started", { guildId, userId, trialEndsAt: config.trialEndsAt });
  saveGuildConfig();
  return true;
}

async function startTrialAndGetCheckoutUrl(guildId, userId) {
  const config = getGuildConfig(guildId);
  if (config.isPremium) return { ok: false, reason: "paid" };
  if (effectivePremium(config, Date.now(), guildId)) return { ok: false, reason: "active" };
  if (config.trialRedeemedAt) return { ok: false, reason: "used" };
  startTrialForConfig(config, guildId, userId);
  if (!stripeClient) return { ok: true, url: SUPPORT_URL };
  try {
    const session = await createTrialCheckoutSession({ guildId, userId });
    return { ok: true, url: session?.url || SUPPORT_URL };
  } catch (err) {
    console.warn("Stripe trial checkout error:", err?.message || err);
    return { ok: true, url: SUPPORT_URL };
  }
}

function premiumValueLines(feature) {
  const common = [
    "Outcome: less manual posting, more daily engagement.",
  ];
  const byFeature = {
    "/date": ["Unlock /date, /tomorrow, /upcoming, and /week for planning ahead."],
    "/search": ["Unlock /search and /random for discoverability and variety."],
    "/random": ["Unlock /random and deeper daily controls for fresher content."],
    "/facts": ["Unlock full /facts output plus analytics to optimize what lands."],
    "/tomorrow": ["Unlock tomorrow/upcoming digests and category-safe filtering."],
    "/upcoming": ["Unlock upcoming/week planning plus timezone/hour scheduling."],
    "/week": ["Unlock week/upcoming plus channel-by-channel scheduling control."],
    "/analytics": ["See best posting times/channels and optimize for more reactions."],
    "/lore": ["Unlock lore, tone, and filters for a server-specific experience."],
    "/setcategories": ["Unlock category controls and work-safe filtering."],
    "/excludesensitive": ["Unlock sensitive-content controls for safer auto-posts."],
  };
  return [...(byFeature[feature] || ["Unlock premium commands plus advanced daily scheduling."]), ...common];
}

async function replyPremiumOnly(interaction, { feature, previewLines = [] } = {}) {
  const upgradeUrl = await getUpgradeUrlForInteraction(interaction);
  const valueLines = premiumValueLines(feature);
  const config = interaction.guildId ? getGuildConfig(interaction.guildId) : null;
  if (config && interaction.guildId) {
    recordEvent(config, "premium_prompt_shown", { guildId: interaction.guildId, source: "premium_only_reply", feature: feature || "unknown" });
    saveGuildConfig();
  }
  const lines = [
    "Premium only.",
    feature ? `Feature: ${feature}` : null,
    previewLines.length ? `Preview: ${previewLines.join(" • ")}` : null,
    ...valueLines,
    "Start a 7-day trial, then $3.99/month. Cancel anytime.",
  ].filter(Boolean);

  return interaction.reply({
    content: lines.join("\n"),
    flags: MessageFlags.Ephemeral,
    components: [
      new ActionRowBuilder().addComponents(
        new ButtonBuilder().setCustomId("start_trial").setLabel("Start 7-day trial").setStyle(ButtonStyle.Success),
        new ButtonBuilder().setLabel("Upgrade to Premium").setStyle(ButtonStyle.Link).setURL(upgradeUrl),
        new ButtonBuilder()
          .setLabel("Learn More")
          .setStyle(ButtonStyle.Link)
          .setURL(SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/")
      ),
    ],
  });
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

function holidaysForRange(startDate, days, config) {
  const list = [];
  for (let i = 0; i < days; i++) {
    const d = new Date(startDate);
    d.setDate(startDate.getDate() + i);
    const mmdd = `${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
    const hits = findByDate(mmdd);
    const filtered = config ? applyServerFilters(hits, config) : hits;
    if (filtered.length) list.push({ date: mmdd, holiday: filtered[0] });
  }
  return list;
}

function lastDateKeys(days) {
  const keys = [];
  const now = new Date();
  for (let i = 0; i < days; i++) {
    const d = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() - i));
    keys.push(d.toISOString().slice(0, 10));
  }
  return keys;
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
      new ButtonBuilder().setCustomId("invite_cta").setLabel("Invite to another server").setStyle(ButtonStyle.Primary)
    ),
  ];
}

function buildTrialActionRow() {
  return new ActionRowBuilder().addComponents(
    new ButtonBuilder().setCustomId("start_trial").setLabel("Start 7-day trial").setStyle(ButtonStyle.Success),
    new ButtonBuilder()
      .setLabel("Learn More")
      .setStyle(ButtonStyle.Link)
      .setURL(SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/")
  );
}

function formatTimestamp(ts) {
  if (!ts) return "unknown";
  return `${new Date(ts).toISOString().slice(0, 16).replace("T", " ")} UTC`;
}

function buildUpgradeRow(url) {
  const upgradeUrl = url || SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/";
  return new ActionRowBuilder().addComponents(
    new ButtonBuilder().setLabel("Upgrade to Premium").setStyle(ButtonStyle.Link).setURL(upgradeUrl),
    new ButtonBuilder().setLabel("Learn More").setStyle(ButtonStyle.Link).setURL(SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/")
  );
}

async function findCustomerIdForGuild(guildId) {
  if (!stripeClient || !guildId) return null;
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
        if (gid === guildId && subscriptionHasPremiumPrice(sub)) {
          return sub.customer;
        }
      }
      if (!subs.has_more) break;
      startingAfter = subs.data[subs.data.length - 1].id;
    }
  } catch (err) {
    console.warn("Stripe lookup error:", err.message);
  }
  return null;
}

async function getPortalUrlForGuild(guildId) {
  if (STRIPE_PORTAL_URL) return STRIPE_PORTAL_URL;
  if (!stripeClient) return null;
  const customerId = await findCustomerIdForGuild(guildId);
  if (!customerId) return null;
  try {
    const session = await stripeClient.billingPortal.sessions.create({
      customer: customerId,
      return_url: STRIPE_PORTAL_RETURN_URL,
    });
    return session?.url || null;
  } catch (err) {
    console.warn("Stripe portal error:", err.message);
    return null;
  }
}

async function getBestUpgradeUrlForGuild(guildId, interaction) {
  const portalUrl = await getPortalUrlForGuild(guildId);
  if (portalUrl) return portalUrl;
  if (interaction) return getUpgradeUrlForInteraction(interaction);
  if (stripeClient && STRIPE_PRICE_ID_STANDARD && STRIPE_PRICE_ID_INTRO) {
    try {
      const session = await createPremiumCheckoutSession({ guildId, userId: "" });
      if (session?.url) return session.url;
    } catch (err) {
      console.warn("Stripe checkout error (best upgrade url):", err.message);
    }
  }
  return SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/";
}

async function maybeSendOnboardingDm(user, guildId) {
  if (!user || !guildId) return;
  const config = getGuildConfig(guildId);
  if (config.onboardingDmSent) return;
  const trialUrl = buildTrialStartUrl(guildId, user.id);
  const lines = [
    "Thanks for adding Obscure Holiday Calendar!",
    "Category Filters let you pick which kinds of holidays your server sees.",
    config.trialRedeemedAt
      ? "Your server has already used its 7-day trial. Use /upgrade to subscribe."
      : trialUrl
        ? `Start a 7-day trial: ${trialUrl}`
        : "Start a 7-day trial: run /premium and click Start 7-day trial.",
    "Use /categories to explore filters, and /setcategories to configure them (admin).",
  ];
  try {
    await user.send(lines.join("\n"));
    config.onboardingDmSent = true;
    recordEvent(config, "onboarding_dm_sent", { guildId, userId: user.id });
    saveGuildConfig();
  } catch (err) {
    console.warn("Onboarding DM failed:", err.message);
  }
}

async function maybeSendActivationNudgeForGuild(guildId, now = Date.now()) {
  if (!guildId) return false;
  const config = getGuildConfig(guildId);
  if (config.activationReminderSentAt) return false;
  if ((config.channelIds || []).length > 0) return false;
  const dueAt = Number(config.activationReminderDueAt || 0);
  if (!dueAt || now < dueAt) return false;
  try {
    const guild = await client.guilds.fetch(guildId);
    const owner = await guild.fetchOwner();
    if (!owner?.user) return false;
    await owner.user.send(
      [
        `Quick setup reminder for **${guild.name}**:`,
        "Run `/setup` in your server to enable daily holiday auto-posts.",
        "Need to share the bot with another community? Use `/share` or `/invite`.",
      ].join("\n")
    );
    config.activationReminderSentAt = now;
    recordEvent(config, "activation_nudge_sent", { guildId, method: "dm_24h" });
    saveGuildConfig();
    return true;
  } catch (err) {
    console.warn("Activation nudge DM failed:", err?.message || err);
    return false;
  }
}

async function sweepActivationNudges() {
  const now = Date.now();
  for (const guildId of Object.keys(guildConfig)) {
    try {
      await maybeSendActivationNudgeForGuild(guildId, now);
    } catch (err) {
      console.warn(`Activation sweep failed for guild ${guildId}:`, err?.message || err);
    }
  }
}

async function maybeSendTrialReminder(guildId) {
  if (!guildId) return;
  const config = getGuildConfig(guildId);
  const now = Date.now();
  if (config.isPremium) {
    if (config.trialReminderPending) {
      config.trialReminderPending = false;
      recordEvent(config, "trial_reminder_skipped", { guildId, reason: "upgraded" });
      saveGuildConfig();
    }
    return;
  }
  const status = getPlanStatus(config, now);
  if (status !== "trial") {
    if (config.trialReminderPending) {
      config.trialReminderPending = false;
      recordEvent(config, "trial_reminder_skipped", { guildId, reason: "no_longer_eligible" });
      saveGuildConfig();
    }
    return;
  }
  if (config.trialReminderSentAt) return;
  const endsAt = Number(config.trialEndsAt || 0);
  if (!endsAt || endsAt - now > 24 * 60 * 60 * 1000) {
    if (config.trialReminderPending) {
      config.trialReminderPending = false;
      recordEvent(config, "trial_reminder_skipped", { guildId, reason: "trial_extended" });
      saveGuildConfig();
    }
    return;
  }
  try {
    const guild = await client.guilds.fetch(guildId);
    const owner = await guild.fetchOwner();
    if (!owner?.user) return;
    const upgradeUrl = await getBestUpgradeUrlForGuild(guildId);
    await owner.user.send(`Trial ends tomorrow — keep filters active by upgrading: ${upgradeUrl}`);
    config.trialReminderSentAt = now;
    config.trialReminderPending = false;
    recordEvent(config, "trial_reminder_sent", { guildId, method: "dm" });
    saveGuildConfig();
  } catch (err) {
    config.trialReminderPending = true;
    saveGuildConfig();
    console.warn("Trial reminder DM failed:", err.message);
  }
}

async function handleToday(interaction) {
  const now = new Date();
  const mmdd = `${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  const hits = findByDate(mmdd);
  if (!hits.length) return interaction.reply({ content: "No holiday found for today.", flags: MessageFlags.Ephemeral });
  const premium = isPremium(interaction.guild, interaction.member);
  const config = getGuildConfig(interaction.guild.id);
  const filtered = premium ? applyServerFilters(hits, config) : hits;
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
  await interaction.reply({
    content: promoNote || undefined,
    embeds: [buildEmbed(pick, { branding: !premium || config.branding, tone: config.tone })],
    components: [...baseComponents, ...promoRows],
  });
  let sentPremiumPrompt = false;
  if (!premium) {
    const hiddenCount = Math.max(0, filtered.length - 1);
    if (hiddenCount > 0 && canShowPremiumPrompt(interaction.guild.id)) {
      const upgradeUrl = await getUpgradeUrlForInteraction(interaction);
      markPremiumPrompt(interaction.guild.id);
      recordEvent(config, "premium_prompt_shown", { guildId: interaction.guild.id, source: "today_followup", hiddenCount });
      saveGuildConfig();
      await interaction.followUp({
        content: [
          `${hiddenCount} more holiday${hiddenCount === 1 ? "" : "s"} available today.`,
          "Premium unlocks the full daily set + /date, /search, /random, /facts, and advanced scheduling.",
          "Start a 7-day trial, then $3.99/month. Cancel anytime.",
        ].join("\n"),
        flags: MessageFlags.Ephemeral,
        components: [
          new ActionRowBuilder().addComponents(
            new ButtonBuilder().setCustomId("start_trial").setLabel("Start 7-day trial").setStyle(ButtonStyle.Success),
            new ButtonBuilder().setLabel("Upgrade to Premium").setStyle(ButtonStyle.Link).setURL(upgradeUrl)
          ),
        ],
      });
      sentPremiumPrompt = true;
    }
  }
  if (!sentPremiumPrompt && interaction.memberPermissions?.has(PermissionsBitField.Flags.ManageGuild) && (!config.channelIds || !config.channelIds.length)) {
    try {
      await interaction.followUp({
        content: "Tip: run /setup to auto-post daily holidays.",
        flags: MessageFlags.Ephemeral,
      });
    } catch {
      // no-op: nudge is optional
    }
  }
  return null;
}

async function handleHelp(interaction) {
  const level = interaction.options.getString("level") || "full";
  if (level === "brief") {
    return interaction.reply({
      content: [
        "ObscureHolidayBot quick help",
        "/today, /fact, /streak",
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
      "/fact [name|MM-DD] — one fun fact (free)",
      "/streak — show the server streak",
      "/categories — list holiday categories + server settings",
      "",
      "Premium content",
      "/date MM-DD — holiday on a date",
      "/search <query> — find matching holidays",
      "/random — surprise me",
      "/facts [name|MM-DD] — fun facts (multiple)",
      "/tomorrow — tomorrow’s holiday",
      "/upcoming [days] — upcoming holidays (max 30)",
      "/week [days] — 7-day digest (3–14)",
      "/setcategories <list|all> — allow categories (admin)",
      "/excludesensitive [true|false] — hide sensitive holidays (admin)",
      "/trial — check 7-day trial status (admin)",
      "",
      "Setup & admin",
      "/setup — configure daily posts",
      "  free: channel",
      "  premium: timezone, hour, branding, holiday_choice, role_mention, quiet, promotions, embed_style, embed_color, skip_weekends",
      "  premium extras: tone, streak_role, streak_goal, filters, blacklist, surprise_days",
      "",
      "Admin controls",
      "/trial — start/check 7-day trial",
      "/categories — view categories",
      "/setcategories — set allowed categories (premium/trial)",
      "/excludesensitive — toggle sensitive filter (premium/trial)",
      "/overrides — blocked/forced lists",
      "/why — explain why something was filtered",
      "/analytics — engagement analytics (premium, admin)",
      "/lore — server lore (premium, admin)",
      "",
      "Account & support",
      "/premium — check premium status",
      "/upgrade — start premium checkout",
      "/manage — manage billing",
      "/share — invite to another server",
      "/vote — vote on top.gg",
      "/rate — leave a review on top.gg",
      "/support — help/landing page",
      "/invite — invite the bot",
      "/app — mobile app links",
      "/slack — Slack bot link",
      "",
      "Tips",
      "Premium adds control, not more noise.",
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
    const input = interaction.options.getString("date", true);
    const parsed = parseDate(input);
    const previewLines = [];
    if (parsed) {
      const hits = findByDate(parsed);
      if (hits.length) previewLines.push(`${prettyDate(parsed)}: ${hits[0].name}`);
    }
    return replyPremiumOnly(interaction, { feature: "/date", previewLines });
  }
  const input = interaction.options.getString("date", true);
  const parsed = parseDate(input);
  if (!parsed) return interaction.reply({ content: "Please provide a date as MM-DD or MM/DD (example: 07-04).", flags: MessageFlags.Ephemeral });
  const config = getGuildConfig(interaction.guild.id);
  const hits = applyServerFilters(findByDate(parsed), config);
  if (!hits.length) return interaction.reply({ content: `No holidays found on ${parsed} with current filters.`, flags: MessageFlags.Ephemeral });
  return interaction.reply({ embeds: [buildEmbed(hits[0], { branding: config.branding, tone: config.tone })], components: buildButtons(hits[0]) });
}

async function handleSearch(interaction) {
  if (!isPremium(interaction.guild, interaction.member)) {
    const query = interaction.options.getString("query", true);
    const matches = findByName(query);
    const previewLines = matches.length ? [`Match: ${matches[0].name}`] : [];
    return replyPremiumOnly(interaction, { feature: "/search", previewLines });
  }
  const query = interaction.options.getString("query", true);
  const config = getGuildConfig(interaction.guild.id);
  const matches = applyServerFilters(findByName(query), config);
  if (!matches.length) return interaction.reply({ content: "No match. Try a simpler phrase.", flags: MessageFlags.Ephemeral });
  const embeds = matches.slice(0, 3).map((h) => buildEmbed(h, { branding: config.branding, tone: config.tone }));
  return interaction.reply({ embeds, components: buildButtons(matches[0]) });
}

async function handleRandom(interaction) {
  if (!isPremium(interaction.guild, interaction.member)) {
    const pick = pickRandom();
    const previewLines = pick ? [`Random pick: ${pick.name}`] : [];
    return replyPremiumOnly(interaction, { feature: "/random", previewLines });
  }
  const config = getGuildConfig(interaction.guild.id);
  const filtered = applyServerFilters(allHolidays, config);
  if (!filtered.length && hasActiveOverrides(config)) {
    return interaction.reply({ content: "No holidays found with current filters.", flags: MessageFlags.Ephemeral });
  }
  const h = pickRandomItem(filtered.length ? filtered : allHolidays);
  return interaction.reply({ embeds: [buildEmbed(h, { branding: config.branding, tone: config.tone })], components: buildButtons(h) });
}

async function handleWeek(interaction) {
  if (!isPremium(interaction.guild, interaction.member)) {
    const now = new Date();
    const items = holidaysForRange(now, 7);
    const previewLines = items.slice(0, 2).map(({ date, holiday }) => `${prettyDate(date)}: ${holiday.name}`);
    return replyPremiumOnly(interaction, { feature: "/week", previewLines });
  }
  const days = Math.max(3, Math.min(interaction.options.getInteger("days") || 7, 14));
  const now = new Date();
  const config = getGuildConfig(interaction.guild.id);
  const items = holidaysForRange(now, days, config);
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
  recordEvent(config, "setup_started", { guildId, userId: interaction.user.id });
  saveGuildConfig();
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
    config.activationReminderSentAt = Date.now();
    recordEvent(config, "setup_completed", { guildId, userId: interaction.user.id, premium: false, channelId: channel.id });
    saveGuildConfig();
    console.log(`Setup saved for guild ${guildId}: ${formatSetupLog(config, channel.id)}`);
    scheduleForChannel(guildId, channel.id);
    const upgradeUrl = await getUpgradeUrlForInteraction(interaction);
    await sendSetupPreview(channel, config, false, null);
    await maybeSendOnboardingDm(interaction.user, guildId);
    return interaction.reply({
      content: [
        `Daily posts set to <#${channel.id}> at 00:00 UTC.`,
        `Promotions: ${config.promotionsEnabled === false ? "off" : "on (weekly vote / monthly review)"}`,
        "Premium unlocks timezone/hour/branding toggles.",
      ].join("\n"),
      flags: MessageFlags.Ephemeral,
      components: [
        new ActionRowBuilder().addComponents(
          new ButtonBuilder().setLabel("Upgrade to Premium").setStyle(ButtonStyle.Link).setURL(upgradeUrl),
          new ButtonBuilder()
            .setLabel("Premium Features")
            .setStyle(ButtonStyle.Link)
            .setURL(SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/")
        ),
      ],
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
  config.activationReminderSentAt = Date.now();
  recordEvent(config, "setup_completed", { guildId, userId: interaction.user.id, premium: true, channelId: channel.id });

  saveGuildConfig();
  console.log(`Setup saved for guild ${guildId}: ${formatSetupLog(config, channel.id)}`);
  scheduleForChannel(guildId, channel.id);
  await sendSetupPreview(channel, config, true, ch);
  await maybeSendOnboardingDm(interaction.user, guildId);

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

async function handleCategories(interaction) {
  if (!interaction.guild) {
    return interaction.reply({ content: "This command can only be used in a server.", flags: MessageFlags.Ephemeral });
  }
  const config = getGuildConfig(interaction.guild.id);
  const allowed = config.allowedCategories;
  const allowedLabel = allowed === null ? "all" : allowed.length ? allowed.join(", ") : "none";
  const trialActive = effectivePremium(config, Date.now(), interaction.guild.id) && !config.isPremium;
  const trialLine = trialActive
    ? `Trial: active until ${formatTimestamp(config.trialEndsAt)}`
    : config.trialRedeemedAt
      ? config.trialEndsAt
        ? `Trial: used (ended ${formatTimestamp(config.trialEndsAt)})`
        : "Trial: used"
      : `Trial: available (${TRIAL_DAYS} days)`;
  const lines = [
    `Available categories: ${ALL_CATEGORIES.join(", ")}`,
    `Allowed categories: ${allowedLabel}`,
    `Exclude sensitive: ${config.excludeSensitive ? "on" : "off"}`,
    trialLine,
  ];
  const premium = isPremium(interaction.guild, interaction.member);
  const components = premium ? [] : [buildTrialActionRow()];
  return interaction.reply({ content: lines.join("\n"), flags: MessageFlags.Ephemeral, components });
}

async function handleSetCategories(interaction) {
  if (!interaction.guild) {
    return interaction.reply({ content: "This command can only be used in a server.", flags: MessageFlags.Ephemeral });
  }
  if (!interaction.memberPermissions?.has(PermissionsBitField.Flags.ManageGuild)) {
    return interaction.reply({ content: "Admins only (Manage Server).", flags: MessageFlags.Ephemeral });
  }
  if (!isPremium(interaction.guild, interaction.member)) {
    return replyPremiumOnly(interaction, { feature: "/setcategories" });
  }
  const input = interaction.options.getString("categories", true).trim().toLowerCase();
  const config = getGuildConfig(interaction.guild.id);
  recordEvent(config, "categories_set_attempt", { guildId: interaction.guildId, input });
  if (["all", "any", "*", "everything", "reset"].includes(input)) {
    config.allowedCategories = null;
  } else if (["none", "clear"].includes(input)) {
    config.allowedCategories = [];
  } else {
    const list = [...new Set(normalizeCategoryList(input))];
    const invalid = list.filter((cat) => !ALL_CATEGORIES.includes(cat));
    if (invalid.length) {
      return interaction.reply({
        content: `Unknown categories: ${invalid.join(", ")}\nAvailable: ${ALL_CATEGORIES.join(", ")}`,
        flags: MessageFlags.Ephemeral,
      });
    }
    config.allowedCategories = list;
  }
  recordEvent(config, "categories_set", {
    guildId: interaction.guildId,
    allowedCategories: config.allowedCategories,
  });
  saveGuildConfig();
  const allowedLabel = config.allowedCategories === null ? "all" : config.allowedCategories.length ? config.allowedCategories.join(", ") : "none";
  return interaction.reply({
    content: `Allowed categories updated: ${allowedLabel}`,
    flags: MessageFlags.Ephemeral,
  });
}

async function handleSetCategoriesAutocomplete(interaction) {
  const focused = interaction.options.getFocused() || "";
  const raw = String(focused);
  const parts = raw.split(",").map((part) => part.trim());
  const last = parts.length ? parts[parts.length - 1].toLowerCase() : "";
  const base = parts.length > 1 ? parts.slice(0, -1).join(", ") + ", " : "";
  const choices = [...ALL_CATEGORIES, "all", "reset"]
    .filter((item) => item.toLowerCase().includes(last))
    .slice(0, 25)
    .map((item) => ({
      name: base + item,
      value: base + item,
    }));
  return interaction.respond(choices);
}

async function handleExcludeSensitive(interaction) {
  if (!interaction.guild) {
    return interaction.reply({ content: "This command can only be used in a server.", flags: MessageFlags.Ephemeral });
  }
  if (!interaction.memberPermissions?.has(PermissionsBitField.Flags.ManageGuild)) {
    return interaction.reply({ content: "Admins only (Manage Server).", flags: MessageFlags.Ephemeral });
  }
  if (!isPremium(interaction.guild, interaction.member)) {
    return replyPremiumOnly(interaction, { feature: "/excludesensitive" });
  }
  const config = getGuildConfig(interaction.guild.id);
  const enabled = interaction.options.getBoolean("enabled");
  config.excludeSensitive = typeof enabled === "boolean" ? enabled : !config.excludeSensitive;
  saveGuildConfig();
  return interaction.reply({
    content: `Exclude sensitive: ${config.excludeSensitive ? "on" : "off"}`,
    flags: MessageFlags.Ephemeral,
  });
}

async function handleStartTrialButton(interaction) {
  if (!interaction.guildId) {
    return interaction.reply({ content: "This action must be used in a server.", flags: MessageFlags.Ephemeral });
  }
  if (!interaction.memberPermissions?.has(PermissionsBitField.Flags.ManageGuild)) {
    return interaction.reply({ content: "Admins only (Manage Server).", flags: MessageFlags.Ephemeral });
  }
  const config = getGuildConfig(interaction.guildId);
  if (config.isPremium) {
    return interaction.reply({ content: "Premium is already active for this server.", flags: MessageFlags.Ephemeral });
  }
  if (effectivePremium(config, Date.now(), interaction.guildId)) {
    return interaction.reply({
      content: `Trial already active until ${formatTimestamp(config.trialEndsAt)}.`,
      flags: MessageFlags.Ephemeral,
    });
  }
  if (config.trialRedeemedAt) {
    const upgradeUrl = await getUpgradeUrlForInteraction(interaction);
    return interaction.reply({ content: "This server already used its 7-day trial.", flags: MessageFlags.Ephemeral, components: [buildUpgradeRow(upgradeUrl)] });
  }
  const result = await startTrialAndGetCheckoutUrl(interaction.guildId, interaction.user.id);
  if (!result.ok) {
    return interaction.reply({ content: "Unable to start the trial right now.", flags: MessageFlags.Ephemeral });
  }
  const url = result.url || SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/";
  return interaction.reply({
    content: `Trial started! Finish checkout here: ${url}`,
    flags: MessageFlags.Ephemeral,
    components: [
      new ActionRowBuilder().addComponents(
        new ButtonBuilder().setLabel("Open Checkout").setStyle(ButtonStyle.Link).setURL(url)
      ),
    ],
  });
}

async function handleTrialStatus(interaction) {
  if (!interaction.guild) {
    return interaction.reply({ content: "This command can only be used in a server.", flags: MessageFlags.Ephemeral });
  }
  if (!interaction.memberPermissions?.has(PermissionsBitField.Flags.ManageGuild)) {
    return interaction.reply({ content: "Admins only (Manage Server).", flags: MessageFlags.Ephemeral });
  }
  const config = getGuildConfig(interaction.guild.id);
  const now = Date.now();
  effectivePremium(config, now, interaction.guild.id);
  const status = getPlanStatus(config, now);
  const premium = status === "premium";
  const trialActive = status === "trial";
  if (premium && config.trialReminderPending) {
    config.trialReminderPending = false;
    recordEvent(config, "trial_reminder_skipped", { guildId: interaction.guildId, reason: "upgraded" });
    saveGuildConfig();
  }
  if (trialActive && config.trialReminderPending && !config.trialReminderSentAt && Number(config.trialEndsAt || 0) - now <= 24 * 60 * 60 * 1000) {
    const upgradeUrl = await getBestUpgradeUrlForGuild(interaction.guild.id, interaction);
    const reminder = `Trial ends tomorrow — keep filters active by upgrading: ${upgradeUrl}`;
    config.trialReminderSentAt = now;
    config.trialReminderPending = false;
    recordEvent(config, "trial_reminder_sent", { guildId: interaction.guildId, method: "fallback_ephemeral" });
    saveGuildConfig();
    return interaction.reply({ content: reminder, flags: MessageFlags.Ephemeral });
  }
  if (!trialActive && config.trialReminderPending) {
    config.trialReminderPending = false;
    recordEvent(config, "trial_reminder_skipped", { guildId: interaction.guildId, reason: "no_longer_eligible" });
    saveGuildConfig();
  }
  const lines = [
    `Status: ${status}`,
    trialActive ? `Trial ends: ${formatTimestamp(config.trialEndsAt)}` : null,
    config.trialRedeemedAt && !trialActive ? `Trial used: ${formatTimestamp(config.trialRedeemedAt)}` : null,
    config.trialRedeemedAt && !trialActive && config.trialEndsAt ? `Trial ended: ${formatTimestamp(config.trialEndsAt)}` : null,
  ].filter(Boolean);
  if (premium) {
    return interaction.reply({ content: lines.join("\n"), flags: MessageFlags.Ephemeral });
  }
  if (trialActive) {
    const remainingMs = Math.max(0, Number(config.trialEndsAt || 0) - now);
    const remainingHours = Math.ceil(remainingMs / (1000 * 60 * 60));
    lines.push(`Time remaining: ~${remainingHours} hour(s)`);
    return interaction.reply({ content: lines.join("\n"), flags: MessageFlags.Ephemeral });
  }
  const upgradeUrl = await getBestUpgradeUrlForGuild(interaction.guild.id, interaction);
  if (config.trialRedeemedAt) {
    return interaction.reply({
      content: lines.join("\n"),
      flags: MessageFlags.Ephemeral,
      components: [buildUpgradeRow(upgradeUrl)],
    });
  }
  return interaction.reply({
    content: lines.concat("Eligible for a 7-day trial.").join("\n"),
    flags: MessageFlags.Ephemeral,
    components: [buildTrialActionRow()],
  });
}

function describeOverrides(config) {
  const blocked = config.blockedHolidayIds || [];
  const forced = config.forcedHolidayIds || [];
  const summarize = (list) => list.slice(0, 15).join(", ") + (list.length > 15 ? "…" : "");
  return [
    blocked.length ? `Blocked: ${summarize(blocked)}` : "Blocked: none",
    forced.length ? `Forced: ${summarize(forced)}` : "Forced: none",
  ];
}

async function handleOverrides(interaction) {
  if (!interaction.guild) {
    return interaction.reply({ content: "This command can only be used in a server.", flags: MessageFlags.Ephemeral });
  }
  if (!interaction.memberPermissions?.has(PermissionsBitField.Flags.ManageGuild)) {
    return interaction.reply({ content: "Admins only (Manage Server).", flags: MessageFlags.Ephemeral });
  }
  const config = getGuildConfig(interaction.guild.id);
  return interaction.reply({ content: describeOverrides(config).join("\n"), flags: MessageFlags.Ephemeral });
}

async function handleOverrideUpdate(interaction, listKey, actionVerb) {
  if (!interaction.guild) {
    return interaction.reply({ content: "This command can only be used in a server.", flags: MessageFlags.Ephemeral });
  }
  if (!interaction.memberPermissions?.has(PermissionsBitField.Flags.ManageGuild)) {
    return interaction.reply({ content: "Admins only (Manage Server).", flags: MessageFlags.Ephemeral });
  }
  const input = interaction.options.getString("id_or_name", true);
  const holiday = resolveHolidayByIdOrName(input);
  if (!holiday) {
    return interaction.reply({ content: "Holiday not found. Try a full name or slug.", flags: MessageFlags.Ephemeral });
  }
  const config = getGuildConfig(interaction.guild.id);
  const id = holidayId(holiday);
  const list = new Set((config[listKey] || []).map((item) => String(item).toLowerCase()));
  if (actionVerb === "add") list.add(id);
  if (actionVerb === "remove") list.delete(id);
  config[listKey] = [...list];
  saveGuildConfig();
  return interaction.reply({
    content: `${listKey === "blockedHolidayIds" ? "Blocked" : "Forced"} updated: ${holiday.name || id}`,
    flags: MessageFlags.Ephemeral,
  });
}

async function handleWhy(interaction) {
  if (!interaction.guild) {
    return interaction.reply({ content: "This command can only be used in a server.", flags: MessageFlags.Ephemeral });
  }
  if (!interaction.memberPermissions?.has(PermissionsBitField.Flags.ManageGuild)) {
    return interaction.reply({ content: "Admins only (Manage Server).", flags: MessageFlags.Ephemeral });
  }
  const input = interaction.options.getString("id_or_name", true);
  const holiday = resolveHolidayByIdOrName(input);
  if (!holiday) {
    return interaction.reply({ content: "Holiday not found. Try a full name or slug.", flags: MessageFlags.Ephemeral });
  }
  ensureHolidayMeta(holiday);
  const config = getGuildConfig(interaction.guild.id);
  const blockedIds = new Set((config.blockedHolidayIds || []).map((id) => String(id).toLowerCase()));
  const forcedIds = new Set((config.forcedHolidayIds || []).map((id) => String(id).toLowerCase()));
  const id = holidayId(holiday);
  const allowed = config.allowedCategories;
  let decision = "allowed";
  if (forcedIds.size && !forcedIds.has(id)) {
    decision = "filtered (not forced)";
  } else if (blockedIds.has(id)) {
    decision = "filtered (blocked)";
  } else if (!filterHoliday(holiday, config.filters)) {
    decision = "filtered (keyword filters)";
  } else if (config.excludeSensitive && holiday.is_sensitive) {
    decision = "filtered (sensitive)";
  } else if (allowed !== null && typeof allowed !== "undefined") {
    const categories = (holiday.categories || []).map((c) => c.toLowerCase());
    if (!categories.some((c) => allowed.includes(c))) {
      decision = "filtered (category)";
    }
  }
  const lines = [
    `Holiday: ${holiday.name || id}`,
    `Id: ${id}`,
    `Categories: ${(holiday.categories || []).join(", ") || "none"}`,
    `Sensitive: ${holiday.is_sensitive ? "yes" : "no"}`,
    `Decision: ${decision}`,
  ];
  return interaction.reply({ content: lines.join("\n"), flags: MessageFlags.Ephemeral });
}

async function handleAdminStats(interaction) {
  if (!isOwner(interaction.user.id)) {
    return interaction.reply({ content: "Owner-only command.", flags: MessageFlags.Ephemeral });
  }
  const now = Date.now();
  const cutoff = now - 30 * 24 * 60 * 60 * 1000;
  const guildStats = [];
  let totalTrials = 0;
  let totalUpgrades = 0;
  let totalCategoryAttempts = 0;
  for (const [guildId, config] of Object.entries(guildConfig)) {
    const events = Array.isArray(config.analytics?.events) ? config.analytics.events : [];
    let upsellCount = 0;
    let trialCount = 0;
    let upgradeCount = 0;
    let categoryAttempts = 0;
    for (const event of events) {
      if (!event || event.at < cutoff) continue;
      if (event.event === "upsell_shown") upsellCount += 1;
      if (event.event === "trial_started") trialCount += 1;
      if (event.event === "upgrade_completed") upgradeCount += 1;
      if (event.event === "categories_set_attempt") categoryAttempts += 1;
    }
    totalTrials += trialCount;
    totalUpgrades += upgradeCount;
    totalCategoryAttempts += categoryAttempts;
    guildStats.push({ guildId, upsellCount, trialCount, upgradeCount, categoryAttempts });
  }
  guildStats.sort((a, b) => b.upsellCount - a.upsellCount);
  const topGuilds = guildStats.slice(0, 5).map((stat) => {
    const guild = client.guilds.cache.get(stat.guildId);
    const label = guild ? `${guild.name} (${stat.guildId})` : stat.guildId;
    return `${label} — upsell ${stat.upsellCount}, trial ${stat.trialCount}, upgrade ${stat.upgradeCount}, categories ${stat.categoryAttempts}`;
  });
  const lines = [
    "Admin stats (last 30 days)",
    `Trials started: ${totalTrials}`,
    `Upgrades completed: ${totalUpgrades}`,
    `Category attempts: ${totalCategoryAttempts}`,
    "Top guilds by upsell_shown:",
    ...(topGuilds.length ? topGuilds : ["none"]),
  ];
  return interaction.reply({ content: lines.join("\n"), flags: MessageFlags.Ephemeral });
}

async function handleAdminFunnel(interaction) {
  if (!isOwner(interaction.user.id)) {
    return interaction.reply({ content: "Owner-only command.", flags: MessageFlags.Ephemeral });
  }
  const endMs = Date.now();
  const startMs = endMs - 14 * 24 * 60 * 60 * 1000;
  const events = queryAnalyticsEventsInRange(startMs, endMs);
  let upsellCount = 0;
  let trialCount = 0;
  let upgradeCount = 0;
  let setupStarted = 0;
  let setupCompleted = 0;
  let inviteShown = 0;
  let inviteClicked = 0;
  let premiumPromptShown = 0;
  for (const event of events) {
    if (event.event === "upsell_shown") upsellCount += 1;
    if (event.event === "trial_started") trialCount += 1;
    if (event.event === "upgrade_completed") upgradeCount += 1;
    if (event.event === "setup_started") setupStarted += 1;
    if (event.event === "setup_completed") setupCompleted += 1;
    if (event.event === "invite_cta_shown") inviteShown += 1;
    if (event.event === "invite_cta_clicked") inviteClicked += 1;
    if (event.event === "premium_prompt_shown") premiumPromptShown += 1;
  }
  const trialRate = upsellCount ? (trialCount / upsellCount) * 100 : 0;
  const upgradeRate = trialCount ? (upgradeCount / trialCount) * 100 : 0;
  const startIso = new Date(startMs).toISOString();
  const endIso = new Date(endMs).toISOString();
  const lines = [
    "Admin funnel (last 14 days)",
    `Query source: guildConfig[*].analytics.events`,
    `Timestamp fields checked: createdAt -> ts -> at`,
    `Range start: ${startIso}`,
    `Range end: ${endIso}`,
  ];
  if (!events.length) {
    lines.push("0 events found in range");
  }
  lines.push(
    `Upsell shown: ${upsellCount}`,
    `Premium prompts shown: ${premiumPromptShown}`,
    `Trials started: ${trialCount}`,
    `Upgrades completed: ${upgradeCount}`,
    `Setup started: ${setupStarted}`,
    `Setup completed: ${setupCompleted}`,
    `Invite CTA shown: ${inviteShown}`,
    `Invite CTA clicked: ${inviteClicked}`,
    `Trial conversion: ${trialRate.toFixed(1)}%`,
    `Upgrade conversion: ${upgradeRate.toFixed(1)}%`
  );
  return interaction.reply({ content: lines.join("\n"), flags: MessageFlags.Ephemeral });
}

async function handleAdminHealth(interaction) {
  if (!isOwner(interaction.user.id)) {
    return interaction.reply({ content: "Owner-only command.", flags: MessageFlags.Ephemeral });
  }
  const sevenDaysAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
  const totalGuilds = client.guilds.cache.size;
  const configs = Object.entries(guildConfig);
  let dailyEnabledGuilds = 0;
  let validChannelGuilds = 0;
  let recentDailyPostGuilds = 0;
  const failureReasons = {};
  const recentAttempts = [];
  for (const [guildId, config] of configs) {
    const channelIds = Array.isArray(config.channelIds) ? config.channelIds : [];
    if (channelIds.length) dailyEnabledGuilds += 1;
    if (Number(config.lastDailyPostAt || 0) >= sevenDaysAgo) recentDailyPostGuilds += 1;

    let hasValidChannel = false;
    if (channelIds.length) {
      const guild = client.guilds.cache.get(guildId);
      for (const channelId of channelIds) {
        if (!/^\d+$/.test(String(channelId || ""))) continue;
        const cached = guild?.channels?.cache?.get(channelId);
        if (cached) {
          hasValidChannel = true;
          break;
        }
      }
    }
    if (hasValidChannel) validChannelGuilds += 1;

    const attempts = Array.isArray(config.lastDailyPostAttempts) ? config.lastDailyPostAttempts : [];
    for (const attempt of attempts) {
      if (!attempt || Number(attempt.at || 0) < sevenDaysAgo) continue;
      const status = String(attempt.status || "");
      const reason = String(attempt.reason || "unknown");
      if (status.startsWith("fail")) {
        failureReasons[reason] = (failureReasons[reason] || 0) + 1;
      }
      recentAttempts.push({
        at: Number(attempt.at || 0),
        guildId: String(attempt.guildId || guildId),
        status,
        reason,
      });
    }
  }
  recentAttempts.sort((a, b) => b.at - a.at);
  const lastTen = recentAttempts.slice(0, 10);
  const reasonLines = Object.entries(failureReasons)
    .sort((a, b) => b[1] - a[1])
    .map(([reason, count]) => `${reason}: ${count}`);
  const totalFailures = Object.values(failureReasons).reduce((sum, count) => sum + count, 0);
  const lines = [
    "Admin health",
    `Total guilds: ${totalGuilds}`,
    `Guilds with daily posting enabled: ${dailyEnabledGuilds}`,
    `Guilds with valid channelId stored: ${validChannelGuilds}`,
    `Guilds with lastDailyPostAt in last 7 days: ${recentDailyPostGuilds}`,
    `Recent post failures (last 7 days): ${totalFailures}`,
    `Failure reasons: ${reasonLines.length ? reasonLines.join(", ") : "none"}`,
    "Last 10 post attempts:",
    ...(lastTen.length
      ? lastTen.map((a) => `${new Date(a.at).toISOString()} guild=${a.guildId} status=${a.status}${a.reason ? ` (${a.reason})` : ""}`)
      : ["none"]),
  ];
  return interaction.reply({ content: lines.join("\n"), flags: MessageFlags.Ephemeral });
}

async function handleAdminFire(interaction) {
  if (!isOwner(interaction.user.id)) {
    return interaction.reply({ content: "Owner-only command.", flags: MessageFlags.Ephemeral });
  }
  const requestedGuildId = interaction.options.getString("guild_id", false);
  const guildId = requestedGuildId || interaction.guildId;
  if (!guildId) {
    return interaction.reply({ content: "Provide guild_id or run this inside a server.", flags: MessageFlags.Ephemeral });
  }
  const config = getGuildConfig(guildId);
  const channelIds = Array.isArray(config.channelIds) ? config.channelIds : [];
  const channelId = channelIds[0] || null;
  if (!channelId) {
    return interaction.reply({ content: `No daily posting channel configured for guild ${guildId}.`, flags: MessageFlags.Ephemeral });
  }
  await interaction.deferReply({ flags: MessageFlags.Ephemeral });
  let result;
  try {
    result = await postTodayForChannel(guildId, channelId, { source: "admin_fire", diagnostics: true });
  } catch (err) {
    const msg = err?.message || "post_failed";
    return interaction.editReply({ content: `Admin fire failed for guild ${guildId} channel ${channelId}: ${msg}` });
  }
  const eventRows = Array.isArray(result?.eventWrites) ? result.eventWrites : [];
  const eventsWriteOk = result?.eventsWriteOk !== false;
  const lines = [
    "Admin fire",
    `Guild: ${guildId}`,
    `Channel: ${channelId}`,
    `Plan status: ${result?.planStatus || getPlanStatus(config)}`,
    `Total holidays for today: ${Number.isFinite(result?.totalHolidays) ? result.totalHolidays : 0}`,
    `shownCount: ${Number.isFinite(result?.shownCount) ? result.shownCount : 0}`,
    `hiddenCount: ${Number.isFinite(result?.hiddenCount) ? result.hiddenCount : 0}`,
    `upsell_shown: ${result?.upsellShown ? "yes" : "no"}${result?.upsellReason ? ` (${result.upsellReason})` : ""}`,
    `events_write_ok: ${eventsWriteOk ? "true" : "false"}`,
    `post_status: ${result?.status || "unknown"}${result?.reason ? ` (${result.reason})` : ""}`,
  ];
  if (eventRows.length) {
    lines.push(
      "events:",
      ...eventRows.slice(-6).map((e) =>
        `${e.event} ok=${e.ok ? "true" : "false"}${e.id ? ` id=${e.id}` : ""}${e.at ? ` at=${new Date(e.at).toISOString()}` : ""}${e.error ? ` err=${e.error}` : ""}`
      )
    );
  } else {
    lines.push("events: none");
  }
  if (result?.eventsWriteError) {
    lines.push(`events_write_error: ${result.eventsWriteError}`);
  }
  return interaction.editReply({ content: lines.join("\n") });
}

async function handleFacts(interaction) {
  if (!isPremium(interaction.guild, interaction.member)) {
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
    const previewLines = holiday ? [`Facts for: ${holiday.name}`] : [];
    return replyPremiumOnly(interaction, { feature: "/facts", previewLines });
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

async function handlePostNowAll(interaction) {
  if (!isOwner(interaction.user.id)) {
    return interaction.reply({ content: "Owner-only command.", flags: MessageFlags.Ephemeral });
  }
  await interaction.reply({ content: "Posting today’s holidays now across all configured guilds…", flags: MessageFlags.Ephemeral });
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  const guildEntries = Object.entries(guildConfig);
  let totalChannels = 0;
  for (const [guildId, cfg] of guildEntries) {
    const channelIds = (cfg && cfg.channelIds) ? cfg.channelIds : [];
    if (!channelIds.length) continue;
    for (const channelId of channelIds) {
      try {
        totalChannels += 1;
        await postTodayForChannel(guildId, channelId);
        await sleep(500);
      } catch (err) {
        console.warn(`Owner post failed for guild ${guildId} channel ${channelId}:`, err?.message || err);
      }
    }
  }
  return interaction.followUp({
    content: `Done. Attempted ${totalChannels} channel${totalChannels === 1 ? "" : "s"}.`,
    flags: MessageFlags.Ephemeral,
  });
}

async function handleTomorrow(interaction) {
  if (!isPremium(interaction.guild, interaction.member)) {
    const now = new Date();
    const tomorrow = new Date(now);
    tomorrow.setDate(now.getDate() + 1);
    const mmdd = `${pad(tomorrow.getMonth() + 1)}-${pad(tomorrow.getDate())}`;
    const hits = findByDate(mmdd);
    const previewLines = hits.length ? [`Tomorrow: ${hits[0].name}`] : [];
    return replyPremiumOnly(interaction, { feature: "/tomorrow", previewLines });
  }
  const now = new Date();
  const tomorrow = new Date(now);
  tomorrow.setDate(now.getDate() + 1);
  const mmdd = `${pad(tomorrow.getMonth() + 1)}-${pad(tomorrow.getDate())}`;
  const config = getGuildConfig(interaction.guild.id);
  const hits = applyServerFilters(findByDate(mmdd), config);
  if (!hits.length) return interaction.reply({ content: "No holiday found for tomorrow with current filters.", flags: MessageFlags.Ephemeral });
  return interaction.reply({ embeds: [buildEmbed(hits[0], { branding: config.branding })], components: buildButtons(hits[0]) });
}

async function handleUpcoming(interaction) {
  if (!isPremium(interaction.guild, interaction.member)) {
    const now = new Date();
    const items = holidaysForRange(now, 5);
    const previewLines = items.slice(0, 2).map(({ date, holiday }) => `${prettyDate(date)}: ${holiday.name}`);
    return replyPremiumOnly(interaction, { feature: "/upcoming", previewLines });
  }
  const days = Math.max(1, Math.min(interaction.options.getInteger("days") || 7, 30));
  const now = new Date();
  const config = getGuildConfig(interaction.guild.id);
  const items = holidaysForRange(now, days, config);
  if (!items.length) return interaction.reply({ content: "No upcoming holidays found.", flags: MessageFlags.Ephemeral });
  const fields = items.slice(0, 5).map(({ date, holiday }) => ({
    name: `${holiday.emoji ? holiday.emoji + " " : ""}${holiday.name}`,
    value: prettyDate(date),
    inline: true,
  }));
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
  effectivePremium(config, Date.now(), interaction.guild.id);
  const trialActive = getPlanStatus(config) === "trial";
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
    "✅ Category filters + sensitive toggle",
  ];

  if (premium || trialActive) {
    const lines = [
      premium ? "✅ Premium is active for this server." : "🧪 Trial is active for this server.",
      !premium && trialActive ? `Trial ends: ${formatTimestamp(config.trialEndsAt)}` : null,
      `Daily channel(s): ${config.channelIds.length ? config.channelIds.map((c) => `<#${c}>`).join(", ") : "not set"}`,
      `Timezone: ${config.timezone} @ ${config.hour}:00`,
      `Branding: ${config.branding === false ? "off" : "on"}`,
      `Holiday pick: ${config.holidayChoice === 1 ? "second of the day" : "first of the day"}`,
      "Premium perks:",
      ...benefits,
    ].filter(Boolean);
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
    "Start a 7-day trial, then $3.99/month. Cancel anytime.",
    "Premium unlocks:",
    ...benefits,
  ];

  return interaction.reply({
    content: lines.join("\n"),
    flags: MessageFlags.Ephemeral,
    components: [
      new ActionRowBuilder().addComponents(
        new ButtonBuilder().setCustomId("start_trial").setLabel("Start 7-day trial").setStyle(ButtonStyle.Success),
        new ButtonBuilder().setLabel("Upgrade to Premium").setStyle(ButtonStyle.Link).setURL(upgradeUrl),
        new ButtonBuilder().setLabel("Learn More").setStyle(ButtonStyle.Link).setURL(SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/")
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
    return replyPremiumOnly(interaction, { feature: "/analytics" });
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
    return replyPremiumOnly(interaction, { feature: "/lore" });
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
    const config = getGuildConfig(guildId);
    recordEvent(config, "premium_prompt_shown", { guildId, source: "upgrade_command" });
    saveGuildConfig();
    return interaction.reply({
      content: [
        "Premium checkout is ready.",
        "Includes: multi-channel daily posts, timezone/hour control, filters, analytics, and premium commands.",
        "Start a 7-day trial, then $3.99/month. Cancel anytime.",
        `Checkout: ${session.url}`,
      ].join("\n"),
      flags: MessageFlags.Ephemeral,
      components: [
        new ActionRowBuilder().addComponents(
          new ButtonBuilder().setCustomId("start_trial").setLabel("Start 7-day trial").setStyle(ButtonStyle.Success),
          new ButtonBuilder().setLabel("Open Checkout").setStyle(ButtonStyle.Link).setURL(session.url)
        ),
      ],
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

async function handleShare(interaction) {
  if (interaction.guildId) {
    const config = getGuildConfig(interaction.guildId);
    recordEvent(config, "invite_cta_shown", { guildId: interaction.guildId, source: "share_command" });
    saveGuildConfig();
  }
  return interaction.reply({
    content: "Share the Obscure Holiday Calendar bot with another server:",
    components: [
      new ActionRowBuilder().addComponents(
        new ButtonBuilder().setLabel("Invite to another server").setStyle(ButtonStyle.Link).setURL(BOT_INVITE_URL),
        new ButtonBuilder().setLabel("Support / Info").setStyle(ButtonStyle.Link).setURL(SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/")
      ),
    ],
    flags: MessageFlags.Ephemeral,
  });
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
  scheduleWeeklyRecap();
  sweepActivationNudges();
  setInterval(sweepActivationNudges, ACTIVATION_SWEEP_INTERVAL_MS);

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

  // Post stats to botlist.me now and on interval
  postBotListStats();
  if (BOTLIST_TOKEN && BOTLIST_POST_INTERVAL_MIN > 0) {
    setInterval(postBotListStats, BOTLIST_POST_INTERVAL_MIN * 60 * 1000);
  }
});

client.on("interactionCreate", async (interaction) => {
  try {
    if (interaction.isChatInputCommand()) {
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
      case "categories":
        return handleCategories(interaction);
      case "setcategories":
        return handleSetCategories(interaction);
      case "excludesensitive":
        return handleExcludeSensitive(interaction);
      case "trial":
        return handleTrialStatus(interaction);
      case "block-holiday":
        return handleOverrideUpdate(interaction, "blockedHolidayIds", "add");
      case "unblock-holiday":
        return handleOverrideUpdate(interaction, "blockedHolidayIds", "remove");
      case "force-holiday":
        return handleOverrideUpdate(interaction, "forcedHolidayIds", "add");
      case "unforce-holiday":
        return handleOverrideUpdate(interaction, "forcedHolidayIds", "remove");
      case "overrides":
        return handleOverrides(interaction);
      case "why":
        return handleWhy(interaction);
      case "admin-stats":
        return handleAdminStats(interaction);
      case "admin-funnel":
        return handleAdminFunnel(interaction);
      case "admin-health":
        return handleAdminHealth(interaction);
      case "admin-fire":
        return handleAdminFire(interaction);
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
        case "postnowall":
          return handlePostNowAll(interaction);
	        case "invite":
	          if (interaction.guildId) {
	            const config = getGuildConfig(interaction.guildId);
	            recordEvent(config, "invite_cta_shown", { guildId: interaction.guildId, source: "invite_command" });
	            saveGuildConfig();
	          }
	          return interaction.reply({
            content: "Invite the bot to your server:",
            components: [
              new ActionRowBuilder().addComponents(
                new ButtonBuilder().setLabel("Invite to another server").setStyle(ButtonStyle.Link).setURL(BOT_INVITE_URL),
                new ButtonBuilder().setLabel("Get the App").setStyle(ButtonStyle.Link).setURL(APP_URL)
              ),
            ],
          });
        case "share":
          return handleShare(interaction);
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
    }
    if (interaction.isButton()) {
      if (interaction.customId === "start_trial") {
        return handleStartTrialButton(interaction);
      }
      if (interaction.customId === "invite_cta") {
        if (interaction.guildId) {
          const config = getGuildConfig(interaction.guildId);
          recordEvent(config, "invite_cta_clicked", {
            guildId: interaction.guildId,
            userId: interaction.user.id,
            source: "message_button",
          });
          saveGuildConfig();
        }
        return interaction.reply({
          content: "Invite the bot to another server:",
          flags: MessageFlags.Ephemeral,
          components: [
            new ActionRowBuilder().addComponents(
              new ButtonBuilder().setLabel("Invite to another server").setStyle(ButtonStyle.Link).setURL(BOT_INVITE_URL),
              new ButtonBuilder().setLabel("Support / Info").setStyle(ButtonStyle.Link).setURL(SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/")
            ),
          ],
        });
      }
    }
    if (interaction.isAutocomplete()) {
      if (interaction.commandName === "setcategories") {
        return handleSetCategoriesAutocomplete(interaction);
      }
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
  const config = getGuildConfig(guild.id);
  const now = Date.now();
  if (!config.firstSeenAt) config.firstSeenAt = now;
  config.activationReminderDueAt = now + ACTIVATION_REMINDER_DELAY_MS;
  config.activationReminderSentAt = 0;
  recordEvent(config, "guild_joined", { guildId: guild.id });
  saveGuildConfig();
  try {
    const owner = await guild.fetchOwner();
    if (!owner?.user) return;
    await maybeSendOnboardingDm(owner.user, guild.id);
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

async function postTodayForChannel(guildId, channelId, options = {}) {
  const config = getGuildConfig(guildId);
  const diagnostics = options?.diagnostics === true;
  const nowMs = Date.now();
  const result = {
    guildId,
    channelId,
    source: options?.source || "scheduler",
    planStatus: getPlanStatus(config, nowMs),
    totalHolidays: 0,
    shownCount: 0,
    hiddenCount: 0,
    upsellShown: false,
    upsellReason: "not_evaluated",
    status: "unknown",
    reason: "",
    eventWrites: [],
    eventsWriteOk: true,
    eventsWriteError: "",
  };

  if (!config.channelIds || !config.channelIds.includes(channelId)) {
    result.status = "fail";
    result.reason = "not_configured";
    markDailyPostAttempt(config, { at: nowMs, guildId, channelId, status: "fail_not_configured", reason: result.reason, planStatus: result.planStatus });
    saveGuildConfig();
    return result;
  }

  const channelSettings = getChannelConfig(guildId, channelId);
  if (channelSettings.skipWeekends) {
    const day = new Date().getDay();
    if (day === 0 || day === 6) {
      result.status = "skipped";
      result.reason = "weekend_skipped";
      markDailyPostAttempt(config, { at: nowMs, guildId, channelId, status: "skip_weekend", reason: result.reason, planStatus: result.planStatus });
      saveGuildConfig();
      return result;
    }
  }

  let channel;
  try {
    channel = await client.channels.fetch(channelId);
  } catch (err) {
    const reason = isMissingAccessError(err) ? "missing_channel_or_access_fetch" : "fetch_error";
    result.status = "fail";
    result.reason = reason;
    markDailyPostAttempt(config, { at: Date.now(), guildId, channelId, status: "fail_fetch", reason, planStatus: result.planStatus });
    if (isMissingAccessError(err)) {
      removeChannelFromConfig(guildId, channelId, `fetch failed: ${err?.code || err?.status || "unknown"}`);
      return result;
    }
    saveGuildConfig();
    throw err;
  }
  if (!channel || !channel.isTextBased()) {
    result.status = "fail";
    result.reason = "invalid_channel";
    markDailyPostAttempt(config, { at: Date.now(), guildId, channelId, status: "fail_invalid_channel", reason: result.reason, planStatus: result.planStatus });
    saveGuildConfig();
    return result;
  }

  const now = new Date();
  const mmdd = `${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  const hits = findByDate(mmdd);
  result.totalHolidays = hits.length;
  const dateKey = getDateKey(now, channelSettings.timezone);
  const premium = isPremiumGuild(channel.guild);
  const wildcardHoliday = premium ? maybePickWildcardHoliday(config, dateKey) : null;
  const filteredHits = premium ? applyServerFilters(hits, config) : hits;

  const writeEvent = (event, meta = {}) => {
    const writeResult = recordEvent(config, event, meta);
    if (diagnostics) {
      result.eventWrites.push({
        event,
        ok: !!writeResult.ok,
        id: writeResult.eventId || null,
        at: writeResult.at || null,
        error: writeResult.error || "",
      });
    }
    if (!writeResult.ok) {
      result.eventsWriteOk = false;
      if (!result.eventsWriteError) result.eventsWriteError = writeResult.error || "event_write_failed";
    }
    return writeResult;
  };

  if (premium) {
    const summary = summarizeFilterReasons(hits, filteredHits, config);
    if (summary) {
      writeEvent("filter_applied", { guildId, channelId, source: "daily_post", ...summary });
    }
  }
  if (!hits.length) {
    await channel.send("No holiday found for today. Check back tomorrow!");
    result.status = "fail";
    result.reason = "no_holidays_today";
    markDailyPostAttempt(config, { at: Date.now(), guildId, channelId, status: "fail_no_holiday", reason: result.reason, planStatus: result.planStatus });
    saveGuildConfig();
    return result;
  }
  if (!filteredHits.length) {
    await channel.send("No holiday found for today with current filters.");
    result.status = "fail";
    result.reason = "all_filtered_out";
    markDailyPostAttempt(config, { at: Date.now(), guildId, channelId, status: "fail_filtered_out", reason: result.reason, planStatus: result.planStatus });
    saveGuildConfig();
    return result;
  }

  const branding = !premium || channelSettings.branding;
  const maxFreeItems = 3;
  const listHits = premium ? filteredHits : filteredHits.slice(0, maxFreeItems);
  const hiddenCount = Math.max(0, filteredHits.length - listHits.length);
  result.shownCount = listHits.length;
  result.hiddenCount = hiddenCount;
  const choice = premium ? Math.min(channelSettings.holidayChoice || 0, filteredHits.length - 1) : 0;
  const pickPool = premium ? filteredHits : listHits;
  const pick =
    wildcardHoliday ||
    pickHolidayForTone(pickPool, channelSettings.tone, choice) ||
    pickPool[choice] ||
    pickPool[0];
  const listNames = listHits.map((h) => h.name).join(", ");
  const todayEmbed = buildEmbed(pick, {
    branding,
    style: channelSettings.style,
    color: channelSettings.color || undefined,
    tone: channelSettings.tone,
  });

  const tomorrow = new Date(now);
  tomorrow.setDate(now.getDate() + 1);
  const tmm = `${pad(tomorrow.getMonth() + 1)}-${pad(tomorrow.getDate())}`;
  const nextHits = applyServerFilters(findByDate(tmm), config);
  const teaser = wildcardHoliday ? "" : nextHits.length ? `Up next: ${nextHits[0].name} (${prettyDate(tmm)})` : "";
  const mention = channelSettings.quiet ? "" : channelSettings.roleId ? `<@&${channelSettings.roleId}> ` : "";
  const { rows: promoRows, note: promoNote } = buildPromoComponents(guildId, { includeRate: true, forceVote: true });
  let trialNote = "";
  let trialRow = null;
  const showUpsell = !premium && shouldShowUpsell(config, now, hiddenCount);
  result.upsellShown = showUpsell;
  if (showUpsell) {
    trialNote = `Try free for 7 days: Category Filters + Work-Safe Mode.\nStart a 7-day trial to see ${hiddenCount} more today.`;
    trialRow = buildTrialActionRow();
    result.upsellReason = "free_plan_hidden_count_threshold_met";
  } else if (premium) {
    result.upsellReason = "premium_or_trial_plan";
  } else if (hiddenCount <= 0) {
    result.upsellReason = "hidden_count_below_threshold";
  } else {
    result.upsellReason = "upsell_rate_limited_or_throttled";
  }
  let shareNote = "";
  if (canShowSharePrompt(guildId)) {
    shareNote = "Like this bot? Invite it to another server to help it grow.";
    markSharePrompt(guildId);
    writeEvent("invite_cta_shown", { guildId, source: "daily_share_note" });
  }
  let announcementNote = "";
  if (!config.featureAnnouncementSentAt) {
    announcementNote = "New: Category Filters + Work-Safe Mode. Try free for 7 days — run /trial.";
  }
  let trialReminderNote = "";
  if (config.trialReminderPending && !config.trialReminderSentAt) {
    const endsAt = Number(config.trialEndsAt || 0);
    if (config.isPremium) {
      config.trialReminderPending = false;
      writeEvent("trial_reminder_skipped", { guildId, reason: "upgraded" });
    } else if (!endsAt || endsAt - Date.now() > 24 * 60 * 60 * 1000) {
      config.trialReminderPending = false;
      writeEvent("trial_reminder_skipped", { guildId, reason: "trial_extended" });
    } else {
      const upgradeUrl = await getBestUpgradeUrlForGuild(guildId);
      trialReminderNote = `Trial ends tomorrow — keep filters active by upgrading: ${upgradeUrl}`;
    }
  }
  const components = [...buildButtons(pick), ...promoRows, ...(trialRow ? [trialRow] : [])];
  const streakLine = config.streakCount ? `\n🔥 Server streak: ${config.streakCount} day${config.streakCount === 1 ? "" : "s"}` : "";
  const wildcardLine = wildcardHoliday ? "\n🪄 Wildcard Day: surprise pick" : "";
  const promptLine = buildMicroPrompt(pick, channelSettings.tone);
  const loreLines = buildLoreLines(config, getDateKey(now, channelSettings.timezone));

  try {
    const sent = await channel.send({
      content: `${mention}🎉 Today’s holidays: ${listNames}${wildcardLine}${teaser ? `\n${teaser}` : ""}${announcementNote ? `\n${announcementNote}` : ""}${trialNote ? `\n${trialNote}` : ""}${trialReminderNote ? `\n${trialReminderNote}` : ""}${streakLine}${loreLines.length ? `\n\n${loreLines.join("\n")}` : ""}${promptLine ? `\n\n${promptLine}` : ""}${promoNote ? `\n\n${promoNote}` : ""}${shareNote ? `\n\n${shareNote}` : ""}`,
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
    if (showUpsell) {
      config.upsellWeekCount = (config.upsellWeekCount || 0) + 1;
      writeEvent("upsell_shown", { guildId, hiddenCount });
    }
    if (announcementNote) {
      config.featureAnnouncementSentAt = Date.now();
    }
    if (trialReminderNote) {
      config.trialReminderSentAt = Date.now();
      config.trialReminderPending = false;
      writeEvent("trial_reminder_sent", { guildId, method: "fallback_post" });
    }
    writeEvent("daily_post_sent", { guildId, channelId, holiday: pick.name || "" });
    markDailyPostAttempt(config, { at: Date.now(), guildId, channelId, status: "success", reason: "sent", planStatus: result.planStatus });
    saveGuildConfig();
    await maybeSendTrialReminder(guildId);
    scheduleDidYouKnow(channel, sent?.id || null, pick);
    result.status = "success";
    result.reason = "sent";
    return result;
  } catch (err) {
    const isRateLimited = Number(err?.status) === 429 || Number(err?.code) === 429;
    const reason = isRateLimited ? "rate_limited" : isMissingAccessError(err) ? "missing_channel_or_access_send" : "send_error";
    result.status = "fail";
    result.reason = reason;
    markDailyPostAttempt(config, { at: Date.now(), guildId, channelId, status: "fail_send", reason, planStatus: result.planStatus });
    if (isMissingAccessError(err)) {
      removeChannelFromConfig(guildId, channelId, `send failed: ${err?.code || err?.status || "unknown"}`);
      return result;
    }
    saveGuildConfig();
    throw err;
  }
}

async function sendSetupPreview(channel, config, premium, channelSettings) {
  try {
    const now = new Date();
    const mmdd = `${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
    const hits = findByDate(mmdd);
    if (!hits.length) return;
    const pick = hits[0];
    const showBranding = !premium || (channelSettings?.branding ?? config.branding);
    const embed = buildEmbed(pick, {
      branding: showBranding,
      tone: config.tone,
    });
    await channel.send({
      content: "Setup complete! Here’s a preview of today’s holiday post:",
      embeds: [embed],
      components: buildButtons(pick),
    });
  } catch (err) {
    console.warn("Setup preview failed:", err?.message || err);
  }
}

async function sendWeeklyRecap(guildId) {
  const config = getGuildConfig(guildId);
  if (!config.channelIds || !config.channelIds.length) return;
  const channelId = config.channelIds[0];
  let channel;
  try {
    channel = await client.channels.fetch(channelId);
  } catch (err) {
    if (isMissingAccessError(err)) {
      removeChannelFromConfig(guildId, channelId, `recap fetch failed: ${err?.code || err?.status || "unknown"}`);
    }
    return;
  }
  if (!channel || !channel.isTextBased()) return;

  const analytics = config.analytics || { channels: {}, holidays: {}, history: [] };
  const history = Array.isArray(analytics.history) ? analytics.history : [];
  const dateKeys = new Set(lastDateKeys(7));
  const lastWeek = history.filter((entry) => entry.dateKey && dateKeys.has(entry.dateKey));

  const totalPosts = lastWeek.length;
  const totalReactions = lastWeek.reduce((sum, entry) => sum + (entry.reactions || 0), 0);

  const topHoliday = lastWeek.reduce((acc, entry) => {
    const key = entry.name || entry.slug || "holiday";
    acc[key] = (acc[key] || 0) + (entry.reactions || 0);
    return acc;
  }, {});
  const topHolidayEntry = Object.entries(topHoliday).sort((a, b) => b[1] - a[1])[0];

  const topChannel = lastWeek
    .reduce((acc, entry) => {
      const key = entry.channelId || "unknown";
      acc[key] = (acc[key] || 0) + (entry.reactions || 0);
      return acc;
    }, {});
  const topChannelEntry = Object.entries(topChannel).sort((a, b) => b[1] - a[1])[0];

  const lines = [
    "Weekly recap — Obscure Holiday Calendar",
    totalPosts ? `Posts: ${totalPosts}` : "Posts: no data yet",
    `Reactions: ${totalReactions}`,
    topHolidayEntry ? `Top holiday: ${topHolidayEntry[0]} (${topHolidayEntry[1]})` : "Top holiday: no data yet",
    topChannelEntry ? `Top channel: <#${topChannelEntry[0]}> (${topChannelEntry[1]})` : "Top channel: no data yet",
  ];

  try {
    await channel.send({
      content: lines.join("\n"),
      components: [
        new ActionRowBuilder().addComponents(
          new ButtonBuilder().setLabel("Invite to another server").setStyle(ButtonStyle.Link).setURL(BOT_INVITE_URL),
          new ButtonBuilder().setLabel("Upgrade to Premium").setStyle(ButtonStyle.Link).setURL(SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/")
        ),
      ],
    });
    config.lastWeeklyRecapAt = Date.now();
    saveGuildConfig();
  } catch (err) {
    console.warn("Weekly recap send failed:", err?.message || err);
  }
}

function scheduleWeeklyRecap() {
  const runRecaps = async () => {
    const guildIds = Object.keys(guildConfig);
    for (const guildId of guildIds) {
      const cfg = getGuildConfig(guildId);
      const last = Number(cfg.lastWeeklyRecapAt || 0);
      if (Date.now() - last >= 7 * 24 * 60 * 60 * 1000) {
        await sendWeeklyRecap(guildId);
      }
    }
  };
  runRecaps();
  setInterval(runRecaps, WEEKLY_RECAP_INTERVAL_MS);
}

// Start HTTP server (Stripe + health)
const listenPort = PORT || 8080;
http.createServer(app).listen(listenPort, () => {
  console.log(`HTTP server listening on ${listenPort}`);
});

client.login(TOKEN);
