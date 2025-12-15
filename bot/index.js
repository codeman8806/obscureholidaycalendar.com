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
const TOPGG_VOTE_URL = process.env.TOPGG_VOTE_URL || "https://top.gg/bot/1447955404142153789/vote";
const TOPGG_REVIEW_URL = process.env.TOPGG_REVIEW_URL || "https://top.gg/bot/1447955404142153789#reviews";
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
const STRIPE_PORTAL_RETURN_URL = process.env.STRIPE_PORTAL_RETURN_URL || `${SITE_URL}/discord-bot/`;
const DEFAULT_HOLIDAY_CHOICE = 0; // which holiday of the day to schedule: 0 = first, 1 = second
const DEFAULT_EMBED_COLOR = 0x1c96f3;
const DEFAULT_EMBED_STYLE = "compact";

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

async function syncPremiumFromStripe() {
  if (!stripeClient || !STRIPE_PRICE_ID) return;
  try {
    let startingAfter = null;
    let total = 0;
    while (true) {
      const page = await stripeClient.subscriptions.list({
        status: "active",
        limit: 100,
        starting_after: startingAfter || undefined,
        expand: ["data.default_payment_method"],
      });
      for (const sub of page.data) {
        const item = sub.items?.data?.[0];
        const priceId = item?.price?.id;
        const guildId = sub.metadata?.guild_id || item?.price?.metadata?.guild_id;
        if (priceId === STRIPE_PRICE_ID && guildId) {
          setPremiumGuild(guildId, true);
          total++;
        }
      }
      if (!page.has_more) break;
      startingAfter = page.data[page.data.length - 1].id;
    }
    if (total) console.log(`Synced ${total} premium guild(s) from Stripe.`);
  } catch (err) {
    console.warn("Failed to sync premium from Stripe:", err.message);
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
      channelSettings: {},
    };
  }
  // Backfill new fields
  if (!guildConfig[guildId].channelSettings) {
    guildConfig[guildId].channelSettings = {};
  }
  if (typeof guildConfig[guildId].holidayChoice !== "number") {
    guildConfig[guildId].holidayChoice = DEFAULT_HOLIDAY_CHOICE;
  }
  return guildConfig[guildId];
}

function saveGuildConfig() {
  writeJsonSafe(CONFIG_PATH, guildConfig);
}

function getChannelConfig(guildId, channelId) {
  const base = getGuildConfig(guildId);
  const channelSettings = base.channelSettings?.[channelId] || {};
  return {
    channelId,
    timezone: channelSettings.timezone || base.timezone || "UTC",
    hour: Number.isInteger(channelSettings.hour) ? channelSettings.hour : base.hour || 0,
    branding: channelSettings.branding ?? base.branding ?? true,
    holidayChoice: Number.isInteger(channelSettings.holidayChoice) ? channelSettings.holidayChoice : base.holidayChoice || 0,
    roleId: channelSettings.roleId || null,
    quiet: channelSettings.quiet || false,
    style: channelSettings.style || DEFAULT_EMBED_STYLE,
    color: channelSettings.color || null,
    skipWeekends: channelSettings.skipWeekends || false,
  };
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
  const fullDesc = h.description || "";
  const style = options.style || DEFAULT_EMBED_STYLE;
  const desc = style === "rich" ? fullDesc.slice(0, 1200) : fullDesc.slice(0, 500);
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
  if (!hits.length) return interaction.reply({ content: "No holiday found for today.", ephemeral: true });
  const premium = isPremium(interaction.guild, interaction.member);
  const config = getGuildConfig(interaction.guild.id);
  const choice = Math.min(config.holidayChoice || 0, hits.length - 1);
  const pick = hits[choice] || hits[0];
  return interaction.reply({ embeds: [buildEmbed(pick, { branding: !premium || config.branding })], components: buildButtons(pick) });
}

