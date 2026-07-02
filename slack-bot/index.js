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
// Must always match the Bot Token Scopes configured in the Slack app dashboard
// (OAuth & Permissions). Not env-configurable on purpose: a stale env var here
// silently desyncs the install URL from the app config and fails Slack review.
const SLACK_OAUTH_SCOPES = "commands,chat:write,channels:read";
const SLACK_REDIRECT_URI = process.env.SLACK_REDIRECT_URI || null;

const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY || null;
const STRIPE_PRICE_ID_INTRO = process.env.STRIPE_PRICE_ID_INTRO || null;
const STRIPE_PRICE_ID_STANDARD = process.env.STRIPE_PRICE_ID_STANDARD || process.env.STRIPE_PRICE_ID || null;
const STRIPE_WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET || null;
const STRIPE_SUCCESS_URL = process.env.STRIPE_SUCCESS_URL || null;
const STRIPE_CANCEL_URL = process.env.STRIPE_CANCEL_URL || null;
const STRIPE_PORTAL_RETURN_URL = process.env.STRIPE_PORTAL_RETURN_URL || null;
const SLACK_ADMIN_TOKEN = process.env.SLACK_ADMIN_TOKEN || null;
const SLACK_ADMIN_USER = process.env.SLACK_ADMIN_USER || null;
const SLACK_ADMIN_PASS = process.env.SLACK_ADMIN_PASS || null;

const stripeClient = STRIPE_SECRET_KEY ? new Stripe(STRIPE_SECRET_KEY) : null;

const SITE_URL = process.env.SITE_URL || null;
const SITE_BASE = SITE_URL ? `${SITE_URL}/holiday` : null;
const APP_URL = process.env.APP_URL || (SITE_URL ? `${SITE_URL}/app/` : null);
const SUPPORT_URL = process.env.SLACK_SUPPORT_URL || (SITE_URL ? `${SITE_URL}/slack-bot/` : null);
const SLACK_INSTALL_URL =
  process.env.SLACK_INSTALL_URL ||
  (SLACK_REDIRECT_URI ? SLACK_REDIRECT_URI.replace(/\/oauth\/callback$/, "/install") : null) ||
  SUPPORT_URL;
const TOPGG_VOTE_URL = process.env.SLACK_VOTE_URL || null;
const TOPGG_REVIEW_URL = process.env.SLACK_REVIEW_URL || null;

const DATA_DIR = process.env.DATA_DIR ? path.resolve(process.env.DATA_DIR) : __dirname;
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

const CONFIG_PATH = path.resolve(DATA_DIR, "workspace-config.json");
const PREMIUM_PATH = path.resolve(DATA_DIR, "premium.json");
const WORKSPACE_TOKENS_PATH = path.resolve(DATA_DIR, "workspace-tokens.json");

const LEGACY_CONFIG_PATH = path.resolve(__dirname, "workspace-config.json");
const LEGACY_PREMIUM_PATH = path.resolve(__dirname, "premium.json");
const LEGACY_WORKSPACE_TOKENS_PATH = path.resolve(__dirname, "workspace-tokens.json");

const DEFAULT_TIMEZONE = "UTC";
const DEFAULT_HOUR = 9;
const DEFAULT_MINUTE = 0;
const DEFAULT_HOLIDAY_CHOICE = 0;
const OAUTH_STATE_TTL_MS = 10 * 60 * 1000;
const oauthStateStore = new Map();

function pruneOauthStateStore(now = Date.now()) {
  for (const [state, expiresAt] of oauthStateStore.entries()) {
    if (!expiresAt || expiresAt <= now) oauthStateStore.delete(state);
  }
}

function readJsonSafe(filePath, fallback, legacyPaths = []) {
  try {
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, "utf8"));
    }
    for (const legacyPath of legacyPaths) {
      if (fs.existsSync(legacyPath)) {
        const data = JSON.parse(fs.readFileSync(legacyPath, "utf8"));
        writeJsonSafe(filePath, data);
        return data;
      }
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

const workspaceConfig = readJsonSafe(CONFIG_PATH, {}, [LEGACY_CONFIG_PATH]);
const premiumAllowlist = readJsonSafe(PREMIUM_PATH, {}, [LEGACY_PREMIUM_PATH]);
const workspaceTokens = readJsonSafe(WORKSPACE_TOKENS_PATH, {}, [LEGACY_WORKSPACE_TOKENS_PATH]);

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
  if (!holiday) return "";
  if (!SITE_BASE) return SITE_URL || "";
  const slugFromHoliday = String(holiday.slug || "").trim();
  const slugFromName = slugFromHoliday ? "" : nameToSlug[normalizeName(holiday.name || "")];
  const slug = slugFromHoliday || slugFromName || "";
  if (!slug) return SITE_BASE;
  return `${SITE_BASE}/${slug}/`;
}

function formatHoliday(holiday, mmdd) {
  if (!holiday) return "No holiday found.";
  const emoji = holiday.emoji ? `${holiday.emoji} ` : "";
  const dateLine = mmdd ? `(${mmdd})` : "";
  const link = holidayUrl(holiday);
  const lines = [`${emoji}*${holiday.name || "Holiday"}* ${dateLine}`, holiday.description || ""];
  if (link) lines.push(link);
  return lines.join("\n");
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
      minute: DEFAULT_MINUTE,
      holidayChoice: DEFAULT_HOLIDAY_CHOICE,
      skipWeekends: false,
      promotionsEnabled: true,
      lastPostedByChannel: {},
      dailyIntro: "",
      monthlyPostCount: 0,
      lastMonthlyHighlightsAt: 0,
    };
  }
  const cfg = workspaceConfig[teamId];
  if (cfg.dailyIntro == null) cfg.dailyIntro = "";
  if (cfg.monthlyPostCount == null) cfg.monthlyPostCount = 0;
  if (cfg.lastMonthlyHighlightsAt == null) cfg.lastMonthlyHighlightsAt = 0;
  return cfg;
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

function isValidTimeZone(timeZone) {
  try {
    Intl.DateTimeFormat("en-US", { timeZone }).format(new Date());
    return true;
  } catch {
    return false;
  }
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

async function slackPostMessage(channel, text, blocks) {
  const token = channel.teamId ? workspaceTokens[channel.teamId]?.access_token : null;
  if (!token) return { ok: false, error: "missing_token" };
  const resp = await fetch("https://slack.com/api/chat.postMessage", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json; charset=utf-8",
    },
    body: JSON.stringify({ channel: channel.id || channel, text, ...(blocks ? { blocks } : {}) }),
  });
  const data = await resp.json().catch(() => ({}));
  if (!data.ok) {
    console.warn("Slack post failed:", data.error || "unknown_error");
    return { ok: false, error: data.error || "unknown_error" };
  }
  return { ok: true };
}

