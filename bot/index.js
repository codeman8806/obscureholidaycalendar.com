import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import {
  Client,
  GatewayIntentBits,
  EmbedBuilder,
  ActivityType,
  ApplicationCommandOptionType,
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
const HOLIDAYS_PATH = path.resolve(__dirname, "..", "holidays.json");
const SITE_BASE = "https://www.obscureholidaycalendar.com/holiday";

function loadHolidays() {
  const raw = fs.readFileSync(HOLIDAYS_PATH, "utf8");
  const data = JSON.parse(raw);
  return data.holidays || {};
}

const holidaysByDate = loadHolidays();
const allHolidays = Object.values(holidaysByDate).flat();

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

function buildEmbed(h) {
  const name = h.name || "Holiday";
  const emoji = h.emoji || "";
  const date = h.date || "??-??";
  const desc = (h.description || "").slice(0, 500);
  const facts = Array.isArray(h.funFacts) ? h.funFacts.slice(0, 3) : [];
  const slug = h.slug || slugify(name);
  const url = `${SITE_BASE}/${slug}/`;

  const embed = new EmbedBuilder()
    .setTitle(`${emoji ? emoji + " " : ""}${name}`)
    .setURL(url)
    .setDescription(desc || "Learn more on the site.")
    .addFields([{ name: "Date", value: prettyDate(date), inline: true }])
    .setColor(0x1c96f3);

  if (facts.length) {
    embed.addFields([{ name: "Fun facts", value: facts.map((f) => `• ${f}`).join("\n") }]);
  }

  return embed;
}

async function handleToday(interaction) {
  const now = new Date();
  const mmdd = `${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  const hits = findByDate(mmdd);
  if (!hits.length) return interaction.reply({ content: "No holiday found for today.", ephemeral: true });
  return interaction.reply({ embeds: [buildEmbed(hits[0])] });
}

async function handleDate(interaction) {
  const input = interaction.options.getString("date", true);
  const parsed = parseDate(input);
  if (!parsed) return interaction.reply({ content: "Please provide a date as MM-DD or MM/DD (example: 07-04).", ephemeral: true });
  const hits = findByDate(parsed);
  if (!hits.length) return interaction.reply({ content: `No holidays found on ${parsed}.`, ephemeral: true });
  return interaction.reply({ embeds: [buildEmbed(hits[0])] });
}

async function handleSearch(interaction) {
  const query = interaction.options.getString("query", true);
  const matches = findByName(query);
  if (!matches.length) return interaction.reply({ content: "No match. Try a simpler phrase.", ephemeral: true });
  return interaction.reply({ embeds: matches.map(buildEmbed).slice(0, 3) });
}

async function handleRandom(interaction) {
  return interaction.reply({ embeds: [buildEmbed(pickRandom())] });
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
  return interaction.reply({ embeds: [embed] });
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

function scheduleDailyPost() {
  if (!DAILY_CHANNEL_ID) {
    console.log("No DAILY_CHANNEL_ID set; skipping auto-post.");
    return;
  }
  const now = new Date();
  const next = new Date(now);
  next.setHours(0, 5, 0, 0); // 00:05 local time to avoid rate spikes
  if (next <= now) next.setDate(next.getDate() + 1);
  const delay = next.getTime() - now.getTime();
  setTimeout(() => {
    postToday().catch((e) => console.error("Daily post failed:", e));
    setInterval(() => {
      postToday().catch((e) => console.error("Daily post failed:", e));
    }, 24 * 60 * 60 * 1000);
  }, delay);
  console.log(`Scheduled daily post in ${Math.round(delay / 1000 / 60)} minutes`);
}

async function postToday() {
  if (!DAILY_CHANNEL_ID) return;
  const channel = await client.channels.fetch(DAILY_CHANNEL_ID);
  if (!channel || !channel.isTextBased()) return;

  const now = new Date();
  const mmdd = `${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  const hits = findByDate(mmdd);
  if (!hits.length) {
    return channel.send("No holiday found for today. Check back tomorrow!");
  }

  const top = hits.slice(0, 2).map((h) => h.name).join(" and ");
  const embed = buildEmbed(hits[0]);
  await channel.send({
    content: `🎉 Today’s holidays: ${top}`,
    embeds: [embed],
  });
}

client.login(TOKEN);