async function handleHelp(interaction) {
  return interaction.reply({
    content: [
      "Holiday bot slash commands:",
      "/today — today’s holiday",
      "/date MM-DD — holiday on a date (premium)",
      "/search <query> — find matching holidays (premium)",
      "/random — surprise me (premium)",
      "/facts <name|MM-DD> — quick fun facts (premium)",
      "/invite — invite the bot",
      "/support — help/landing page",
      "/vote — vote on top.gg",
      "/rate — leave a review on top.gg",
      "/app — mobile app links",
      "/setup — configure daily posts (premium unlocks time/timezone/branding)",
      "/premium — check your premium status",
      "/upgrade — start a premium checkout",
      "/manage — manage/cancel premium (billing portal)",
      "/tomorrow — tomorrow’s holiday (premium)",
      "/upcoming — upcoming holidays (premium)",
      "/week — 7-day digest (premium)",
      "/help — list commands",
    ].join("\n"),
    ephemeral: true,
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
    ephemeral: true,
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
    ephemeral: true,
  });
}

async function handleDate(interaction) {
  if (!isPremium(interaction.guild, interaction.member)) {
    return interaction.reply({ content: "Premium only. Upgrade with /upgrade to use /date.", ephemeral: true });
  }
  const input = interaction.options.getString("date", true);
  const parsed = parseDate(input);
  if (!parsed) return interaction.reply({ content: "Please provide a date as MM-DD or MM/DD (example: 07-04).", ephemeral: true });
  const hits = findByDate(parsed);
  if (!hits.length) return interaction.reply({ content: `No holidays found on ${parsed}.`, ephemeral: true });
  const config = getGuildConfig(interaction.guild.id);
  return interaction.reply({ embeds: [buildEmbed(hits[0], { branding: config.branding })], components: buildButtons(hits[0]) });
}

async function handleSearch(interaction) {
  if (!isPremium(interaction.guild, interaction.member)) {
    return interaction.reply({ content: "Premium only. Upgrade with /upgrade to use /search.", ephemeral: true });
  }
  const query = interaction.options.getString("query", true);
  const matches = findByName(query);
  if (!matches.length) return interaction.reply({ content: "No match. Try a simpler phrase.", ephemeral: true });
  const config = getGuildConfig(interaction.guild.id);
  const embeds = matches.slice(0, 3).map((h) => buildEmbed(h, { branding: config.branding }));
  return interaction.reply({ embeds, components: buildButtons(matches[0]) });
}

async function handleRandom(interaction) {
  if (!isPremium(interaction.guild, interaction.member)) {
    return interaction.reply({ content: "Premium only. Upgrade with /upgrade to use /random.", ephemeral: true });
  }
  const h = pickRandom();
  const config = getGuildConfig(interaction.guild.id);
  return interaction.reply({ embeds: [buildEmbed(h, { branding: config.branding })], components: buildButtons(h) });
}

async function handleWeek(interaction) {
  const premium = isPremium(interaction.guild, interaction.member);
  if (!premium) {
    return interaction.reply({ content: "Premium only. Upgrade to get the 7-day digest.", ephemeral: true });
  }
  const days = Math.max(3, Math.min(interaction.options.getInteger("days") || 7, 14));
  const now = new Date();
  const items = holidaysForRange(now, days);
  if (!items.length) return interaction.reply({ content: "No upcoming holidays found.", ephemeral: true });
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
  return interaction.reply({ embeds: [embed] });
}