async function slackPostEphemeral(teamId, channel, user, text, blocks) {
  const token = teamId ? workspaceTokens[teamId]?.access_token : null;
  if (!token) return { ok: false, error: "missing_token" };
  const resp = await fetch("https://slack.com/api/chat.postEphemeral", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json; charset=utf-8",
    },
    body: JSON.stringify({ channel, user, text, blocks }),
  });
  const data = await resp.json().catch(() => ({}));
  return data.ok ? { ok: true } : { ok: false, error: data.error || "unknown_error" };
}

async function slackOpenModal(teamId, triggerId, view) {
  const token = teamId ? workspaceTokens[teamId]?.access_token : null;
  if (!token) return { ok: false, error: "missing_token" };
  const resp = await fetch("https://slack.com/api/views.open", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json; charset=utf-8",
    },
    body: JSON.stringify({ trigger_id: triggerId, view }),
  });
  const data = await resp.json().catch(() => ({}));
  return data.ok ? { ok: true } : { ok: false, error: data.error || "unknown_error" };
}

async function slackPublishHome(teamId, userId) {
  const token = teamId ? workspaceTokens[teamId]?.access_token : null;
  if (!token) {
    console.warn(`Slack Home publish skipped: missing token for team ${teamId}`);
    return;
  }
  const mmdd = toMMDD(new Date());
  const todayHits = findByDate(mmdd);
  const todayHoliday = todayHits[0];
  const todayFact =
    todayHoliday && Array.isArray(todayHoliday.funFacts) && todayHoliday.funFacts.length
      ? todayHoliday.funFacts[0]
      : null;
  const view = {
    type: "home",
    blocks: [
      {
        type: "header",
        text: { type: "plain_text", text: "Obscure Holiday Calendar", emoji: true },
      },
      {
        type: "section",
        text: {
          type: "mrkdwn",
          text: "Daily holiday posts, quick facts, and slash commands right inside Slack.",
        },
      },
      ...(todayHoliday
        ? [
            {
              type: "section",
              text: {
                type: "mrkdwn",
                text: `*Today’s holiday:* ${todayHoliday.emoji || ""} ${todayHoliday.name}`,
              },
            },
            ...(todayFact
              ? [
                  {
                    type: "context",
                    elements: [{ type: "mrkdwn", text: `Fun fact: ${todayFact}` }],
                  },
                ]
              : []),
          ]
        : []),
      {
        type: "actions",
        elements: [
          { type: "button", text: { type: "plain_text", text: "Post today’s holiday" }, action_id: "post_today" },
          { type: "button", text: { type: "plain_text", text: "Set up schedule" }, action_id: "setup_modal" },
          { type: "button", text: { type: "plain_text", text: "Upgrade" }, action_id: "upgrade_link" },
        ],
      },
      {
        type: "context",
        elements: [{ type: "mrkdwn", text: "Need help? Use `/ohc-help` anytime." }],
      },
    ],
  };
  const resp = await fetch("https://slack.com/api/views.publish", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json; charset=utf-8",
    },
    body: JSON.stringify({ user_id: userId, view }),
  });
  const data = await resp.json().catch(() => ({}));
  if (!data.ok) {
    console.warn("Slack Home publish failed:", data.error || "unknown_error");
  } else {
    console.log("Slack Home published for user", userId);
  }
}

function buildSetupModal(config, isPremium, metadata) {
  const hourOptions = Array.from({ length: 24 }, (_, i) => ({
    text: { type: "plain_text", text: String(i).padStart(2, "0") },
    value: String(i),
  }));
  const minuteOptions = Array.from({ length: 60 }, (_, i) => ({
    text: { type: "plain_text", text: String(i).padStart(2, "0") },
    value: String(i),
  }));
  return {
    type: "modal",
    callback_id: "setup_modal",
    title: { type: "plain_text", text: "Set up schedule" },
    submit: { type: "plain_text", text: "Save" },
    close: { type: "plain_text", text: "Cancel" },
    private_metadata: JSON.stringify(metadata || {}),
    blocks: [
      {
        type: "input",
        block_id: "channel_block",
        label: { type: "plain_text", text: "Post to channel" },
        element: {
          type: "conversations_select",
          action_id: "channel",
          default_to_current_conversation: true,
          filter: {
            include: ["public", "private"],
            exclude_bot_users: true,
          },
        },
      },
      {
        type: "input",
        block_id: "timezone_block",
        label: { type: "plain_text", text: "Timezone" },
        element: {
          type: "plain_text_input",
          action_id: "timezone",
          initial_value: config.timezone || DEFAULT_TIMEZONE,
          placeholder: { type: "plain_text", text: "America/New_York" },
        },
      },
      {
        type: "input",
        block_id: "hour_block",
        label: { type: "plain_text", text: "Hour (0-23)" },
        element: {
          type: "static_select",
          action_id: "hour",
          options: hourOptions,
          initial_option: hourOptions.find((opt) => opt.value === String(config.hour ?? DEFAULT_HOUR)),
        },
      },
      {
        type: "input",
        block_id: "minute_block",
        label: { type: "plain_text", text: "Minute (0-59)" },
        element: {
          type: "static_select",
          action_id: "minute",
          options: minuteOptions,
          initial_option: minuteOptions.find((opt) => opt.value === String(config.minute ?? DEFAULT_MINUTE)),
        },
      },
      {
        type: "input",
        block_id: "choice_block",
        label: { type: "plain_text", text: "Holiday choice" },
        element: {
          type: "static_select",
          action_id: "holiday_choice",
          options: [
            { text: { type: "plain_text", text: "First holiday" }, value: "0" },
            { text: { type: "plain_text", text: "Second holiday (Premium)" }, value: "1" },
          ],
          initial_option: {
            text: {
              type: "plain_text",
              text: (config.holidayChoice || 0) === 1 ? "Second holiday (Premium)" : "First holiday",
            },
            value: String(config.holidayChoice || 0),
          },
        },
      },
      {
        type: "input",
        block_id: "options_block",
        optional: true,
        label: { type: "plain_text", text: "Options" },
        element: {
          type: "checkboxes",
          action_id: "options",
          options: [
            { text: { type: "plain_text", text: "Skip weekends (Premium)" }, value: "skip_weekends" },
            { text: { type: "plain_text", text: "Allow promotions (Premium)" }, value: "promotions" },
          ],
          initial_options: [
            config.skipWeekends
              ? { text: { type: "plain_text", text: "Skip weekends (Premium)" }, value: "skip_weekends" }
              : null,
            config.promotionsEnabled
              ? { text: { type: "plain_text", text: "Allow promotions (Premium)" }, value: "promotions" }
              : null,
          ].filter(Boolean),
        },
      },
      {
        type: "context",
        elements: [
          {
            type: "mrkdwn",
            text: isPremium
              ? "Premium settings are enabled for this workspace."
              : "Premium settings require an upgrade to take effect.",
          },
        ],
      },
      {
        type: "input",
        block_id: "daily_intro_block",
        optional: true,
        label: { type: "plain_text", text: "Custom daily intro (Premium)" },
        element: {
          type: "plain_text_input",
          action_id: "daily_intro",
          initial_value: config.dailyIntro || "",
          placeholder: { type: "plain_text", text: "Intro line at the top of every daily post. Leave blank to remove." },
          max_length: 200,
        },
      },
      {
        type: "section",
        text: {
          type: "mrkdwn",
          text: "*Free vs Premium*\n• Free: /ohc-today + daily posts (UTC)\n• Premium: /ohc-date, /ohc-search, /ohc-random, /ohc-facts, /ohc-poll, /ohc-tip, /ohc-tomorrow, /ohc-upcoming, /ohc-week + custom schedule + daily intro + monthly recap",
        },
      },
    ],
  };
}

