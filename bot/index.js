import fs from "fs";
import path from "path";
import http from "http";
import express from "express";
import Stripe from "stripe";
import { fileURLToPath } from "url";
import {
  Client,
  GatewayIntentBits,
  EmbedBuilder,
  ActivityType,
  ApplicationCommandOptionType,
  ActionRowBuilder,
  ButtonBuilder,
  ButtonStyle,
} from "discord.js";

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
const PREMIUM_ROLE_ID = process.env.PREMIUM_ROLE_ID || null; // Discord Server Subscription role id
const CONFIG_PATH = path.resolve(__dirname, "guild-config.json");
const PREMIUM_PATH = path.resolve(__dirname, "premium.json"); // optional allowlist
const BOT_OWNER_ID = process.env.BOT_OWNER_ID || null;
const TOPGG_TOKEN = process.env.TOPGG_TOKEN || null; // for posting stats to top.gg
const TOPGG_POST_INTERVAL_MIN = Number(process.env.TOPGG_POST_INTERVAL_MIN || "30");
const PORT = process.env.PORT || null; // for Railway/health checks (optional)
const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY || null;
const STRIPE_PRICE_ID = process.env.STRIPE_PRICE_ID || null; // subscription price id
const STRIPE_LOOKUP_KEY = process.env.STRIPE_LOOKUP_KEY || null; // optional lookup key
const STRIPE_WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET || null;
const STRIPE_SUCCESS_URL = process.env.STRIPE_SUCCESS_URL || `${SITE_URL}/discord-bot/?success=1`;
const STRIPE_CANCEL_URL = process.env.STRIPE_CANCEL_URL || `${SITE_URL}/discord-bot/?canceled=1`;

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

function loadHolidays() {
  const raw = fs.readFileSync(HOLIDAYS_PATH, "utf8");
  const data = JSON.parse(raw);
  return data.holidays || {};
}

const holidaysByDate = loadHolidays();
const allHolidays = Object.values(holidaysByDate).flat();

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
    const botId = client.user?.id;
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