async function handleSetup(interaction) {
  const guildId = interaction.guild.id;
  const config = getGuildConfig(guildId);
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
  const premium = isPremium(interaction.guild, interaction.member);

  if (!channel.isTextBased()) {
    return interaction.reply({ content: "Please pick a text channel.", ephemeral: true });
  }

  if (!premium) {
    config.channelIds = [channel.id];
    config.timezone = "UTC";
    config.hour = 0;
    config.branding = true;
    config.holidayChoice = DEFAULT_HOLIDAY_CHOICE;
    saveGuildConfig();
    scheduleForChannel(guildId, channel.id);
    return interaction.reply({ content: `Daily posts set to <#${channel.id}> at 00:00 UTC. Premium unlocks timezone/hour/branding toggles.`, ephemeral: true });
  }

  // Premium path: allow multiple channels, timezone/hour, branding toggle, holiday choice, role mention, quiet, style, color, skip weekends
  if (!config.channelIds.includes(channel.id)) {
    config.channelIds.push(channel.id);
  }
  if (!config.channelSettings) config.channelSettings = {};
  const ch = config.channelSettings[channel.id] || {};
  if (tz) ch.timezone = tz;
  if (Number.isInteger(hour)) ch.hour = Math.max(0, Math.min(hour, 23));
  if (typeof brandingOpt === "boolean") ch.branding = brandingOpt;
  if (Number.isInteger(holidayChoice)) ch.holidayChoice = Math.min(Math.max(holidayChoice, 0), 1);
  if (role) ch.roleId = role.id;
  if (typeof quiet === "boolean") ch.quiet = quiet;
  if (embedStyle) ch.style = embedStyle;
  if (embedColor && /^#?[0-9a-fA-F]{6}$/.test(embedColor)) {
    ch.color = Number.parseInt(embedColor.replace("#", ""), 16);
  }
  if (typeof skipWeekends === "boolean") ch.skipWeekends = skipWeekends;
  config.channelSettings[channel.id] = ch;

  saveGuildConfig();
  scheduleForChannel(guildId, channel.id);

  return interaction.reply({
    content: [
      `Daily posts set to ${config.channelIds.map((c) => `<#${c}>`).join(", ")}`,
      `Time: ${(ch.hour ?? config.hour)}:00 in ${ch.timezone || config.timezone}`,
      `Branding: ${ch.branding === false ? "off" : "on"}`,
      `Holiday pick: ${ch.holidayChoice === 1 ? "second of the day" : "first of the day"}`,
      role ? `Role ping: <@&${role.id}>` : "Role ping: none",
      `Quiet mode: ${ch.quiet ? "on" : "off"}`,
      `Skip weekends: ${ch.skipWeekends ? "yes" : "no"}`,
    ].join("\n"),
    ephemeral: true,
  });
}