async function resolveChannelId(teamId, rawChannel) {
  if (!rawChannel) return null;
  if (rawChannel.startsWith("<#") && rawChannel.includes("|")) {
    return rawChannel.split("|")[0].replace("<#", "");
  }
  const trimmed = rawChannel.trim();
  if (trimmed.startsWith("C") || trimmed.startsWith("G")) return trimmed;
  const name = trimmed.replace(/^#/, "").toLowerCase();
  const token = teamId ? workspaceTokens[teamId]?.access_token : null;
  if (!token) return null;
  let cursor;
  do {
    const resp = await fetch(
      `https://slack.com/api/conversations.list?types=public_channel&limit=200${cursor ? `&cursor=${cursor}` : ""}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json; charset=utf-8",
        },
      }
    );
    const data = await resp.json();
    if (!data.ok) {
      if (data.error === "missing_scope") {
        console.warn("Slack channel lookup missing scope: add channels:read or use channel ID.");
      }
      return null;
    }
    const match = (data.channels || []).find((c) => c.name === name);
    if (match) return match.id;
    cursor = data.response_metadata?.next_cursor || "";
  } while (cursor);
  return null;
}

async function handleDailyPosts() {
  for (const [teamId, config] of Object.entries(workspaceConfig)) {
    if (!config.channelId) continue;
    if (!workspaceTokens[teamId]?.access_token) continue;
    const tz = config.timezone || DEFAULT_TIMEZONE;
    const parts = getLocalParts(tz);
    if (config.skipWeekends && (parts.weekday === "Sat" || parts.weekday === "Sun")) continue;
    const lastPostedByChannel = config.lastPostedByChannel || {};
    if (lastPostedByChannel[config.channelId] === parts.ymd) continue;
    const scheduledMinute = Number(config.minute ?? 0);
    const scheduledHour = Number(config.hour);
    if (parts.hour !== scheduledHour) continue;
    const minuteDelta = parts.minute - scheduledMinute;
    if (minuteDelta < 0 || minuteDelta > 5) continue;

    const mmdd = `${parts.month}-${parts.day}`;
    const hits = findByDate(mmdd);
    if (!hits.length) continue;
    const choice = Math.min(config.holidayChoice || 0, hits.length - 1);
    const holiday = hits[choice];
    const baseText = formatHoliday(holiday, mmdd);
    const postText =
      isPremiumTeam(teamId) && config.dailyIntro ? `${config.dailyIntro}\n${baseText}` : baseText;
    const postResult = await slackPostMessage({ id: config.channelId, teamId }, postText);
    if (!postResult.ok) {
      console.warn(`Daily post failed for team ${teamId}: ${postResult.error}`);
      continue;
    }
    config.monthlyPostCount = (config.monthlyPostCount || 0) + 1;
    config.lastPostedByChannel = {
      ...(config.lastPostedByChannel || {}),
      [config.channelId]: parts.ymd,
    };
    writeJsonSafe(CONFIG_PATH, workspaceConfig);
  }
}

async function sendMonthlyHighlightsForTeam(teamId, config) {
  if (!workspaceTokens[teamId]?.access_token) return;
  if (!config.channelId) return;
  const postCount = config.monthlyPostCount || 0;
  config.lastMonthlyHighlightsAt = Date.now();
  config.monthlyPostCount = 0;
  writeJsonSafe(CONFIG_PATH, workspaceConfig);

  const now = new Date();
  const monthName = now.toLocaleString("en-US", { month: "long", year: "numeric" });
  const blocks = [
    {
      type: "header",
      text: { type: "plain_text", text: "📊 Monthly Holiday Recap", emoji: true },
    },
    {
      type: "section",
      text: {
        type: "mrkdwn",
        text: [
          `*${monthName}* — here's how the holiday celebrations went:`,
          "",
          `• 📅 *${postCount}* daily holiday post${postCount !== 1 ? "s" : ""} sent this month`,
          `• 🎉 Keep the streak going — tomorrow's holiday is already lined up!`,
        ].join("\n"),
      },
    },
    {
      type: "context",
      elements: [
        {
          type: "mrkdwn",
          text: `Powered by <${SITE_URL || "https://obscureholidaycalendar.com"}|Obscure Holiday Calendar> · Use \`/ohc-upcoming\` to preview what's ahead.`,
        },
      ],
    },
  ];
  await slackPostMessage(
    { id: config.channelId, teamId },
    `📊 Monthly holiday recap — ${monthName}`,
    blocks
  );
}

