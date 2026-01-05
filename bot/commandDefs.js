import { ApplicationCommandOptionType } from "discord.js";

export const commandDefs = [
  {
    name: "today",
    description: "Show today’s holiday",
    options: [
      {
        name: "holiday_choice",
        description: "Premium: choose Holiday #1 or #2 for today",
        type: ApplicationCommandOptionType.Integer,
        required: false,
        choices: [
          { name: "Holiday #1 (default)", value: 0 },
          { name: "Holiday #2", value: 1 },
        ],
      },
    ],
  },
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
  { name: "slack", description: "Get the Slack bot link" },
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
        description: "Premium: choose which of the two holidays to auto-post",
        type: ApplicationCommandOptionType.Integer,
        required: false,
        choices: [
          { name: "Holiday #1 (top result)", value: 0 },
          { name: "Holiday #2 (second result)", value: 1 },
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
        name: "promotions",
        description: "Enable optional vote/review prompts (default on)",
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
    description: "Show a 7-day digest",
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
    description: "See tomorrow’s holiday",
  },
  {
    name: "upcoming",
    description: "See upcoming holidays",
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