async function handleFacts(interaction) {
  if (!isPremium(interaction.guild, interaction.member)) {
    return interaction.reply({ content: "Premium only. Upgrade with /upgrade to use /facts.", ephemeral: true });
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
  const benefits = [
    "✅ Multiple daily channels",
    "✅ Custom timezone & hour",
    "✅ Premium commands: /tomorrow, /upcoming",
    "✅ Branding toggle",
    "✅ Pick which of the day’s holidays to auto-post",
    "✅ Per-channel role pings & quiet mode",
    "✅ Rich/compact embeds, custom color",
    "✅ Skip-weekends scheduling",
    "✅ 7-day digest: /week",
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
    return interaction.reply({ content: lines.join("\n"), ephemeral: true });
  }

  // Not premium: offer upgrade
  let upgradeUrl = SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/";
  if (stripeClient && STRIPE_PRICE_ID) {
    try {
      const session = await stripeClient.checkout.sessions.create({
        mode: "subscription",
        line_items: [{ price: STRIPE_PRICE_ID, quantity: 1 }],
        success_url: STRIPE_SUCCESS_URL,
        cancel_url: STRIPE_CANCEL_URL,
        metadata: { guild_id: interaction.guildId, user_id: interaction.user.id },
        subscription_data: { metadata: { guild_id: interaction.guildId, user_id: interaction.user.id } },
      });
      if (session.url) upgradeUrl = session.url;
    } catch (err) {
      console.error("Stripe checkout error (premium status):", err);
    }
  }

  const lines = [
    "⚠️ Premium not active.",
    "Premium unlocks:",
    ...benefits,
  ];

  return interaction.reply({
    content: lines.join("\n"),
    ephemeral: true,
    components: [
      new ActionRowBuilder().addComponents(
        new ButtonBuilder().setLabel("Upgrade to Premium").setStyle(ButtonStyle.Link).setURL(upgradeUrl),
        new ButtonBuilder().setLabel("Support / Info").setStyle(ButtonStyle.Link).setURL(SUPPORT_URL || "https://www.obscureholidaycalendar.com/discord-bot/")
      ),
    ],
  });
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

async function handleManage(interaction) {
  if (!stripeClient) return interaction.reply({ content: "Stripe is not configured.", ephemeral: true });
  const premium = isPremium(interaction.guild, interaction.member);
  if (!premium) {
    return interaction.reply({ content: "This server is not premium yet. Use /upgrade to start a subscription.", ephemeral: true });
  }
  // Find the customer for this guild by looking up active subscriptions with matching metadata
  let customerId = null;
  try {
    let startingAfter = null;
    while (true) {
      const subs = await stripeClient.subscriptions.list({
        status: "active",
        price: STRIPE_PRICE_ID || undefined,
        limit: 100,
        starting_after: startingAfter || undefined,
      });
      for (const sub of subs.data) {
        const gid = sub.metadata?.guild_id || sub.items?.data?.[0]?.metadata?.guild_id;
        if (gid === interaction.guildId) {
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
      return interaction.reply({ content: `Manage your subscription here: ${session.url}`, ephemeral: true });
    }
  } catch (err) {
    console.error("Stripe portal error:", err);
  }
  return interaction.reply({ content: "Unable to open the billing portal right now. If you just subscribed, give it a minute and try again.", ephemeral: true });
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
  { name: "vote", description: "Vote for the bot on top.gg" },
  { name: "rate", description: "Leave a review on top.gg" },
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
      {
        name: "holiday_choice",
        description: "Premium: pick which of the day’s holidays to post",
        type: ApplicationCommandOptionType.Integer,
        required: false,
        choices: [
          { name: "First holiday of the day", value: 0 },
          { name: "Second holiday of the day", value: 1 },
        ],
      },
      {
        name: "role_mention",
        description: "Premium: role to mention in daily posts",
        type: ApplicationCommandOptionType.Role,
        required: false,
      },
      {
        name: "quiet",
        description: "Premium: don’t mention anyone",
        type: ApplicationCommandOptionType.Boolean,
        required: false,
      },
      {
        name: "embed_style",
        description: "Premium: choose compact vs rich content",
        type: ApplicationCommandOptionType.String,
        required: false,
        choices: [
          { name: "Compact", value: "compact" },
          { name: "Rich", value: "rich" },
        ],
      },
      {
        name: "embed_color",
        description: "Premium: hex color like #1c96f3",
        type: ApplicationCommandOptionType.String,
        required: false,
      },
      {
        name: "skip_weekends",
        description: "Premium: don’t post on Sat/Sun",
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
    name: "week",
    description: "Premium: show a 7-day digest",
    options: [
      {
        name: "days",
        description: "How many days (3-14)",
        type: ApplicationCommandOptionType.Integer,
        required: false,
      },
    ],
  },
  {
    name: "upgrade",
    description: "Get a premium checkout link",
  },
  {
    name: "manage",
    description: "Manage your premium subscription (billing portal)",
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

  // Sync premium allowlist from Stripe on startup
  await syncPremiumFromStripe();

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
      case "vote":
        return handleVote(interaction);
      case "rate":
        return handleRate(interaction);
      case "facts":
        return handleFacts(interaction);
      case "setup":
        return handleSetup(interaction);
      case "premium":
        return handlePremiumStatus(interaction);
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
  Object.keys(guildConfig).forEach((guildId) => {
    const cfg = getGuildConfig(guildId);
    (cfg.channelIds || []).forEach((chId) => scheduleForChannel(guildId, chId));
  });
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
  const channel = await client.channels.fetch(channelId);
  if (!channel || !channel.isTextBased()) return;

  const now = new Date();
  const mmdd = `${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  const hits = findByDate(mmdd);
  if (!hits.length) {
    return channel.send("No holiday found for today. Check back tomorrow!");
  }

  const premium = isPremiumGuild(channel.guild);
  const branding = !premium || channelSettings.branding;
  const choice = Math.min(channelSettings.holidayChoice || 0, hits.length - 1);
  const pick = hits[choice] || hits[0];
  const topNames = hits.slice(0, 2).map((h) => h.name).join(" and ");
  const todayEmbed = buildEmbed(pick, { branding, style: channelSettings.style, color: channelSettings.color || undefined });

  // Coming up tomorrow teaser
  const tomorrow = new Date(now);
  tomorrow.setDate(now.getDate() + 1);
  const tmm = `${pad(tomorrow.getMonth() + 1)}-${pad(tomorrow.getDate())}`;
  const nextHits = findByDate(tmm);
  const teaser = nextHits.length ? `Up next: ${nextHits[0].name} (${prettyDate(tmm)})` : "";

  const mention = channelSettings.quiet ? "" : channelSettings.roleId ? `<@&${channelSettings.roleId}> ` : "";

  await channel.send({
    content: `${mention}🎉 Today’s holidays: ${topNames}${teaser ? `\n${teaser}` : ""}`,
    embeds: [todayEmbed],
    components: buildButtons(pick),
  });
}

// Start HTTP server (Stripe + health)
const listenPort = PORT || 8080;
http.createServer(app).listen(listenPort, () => {
  console.log(`HTTP server listening on ${listenPort}`);
});

client.login(TOKEN);