async function handleMonthlyHighlights() {
  const now = Date.now();
  const TWENTY_EIGHT_DAYS = 28 * 24 * 60 * 60 * 1000;
  for (const [teamId, config] of Object.entries(workspaceConfig)) {
    if (!isPremiumTeam(teamId)) continue;
    if (!config.channelId) continue;
    const lastSent = config.lastMonthlyHighlightsAt || 0;
    if (now - lastSent < TWENTY_EIGHT_DAYS) continue;
    await sendMonthlyHighlightsForTeam(teamId, config).catch((err) =>
      console.warn(`Monthly highlights failed for team ${teamId}:`, err.message)
    );
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
  const timestamp = Number(req.headers["x-slack-request-timestamp"]);
  const signature = req.headers["x-slack-signature"];
  if (!Number.isFinite(timestamp) || !signature) return false;
  const fiveMinutes = 60 * 5;
  const now = Math.floor(Date.now() / 1000);
  if (Math.abs(now - timestamp) > fiveMinutes) return false;
  const sigBase = `v0:${timestamp}:${req.rawBody || ""}`;
  const hmac = crypto.createHmac("sha256", SLACK_SIGNING_SECRET).update(sigBase).digest("hex");
  const computed = `v0=${hmac}`;
  if (computed.length !== signature.length) return false;
  return crypto.timingSafeEqual(Buffer.from(computed), Buffer.from(signature));
}

function checkBasicAuth(req) {
  if (!SLACK_ADMIN_USER || !SLACK_ADMIN_PASS) return false;
  const header = req.headers.authorization || "";
  if (!header.startsWith("Basic ")) return false;
  const decoded = Buffer.from(header.slice(6), "base64").toString("utf8");
  const [user, pass] = decoded.split(":", 2);
  return user === SLACK_ADMIN_USER && pass === SLACK_ADMIN_PASS;
}

function requireAdminAuth(req, res, next) {
  if (SLACK_ADMIN_USER && SLACK_ADMIN_PASS) {
    if (!checkBasicAuth(req)) {
      res.set("WWW-Authenticate", 'Basic realm="Admin"');
      return res.status(401).send("Unauthorized");
    }
    return next();
  }
  const token = req.headers["x-admin-token"];
  if (!SLACK_ADMIN_TOKEN || token !== SLACK_ADMIN_TOKEN) {
    return res.status(403).send("Forbidden");
  }
  return next();
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

app.use(
  "/slack/interactions",
  express.urlencoded({
    extended: false,
    verify: (req, res, buf) => {
      req.rawBody = buf.toString("utf8");
    },
  })
);

app.use(
  "/slack/events",
  express.json({
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
  pruneOauthStateStore();
  const state = crypto.randomBytes(16).toString("hex");
  oauthStateStore.set(state, Date.now() + OAUTH_STATE_TTL_MS);
  const url = new URL("https://slack.com/oauth/v2/authorize");
  url.searchParams.set("client_id", SLACK_CLIENT_ID);
  url.searchParams.set("scope", SLACK_OAUTH_SCOPES);
  url.searchParams.set("redirect_uri", SLACK_REDIRECT_URI);
  url.searchParams.set("state", state);
  return res.redirect(url.toString());
});

app.get("/slack/oauth/callback", async (req, res) => {
  if (!SLACK_CLIENT_ID || !SLACK_CLIENT_SECRET || !SLACK_REDIRECT_URI) {
    return res.status(400).send("Slack OAuth not configured.");
  }
  const code = req.query.code;
  const state = req.query.state;
  if (!code) return res.status(400).send("Missing code.");
  if (!state || !oauthStateStore.has(String(state))) return res.status(400).send("Invalid OAuth state.");
  const expiresAt = oauthStateStore.get(String(state));
  oauthStateStore.delete(String(state));
  if (!expiresAt || Date.now() > expiresAt) return res.status(400).send("Expired OAuth state.");
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
  const { command, text, team_id, user_id, channel_id, trigger_id } = req.body || {};
  const teamId = team_id || "unknown";
  const config = ensureWorkspace(teamId);

  const respond = (message) => res.json({ response_type: "ephemeral", text: message });

  if (!command) return respond("Missing command.");

  const rawCmd = command.replace("/", "");
  const CMD_PREFIX = "ohc-";
  const cmd = rawCmd.startsWith(CMD_PREFIX) ? rawCmd.slice(CMD_PREFIX.length) : rawCmd;
  const isPremium = isPremiumTeam(teamId);

  const HELP_TEXT = {
    today: "/ohc-today [2] — show today's holiday. Add 2 to see the second holiday (Premium).",
    tomorrow: "/ohc-tomorrow [2] — show tomorrow's holiday (Premium). Add 2 for the second holiday.",
    week: "/ohc-week [days] — preview the next N days of holidays, 3-30 (Premium). Default 7.",
    upcoming: "/ohc-upcoming [days] — preview the next N days of holidays, 3-30 (Premium). Default 7.",
    date: "/ohc-date MM-DD [2] — look up the holiday(s) on a specific date (Premium), e.g. /ohc-date 12-25.",
    search: "/ohc-search <query> — search 700+ holidays by name (Premium), e.g. /ohc-search pizza.",
    random: "/ohc-random — get a random holiday from the full calendar (Premium).",
    facts: "/ohc-facts [name or MM-DD] — get fun facts for a holiday (Premium). Defaults to today.",
    poll: "/ohc-poll — post a fun holiday poll to your configured channel (Premium).",
    tip: "/ohc-tip — get an actionable celebration tip for today's holiday (Premium).",
    setup: "/ohc-setup key=value ... — configure your channel, timezone, and daily post time. Run with no arguments to see all options.",
    premium: "/ohc-premium [refresh] — show Premium status for this workspace, or refresh it after subscribing.",
    upgrade: "/ohc-upgrade — get a checkout link to unlock Premium features.",
    manage: "/ohc-manage — open the Stripe billing portal to manage your subscription.",
    invite: "/ohc-invite — get the link to install this app in another workspace.",
    vote: "/ohc-vote — get the link to vote for this app.",
    rate: "/ohc-rate — get the link to leave a review.",
    support: "/ohc-support — get the support/contact link.",
    app: "/ohc-app — get links to the Obscure Holiday Calendar mobile app.",
    schedule: "/ohc-schedule test|status|debug — test a post, check status, or debug your automated daily posts (Premium).",
    help: "/ohc-help — list all available commands.",
  };

  const trimmedText = (text || "").trim();
  if (trimmedText.toLowerCase() === "help" && cmd !== "help") {
    return respond(HELP_TEXT[cmd] || `No help available for /ohc-${cmd}.`);
  }

  // Commands that don't take any arguments: any other input is unrecognized.
  const NO_ARG_COMMANDS = new Set(["manage", "invite", "vote", "rate", "support", "app", "upgrade"]);
  if (NO_ARG_COMMANDS.has(cmd) && trimmedText) {
    return respond(`/ohc-${cmd} doesn't take any arguments. ${HELP_TEXT[cmd] || ""}`);
  }

  if (cmd === "help") {
    if (trigger_id) {
      const blocks = [
        {
          type: "section",
          text: {
            type: "mrkdwn",
            text: [
              "*Holiday bot commands:*",
              "• /ohc-today",
              "• /ohc-today 2 *(Premium)*",
              "• /ohc-tomorrow *(Premium)*",
              "• /ohc-week [days] *(Premium)*",
              "• /ohc-upcoming [days] *(Premium)*",
              "• /ohc-date MM-DD *(Premium)*",
              "• /ohc-search <query> *(Premium)*",
              "• /ohc-random *(Premium)*",
              "• /ohc-facts [name or MM-DD] *(Premium)*",
              "• /ohc-poll *(Premium)* — post a holiday poll",
              "• /ohc-tip *(Premium)* — get a celebration idea",
              "• /ohc-setup",
              "• /ohc-premium [refresh]",
              "• /ohc-upgrade",
              "• /ohc-manage",
              "• /ohc-invite",
              "• /ohc-vote, /ohc-rate",
              "• /ohc-support, /ohc-app",
              "",
              "Tip: add \"help\" after any command for details, e.g. /ohc-today help",
            ].join("\n"),
          },
        },
        {
          type: "actions",
          elements: [
            { type: "button", text: { type: "plain_text", text: "Open setup" }, action_id: "setup_modal" },
            { type: "button", text: { type: "plain_text", text: "Post today" }, action_id: "post_today" },
          ],
        },
      ];
      const sent = await slackPostEphemeral(teamId, channel_id, user_id, "Help menu", blocks);
      if (sent.ok) return res.json({ response_type: "ephemeral", text: "✅ Help sent." });
    }
    return respond(
      [
        "Holiday bot commands:",
        "/ohc-today",
        "/ohc-today 2 *(Premium)*: second holiday",
        "/ohc-tomorrow *(Premium)* add 2 for second holiday",
        "/ohc-week [days] *(Premium)*",
        "/ohc-upcoming [days] *(Premium)*",
        "/ohc-date MM-DD *(Premium)* add 2 for second holiday",
        "/ohc-search <query> *(Premium)*",
        "/ohc-random *(Premium)*",
        "/ohc-facts [name or MM-DD] *(Premium)*",
        "/ohc-poll *(Premium)* — post a fun holiday poll to your channel",
        "/ohc-tip *(Premium)* — get an actionable celebration idea",
        "/ohc-setup key=value ...",
        "/ohc-premium [refresh]",
        "/ohc-upgrade",
        "/ohc-manage",
        "/ohc-invite",
        "/ohc-vote",
        "/ohc-rate",
        "/ohc-support",
        "/ohc-app",
        "",
        "Tip: Use `/ohc-setup` to open the guided setup modal. Add \"help\" after any command for details.",
      ].join("\n")
    );
  }

  if (cmd === "support") return respond(SUPPORT_URL ? `Support: ${SUPPORT_URL}` : "Support link not configured.");
  if (cmd === "app") return respond(APP_URL ? `App: ${APP_URL}` : "App link not configured.");
  if (cmd === "invite") return respond(SLACK_INSTALL_URL ? `Install the Slack bot: ${SLACK_INSTALL_URL}` : "Invite link not configured.");
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
    return respond(
      [
        "✨ *Premium* unlocks the full Obscure Holiday experience:",
        "",
        "• `/ohc-poll` — post fun holiday polls to your channel",
        "• `/ohc-tip` — get actionable celebration ideas",
        "• `/ohc-date`, `/ohc-search`, `/ohc-random`, `/ohc-facts`",
        "• `/ohc-tomorrow`, `/ohc-week`, `/ohc-upcoming`",
        "• Custom schedule: any timezone & post time",
        "• Custom daily intro line on every post",
        "• Monthly highlights recap in your channel",
        "",
        "Use `/ohc-upgrade` to get started.",
      ].join("\n")
    );
  }

  if (cmd === "upgrade") {
    if (!stripeClient || !STRIPE_PRICE_ID_INTRO || !STRIPE_PRICE_ID_STANDARD || !STRIPE_SUCCESS_URL || !STRIPE_CANCEL_URL) {
      return respond("Stripe is not configured.");
    }
    try {
      const session = await createPremiumCheckoutSession({ teamId, userId: user_id });
      return respond(
        [
          "✨ *Upgrade to Premium* — unlock the full holiday experience:",
          "• `/ohc-poll`, `/ohc-tip`, `/ohc-facts`, `/ohc-search`, `/ohc-random`",
          "• Custom schedule, timezone, and daily intro",
          "• Monthly highlights recap for your channel",
          "",
          session.url,
        ].join("\n")
      );
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
    if (!text || text.toLowerCase().includes("help")) {
      if (trigger_id) {
        const open = await slackOpenModal(teamId, trigger_id, buildSetupModal(config, isPremium, { channel_id, user_id }));
        if (open.ok) return respond("Opening setup...");
      }
      const modalHint =
        trigger_id
          ? ""
          : "\nTip: Open the App Home tab and tap “Set up schedule” for the guided setup modal.";
      return respond(
        [
          "Setup options (key=value):",
          "channel=#your-channel (optional; posts to this channel)",
          "timezone=America/New_York",
          "hour=9 (0-23)",
          "minute=30 (0-59)",
          "holiday_choice=1 (0=first, 1=second, premium)",
          "skip_weekends=true|false (premium)",
          "promotions=true|false (premium)",
          "",
          "Note: channel name lookup requires channels:read scope. Channel IDs (C...) always work.",
          "",
          "Example:",
          "/ohc-setup channel=#general timezone=America/New_York hour=6 minute=45 holiday_choice=1 skip_weekends=true",
          "",
          "Template:",
          "timezone= hour= minute= holiday_choice= skip_weekends= promotions=",
          modalHint,
        ].join("\n")
      );
    }
    const args = parseSetupArgs(text || "");
    const errors = [];
    let resolvedChannel = null;

    if (args.channel) {
      resolvedChannel = await resolveChannelId(teamId, args.channel);
      if (!resolvedChannel) {
        errors.push("Channel not found. Use #channel or a valid channel ID (C...).");
      }
    }
    if (args.timezone && !isValidTimeZone(args.timezone)) {
      errors.push("Invalid timezone. Example: America/New_York");
    }
    if (args.hour) {
      const hourVal = Number(args.hour);
      if (!Number.isInteger(hourVal) || hourVal < 0 || hourVal > 23) {
        errors.push("Hour must be an integer from 0 to 23.");
      }
    }
    if (args.minute) {
      const minuteVal = Number(args.minute);
      if (!Number.isInteger(minuteVal) || minuteVal < 0 || minuteVal > 59) {
        errors.push("Minute must be an integer from 0 to 59.");
      }
    }
    if (args.holiday_choice && !["0", "1"].includes(String(args.holiday_choice))) {
      errors.push("holiday_choice must be 0 (first) or 1 (second).");
    }
    if (args.skip_weekends && !["true", "false"].includes(String(args.skip_weekends).toLowerCase())) {
      errors.push("skip_weekends must be true or false.");
    }
    if (args.promotions && !["true", "false"].includes(String(args.promotions).toLowerCase())) {
      errors.push("promotions must be true or false.");
    }
    if (errors.length) {
      return respond(`Setup errors:\n• ${errors.join("\n• ")}`);
    }
    if (args.channel) {
      config.channelId = resolvedChannel || channel_id;
    } else {
      config.channelId = channel_id;
    }
    if (args.timezone && isPremium) config.timezone = args.timezone;
    if (args.hour && isPremium) config.hour = Math.min(Math.max(Number(args.hour), 0), 23);
    if (args.minute && isPremium) config.minute = Math.min(Math.max(Number(args.minute), 0), 59);
    if (args.holiday_choice && isPremium) config.holidayChoice = Number(args.holiday_choice) ? 1 : 0;
    if (args.skip_weekends && isPremium) config.skipWeekends = args.skip_weekends === "true";
    if (args.promotions && isPremium) config.promotionsEnabled = args.promotions === "true";
    writeJsonSafe(CONFIG_PATH, workspaceConfig);
    return respond(
      `Saved. Channel: <#${config.channelId}>, timezone: ${config.timezone}, hour: ${config.hour}, minute: ${config.minute ?? 0}, holiday_choice: ${config.holidayChoice}`
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
    const mainText = formatHoliday(hits[choice], mmdd);
    if (!isPremium && hits.length > 1) {
      return respond(
        `${mainText}\n\n🔓 _${hits.length - 1} more holiday${hits.length > 2 ? "s" : ""} today — unlock all with Premium. Use \`/ohc-upgrade\` to start._`
      );
    }
    return respond(mainText);
  }

  if (cmd === "tomorrow") {
    if (!isPremium) return respond("🔒 */ohc-tomorrow* is a Premium feature — see what's coming up. Use `/ohc-upgrade` to unlock.");
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
    if (!isPremium) return respond("🔒 */ohc-date* is a Premium feature — look up any date's holiday. Use `/ohc-upgrade` to unlock.");
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
    if (!isPremium) return respond("🔒 */ohc-search* is a Premium feature — find any of 700+ holidays by name. Use `/ohc-upgrade` to unlock.");
    if (!text) return respond("Provide a search query.");
    const hits = findByName(text).slice(0, 5);
    if (!hits.length) return respond("No matches found.");
    const lines = hits.map((h) => `• ${h.emoji || ""} ${h.name} — ${holidayUrl(h)}`);
    return respond(lines.join("\n"));
  }

  if (cmd === "random") {
    if (!isPremium) return respond("🔒 */ohc-random* is a Premium feature — discover a surprise holiday anytime. Use `/ohc-upgrade` to unlock.");
    const pick = allHolidays[Math.floor(Math.random() * allHolidays.length)];
    return respond(formatHoliday(pick));
  }

  if (cmd === "facts") {
    if (!isPremium) return respond("🔒 */ohc-facts* is a Premium feature — get fun facts for any holiday. Use `/ohc-upgrade` to unlock.");
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

  if (cmd === "poll") {
    if (!isPremium) return respond("\ud83d\udd12 */ohc-poll* is a Premium feature \u2014 post fun holiday polls to your channel. Use `/ohc-upgrade` to unlock.");
    const mmdd = toMMDD(new Date());
    const hits = findByDate(mmdd);
    if (!hits.length) return respond("No holiday found for today.");
    const holiday = hits[Math.min(config.holidayChoice || 0, hits.length - 1)];
    const pollTemplates = [
      `Are you celebrating ${holiday.emoji || ""} *${holiday.name}* today?`,
      `It's ${holiday.emoji || ""} *${holiday.name}* \u2014 are you in?`,
      `Did you know today is ${holiday.emoji || ""} *${holiday.name}*? Will you mark it?`,
      `${holiday.emoji || ""} *${holiday.name}* is today \u2014 are you a fan?`,
      `How are you marking ${holiday.emoji || ""} *${holiday.name}* today?`,
    ];
    const question = pollTemplates[Math.floor(Math.random() * pollTemplates.length)];
    const targetChannel = config.channelId || channel_id;
    if (!targetChannel) return respond("No channel configured. Run `/ohc-setup` first.");
    const blocks = [
      {
        type: "section",
        text: { type: "mrkdwn", text: `\ud83d\udcca *Holiday Poll*\n${question}` },
      },
      {
        type: "actions",
        elements: [
          {
            type: "button",
            text: { type: "plain_text", text: "\u2705 Yes!" },
            action_id: "poll_vote_yes",
            value: holiday.name,
          },
          {
            type: "button",
            text: { type: "plain_text", text: "\u274c Nope" },
            action_id: "poll_vote_no",
            value: holiday.name,
          },
        ],
      },
      {
        type: "context",
        elements: [
          {
            type: "mrkdwn",
            text: `Powered by <${SITE_URL || "https://obscureholidaycalendar.com"}|Obscure Holiday Calendar>`,
          },
        ],
      },
    ];
    const postResult = await slackPostMessage({ id: targetChannel, teamId }, `\ud83d\udcca ${question}`, blocks);
    if (!postResult.ok) return respond(`Could not post poll: ${postResult.error}`);
    return respond(`\u2705 Poll posted to <#${targetChannel}>!`);
  }

  if (cmd === "tip") {
    if (!isPremium) return respond("\ud83d\udd12 */ohc-tip* is a Premium feature \u2014 get fun actionable celebration ideas for any holiday. Use `/ohc-upgrade` to unlock.");
    const mmdd = toMMDD(new Date());
    const hits = findByDate(mmdd);
    if (!hits.length) return respond("No holiday found for today.");
    const holiday = hits[Math.min(config.holidayChoice || 0, hits.length - 1)];
    const desc = (holiday.description || "").toLowerCase();
    let tips;
    if (desc.includes("food") || desc.includes("eat") || desc.includes("cook") || desc.includes("bake") || desc.includes("drink")) {
      tips = [
        `Try making a ${holiday.name}-themed dish and share a photo in the channel!`,
        `Look up a recipe inspired by ${holiday.name} \u2014 bonus points for sharing with coworkers.`,
        `Host a mini taste test in honor of ${holiday.name}. Everyone brings something!`,
      ];
    } else if (desc.includes("animal") || desc.includes("pet") || desc.includes("dog") || desc.includes("cat")) {
      tips = [
        `Give your pet some extra playtime to mark ${holiday.name}.`,
        `Share a photo of your pet in the channel in honor of ${holiday.name}!`,
        `Consider donating to a local animal shelter for ${holiday.name}.`,
      ];
    } else if (desc.includes("book") || desc.includes("read") || desc.includes("story") || desc.includes("literature")) {
      tips = [
        `Pick up a book tied to the theme of ${holiday.name} and share what you chose.`,
        `Share your current read in the channel to mark ${holiday.name}.`,
        `Ask the team: what book best captures the spirit of ${holiday.name}?`,
      ];
    } else if (desc.includes("music") || desc.includes("song") || desc.includes("sing") || desc.includes("dance")) {
      tips = [
        `Share a playlist that matches the vibe of ${holiday.name}.`,
        `Drop your favorite track in honor of ${holiday.name} \u2014 see who vibes with it.`,
        `Host a 5-minute music moment: everyone shares one song for ${holiday.name}.`,
      ];
    } else if (desc.includes("science") || desc.includes("space") || desc.includes("math") || desc.includes("tech")) {
      tips = [
        `Share a cool fact or article to celebrate ${holiday.name}.`,
        `Challenge the team: who can share the most mind-blowing thing related to ${holiday.name}?`,
        `Take 5 minutes to look something up in the spirit of ${holiday.name}.`,
      ];
    } else if (desc.includes("nature") || desc.includes("outdoor") || desc.includes("plant") || desc.includes("garden")) {
      tips = [
        `Take a short walk outside to celebrate ${holiday.name}.`,
        `Share a nature photo to mark ${holiday.name}.`,
        `Plant or water something in honor of ${holiday.name}.`,
      ];
    } else {
      tips = [
        `Share something about ${holiday.name} with your team today.`,
        `Challenge someone to explain ${holiday.name} in one sentence.`,
        `Take 5 minutes to learn something new about ${holiday.name}.`,
        `Post an emoji that captures ${holiday.name} \u2014 see if anyone can guess it.`,
      ];
    }
    const tip = tips[Math.floor(Math.random() * tips.length)];
    return respond(
      `\ud83d\udca1 *${holiday.emoji || ""} ${holiday.name} \u2014 Celebration Tip*\n\n${tip}`
    );
  }

  if (cmd === "week" || cmd === "upcoming") {
    if (!isPremium) return respond("🔒 */ohc-week* is a Premium feature — preview the full week of holidays ahead. Use `/ohc-upgrade` to unlock.");
    if (trimmedText && Number.isNaN(Number(trimmedText))) {
      return respond(`Invalid input. ${HELP_TEXT[cmd]}`);
    }
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

  if (cmd === "schedule") {
    if (!isPremium) return respond("🔒 */ohc-schedule* is a Premium feature — test and debug your automated daily posts. Use `/ohc-upgrade` to unlock.");
    const lower = (text || "").toLowerCase();
    if (lower.includes("status")) {
      const parts = getLocalParts(config.timezone || DEFAULT_TIMEZONE);
      const hasToken = Boolean(workspaceTokens[teamId]?.access_token);
      const lastPosted =
        (config.lastPostedByChannel && config.lastPostedByChannel[config.channelId]) ||
        config.lastPostedDate ||
        "never";
      return respond(
        [
          `Channel: ${config.channelId ? `<#${config.channelId}>` : "not set"}`,
          `Timezone: ${config.timezone || DEFAULT_TIMEZONE}`,
          `Scheduled: ${String(config.hour).padStart(2, "0")}:${String(config.minute ?? 0).padStart(2, "0")}`,
          `Now: ${parts.year}-${parts.month}-${parts.day} ${String(parts.hour).padStart(2, "0")}:${String(parts.minute).padStart(2, "0")} (${parts.weekday})`,
          `Last posted: ${lastPosted}`,
          `Token: ${hasToken ? "ok" : "missing"}`,
        ].join("\n")
      );
    }
    if (lower.includes("debug")) {
      const parts = getLocalParts(config.timezone || DEFAULT_TIMEZONE);
      const hasToken = Boolean(workspaceTokens[teamId]?.access_token);
      const reasons = [];
      if (!config.channelId) reasons.push("no channel set");
      if (!hasToken) reasons.push("missing token");
      if (config.skipWeekends && (parts.weekday === "Sat" || parts.weekday === "Sun")) {
        reasons.push("skip weekends enabled");
      }
      const lastPosted =
        (config.lastPostedByChannel && config.lastPostedByChannel[config.channelId]) ||
        config.lastPostedDate ||
        null;
      if (lastPosted === parts.ymd) reasons.push("already posted today (channel)");
      const scheduledHour = Number(config.hour);
      const scheduledMinute = Number(config.minute ?? 0);
      if (parts.hour !== scheduledHour) reasons.push(`hour mismatch (now ${parts.hour})`);
      const minuteDelta = parts.minute - scheduledMinute;
      if (minuteDelta < 0 || minuteDelta > 5) {
        reasons.push(`minute outside window (now ${parts.minute}, scheduled ${scheduledMinute})`);
      }
      return respond(
        [
          `Channel: ${config.channelId ? `<#${config.channelId}>` : "not set"}`,
          `Timezone: ${config.timezone || DEFAULT_TIMEZONE}`,
          `Scheduled: ${String(config.hour).padStart(2, "0")}:${String(config.minute ?? 0).padStart(2, "0")}`,
          `Now: ${parts.year}-${parts.month}-${parts.day} ${String(parts.hour).padStart(2, "0")}:${String(parts.minute).padStart(2, "0")} (${parts.weekday})`,
          `Last posted: ${lastPosted || "never"}`,
          `Token: ${hasToken ? "ok" : "missing"}`,
          reasons.length ? `Blocked: ${reasons.join(", ")}` : "Eligible: would post now",
        ].join("\n")
      );
    }
    if (!lower.includes("test")) {
      return respond("Use `/ohc-schedule test` to post today's holiday right now, `/ohc-schedule status`, or `/ohc-schedule debug`.");
    }
    if (!config.channelId) {
      return respond("No channel is configured. Run /ohc-setup first.");
    }
    const mmdd = toMMDD(new Date());
    const hits = findByDate(mmdd);
    if (!hits.length) return respond("No holiday found for today.");
    const choice = Math.min(config.holidayChoice || 0, hits.length - 1);
    const holiday = hits[choice];
    const textOut = formatHoliday(holiday, mmdd);
    const postResult = await slackPostMessage({ id: config.channelId, teamId }, textOut);
    if (!postResult.ok) {
      if (postResult.error === "missing_token") {
        return respond("Missing Slack token. Reinstall the app via /slack/install and try again.");
      }
      return respond(`Unable to send test post: ${postResult.error}`);
    }
    return respond("✅ Test post sent.");
  }

  return respond(`Unknown command: ${cmd}`);
});

app.post("/slack/interactions", async (req, res) => {
  if (!verifySlackSignature(req)) return res.status(401).send("Invalid signature");
  let payload = null;
  try {
    payload = req.body?.payload ? JSON.parse(req.body.payload) : null;
  } catch {
    return res.status(400).send("Invalid payload");
  }
  if (!payload) return res.status(400).send("Missing payload");

  if (payload.type === "block_actions") {
    res.json({ ok: true });
    const teamId = payload.team?.id;
    const userId = payload.user?.id;
    const triggerId = payload.trigger_id;
    const actionId = payload.actions?.[0]?.action_id;
    (async () => {
      if (actionId === "setup_modal") {
        const config = ensureWorkspace(teamId);
        const isPremium = isPremiumTeam(teamId);
        await slackOpenModal(teamId, triggerId, buildSetupModal(config, isPremium, { channel_id: null, user_id: userId }));
      }
      if (actionId === "post_today") {
        const mmdd = toMMDD(new Date());
        const hits = findByDate(mmdd);
        if (hits.length) {
          const holiday = hits[0];
          await slackPostMessage({ id: userId, teamId }, formatHoliday(holiday, mmdd));
        }
      }
      if (actionId === "upgrade_link") {
        if (!stripeClient || !STRIPE_PRICE_ID_INTRO || !STRIPE_PRICE_ID_STANDARD || !STRIPE_SUCCESS_URL || !STRIPE_CANCEL_URL) {
          await slackPostMessage({ id: userId, teamId }, "Stripe is not configured.");
          return;
        }
        try {
          const session = await createPremiumCheckoutSession({ teamId, userId });
          await slackPostMessage(
            { id: userId, teamId },
            [
              "✨ *Upgrade to Premium* — unlock the full holiday experience:",
              "• `/ohc-poll`, `/ohc-tip`, `/ohc-facts`, `/ohc-search`, `/ohc-random`",
              "• Custom schedule, timezone, and daily intro",
              "• Monthly highlights recap for your channel",
              "",
              session.url,
            ].join("\n")
          );
        } catch (e) {
          await slackPostMessage({ id: userId, teamId }, "Unable to create checkout session right now.");
        }
      }
      if (actionId === "poll_vote_yes") {
        const holidayName = payload.actions?.[0]?.value || "today's holiday";
        await slackPostEphemeral(teamId, payload.channel?.id, userId, `✅ You're celebrating ${holidayName}! 🎉`);
      }
      if (actionId === "poll_vote_no") {
        const holidayName = payload.actions?.[0]?.value || "today's holiday";
        await slackPostEphemeral(teamId, payload.channel?.id, userId, `Maybe next time! Check out what ${holidayName} is all about.`);
      }
    })().catch((err) => {
      console.warn("Slack interaction action failed:", err.message);
    });
    return;
  }

  if (payload.type === "view_submission" && payload.view?.callback_id === "setup_modal") {
    const teamId = payload.team?.id;
    const userId = payload.user?.id;
    const state = payload.view?.state?.values || {};
    const config = ensureWorkspace(teamId);
    const isPremium = isPremiumTeam(teamId);
    const channelId = state.channel_block?.channel?.selected_conversation || null;
    const timezone = state.timezone_block?.timezone?.value;
    const hour = state.hour_block?.hour?.selected_option?.value;
    const minute = state.minute_block?.minute?.selected_option?.value;
    const choice = state.choice_block?.holiday_choice?.selected_option?.value;
    const options = state.options_block?.options?.selected_options?.map((opt) => opt.value) || [];
    const dailyIntroRaw = state.daily_intro_block?.daily_intro?.value ?? "";

    const errors = {};
    if (timezone && !isValidTimeZone(timezone)) errors.timezone_block = "Invalid timezone.";
    if (hour && (Number(hour) < 0 || Number(hour) > 23)) errors.hour_block = "Hour must be 0-23.";
    if (minute && (Number(minute) < 0 || Number(minute) > 59)) errors.minute_block = "Minute must be 0-59.";
    if (Object.keys(errors).length) {
      return res.json({ response_action: "errors", errors });
    }

    if (channelId) config.channelId = channelId;
    if (timezone && isPremium) config.timezone = timezone;
    if (hour && isPremium) config.hour = Number(hour);
    if (minute && isPremium) config.minute = Number(minute);
    if (choice && isPremium) config.holidayChoice = Number(choice);
    if (isPremium) {
      config.skipWeekends = options.includes("skip_weekends");
      config.promotionsEnabled = options.includes("promotions");
      config.dailyIntro = dailyIntroRaw.trim().slice(0, 200);
    }
    writeJsonSafe(CONFIG_PATH, workspaceConfig);
    res.json({});
    if (channelId && userId) {
      slackPostEphemeral(teamId, channelId, userId, "✅ Schedule saved. You can update anytime with /ohc-setup.")
        .catch((err) => console.warn("Slack setup confirmation failed:", err.message));
    }
    return;
  }

  return res.json({ ok: true });
});

app.post("/slack/events", async (req, res) => {
  if (!verifySlackSignature(req)) return res.status(401).send("Invalid signature");
  const payload = req.body || {};
  console.log("Slack events payload type:", payload.type);
  if (payload.type === "url_verification") {
    return res.json({ challenge: payload.challenge });
  }
  if (payload.type === "event_callback") {
    res.json({ ok: true });
    const event = payload.event;
    (async () => {
      console.log("Slack event received:", event?.type);
      if (event?.type === "app_uninstalled") {
        const teamId = payload.team_id;
        if (teamId) {
          delete workspaceTokens[teamId];
          delete workspaceConfig[teamId];
          delete premiumAllowlist[teamId];
          writeJsonSafe(WORKSPACE_TOKENS_PATH, workspaceTokens);
          writeJsonSafe(CONFIG_PATH, workspaceConfig);
          writeJsonSafe(PREMIUM_PATH, premiumAllowlist);
          console.log(`Slack app uninstalled for team ${teamId}; cleaned stored workspace data.`);
        }
        return;
      }
      if (event?.type === "app_home_opened") {
        const teamId = event.team_id || payload.team_id;
        const userId = event.user;
        console.log("App Home open for team", teamId, "user", userId);
        await slackPublishHome(teamId, userId);
        const config = ensureWorkspace(teamId);
        config.welcomedUsers = config.welcomedUsers || {};
        if (!config.welcomedUsers[userId]) {
          config.welcomedUsers[userId] = true;
          writeJsonSafe(CONFIG_PATH, workspaceConfig);
          await slackPostMessage(
            { id: userId, teamId },
            [
              `\ud83d\udc4b *Welcome to Obscure Holiday Calendar!*`,
              "",
              "Here's how to get started:",
              "1\ufe0f\u20e3 Run `/ohc-setup` to pick a channel and post time",
              "2\ufe0f\u20e3 Run `/ohc-today` to see what's happening right now",
              "3\ufe0f\u20e3 Run `/ohc-upgrade` to unlock Premium features",
              "",
              "\ud83d\udca1 Tip: Open the App Home tab for quick controls.",
            ].join("\n")
          );
        }
      }
    })().catch((err) => {
      console.warn("Slack event handling failed:", err.message);
    });
    return;
  }
  res.json({ ok: true });
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

app.post("/run-schedule", requireAdminAuth, async (req, res) => {
  try {
    await handleDailyPosts();
    return res.json({ ok: true });
  } catch (err) {
    console.warn("Manual schedule run failed:", err.message);
    return res.status(500).json({ ok: false, error: "schedule_failed" });
  }
});

app.get("/admin/installs", requireAdminAuth, (req, res) => {
  const installs = Object.entries(workspaceTokens).map(([teamId, data]) => ({
    team_id: teamId,
    team_name: data.team_name || "",
    bot_user_id: data.bot_user_id || "",
  }));
  return res.json({
    count: installs.length,
    installs,
  });
});

app.get("/admin/installs.html", requireAdminAuth, (req, res) => {
  const pagePath = path.resolve(__dirname, "admin-installs.html");
  res.sendFile(pagePath);
});

app.listen(PORT, async () => {
  if (stripeClient) await syncPremiumFromStripe();
  setInterval(pruneOauthStateStore, 60 * 1000);
  setInterval(handleDailyPosts, 60 * 1000);
  setInterval(handleMonthlyHighlights, 6 * 60 * 60 * 1000);
  console.log(`${SLACK_APP_NAME} Slack bot running on ${PORT}`);
});
