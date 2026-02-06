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
    description: "Premium: show holidays on a specific date",
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
    description: "Premium: search for a holiday by name/keywords",
    options: [
      {
        name: "query",
        description: "e.g., bacon, pizza, cat",
        type: ApplicationCommandOptionType.String,
        required: true,
      },
    ],
  },
  { name: "random", description: "Premium: get a random holiday" },
  { name: "vote", description: "Vote for the bot on top.gg" },
  { name: "rate", description: "Leave a review on top.gg" },
  {
    name: "facts",
    description: "Premium: get fun facts for a holiday",
    options: [
      {
        name: "name_or_date",
        description: "Name or MM-DD (leave empty for today)",
        type: ApplicationCommandOptionType.String,
        required: false,
      },
    ],
  },
  {
    name: "fact",
    description: "Get one fun fact (free)",
    options: [
      {
        name: "name_or_date",
        description: "Name or MM-DD (leave empty for today)",
        type: ApplicationCommandOptionType.String,
        required: false,
      },
    ],
  },
  { name: "streak", description: "Show the server’s current streak" },
  { name: "invite", description: "Get the bot invite link" },
  { name: "share", description: "Share the bot invite link" },
  { name: "support", description: "Get help/landing page link" },
  { name: "app", description: "Get the mobile app links" },
  { name: "slack", description: "Get the Slack bot link" },
  {
    name: "help",
    description: "Show help",
    options: [
      {
        name: "level",
        description: "brief or full",
        type: ApplicationCommandOptionType.String,
        required: false,
        choices: [
          { name: "Brief", value: "brief" },
          { name: "Full", value: "full" },
        ],
      },
    ],
  },
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
      {
        name: "filter_no_food",
        description: "Premium: exclude food holidays",
        type: ApplicationCommandOptionType.Boolean,
        required: false,
      },
      {
        name: "filter_no_religious",
        description: "Premium: exclude religious holidays",
        type: ApplicationCommandOptionType.Boolean,
        required: false,
      },
      {
        name: "filter_only_weird",
        description: "Premium: only weird/absurd holidays",
        type: ApplicationCommandOptionType.Boolean,
        required: false,
      },
      {
        name: "filter_only_international",
        description: "Premium: only international holidays",
        type: ApplicationCommandOptionType.Boolean,
        required: false,
      },
      {
        name: "filter_safe_mode",
        description: "Premium: filter out sensitive themes",
        type: ApplicationCommandOptionType.Boolean,
        required: false,
      },
      {
        name: "filter_blacklist",
        description: "Premium: comma-separated keywords to exclude",
        type: ApplicationCommandOptionType.String,
        required: false,
      },
      {
        name: "surprise_days",
        description: "Premium: enable wildcard surprise days (1–2 per month)",
        type: ApplicationCommandOptionType.Boolean,
        required: false,
      },
      {
        name: "tone",
        description: "Premium: daily mood/tone for posts",
        type: ApplicationCommandOptionType.String,
        required: false,
        choices: [
          { name: "Wholesome", value: "wholesome" },
          { name: "Silly", value: "silly" },
          { name: "Nerdy", value: "nerdy" },
          { name: "Historical", value: "historical" },
          { name: "Global", value: "global" },
        ],
      },
      {
        name: "streak_role",
        description: "Premium: role to grant when streak goal is reached",
        type: ApplicationCommandOptionType.Role,
        required: false,
      },
      {
        name: "streak_goal",
        description: "Premium: streak days required for the streak role",
        type: ApplicationCommandOptionType.Integer,
        required: false,
      },
    ],
  },
  {
    name: "categories",
    description: "Show available holiday categories and current server settings",
  },
  {
    name: "setcategories",
    description: "Premium: set allowed holiday categories",
    options: [
      {
        name: "categories",
        description: "Comma-separated list (or 'all' for no filter)",
        type: ApplicationCommandOptionType.String,
        required: true,
        autocomplete: true,
      },
    ],
  },
  {
    name: "excludesensitive",
    description: "Premium: toggle sensitive holiday filtering",
    options: [
      {
        name: "enabled",
        description: "true to exclude, false to allow (omit to toggle)",
        type: ApplicationCommandOptionType.Boolean,
        required: false,
      },
    ],
  },
  {
    name: "trial",
    description: "Admin: view trial status or start the 7-day trial",
  },
  {
    name: "block-holiday",
    description: "Admin: block a holiday by id or name",
    options: [
      {
        name: "id_or_name",
        description: "Holiday id, slug, or name",
        type: ApplicationCommandOptionType.String,
        required: true,
      },
    ],
  },
  {
    name: "unblock-holiday",
    description: "Admin: unblock a holiday by id or name",
    options: [
      {
        name: "id_or_name",
        description: "Holiday id, slug, or name",
        type: ApplicationCommandOptionType.String,
        required: true,
      },
    ],
  },
  {
    name: "force-holiday",
    description: "Admin: force-include a holiday by id or name",
    options: [
      {
        name: "id_or_name",
        description: "Holiday id, slug, or name",
        type: ApplicationCommandOptionType.String,
        required: true,
      },
    ],
  },
  {
    name: "unforce-holiday",
    description: "Admin: remove forced holiday by id or name",
    options: [
      {
        name: "id_or_name",
        description: "Holiday id, slug, or name",
        type: ApplicationCommandOptionType.String,
        required: true,
      },
    ],
  },
  {
    name: "overrides",
    description: "Admin: show blocked/forced holiday overrides",
  },
  {
    name: "why",
    description: "Admin: explain why a holiday is filtered",
    options: [
      {
        name: "id_or_name",
        description: "Holiday id, slug, or name",
        type: ApplicationCommandOptionType.String,
        required: true,
      },
    ],
  },
  {
    name: "admin-stats",
    description: "Owner: growth/upsell stats",
  },
  {
    name: "admin-funnel",
    description: "Owner: conversion funnel summary",
  },
  {
    name: "postnowall",
    description: "Owner: post today’s holidays now (all servers)",
  },
  {
    name: "premium",
    description: "See premium status",
  },
  {
    name: "analytics",
    description: "Premium: view engagement analytics for this server",
  },
  {
    name: "lore",
    description: "Premium: manage server lore (anniversary, keywords, mini-holidays)",
    options: [
      {
        name: "action",
        description: "What do you want to do?",
        type: ApplicationCommandOptionType.String,
        required: true,
        choices: [
          { name: "Set anniversary (MM-DD)", value: "set_anniversary" },
          { name: "Add inside joke keyword", value: "add_keyword" },
          { name: "Remove inside joke keyword", value: "remove_keyword" },
          { name: "Add custom mini-holiday", value: "add_custom" },
          { name: "Remove custom mini-holiday", value: "remove_custom" },
          { name: "List lore", value: "list" },
        ],
      },
      {
        name: "value",
        description: "Keyword or holiday name",
        type: ApplicationCommandOptionType.String,
        required: false,
      },
      {
        name: "date",
        description: "MM-DD (for anniversary or custom holiday)",
        type: ApplicationCommandOptionType.String,
        required: false,
      },
      {
        name: "description",
        description: "Short description (for custom holiday)",
        type: ApplicationCommandOptionType.String,
        required: false,
      },
    ],
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
    description: "Premium: see tomorrow’s holiday",
  },
  {
    name: "upcoming",
    description: "Premium: see upcoming holidays",
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
];