// Stripe Checkout session creation
app.post("/create-checkout-session", express.json(), async (req, res) => {
  if (!stripeClient) return res.status(400).json({ error: "Stripe not configured" });
  try {
    const { guild_id, user_id } = req.body || {};
    if (!guild_id) return res.status(400).json({ error: "Missing guild_id" });
    const priceId = STRIPE_PRICE_ID;
    if (!priceId) return res.status(400).json({ error: "Missing STRIPE_PRICE_ID" });
    const session = await stripeClient.checkout.sessions.create({
      mode: "subscription",
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: STRIPE_SUCCESS_URL,
      cancel_url: STRIPE_CANCEL_URL,
      metadata: { guild_id, user_id: user_id || "" },
      subscription_data: {
        metadata: { guild_id, user_id: user_id || "" },
      },
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
  (req, res) => {
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
      timezone: "UTC",
      hour: 0, // 00:00 UTC-ish
      branding: true,
    };
  }
  return guildConfig[guildId];
}

function saveGuildConfig() {
  writeJsonSafe(CONFIG_PATH, guildConfig);
}

function slugify(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
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
  const desc = (h.description || "").slice(0, 500);
  const facts = Array.isArray(h.funFacts) ? h.funFacts.slice(0, 3) : [];
  const slug = h.slug || slugify(name);
  const url = `${SITE_BASE}/${slug}/`;
  const showBranding = options.branding !== false; // default true

  const embed = new EmbedBuilder()
    .setTitle(`${emoji ? emoji + " " : ""}${name}`)
    .setURL(url)
    .setDescription(desc || "Learn more on the site.")
    .addFields([{ name: "Date", value: prettyDate(date), inline: true }])
    .setColor(0x1c96f3);

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
  if (!hits.length) return interaction.reply({ content: "No holiday found for today.", ephemeral: true });
  const premium = isPremium(interaction.guild, interaction.member);
  return interaction.reply({ embeds: [buildEmbed(hits[0], { branding: !premium || getGuildConfig(interaction.guild.id).branding })], components: buildButtons(hits[0]) });
}

async function handleDate(interaction) {
  const input = interaction.options.getString("date", true);
  const parsed = parseDate(input);
  if (!parsed) return interaction.reply({ content: "Please provide a date as MM-DD or MM/DD (example: 07-04).", ephemeral: true });
  const hits = findByDate(parsed);
  if (!hits.length) return interaction.reply({ content: `No holidays found on ${parsed}.`, ephemeral: true });
  const premium = isPremium(interaction.guild, interaction.member);
  return interaction.reply({ embeds: [buildEmbed(hits[0], { branding: !premium || getGuildConfig(interaction.guild.id).branding })], components: buildButtons(hits[0]) });
}

async function handleSearch(interaction) {
  const query = interaction.options.getString("query", true);
  const matches = findByName(query);
  if (!matches.length) return interaction.reply({ content: "No match. Try a simpler phrase.", ephemeral: true });
  const premium = isPremium(interaction.guild, interaction.member);
  const embeds = matches.slice(0, 3).map((h) => buildEmbed(h, { branding: !premium || getGuildConfig(interaction.guild.id).branding }));
  return interaction.reply({ embeds, components: buildButtons(matches[0]) });
}

async function handleRandom(interaction) {
  const h = pickRandom();
  const premium = isPremium(interaction.guild, interaction.member);
  return interaction.reply({ embeds: [buildEmbed(h, { branding: !premium || getGuildConfig(interaction.guild.id).branding })], components: buildButtons(h) });
}

async function handleSetup(interaction) {
  const guildId = interaction.guild.id;
  const config = getGuildConfig(guildId);
  const channel = interaction.options.getChannel("channel", true);
  const tz = interaction.options.getString("timezone");
  const hour = interaction.options.getInteger("hour");
  const brandingOpt = interaction.options.getBoolean("branding");
  const premium = isPremium(interaction.guild, interaction.member);

  if (!channel.isTextBased()) {
    return interaction.reply({ content: "Please pick a text channel.", ephemeral: true });
  }

  if (!premium) {
    config.channelIds = [channel.id];
    config.timezone = "UTC";
    config.hour = 0;
    config.branding = true;
    saveGuildConfig();
    scheduleForGuild(guildId);
    return interaction.reply({ content: `Daily posts set to <#${channel.id}> at 00:00 UTC. Premium unlocks timezone/hour/branding toggles.`, ephemeral: true });
  }

  // Premium path: allow multiple channels (cap 3), timezone/hour, branding toggle
  const MAX_CHANNELS = 3;
  if (!config.channelIds.includes(channel.id)) {
    if (config.channelIds.length >= MAX_CHANNELS) {
      config.channelIds.shift();
    }
    config.channelIds.push(channel.id);
  }
  if (tz) config.timezone = tz;
  if (Number.isInteger(hour)) config.hour = Math.max(0, Math.min(hour, 23));
  if (typeof brandingOpt === "boolean") config.branding = brandingOpt;

  saveGuildConfig();
  scheduleForGuild(guildId);

  return interaction.reply({
    content: [
      `Daily posts set to ${config.channelIds.map((c) => `<#${c}>`).join(", ")}`,
      `Time: ${config.hour}:00 in ${config.timezone}`,
      `Branding: ${config.branding === false ? "off" : "on"}`,
    ].join("\n"),
    ephemeral: true,
  });
}

async function handleFacts(interaction) {
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

  if (!holiday) return interaction.reply({ content: "Couldn't find fun facts for that. Try 12-25 or \"bacon\".", ephemeral: true });
  const facts = Array.isArray(holiday.funFacts) ? holiday.funFacts.slice(0, 5) : [];
  if (!facts.length) return interaction.reply({ content: "No fun facts on file for that one.", ephemeral: true });
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

async function handleTomorrow(interaction) {
  const premium = isPremium(interaction.guild, interaction.member);
  if (!premium) {
    return interaction.reply({ content: "Premium only. Unlock premium via Server Subscription and retry.", ephemeral: true });
  }
  const now = new Date();
  const tomorrow = new Date(now);
  tomorrow.setDate(now.getDate() + 1);
  const mmdd = `${pad(tomorrow.getMonth() + 1)}-${pad(tomorrow.getDate())}`;
  const hits = findByDate(mmdd);
  if (!hits.length) return interaction.reply({ content: "No holiday found for tomorrow.", ephemeral: true });
  const config = getGuildConfig(interaction.guild.id);
  return interaction.reply({ embeds: [buildEmbed(hits[0], { branding: config.branding })], components: buildButtons(hits[0]) });
}

async function handleUpcoming(interaction) {
  const premium = isPremium(interaction.guild, interaction.member);
  if (!premium) {
    return interaction.reply({ content: "Premium only. Unlock premium via Server Subscription and retry.", ephemeral: true });
  }
  const days = Math.max(1, Math.min(interaction.options.getInteger("days") || 7, 30));
  const now = new Date();
  const items = holidaysForRange(now, days);
  if (!items.length) return interaction.reply({ content: "No upcoming holidays found.", ephemeral: true });
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
  const lines = [
    premium ? "✅ Premium active (Server Subscription role or allowlist)." : "⚠️ Premium not active.",
    `Daily channel(s): ${config.channelIds.length ? config.channelIds.map((c) => `<#${c}>`).join(", ") : "not set"}`,
    `Timezone: ${config.timezone} @ ${config.hour}:00`,
    `Branding: ${config.branding === false ? "off" : "on"}`,
  ];
  if (!premium) lines.push(`Upgrade: ${SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/"}`);
  return interaction.reply({ content: lines.join("\n"), ephemeral: true });
}

async function handleUpgrade(interaction) {
  if (!stripeClient || !STRIPE_PRICE_ID) {
    return interaction.reply({ content: "Stripe is not configured. Try again later.", ephemeral: true });
  }
  const guildId = interaction.guildId;
  const userId = interaction.user.id;
  try {
    const session = await stripeClient.checkout.sessions.create({
      mode: "subscription",
      line_items: [{ price: STRIPE_PRICE_ID, quantity: 1 }],
      success_url: STRIPE_SUCCESS_URL,
      cancel_url: STRIPE_CANCEL_URL,
      metadata: { guild_id: guildId, user_id: userId },
      subscription_data: {
        metadata: { guild_id: guildId, user_id: userId },
      },
    });
    return interaction.reply({
      content: `Upgrade to premium using Stripe Checkout: ${session.url}`,
      ephemeral: true,
    });
  } catch (err) {
    console.error("Stripe checkout error:", err);
    return interaction.reply({ content: "Unable to create checkout session right now.", ephemeral: true });
  }
}

async function handleGrantPremium(interaction) {
  if (!isOwner(interaction.user.id)) {
    return interaction.reply({ content: "Owner-only command.", ephemeral: true });
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
  return interaction.reply({ content: `Premium ${flag ? "granted to" : "revoked from"} ${serverId}.`, ephemeral: true });
}

async function handleInstallCount(interaction) {
  if (!isOwner(interaction.user.id)) {
    return interaction.reply({ content: "Owner-only command.", ephemeral: true });
  }
  const count = client.guilds.cache.size;
  return interaction.reply({ content: `I am currently in ${count} server(s).`, ephemeral: true });
}
async function handleHelp(interaction) {
  return interaction.reply({
    content: [
      "Holiday bot slash commands:",
      "/today — today’s holiday",
      "/date MM-DD — holiday on a date (e.g., 12-08)",
      "/search <query> — find matching holidays",
      "/random — surprise me",
      "/facts <name|MM-DD> — quick fun facts",
      "/invite — invite the bot",
      "/support — help/landing page",
      "/app — mobile app links",
      "/setup — configure daily posts (premium unlocks time/timezone/branding)",
      "/premium — check your premium status",
      "/tomorrow — tomorrow’s holiday (premium)",
      "/upcoming — upcoming holidays (premium)",
    ].join("\n"),
    ephemeral: true,
  });
}

const commandDefs = [
  { name: "today", description: "Show today’s holiday" },
  {
    name: "date",
    description: "Show holidays on a specific date",
    options: [
      {
        name: "date",
        description: "MM-DD or MM/DD (e.g., 12-08)",
        type: ApplicationCommandOptionType.String,
        required: true,
      },
    ],
  },
  {
    name: "search",
    description: "Search for a holiday by name/keywords",
    options: [
      {
        name: "query",
        description: "e.g., bacon, pizza, cat",
        type: ApplicationCommandOptionType.String,
        required: true,
      },
    ],
  },
  { name: "random", description: "Get a random holiday" },
  {
    name: "facts",
    description: "Get fun facts for a holiday",
    options: [
      {
        name: "name_or_date",
        description: "Name or MM-DD (leave empty for today)",
        type: ApplicationCommandOptionType.String,
        required: false,
      },
    ],
  },
  { name: "invite", description: "Get the bot invite link" },
  { name: "support", description: "Get help/landing page link" },
  { name: "app", description: "Get the mobile app links" },
  {
    name: "setup",
    description: "Configure daily posts (channel/time). Premium unlocks timezone/hour/branding toggles.",
    options: [
      {
        name: "channel",
        description: "Channel for daily posts",
        type: ApplicationCommandOptionType.Channel,
        required: true,
      },
      {
        name: "timezone",
        description: "IANA timezone (e.g., America/New_York) — Premium only",
        type: ApplicationCommandOptionType.String,
        required: false,
      },
      {
        name: "hour",
        description: "Hour of day 0-23 in that timezone — Premium only",
        type: ApplicationCommandOptionType.Integer,
        required: false,
      },
      {
        name: "branding",
        description: "Show branding footer? true/false (Premium can turn off)",
        type: ApplicationCommandOptionType.Boolean,
        required: false,
      },
    ],
  },
  {
    name: "premium",
    description: "See premium status",
  },
  {
    name: "upgrade",
    description: "Get a premium checkout link",
  },
  {
    name: "tomorrow",
    description: "See tomorrow’s holiday (Premium only)",
  },
  {
    name: "upcoming",
    description: "See upcoming holidays (Premium only)",
    options: [
      {
        name: "days",
        description: "How many days ahead (max 30)",
        type: ApplicationCommandOptionType.Integer,
        required: false,
      },
    ],
  },
  {
    name: "grantpremium",
    description: "Owner-only: grant premium to a server id",
    options: [
      {
        name: "server_id",
        description: "Discord server (guild) ID",
        type: ApplicationCommandOptionType.String,
        required: true,
      },
      {
        name: "enabled",
        description: "true to enable, false to revoke (default true)",
        type: ApplicationCommandOptionType.Boolean,
        required: false,
      },
    ],
  },
  {
    name: "installcount",
    description: "Owner-only: show how many servers this bot is in",
  },
  { name: "help", description: "List commands" },
];

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

client.once("ready", async () => {
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

  // Schedule daily auto-post
  scheduleDailyPost();

  // Post stats to top.gg now and on interval
  postTopGGStats();
  if (TOPGG_TOKEN && TOPGG_POST_INTERVAL_MIN > 0) {
    setInterval(postTopGGStats, TOPGG_POST_INTERVAL_MIN * 60 * 1000);
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
      case "facts":
        return handleFacts(interaction);
      case "setup":
        return handleSetup(interaction);
      case "premium":
        return handlePremiumStatus(interaction);
      case "upgrade":
        return handleUpgrade(interaction);
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
          ephemeral: true,
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
          ephemeral: true,
        });
      case "help":
        return handleHelp(interaction);
      default:
        return interaction.reply({ content: "Unknown command.", ephemeral: true });
    }
  } catch (err) {
    console.error(err);
    if (interaction.replied || interaction.deferred) {
      return interaction.followUp({ content: "Something went wrong handling that request.", ephemeral: true });
    }
    return interaction.reply({ content: "Something went wrong handling that request.", ephemeral: true });
  }
});

client.on("guildCreate", () => {
  postTopGGStats();
});

client.on("guildDelete", () => {
  postTopGGStats();
});

function scheduleDailyPost() {
  console.log("Scheduling daily posts per guild config...");
  Object.keys(guildConfig).forEach((guildId) => scheduleForGuild(guildId));
}

const guildTimers = new Map();

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

function scheduleForGuild(guildId) {
  const config = getGuildConfig(guildId);
  if (!config.channelIds || !config.channelIds.length) return;
  const runAt = nextRunTimestamp(config);
  const delay = Math.max(1000, runAt - Date.now());
  if (guildTimers.has(guildId)) clearTimeout(guildTimers.get(guildId));
  const timer = setTimeout(async () => {
    try {
      await postTodayForGuild(guildId);
    } catch (e) {
      console.error(`Daily post failed for guild ${guildId}:`, e);
    } finally {
      scheduleForGuild(guildId);
    }
  }, delay);
  guildTimers.set(guildId, timer);
  console.log(`Scheduled ${guildId} in ${Math.round(delay / 1000 / 60)} minutes (${config.timezone} @ ${config.hour}:00)`);
}

async function postTodayForGuild(guildId) {
  const config = getGuildConfig(guildId);
  const channelId = config.channelIds[0];
  if (!channelId) return;
  const channel = await client.channels.fetch(channelId);
  if (!channel || !channel.isTextBased()) return;

  const now = new Date();
  const mmdd = `${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  const hits = findByDate(mmdd);
  if (!hits.length) {
    return channel.send("No holiday found for today. Check back tomorrow!");
  }

  const premium = isPremiumGuild(channel.guild);
  const branding = !premium || config.branding;
  const topNames = hits.slice(0, 2).map((h) => h.name).join(" and ");
  const todayEmbed = buildEmbed(hits[0], { branding });

  // Coming up tomorrow teaser
  const tomorrow = new Date(now);
  tomorrow.setDate(now.getDate() + 1);
  const tmm = `${pad(tomorrow.getMonth() + 1)}-${pad(tomorrow.getDate())}`;
  const nextHits = findByDate(tmm);
  const teaser = nextHits.length ? `Up next: ${nextHits[0].name} (${prettyDate(tmm)})` : "";

  await channel.send({
    content: `🎉 Today’s holidays: ${topNames}${teaser ? `\n${teaser}` : ""}`,
    embeds: [todayEmbed],
    components: buildButtons(hits[0]),
  });
}

// Start HTTP server (Stripe + health)
const listenPort = PORT || 8080;
http.createServer(app).listen(listenPort, () => {
  console.log(`HTTP server listening on ${listenPort}`);
});

client.login(TOKEN);
