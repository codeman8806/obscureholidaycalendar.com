"""
Hand-written content for each monthly guide page, consumed by build_month_guide.py.
Each entry's blurb is original commentary grounded in holidays.json's description/funFacts,
not copied from it or from the live /holiday/{slug}/ page.
"""

DECEMBER = {
    "month_num": 12,
    "month_name": "December",
    "url_slug": "december",
    "title": "The Complete Guide to December's Obscure Holidays | Obscure Holiday Calendar",
    "description": (
        "A complete, day-by-day guide to all 64 obscure and offbeat holidays in December — "
        "from Antarctica Day to No Interruptions Day — with history, context, and links to the "
        "full write-up for each one."
    ),
    "h1": "The Complete Guide to December's Obscure Holidays",
    "date_published": "2026-02-10",
    "date_modified": "2026-07-28",
    "intro_html": """    <p>December already has Christmas, Hanukkah, and New Year's Eve carrying the headline. Underneath
    that, the month runs a full second calendar: 64 additional observances, one or two on nearly every
    single day, covering everything from a 1959 international treaty (Antarctica Day) to a Seinfeld bit
    that turned into a real tradition (Festivus).</p>

    <p>This guide walks through all 64, day by day, with a bit of history or context for each one and a
    link to the full write-up &mdash; complete fun facts, ways to celebrate, and sourcing &mdash; on its own page.</p>""",
    "why_html": """    <p>Less a single theme than three different calendars stacked on top of each other. A good chunk are
    old folk and religious traditions that predate the modern calendar entirely &mdash; Saint Nicholas Day,
    Krampusnacht, caroling, gingerbread houses. Another chunk are genuine government or international
    observances that happen to fall in December for reasons of their own: Bill of Rights Day, Human Rights
    Day, International Civil Aviation Day, the winter solstice itself. And a growing share are recent,
    openly invented internet-era holidays &mdash; Barbie and Barney Backlash Day, Answer the Telephone Like
    Buddy the Elf Day, Pretend to Be a Time Traveler Day &mdash; that exist purely because December is when
    people are already in the mood to celebrate something.</p>""",
    "how_to_use_html": """    <p>Holidays are grouped by date below. Each entry gets a short original write-up &mdash; not a repeat
    of the fact sheet &mdash; plus a link to the full holiday page if you want the deeper dive: complete fun
    facts, ways to celebrate, and sourcing.</p>""",
    "about_html": """    <p>This guide is part of the Obscure Holiday Calendar project &mdash; the same database that powers
    the iOS and Android apps and the individual holiday pages on this site. It exists to give a single,
    readable overview of an entire month at once, instead of requiring 64 separate page visits.</p>""",
    "faq": [
        (
            "How many obscure holidays are there in December?",
            "64 in 2026, spread across all 31 days, with at least one falling on every date and two on most days.",
        ),
        (
            "What's the strangest holiday in December?",
            "Hard to pick just one, but Barbie and Barney Backlash Day (Dec 16) and Answer the Telephone Like "
            "Buddy the Elf Day (Dec 18) are strong contenders — both are purely comedic and invented well "
            "within recent memory.",
        ),
        (
            "Are any December holidays official government or international observances?",
            "A few: Bill of Rights Day (established by President Franklin D. Roosevelt in 1941), Human Rights "
            "Day (adopted by the UN General Assembly in 1948), and International Civil Aviation Day (backed by "
            "the UN agency ICAO) are all tied to real institutions, unlike most of the informally invented days "
            "on this list.",
        ),
        (
            "Where can I find the full history and fun facts for each holiday?",
            "Every holiday name in this guide links to its own dedicated page with a longer write-up, sourced "
            "fun facts, and ideas for how to celebrate.",
        ),
    ],
    "entries": [
        ("antarctica-day",
         "Antarctica Day marks the 1959 signing of the Antarctic Treaty, the rare international agreement that "
         "turned an entire continent into a demilitarized zone reserved for science. Twelve countries signed on, "
         "and more than sixty years later Antarctica is still the only continent with no permanent residents and "
         "no owner &mdash; just researchers, penguins, and a lot of ice. <a href=\"/holiday/antarctica-day/\">Full holiday page &rarr;</a>"),
        ("eat-a-red-apple-day",
         "A holiday with the lowest possible barrier to entry: eat an apple. With more than 7,500 apple varieties "
         "in existence worldwide, &ldquo;red&rdquo; is really a whole spectrum &mdash; from a snappy Honeycrisp to a classic "
         "Red Delicious &mdash; and the day works better as a nudge toward normal snacking than a grand celebration. "
         "<a href=\"/holiday/eat-a-red-apple-day/\">Full holiday page &rarr;</a>"),

        ("national-mutt-day",
         "Founded in 2005 by pet advocate Colleen Paige, National Mutt Day runs twice a year &mdash; July 31st and "
         "December 2nd &mdash; specifically to get more mixed-breed dogs adopted out of shelters, where they make up "
         "an estimated 80% of the population. The pitch isn't pure charity, either: mutts tend to have fewer "
         "inherited health problems than purebreds, thanks to a wider gene pool. "
         "<a href=\"/holiday/national-mutt-day/\">Full holiday page &rarr;</a>"),
        ("special-education-day",
         "This one marks a real legislative milestone: December 2, 1975, when President Gerald Ford signed the "
         "Education for All Handicapped Children Act, later reauthorized as IDEA. The law guarantees a free, "
         "appropriate public education to kids with disabilities from birth through age 21, across 13 recognized "
         "disability categories &mdash; a rare case of an &ldquo;obscure holiday&rdquo; tied to something genuinely "
         "load-bearing in American life. <a href=\"/holiday/special-education-day/\">Full holiday page &rarr;</a>"),

        ("make-a-gift-day",
         "The anti-Black-Friday holiday: instead of buying something, you make it. It's less about the finished "
         "craft and more about resetting expectations right before a month that pressures everyone into spending. "
         "<a href=\"/holiday/make-a-gift-day/\">Full holiday page &rarr;</a>"),
        ("national-roof-over-your-head-day",
         "A quiet gratitude holiday with real stakes behind it &mdash; an estimated 1.6 billion people worldwide live "
         "in substandard housing, and more than 100 million have no home at all. The day asks you to notice the "
         "roof over your head specifically because so many people this time of year don't have one. "
         "<a href=\"/holiday/national-roof-over-your-head-day/\">Full holiday page &rarr;</a>"),

        ("national-cookie-day",
         "Cookie Day has history behind it: the word comes from the Dutch <em>koekje</em> (&ldquo;little cake&rdquo;), and the "
         "chocolate chip version that now dominates home baking wasn't invented until 1938, when Ruth Wakefield "
         "ran out of baker's chocolate at the Toll House Inn and chopped up a candy bar instead. "
         "<a href=\"/holiday/national-cookie-day/\">Full holiday page &rarr;</a>"),
        ("wear-brown-shoes-day",
         "There's no real origin story here &mdash; it just shows up on obscure-holiday lists year after year. The "
         "closest thing to a point is a low-key argument that brown shoes pair with more outfits than black ones, "
         "which is either useful styling advice or an excuse to wear the shoes you already own. "
         "<a href=\"/holiday/wear-brown-shoes-day/\">Full holiday page &rarr;</a>"),

        ("international-ninja-day",
         "Fittingly for a holiday about covert operatives, the origin is murky &mdash; most trace it to the 2005 web "
         "series &ldquo;Ask a Ninja.&rdquo; The real history is more interesting than the myth: ninjas (shinobi) were spies "
         "and infiltrators who trained in disguise and survival as much as combat, a sharp contrast to the more "
         "visible, honor-bound samurai. <a href=\"/holiday/international-ninja-day/\">Full holiday page &rarr;</a>"),
        ("krampusnacht",
         "The night before Saint Nicholas Day belongs to his opposite number: Krampus, a horned, chain-dragging "
         "Alpine folk figure who punishes naughty children instead of rewarding good ones. Krampuslauf parades "
         "&mdash; costumed Krampus runs through the streets &mdash; turn the legend into a genuinely startling public event "
         "across Austria, Germany, and beyond. <a href=\"/holiday/krampusnacht/\">Full holiday page &rarr;</a>"),

        ("put-on-your-own-shoes-day",
         "A holiday for toddlers, really: putting on your own shoes is a real developmental milestone, and this "
         "day quietly celebrates the first taste of getting dressed without help. It's also a decent excuse to "
         "note that shoes have existed for over 5,500 years, so at least nobody's lacing up cowhide anymore. "
         "<a href=\"/holiday/put-on-your-own-shoes-day/\">Full holiday page &rarr;</a>"),
        ("saint-nicholas-day",
         "The actual historical basis for Santa Claus: a 4th-century bishop from Myra, in modern Turkey, known "
         "for secretly giving money to the poor &mdash; including, as legend has it, dropping coins down chimneys. "
         "European kids leave shoes out the night before for coins and treats, a much older and smaller-scale "
         "version of what Christmas Eve later became. <a href=\"/holiday/saint-nicholas-day/\">Full holiday page &rarr;</a>"),

        ("international-civil-aviation-day",
         "Established in 1994 for the 50th anniversary of the Chicago Convention &mdash; the 1944 agreement that "
         "created the rulebook for international air travel &mdash; this is one of the more institutional entries on "
         "the calendar, backed by an actual UN agency, ICAO. A good reminder that &ldquo;obscure holiday&rdquo; doesn't "
         "always mean &ldquo;silly holiday.&rdquo; <a href=\"/holiday/international-civil-aviation-day/\">Full holiday page &rarr;</a>"),
        ("national-letter-writing-day",
         "Before texting and email, letters were the only way to reach someone far away, and this day is a nudge "
         "to remember what that felt like. A handwritten letter still triggers a different emotional response "
         "than a text &mdash; the visible effort behind it is part of the message. "
         "<a href=\"/holiday/national-letter-writing-day/\">Full holiday page &rarr;</a>"),

        ("national-brownie-day",
         "The brownie's origin is genuinely disputed: some credit the 1893 World's Columbian Exposition in "
         "Chicago, others point to a baker who simply forgot the baking powder in a chocolate cake. Either way, "
         "the fudgy-versus-cakey debate is older than most families' recipe cards. "
         "<a href=\"/holiday/national-brownie-day/\">Full holiday page &rarr;</a>"),
        ("pretend-to-be-a-time-traveler-day",
         "Invented in 2007 by science fiction fans, this is one of the more purely playful entries on the "
         "calendar: dress from another era, speak in slang that doesn't belong, and &ldquo;correct&rdquo; tour guides about "
         "historical events as though you were there. The bar for participation is just a willingness to be a "
         "little weird in public. <a href=\"/holiday/pretend-to-be-a-time-traveler-day/\">Full holiday page &rarr;</a>"),

        ("christmas-card-day",
         "This one has an exact founding moment: December 1843, when Sir Henry Cole commissioned the first "
         "commercial Christmas card from illustrator John Callcott Horsley, with only 1,000 printed. Cards "
         "weren't even winter-specific at first &mdash; Victorian designs often featured spring flowers, since the "
         "format got reused for greetings year-round. <a href=\"/holiday/christmas-card-day/\">Full holiday page &rarr;</a>"),
        ("national-pastry-day",
         "From flaky croissants to savory empanadas, &ldquo;pastry&rdquo; is a bigger tent than most people assume &mdash; the "
         "term covers sweet and savory alike, unified by technique rather than flavor. Ancient Egyptians, Greeks, "
         "and Romans all had early versions of baked, filled dough, making this one of the oldest food categories "
         "on the entire calendar. <a href=\"/holiday/national-pastry-day/\">Full holiday page &rarr;</a>"),

        ("human-rights-day",
         "December 10th marks the 1948 adoption of the Universal Declaration of Human Rights by the UN General "
         "Assembly &mdash; now the most translated document on Earth, available in over 500 languages. Eleanor "
         "Roosevelt chaired the drafting committee, one of the more consequential things a former First Lady has "
         "ever put her name to. <a href=\"/holiday/human-rights-day/\">Full holiday page &rarr;</a>"),
        ("nobel-prize-day",
         "The date is deliberate: December 10th is the anniversary of Alfred Nobel's death, and the prizes he "
         "funded &mdash; in his will, using dynamite money &mdash; have been awarded in Stockholm and Oslo every year since "
         "1901. Marie Curie remains the only person ever to win in two different sciences. "
         "<a href=\"/holiday/nobel-prize-day/\">Full holiday page &rarr;</a>"),

        ("have-a-bagel-day",
         "Bagels trace back to Jewish communities in Poland, with the first documented mention in Krak&oacute;w in "
         "1610 &mdash; centuries before &ldquo;everything&rdquo; became a legitimate topping category. The boil-then-bake "
         "method is what gives them their shiny crust and chew, and yes, New Yorkers really will argue that the "
         "city's water is why their bagels taste different. <a href=\"/holiday/have-a-bagel-day/\">Full holiday page &rarr;</a>"),
        ("international-mountain-day",
         "The UN gave mountains their own day in 2003 for good reason: they cover about a quarter of the "
         "planet's land, supply 60&ndash;80% of the world's fresh water, and are home to roughly 15% of the human "
         "population. One of the rare &ldquo;obscure holidays&rdquo; backed by genuine global infrastructure numbers. "
         "<a href=\"/holiday/international-mountain-day/\">Full holiday page &rarr;</a>"),

        ("gingerbread-house-day",
         "The tradition traces to 16th-century Germany and got a popularity boost from the Brothers Grimm's "
         "&ldquo;Hansel and Gretel&rdquo; &mdash; a story that, read literally, is not exactly a gingerbread endorsement. The "
         "world's largest gingerbread house, built in Texas in 2013, covered over 2,500 square feet, which is a "
         "lot of edible drywall. <a href=\"/holiday/gingerbread-house-day/\">Full holiday page &rarr;</a>"),
        ("national-ding-a-ling-day",
         "The entire holiday is an excuse to call someone you've been meaning to call &mdash; no elaborate ritual, no "
         "shopping list, just picking up the phone for someone you haven't talked to in a while. One of the "
         "lowest-effort, highest-payoff entries on the whole calendar. "
         "<a href=\"/holiday/national-ding-a-ling-day/\">Full holiday page &rarr;</a>"),

        ("national-cocoa-day",
         "Cacao was valuable enough in Aztec and Mayan society to function as literal currency, long before it "
         "became a mug of instant cocoa mix. The solid chocolate bar didn't exist until 1847; before that, cocoa "
         "was strictly a drink. <a href=\"/holiday/national-cocoa-day/\">Full holiday page &rarr;</a>"),
        ("violin-day",
         "The modern violin took shape in 16th-century Italy, and instruments built centuries later by Stradivari "
         "and Guarneri are still considered the gold standard &mdash; a small handful are worth millions of dollars "
         "today. Four strings, tuned G-D-A-E, largely unchanged since the design was finalized four hundred years "
         "ago. <a href=\"/holiday/violin-day/\">Full holiday page &rarr;</a>"),

        ("monkey-day",
         "Started as a joke in 2000, when artist Eric Millikin jokingly wrote &ldquo;Monkey Day&rdquo; on fellow artist "
         "Casey Sorrow's calendar, this holiday somehow grew into a genuine platform for primate conservation "
         "awareness, with zoos and wildlife groups running real programming around it. Proof that a bit can "
         "outlive the joke. <a href=\"/holiday/monkey-day/\">Full holiday page &rarr;</a>"),
        ("roast-chestnuts-day",
         "The &ldquo;Chestnuts roasting on an open fire&rdquo; lyric from 1945's &ldquo;The Christmas Song&rdquo; probably did more "
         "to cement this tradition in American culture than the actual eating of chestnuts ever has. They're "
         "scored with a knife before roasting for a practical reason: skip that step and steam buildup can make "
         "them explode. <a href=\"/holiday/roast-chestnuts-day/\">Full holiday page &rarr;</a>"),

        ("bill-of-rights-day",
         "December 15, 1791 is when the first ten amendments to the Constitution were ratified &mdash; but the "
         "holiday itself is much younger, created by FDR in 1941, in the middle of World War II, as a deliberate "
         "statement about what the country was fighting for. Twelve amendments were originally proposed; only ten "
         "made the cut. <a href=\"/holiday/bill-of-rights-day/\">Full holiday page &rarr;</a>"),
        ("national-cupcake-day",
         "Cupcakes are named for their original measuring method, not their size &mdash; recipes literally called for "
         "ingredients &ldquo;by the cup,&rdquo; a naming convention going back to Amelia Simmons's 1796 &ldquo;American Cookery.&rdquo; "
         "Red velvet remains the reigning most-popular flavor almost two centuries later. "
         "<a href=\"/holiday/national-cupcake-day/\">Full holiday page &rarr;</a>"),

        ("barbie-and-barney-backlash-day",
         "Less a holiday than a shared joke: a day for adults to gripe, affectionately, about the relentless, "
         "sugary positivity of children's media. It's not really about Barbie or Barney specifically &mdash; they're "
         "just the most famous examples of an entire genre built on being aggressively upbeat. "
         "<a href=\"/holiday/barbie-and-barney-backlash-day/\">Full holiday page &rarr;</a>"),
        ("national-chocolate-covered-anything-day",
         "The instruction is right there in the name, and people take it seriously &mdash; coffee beans, bacon, potato "
         "chips, and gummy bears have all shown up as chocolate-covered submissions. Dunking odd things in "
         "chocolate is at least a few thousand years old, tracing back to Mesoamerican cacao traditions long "
         "before it became an internet dare. <a href=\"/holiday/national-chocolate-covered-anything-day/\">Full holiday page &rarr;</a>"),

        ("national-maple-syrup-day",
         "It takes roughly 40 gallons of maple sap to make a single gallon of syrup, which goes a long way toward "
         "explaining the price tag. Quebec alone produces more than 70% of the world's supply &mdash; a fact that will "
         "surprise nobody who's seen a Canadian grocery store's syrup aisle. "
         "<a href=\"/holiday/national-maple-syrup-day/\">Full holiday page &rarr;</a>"),
        ("wright-brother-day",
         "The first successful powered flight, on December 17, 1903, lasted all of 12 seconds and covered 120 "
         "feet &mdash; shorter than the wingspan of a modern jumbo jet. The Wrights funded the whole project with "
         "money from their bicycle repair shop in Dayton, Ohio, a fairly unglamorous origin story for the birth "
         "of aviation. <a href=\"/holiday/wright-brother-day/\">Full holiday page &rarr;</a>"),

        ("answer-the-telephone-like-buddy-the-elf-day",
         "Straight from the 2003 film &ldquo;Elf&rdquo;: pick up the phone the way Buddy does, with maximum enthusiasm and a "
         "non-sequitur greeting (&ldquo;Buddy the Elf, what's your favorite color?&rdquo;). The North Pole scenes were shot "
         "in Vancouver, which somewhat undercuts the mythology, but the bit still works. "
         "<a href=\"/holiday/answer-the-telephone-like-buddy-the-elf-day/\">Full holiday page &rarr;</a>"),
        ("bake-cookies-day",
         "Distinct from December's other cookie-adjacent holiday (National Cookie Day, the 4th), this one is "
         "squarely about the baking itself &mdash; flour on the counter, timers going off, a house that smells like "
         "vanilla for a day. Over 200 cookie recipes are registered with the American Cookie Association, which "
         "is a real organization keeping real track. <a href=\"/holiday/bake-cookies-day/\">Full holiday page &rarr;</a>"),
        ("national-ugly-sweater-day",
         "What started as ironic 1980s fashion turned into an organized tradition around 2002, when a Vancouver "
         "group is credited with throwing the first dedicated Ugly Sweater Party. Most modern events double as "
         "charity fundraisers, so the tackier the sweater &mdash; tinsel, LED lights, oversized appliqu&eacute;s &mdash; the better "
         "the cause tends to do. <a href=\"/holiday/national-ugly-sweater-day/\">Full holiday page &rarr;</a>"),

        ("national-hard-candy-day",
         "Hard candy's roots are medicinal &mdash; early versions were lozenges, not treats &mdash; before sugar boiled to a "
         "glass-like consistency became a category of its own. One recorded candy reportedly took over seven "
         "hours to fully dissolve in someone's mouth, which is either impressive restraint or a genuine test of "
         "patience. <a href=\"/holiday/national-hard-candy-day/\">Full holiday page &rarr;</a>"),
        ("national-oatmeal-muffin-day",
         "The oatmeal muffin sits in an odd, useful middle ground &mdash; heart-healthier than a cupcake thanks to "
         "oats' soluble fiber, but sweeter and more forgiving than a bowl of plain oatmeal. Structurally it's just "
         "a quick bread, leavened with baking powder rather than yeast, dressed up to look like dessert. "
         "<a href=\"/holiday/national-oatmeal-muffin-day/\">Full holiday page &rarr;</a>"),

        ("go-caroling-day",
         "Caroling wasn't originally religious at all &mdash; &ldquo;carol&rdquo; once just meant a dance accompanied by "
         "singing. Victorian England is responsible for most of the caroling tradition as it's practiced today, "
         "since a huge share of the standard carol repertoire was composed during that era. "
         "<a href=\"/holiday/go-caroling-day/\">Full holiday page &rarr;</a>"),
        ("international-human-solidarity-day",
         "A UN-established day (2005) aimed squarely at poverty eradication and sustainable development, built "
         "around the idea that solidarity between nations is a prerequisite for solving problems no single "
         "country can fix alone. One of the more policy-flavored entries on the calendar, closer to a UN "
         "awareness campaign than a folk tradition. <a href=\"/holiday/international-human-solidarity-day/\">Full holiday page &rarr;</a>"),

        ("national-crossword-puzzle-day",
         "The first crossword ran in the New York World on exactly this date in 1913, created by journalist "
         "Arthur Wynne &mdash; who actually called it a &ldquo;Word-Cross&rdquo; until a typesetting error flipped it to "
         "&ldquo;Cross-Word&rdquo; and the name stuck. By the 1920s, crossword-themed parties were an actual social fad. "
         "<a href=\"/holiday/national-crossword-puzzle-day/\">Full holiday page &rarr;</a>"),
        ("national-french-fried-shrimp-day",
         "A straightforward one: batter or bread shrimp, fry until golden, serve with cocktail or tartar sauce. "
         "It happens to fall on the same date as the winter solstice, giving seafood fans a genuinely warm meal "
         "on the year's darkest day. <a href=\"/holiday/national-french-fried-shrimp-day/\">Full holiday page &rarr;</a>"),
        ("winter-solstice",
         "The actual astronomical event, not just a folk holiday &mdash; the shortest day and longest night of the "
         "year in the Northern Hemisphere, marking the sun's most southerly point and the technical start of "
         "winter. Stonehenge is precisely aligned to it, and cultures worldwide have marked the turning point for "
         "millennia under names like Yule and Dongzhi &mdash; long before it shared a date with fried shrimp. "
         "<a href=\"/holiday/winter-solstice/\">Full holiday page &rarr;</a>"),

        ("national-cookie-exchange-day",
         "The format is simple and genuinely efficient: everyone bakes one big batch of a single cookie, then "
         "trades within the group, so each person walks away with a full assortment instead of a freezer full of "
         "just one kind. Cookie swap parties date back to the early 20th century &mdash; older than it feels. "
         "<a href=\"/holiday/national-cookie-exchange-day/\">Full holiday page &rarr;</a>"),
        ("national-date-nut-bread-day",
         "A quick bread, meaning no yeast and no waiting around &mdash; just dates, walnuts or pecans, and enough "
         "spice to make it feel seasonal. It's one of those recipes that tends to get handed down inside a single "
         "family rather than picked up from a cookbook. <a href=\"/holiday/national-date-nut-bread-day/\">Full holiday page &rarr;</a>"),

        ("festivus",
         "Yes, it's from Seinfeld &mdash; specifically the 1997 episode &ldquo;The Strike&rdquo; &mdash; but the holiday itself was "
         "real before the show borrowed it, invented by writer Dan O'Keefe's own father. The traditions are "
         "deliberately anti-commercial: an unadorned aluminum pole instead of a tree, an &ldquo;Airing of Grievances&rdquo; "
         "instead of pleasantries, and &ldquo;Feats of Strength&rdquo; to close things out. "
         "<a href=\"/holiday/festivus/\">Full holiday page &rarr;</a>"),
        ("pfeffernusse-day",
         "The name translates from German as &ldquo;pepper nuts,&rdquo; though there's usually no actual nuts involved &mdash; "
         "&ldquo;pepper&rdquo; refers to the mix of warm spices (cinnamon, cloves, nutmeg, cardamom, sometimes anise) "
         "rather than literal pepper. Texture is a genuine point of regional disagreement: some versions are "
         "soft and cake-like, others hard enough to require a dunk in coffee. "
         "<a href=\"/holiday/pfeffernusse-day/\">Full holiday page &rarr;</a>"),

        ("christmas-eve",
         "The anticipation night &mdash; trees get decorated, meals get cooked (R&eacute;veillon in French-speaking "
         "regions, Nochebuena in Spanish-speaking ones), and in parts of Europe, especially Germany, gifts are "
         "opened tonight rather than waiting for Christmas morning. Midnight Mass traces back to the 4th century. "
         "<a href=\"/holiday/christmas-eve/\">Full holiday page &rarr;</a>"),
        ("national-eggnog-day",
         "Eggnog descends from a medieval British drink called posset &mdash; hot milk curdled with ale or wine &mdash; and "
         "its name likely comes from &ldquo;grog&rdquo; plus &ldquo;noggin,&rdquo; a small wooden cup. George Washington had his own "
         "recipe, and it was not subtle: rye whiskey, rum, and sherry, all in one glass. "
         "<a href=\"/holiday/national-eggnog-day/\">Full holiday page &rarr;</a>"),

        ("christmas-day",
         "The decorated evergreen tree tradition is younger than people assume &mdash; it started in 16th-century "
         "Germany, well after the holiday's origins. The word &ldquo;Xmas&rdquo; is even older than that, first recorded in "
         "1551, with the &ldquo;X&rdquo; standing in for the Greek letter that begins &ldquo;Christ.&rdquo; "
         "<a href=\"/holiday/christmas-day/\">Full holiday page &rarr;</a>"),
        ("national-pumpkin-pie-day",
         "Landing on Christmas rather than Thanksgiving is a little bit of a rebellion, but the pie itself "
         "predates both American holidays &mdash; a 1675 English cookbook has a version of it, decades before the "
         "country existed. Also: pumpkins are technically a fruit, a type of berry, so this dessert has been "
         "misfiled as a vegetable pie forever. <a href=\"/holiday/national-pumpkin-pie-day/\">Full holiday page &rarr;</a>"),

        ("boxing-day",
         "The name has nothing to do with fighting &mdash; it comes from the &ldquo;Christmas box,&rdquo; a gift employers "
         "historically gave staff and servants the day after Christmas. It's now a major shopping holiday across "
         "Commonwealth countries, essentially the UK's answer to Black Friday, with football matches and horse "
         "racing thrown in. <a href=\"/holiday/boxing-day/\">Full holiday page &rarr;</a>"),
        ("national-candy-cane-day",
         "Original candy canes were plain white sugar sticks, handed to children in 17th-century Germany mostly "
         "to keep them quiet during long church services &mdash; the red stripes and peppermint flavor didn't show up "
         "until the early 1900s and didn't become standard until the 1950s. Most of the religious symbolism "
         "attached itself after the design was already popular, not before. "
         "<a href=\"/holiday/national-candy-cane-day/\">Full holiday page &rarr;</a>"),

        ("make-cut-out-snowflakes-day",
         "Real snowflakes are famously unique thanks to their six-sided crystalline structure, and this holiday "
         "is basically a low-tech attempt to recreate that individuality with paper and scissors. It also doubles "
         "as a genuinely good fine-motor-skills activity for kids, dressed up as a craft project instead of an "
         "exercise. <a href=\"/holiday/make-cut-out-snowflakes-day/\">Full holiday page &rarr;</a>"),
        ("visit-the-zoo-day",
         "The world's oldest still-operating zoo, Vienna's Tiergarten Sch&ouml;nbrunn, has been open since 1752 &mdash; a "
         "reminder that zoos as an institution are a lot older than most of the conservation missions they now "
         "center themselves around. Modern accredited zoos run actual breeding programs for endangered species, "
         "a meaningfully different job than the menageries they started as. "
         "<a href=\"/holiday/visit-the-zoo-day/\">Full holiday page &rarr;</a>"),

        ("card-playing-day",
         "Playing cards trace back to China, likely during the Tang dynasty, before making their way west through "
         "the Middle East and into Europe. The math is almost absurd: a standard 52-card deck has more possible "
         "shuffle orders than there are atoms on Earth, meaning any deck you shuffle tonight has, in all "
         "likelihood, never existed in that exact order before. <a href=\"/holiday/card-playing-day/\">Full holiday page &rarr;</a>"),
        ("pledge-of-allegiance-day",
         "Congress officially recognized the Pledge on this date in 1945 &mdash; but that's not the version most "
         "people know, since &ldquo;under God&rdquo; wasn't added until 1954, under Eisenhower. The original 1892 salute "
         "(arm extended outward) was dropped for the hand-over-heart gesture during World War II, for reasons "
         "that probably don't need explaining. <a href=\"/holiday/pledge-of-allegiance-day/\">Full holiday page &rarr;</a>"),

        ("still-need-to-do-day",
         "The honest holiday: an acknowledgment that most people hit year-end with a backlog of tasks they were "
         "supposed to finish weeks ago. Less a celebration than a permission slip &mdash; either scramble to close "
         "things out, or accept that some of it rolls into next year. "
         "<a href=\"/holiday/still-need-to-do-day/\">Full holiday page &rarr;</a>"),
        ("tick-tock-day",
         "Two days before the new year, this is the moment most people actually start reviewing whatever "
         "resolutions they made twelve months ago &mdash; and quietly start drafting the next batch. The whole "
         "holiday is built around the discomfort of watching time run out, which is either motivating or mildly "
         "stressful depending on how the year went. <a href=\"/holiday/tick-tock-day/\">Full holiday page &rarr;</a>"),

        ("bacon-day",
         "The word &ldquo;bacon&rdquo; comes from an Old High German word for &ldquo;buttock&rdquo; &mdash; an unglamorous etymology for "
         "a food this beloved. Ancient Romans were already curing pork belly for preservation, so bacon's basic "
         "technique predates refrigeration by roughly two thousand years. "
         "<a href=\"/holiday/bacon-day/\">Full holiday page &rarr;</a>"),
        ("falling-needles-family-fest-day",
         "A holiday that turns a chore into an event: your real Christmas tree is shedding needles by now "
         "regardless, so this one just asks families to do the cleanup together instead of alone. Many "
         "communities run tree-recycling programs that chip the trees into mulch for parks, so the needles get "
         "one more use before the season fully ends. <a href=\"/holiday/falling-needles-family-fest-day/\">Full holiday page &rarr;</a>"),

        ("make-up-your-mind-day",
         "Built for anyone who's spent the whole year putting off a decision &mdash; the day is essentially a deadline "
         "for &ldquo;analysis paralysis,&rdquo; the well-documented tendency to overthink a choice until it makes itself. "
         "Research suggests decisions made earlier in the day, when mental energy is higher, tend to go better. "
         "<a href=\"/holiday/make-up-your-mind-day/\">Full holiday page &rarr;</a>"),
        ("no-interruptions-day",
         "It takes an average of 23 minutes to fully regain focus after being interrupted, which is the kind of "
         "statistic that makes &ldquo;just turn off notifications for a day&rdquo; sound less like self-help and more like "
         "basic infrastructure. A fitting way to close out the year: one day of actual, uninterrupted quiet "
         "before everything starts again. <a href=\"/holiday/no-interruptions-day/\">Full holiday page &rarr;</a>"),
    ],
}

JANUARY = {
    "month_num": 1,
    "month_name": "January",
    "url_slug": "january",
    "title": "The Complete Guide to January's Obscure Holidays | Obscure Holiday Calendar",
    "description": (
        "A complete, day-by-day guide to all 62 obscure and offbeat holidays in January — "
        "from National Hangover Day to Inspire Your Heart With Art Day — with history, context, "
        "and links to the full write-up for each one."
    ),
    "h1": "The Complete Guide to January's Obscure Holidays",
    "date_published": "2026-07-28",
    "date_modified": "2026-07-28",
    "intro_html": """    <p>January runs on New Year's momentum &mdash; equal parts self-improvement and recovery from
    whatever December's 64 holidays talked you into. Underneath the resolutions, the month packs in 62
    obscure observances of its own, from a UN data-protection treaty (Data Privacy Day) to a fake holiday
    invented specifically so nobody has to do anything (National Nothing Day).</p>

    <p>This guide walks through all 62, day by day, with a bit of history or context for each one and a
    link to the full write-up &mdash; complete fun facts, ways to celebrate, and sourcing &mdash; on its own page.</p>""",
    "why_html": """    <p>Two clusters stand out. The first is resolution-adjacent: Organize Your Home Day, National Hugging
    Day, National Compliment Day, and Celebration of Life Day all lean on the same fresh-start energy that
    gets people through the front two weeks of January before it fades. The second is a surprising density of
    &ldquo;this exact date, something got invented or patented&rdquo; holidays &mdash; Braille (Jan 4), Foucault's pendulum
    proving Earth's rotation (Jan 8), the tin can patent (Jan 19), the LEGO coupling-system patent (Jan 28),
    and Wikipedia's launch (Jan 15) all happen to fall in the same 31 days.</p>""",
    "how_to_use_html": """    <p>Holidays are grouped by date below. Each entry gets a short original write-up &mdash; not a repeat
    of the fact sheet &mdash; plus a link to the full holiday page if you want the deeper dive: complete fun
    facts, ways to celebrate, and sourcing.</p>""",
    "about_html": """    <p>This guide is part of the Obscure Holiday Calendar project &mdash; the same database that powers
    the iOS and Android apps and the individual holiday pages on this site. It exists to give a single,
    readable overview of an entire month at once, instead of requiring 62 separate page visits.</p>""",
    "faq": [
        (
            "How many obscure holidays are there in January?",
            "62 in 2026, spread across all 31 days, with at least one falling on every date and two on most days.",
        ),
        (
            "What's the most historically significant holiday in January?",
            "Data Privacy Day (Jan 28) has a real legal backbone — it marks the 1981 signing of Convention 108, "
            "the first legally binding international data-protection treaty. Korean American Day (Jan 13) also "
            "marks a real historical event: the 1903 arrival of the first Korean immigrants to the United States.",
        ),
        (
            "Are there a lot of food holidays in January?",
            "Yes — National Spaghetti Day, National Pie Day, National Croissant Day, Chocolate Cake Day, Corn "
            "Chip Day, National Cheese Lovers Day, and several more make up close to a third of the month.",
        ),
        (
            "Where can I find the full history and fun facts for each holiday?",
            "Every holiday name in this guide links to its own dedicated page with a longer write-up, sourced "
            "fun facts, and ideas for how to celebrate.",
        ),
    ],
    "entries": [
        ("national-hangover-day",
         "The other January 1st holiday &mdash; less resolutions, more rehydration. The word &ldquo;hangover&rdquo; itself "
         "dates to the late 1800s, originally describing anything left over from a previous event, not "
         "specifically the alcohol kind. <a href=\"/holiday/national-hangover-day/\">Full holiday page &rarr;</a>"),
        ("new-years-day",
         "The Babylonians started this 4,000 years ago, but in March, not January &mdash; the January 1st date only "
         "became standard in 1582, when Pope Gregory XIII's calendar reform locked it in. One tradition has held "
         "up since Babylon: they made resolutions too, mostly involving returning borrowed farm equipment. "
         "<a href=\"/holiday/new-years-day/\">Full holiday page &rarr;</a>"),

        ("national-buffet-day",
         "The word comes from the French for sideboard &mdash; the piece of furniture, not the meal &mdash; and the "
         "self-serve format got its real boost from the Scandinavian sm&ouml;rg&aring;sbord. Early American buffets were "
         "largely a casino and hotel tactic to keep guests on the property, which is still basically the "
         "business model today. <a href=\"/holiday/national-buffet-day/\">Full holiday page &rarr;</a>"),
        ("science-fiction-day",
         "Timed to Isaac Asimov's birthday, whose output was almost unbelievable: over 500 books across science "
         "fiction, nonfiction, and mystery. The genre itself is often traced back further than people expect "
         "&mdash; to Mary Shelley's Frankenstein in 1818, more than a century before the word &ldquo;robot&rdquo; existed. "
         "<a href=\"/holiday/science-fiction-day/\">Full holiday page &rarr;</a>"),

        ("fruitcake-toss-day",
         "Manitou Springs, Colorado runs an actual annual &ldquo;Great Fruitcake Toss,&rdquo; complete with catapults and "
         "homemade cannons, built entirely around the fruitcake's reputation as the dessert nobody wants but "
         "nobody can throw away. That reputation is earned &mdash; some historical fruitcakes have reportedly stayed "
         "edible for decades. <a href=\"/holiday/fruitcake-toss-day/\">Full holiday page &rarr;</a>"),
        ("women-rock-day",
         "A broad, deliberately non-specific celebration &mdash; no single founder or origin story, just an annual nod "
         "to contributions and resilience across every field. The loosest of January's holidays in terms of how "
         "to observe it: support a woman-owned business, or just say something nice to one. "
         "<a href=\"/holiday/women-rock-day/\">Full holiday page &rarr;</a>"),

        ("national-spaghetti-day",
         "Strongly Italian in reputation, but archaeologists have traced noodle-like dishes back over 4,000 years "
         "in China, well before spaghetti as Italy knows it existed. Americans alone eat more than 6 billion "
         "pounds of pasta a year, and spaghetti is still the most requested shape. "
         "<a href=\"/holiday/national-spaghetti-day/\">Full holiday page &rarr;</a>"),
        ("world-braille-day",
         "Louis Braille was 15 when he invented the system, adapting a French military code called &ldquo;night "
         "writing&rdquo; that was originally designed for silent battlefield communication, not literacy. Braille "
         "isn't a language &mdash; it's a six-dot tactile alphabet that can represent almost any language written on "
         "top of it. <a href=\"/holiday/world-braille-day/\">Full holiday page &rarr;</a>"),

        ("national-bird-day",
         "Deliberately scheduled the day after the Christmas Bird Count wraps up, so birdwatchers already primed "
         "for counting have somewhere to redirect that energy. The oldest verified bird on record, a cockatoo "
         "named Cookie, lived to 82 &mdash; longer than most of the people who visited her at the Brookfield Zoo. "
         "<a href=\"/holiday/national-bird-day/\">Full holiday page &rarr;</a>"),
        ("national-whipped-cream-day",
         "Named, whether intentionally or not, for Aaron &ldquo;Bunny&rdquo; Lapin's birthday &mdash; the inventor of "
         "Reddi-Wip. Long before the aerosol can, 16th-century Italy and France called it &ldquo;milk snow,&rdquo; which is "
         "a better name than what most cans say on the label. <a href=\"/holiday/national-whipped-cream-day/\">Full holiday page &rarr;</a>"),

        ("cuddle-up-day",
         "The physiological case for this one is real: cuddling releases oxytocin, the same hormone tied to "
         "bonding and trust, and studies link it to measurably lower blood pressure. Doesn't require a person, "
         "either &mdash; pets count, and so does a really good blanket. <a href=\"/holiday/cuddle-up-day/\">Full holiday page &rarr;</a>"),
        ("national-technology-day",
         "A useful trivia magnet: Ada Lovelace is generally credited as the first computer programmer, in the "
         "mid-1800s, decades before an actual computer existed to run her work on. The first computer mouse, "
         "built by Douglas Engelbart in 1964, was made of wood. <a href=\"/holiday/national-technology-day/\">Full holiday page &rarr;</a>"),

        ("national-tempura-day",
         "Tempura's origin isn't Japanese at all &mdash; it arrived with 16th-century Portuguese Jesuit missionaries, "
         "and the name likely comes from the Latin &ldquo;tempora,&rdquo; referring to fasting days when Catholics avoided "
         "meat and ate battered, fried fish instead. Four centuries later it's about as Japanese a dish as "
         "exists. <a href=\"/holiday/national-tempura-day/\">Full holiday page &rarr;</a>"),
        ("old-rock-day",
         "The oldest confirmed rocks on Earth are about 4 billion years old, found in Canada and Australia &mdash; "
         "meaning some of what's under your feet has been there since not long after the planet formed. Rocks "
         "split into just three categories (igneous, sedimentary, metamorphic), a tidy system for something that "
         "covers the entire surface of the planet. <a href=\"/holiday/old-rock-day/\">Full holiday page &rarr;</a>"),

        ("bubble-bath-day",
         "Baths are ancient; the bubbles are not. Bubble bath as a mass-market product is a mid-20th-century "
         "invention, and the science behind why it works &mdash; surface tension trapping air in a thin liquid film "
         "&mdash; is the same principle behind soap bubbles blown outside. <a href=\"/holiday/bubble-bath-day/\">Full holiday page &rarr;</a>"),
        ("earths-rotation-day",
         "The date marks a real event: January 8, 1851, when physicist L&eacute;on Foucault publicly demonstrated "
         "Earth's rotation at the Paris Observatory using a swinging pendulum. The pendulum doesn't change "
         "direction &mdash; the Earth rotates underneath it, which is obvious once you see it and baffling before. "
         "<a href=\"/holiday/earths-rotation-day/\">Full holiday page &rarr;</a>"),

        ("national-law-enforcement-appreciation-day",
         "Founded in 2015 by a coalition including Concerns of Police Survivors, deliberately placed early in "
         "the year as a fresh-start opportunity for recognition. The &ldquo;wear blue&rdquo; custom is the most visible "
         "way people participate, with entire buildings sometimes lit blue for the occasion. "
         "<a href=\"/holiday/national-law-enforcement-appreciation-day/\">Full holiday page &rarr;</a>"),
        ("static-electricity-day",
         "That shock from touching a doorknob is a rapid discharge of built-up static &mdash; and lightning is the "
         "same phenomenon at a planetary scale, just discharging between clouds and ground instead of you and a "
         "doorknob. Walking across a carpet in socks can build up several thousand volts on your body. "
         "<a href=\"/holiday/static-electricity-day/\">Full holiday page &rarr;</a>"),

        ("houseplant-appreciation-day",
         "Backed by real research: houseplants measurably improve indoor air quality and are linked to lower "
         "stress and better concentration, not just as decor but as a passive intervention. Snake plants and ZZ "
         "plants get recommended constantly for a reason &mdash; they're nearly impossible to kill. "
         "<a href=\"/holiday/houseplant-appreciation-day/\">Full holiday page &rarr;</a>"),
        ("peculiar-people-day",
         "The word's meaning has drifted a long way from its Latin root, <em>peculium</em>, meaning &ldquo;private "
         "property&rdquo; &mdash; something that belonged distinctly to one person. By the 17th century it had shifted to "
         "mean &ldquo;strange,&rdquo; a fitting evolution for a holiday about embracing what makes you different. "
         "<a href=\"/holiday/peculiar-people-day/\">Full holiday page &rarr;</a>"),

        ("learn-your-name-in-morse-code-day",
         "Morse code, developed in the 1830s by Samuel Morse and Alfred Vail, is really just an ordered sequence "
         "of short and long pulses, simple enough that this holiday's entire premise takes about ten minutes. "
         "The most famous sequence in the whole system, SOS, wasn't standardized until 1908. "
         "<a href=\"/holiday/learn-your-name-in-morse-code-day/\">Full holiday page &rarr;</a>"),
        ("national-milk-day",
         "Marks a specific 1878 event: the first home delivery of milk in sterilized glass bottles, a genuine "
         "hygiene breakthrough at the time. A single dairy cow produces around 6.3 gallons of milk a day, more "
         "than 2,300 gallons over a year from one animal. <a href=\"/holiday/national-milk-day/\">Full holiday page &rarr;</a>"),

        ("national-hot-tea-day",
         "All &ldquo;true&rdquo; teas &mdash; black, green, white, oolong, pu-erh &mdash; come from exactly one plant, Camellia "
         "sinensis; every difference in flavor comes down to processing, not the plant itself. Tea bags, now the "
         "default format for most drinkers, were reportedly an accident, invented by a New York merchant who "
         "never meant for people to steep the silk sample sachets he was mailing out. "
         "<a href=\"/holiday/national-hot-tea-day/\">Full holiday page &rarr;</a>"),
        ("national-pharmacist-day",
         "Pharmacists do a lot more than count pills &mdash; modern scope of practice includes immunizations and "
         "chronic disease management, and getting there requires a Doctor of Pharmacy degree on top of undergrad. "
         "The first pharmacy in the American colonies opened in Philadelphia in 1729. "
         "<a href=\"/holiday/national-pharmacist-day/\">Full holiday page &rarr;</a>"),

        ("korean-american-day",
         "Marks a specific arrival: January 13, 1903, when 102 Korean immigrants landed in Honolulu aboard the SS "
         "Gaelic, the first wave of Korean immigration to the United States. Congress formally recognized the "
         "day in 2005, more than a century later. <a href=\"/holiday/korean-american-day/\">Full holiday page &rarr;</a>"),
        ("national-rubber-ducky-day",
         "Ernie's 1970 Sesame Street song did more for the rubber duck's cultural status than anything before it, "
         "but its most interesting moment came in 1992, when a cargo ship spilled 28,000 of them into the "
         "Pacific &mdash; and oceanographers used the drifting ducks to map ocean currents for years afterward. "
         "<a href=\"/holiday/national-rubber-ducky-day/\">Full holiday page &rarr;</a>"),

        ("dress-up-your-pet-day",
         "Pet costuming has more history than it looks like it should &mdash; Victorian-era photographs already show "
         "dressed-up pets, well over a century before it became an Instagram genre. The genuinely useful version "
         "is less about cuteness and more about function: sweaters, booties, and raincoats for bad weather. "
         "<a href=\"/holiday/dress-up-your-pet-day/\">Full holiday page &rarr;</a>"),
        ("organize-your-home-day",
         "Landing two weeks into January, this is really a second chance at a New Year's resolution for anyone "
         "whose January 1st momentum already faded. The KonMari method turned decluttering into a global "
         "phenomenon by reframing it around what sparks joy rather than what you might need someday. "
         "<a href=\"/holiday/organize-your-home-day/\">Full holiday page &rarr;</a>"),

        ("national-hat-day",
         "Hats go back to ancient Egypt, where straw versions were mostly sun protection rather than fashion "
         "&mdash; the status symbolism came later, peaking with the 19th-century top hat as shorthand for wealth. The "
         "largest hat on record, built for this holiday in Texas in 2018, stood over 14 feet tall. "
         "<a href=\"/holiday/national-hat-day/\">Full holiday page &rarr;</a>"),
        ("wikipedia-day",
         "Marks the exact 2001 launch date of a site that now holds more than 6.8 million English-language "
         "articles, built entirely by volunteers with no editorial staff in the traditional sense. The name "
         "itself is a mashup: &ldquo;wiki,&rdquo; a Hawaiian word for quick, plus &ldquo;encyclopedia.&rdquo; "
         "<a href=\"/holiday/wikipedia-day/\">Full holiday page &rarr;</a>"),

        ("appreciate-a-dragon-day",
         "Dragons split hard by culture &mdash; protective, wise guardians in much of East Asian folklore, versus "
         "destructive monsters in most Western tales &mdash; and this holiday is really an invitation to notice how "
         "differently the same mythical creature gets cast depending on where the story comes from. "
         "<a href=\"/holiday/appreciate-a-dragon-day/\">Full holiday page &rarr;</a>"),
        ("national-nothing-day",
         "Proposed in 1972 by columnist Harold Coffin with one explicit goal: a day Americans weren't expected to "
         "celebrate, honor, or observe anything at all. It's been in Chase's Calendar of Events since 1973, "
         "about as close to official recognition as a holiday about doing nothing is ever going to get. "
         "<a href=\"/holiday/national-nothing-day/\">Full holiday page &rarr;</a>"),

        ("kid-inventors-day",
         "Timed to Benjamin Franklin's birthday, who invented swim fins at age 12 &mdash; one of several young "
         "inventors the day is built around, alongside Louis Braille (15) and Frank Epperson, who invented the "
         "Popsicle at 11. <a href=\"/holiday/kid-inventors-day/\">Full holiday page &rarr;</a>"),
        ("popeye-s-birthday",
         "Popeye wasn't originally the star of his own comic strip &mdash; he showed up as a minor character in "
         "Thimble Theatre in 1929 and quickly took the whole thing over. The spinach connection came two years "
         "later, in a 1931 storyline that decided, somewhat arbitrarily, what his superpower source would be. "
         "<a href=\"/holiday/popeye-s-birthday/\">Full holiday page &rarr;</a>"),

        ("thesaurus-day",
         "Marks Peter Mark Roget's birthday, and his original 1852 thesaurus wasn't alphabetical at all &mdash; it "
         "organized words by concept and meaning, closer to a mind map than a dictionary. The word comes from "
         "Greek <em>th&#275;sauros</em>, meaning &ldquo;treasury,&rdquo; a grand name for a book of synonyms. "
         "<a href=\"/holiday/thesaurus-day/\">Full holiday page &rarr;</a>"),
        ("winnie-the-pooh-day",
         "Marks A.A. Milne's birthday, and nearly every character traces back to something real: Christopher "
         "Robin was Milne's actual son, &ldquo;Winnie&rdquo; came from a real black bear at the London Zoo, and most of "
         "the Hundred Acre Wood cast were literally Christopher Robin's stuffed animals. "
         "<a href=\"/holiday/winnie-the-pooh-day/\">Full holiday page &rarr;</a>"),

        ("national-popcorn-day",
         "Popcorn is older than most people assume &mdash; kernels have been found in Peru dating back over 6,500 "
         "years, and in New Mexico over 5,600. The &ldquo;pop&rdquo; itself is just physics: trapped moisture turns to "
         "steam, pressure builds, and the kernel bursts inside out. <a href=\"/holiday/national-popcorn-day/\">Full holiday page &rarr;</a>"),
        ("tin-can-day",
         "Marks Peter Durand's 1810 patent for the tin can &mdash; but for nearly 50 years afterward, there was no "
         "dedicated can opener, so people used chisels, hammers, or bayonets. The first real can opener wasn't "
         "patented until 1855, meaning the can predates the tool built to open it by almost half a century. "
         "<a href=\"/holiday/tin-can-day/\">Full holiday page &rarr;</a>"),

        ("national-cheese-lovers-day",
         "There are more than 1,800 recognized types of cheese worldwide, and a genuine cheese enthusiast has an "
         "actual name for it: turophile, from the Greek for &ldquo;cheese-loving.&rdquo; The world's most expensive "
         "cheese, Serbia's Pule, is made from Balkan donkey milk and runs around $600 a pound. "
         "<a href=\"/holiday/national-cheese-lovers-day/\">Full holiday page &rarr;</a>"),
        ("penguin-awareness-day",
         "All 18 recognized penguin species live exclusively in the Southern Hemisphere &mdash; there's no such "
         "thing as a wild Northern Hemisphere penguin, despite how often cartoons put them next to polar bears. "
         "Penguins can safely drink seawater because a gland above their eyes filters the salt straight out of "
         "their bloodstream. <a href=\"/holiday/penguin-awareness-day/\">Full holiday page &rarr;</a>"),

        ("national-hugging-day",
         "Created in 1986 by Kevin Zaborney in Caro, Michigan, who deliberately picked this date because it falls "
         "in the flat stretch between the winter holidays and Valentine's Day, when people's spirits tend to "
         "dip. The science backs the sentiment: hugging releases oxytocin and is linked to lower blood pressure. "
         "<a href=\"/holiday/national-hugging-day/\">Full holiday page &rarr;</a>"),
        ("squirrel-appreciation-day",
         "Founded in 2001 by wildlife rehabilitator Christy Hargrove, timed for the coldest stretch of the year "
         "when squirrels genuinely need the extra help. Their forgotten buried nuts aren't wasted &mdash; the ones "
         "squirrels never dig back up often grow into new trees, making them accidental foresters. "
         "<a href=\"/holiday/squirrel-appreciation-day/\">Full holiday page &rarr;</a>"),

        ("celebration-of-life-day",
         "Deliberately unofficial and open to interpretation &mdash; some treat it as a personal gratitude check-in, "
         "others use it to remember people who've passed and the legacy they left. It lands squarely in the "
         "window where New Year's resolutions either take hold or quietly die, which may not be a coincidence. "
         "<a href=\"/holiday/celebration-of-life-day/\">Full holiday page &rarr;</a>"),
        ("national-answer-your-cat-s-questions-day",
         "Built entirely around interpreting cat behavior as unspoken questions &mdash; a slow blink or a head bunt "
         "is a real form of feline communication, generally signaling trust rather than an actual inquiry. The "
         "&ldquo;answer,&rdquo; as the holiday frames it, is just more attention, play, or treats. "
         "<a href=\"/holiday/national-answer-your-cat-s-questions-day/\">Full holiday page &rarr;</a>"),

        ("national-measure-your-feet-day",
         "A real practical nudge: foot size changes over a lifetime with age, weight, and pregnancy, and a "
         "surprisingly large share of adults are wearing the wrong shoe size without realizing it. A proper fit "
         "isn't cosmetic &mdash; it affects posture and joint strain, not just comfort. "
         "<a href=\"/holiday/national-measure-your-feet-day/\">Full holiday page &rarr;</a>"),
        ("national-pie-day",
         "Backed by an actual trade group, the American Pie Council, which makes it more organized than most days "
         "on this calendar. Ancient Egyptian and Roman pies weren't really food in the way we think of pie &mdash; the "
         "crust was a sturdy cooking vessel, often discarded rather than eaten. "
         "<a href=\"/holiday/national-pie-day/\">Full holiday page &rarr;</a>"),

        ("global-belly-laugh-day",
         "Founded in 1997 by Elaine Esposito, who went by &ldquo;The Laugh Lady&rdquo; &mdash; a title that undersells how "
         "physical laughing actually is, engaging the diaphragm, abs, and shoulders like a small workout. "
         "Preschoolers reportedly laugh up to 400 times a day; the average adult manages 15 to 20. "
         "<a href=\"/holiday/global-belly-laugh-day/\">Full holiday page &rarr;</a>"),
        ("national-compliment-day",
         "The neuroscience is genuinely interesting here: a sincere compliment activates the same brain reward "
         "circuitry as a small cash payout. The best ones, per most advice on the subject, are specific &mdash; "
         "praising an action or quality rather than offering vague, generic flattery. "
         "<a href=\"/holiday/national-compliment-day/\">Full holiday page &rarr;</a>"),

        ("irish-coffee-day",
         "Invented in the 1940s by chef Joe Sheridan at Foynes Airbase in Ireland, specifically to warm up cold, "
         "cranky American passengers stepping off transatlantic flying boats. It only took off in the US after "
         "San Francisco's Buena Vista Cafe started serving it in 1952 &mdash; the tradition is to drink it unstirred, "
         "sipping hot coffee through a layer of cool cream. <a href=\"/holiday/irish-coffee-day/\">Full holiday page &rarr;</a>"),
        ("opposite-day",
         "Entirely unofficial, with zero formal recognition anywhere, and mostly kept alive in classrooms where "
         "saying the opposite of what you mean briefly becomes an acceptable excuse for chaos. It shows up "
         "constantly in kids' media, almost always as a plot device rather than a real observance. "
         "<a href=\"/holiday/opposite-day/\">Full holiday page &rarr;</a>"),

        ("australia-day",
         "Marks the 1788 arrival of the First Fleet and the raising of the British flag at Sydney Cove &mdash; a "
         "genuinely contested date, observed by many Australians as a celebration and by Indigenous Australians "
         "and allies as &ldquo;Invasion Day&rdquo; or a &ldquo;Day of Mourning.&rdquo; It wasn't consistently celebrated on this "
         "date nationwide until 1994. <a href=\"/holiday/australia-day/\">Full holiday page &rarr;</a>"),
        ("spouse-s-day",
         "A quieter, less commercialized alternative to Valentine's Day, built around specific gestures &mdash; a "
         "favorite meal, real quality time &mdash; rather than gifts. Its origins are murky enough that even sources "
         "promoting the day don't agree on where it started. <a href=\"/holiday/spouse-s-day/\">Full holiday page &rarr;</a>"),

        ("chocolate-cake-day",
         "The first printed chocolate cake recipe didn't appear until 1847, in Britain &mdash; a surprisingly late "
         "date for something that's now the single most popular cake flavor in America, edging out vanilla. The "
         "largest chocolate cake on record, built in Australia in 2016, weighed over 4,000 pounds. "
         "<a href=\"/holiday/chocolate-cake-day/\">Full holiday page &rarr;</a>"),
        ("punch-the-clock-day",
         "A fairly recent invention, dating to the early 2000s, built around workplace morale rather than any "
         "historical event &mdash; some offices mark it with a &ldquo;no overtime&rdquo; rule for the day. The name itself is "
         "a holdover from actual punch-card time clocks, which most modern employees have never touched. "
         "<a href=\"/holiday/punch-the-clock-day/\">Full holiday page &rarr;</a>"),

        ("data-privacy-day",
         "Marks the 1981 signing of Convention 108, the first legally binding international treaty on data "
         "protection &mdash; decades before most people had any data worth protecting. A recurring Pew Research "
         "finding around this date: most Americans believe their personal information is less secure now than it "
         "was five years ago. <a href=\"/holiday/data-privacy-day/\">Full holiday page &rarr;</a>"),
        ("international-lego-day",
         "Marks the exact day in 1958 that Godtfred Kirk Christiansen filed the patent for LEGO's stud-and-tube "
         "coupling system &mdash; the mechanism that made every brick since compatible with every other brick. LEGO "
         "also happens to be, by volume, the world's largest tire manufacturer, producing over 300 million tiny "
         "rubber tires a year. <a href=\"/holiday/international-lego-day/\">Full holiday page &rarr;</a>"),

        ("corn-chip-day",
         "Elmer Doolin bought the original Fritos recipe from a street vendor in San Antonio for $100 in 1932 "
         "&mdash; one of the better returns on investment in snack food history, given that his company eventually "
         "merged into what's now Frito-Lay. Real corn chips are made from ground cornmeal, not the nixtamalized "
         "masa dough used for tortilla chips. <a href=\"/holiday/corn-chip-day/\">Full holiday page &rarr;</a>"),
        ("national-puzzle-day",
         "Jigsaw puzzles started as an educational tool, not entertainment &mdash; European cartographer John "
         "Spilsbury cut up maps around 1760 to teach geography. The largest jigsaw puzzle ever assembled had "
         "551,232 pieces and measured over 14 by 23 feet, closer to a construction project than a rainy-day "
         "activity. <a href=\"/holiday/national-puzzle-day/\">Full holiday page &rarr;</a>"),

        ("national-croissant-day",
         "The croissant's real ancestor is Austrian, not French &mdash; a crescent-shaped pastry called the kipferl. "
         "The popular legend that the shape commemorates a victory over the Ottoman Empire in 1683 is mostly "
         "myth; the buttery, laminated version people associate with the word &ldquo;croissant&rdquo; was developed later, "
         "in 19th-century Parisian bakeries. <a href=\"/holiday/national-croissant-day/\">Full holiday page &rarr;</a>"),
        ("national-inane-answering-machine-day",
         "The earliest ancestor of the answering machine, the &ldquo;Telegraphone,&rdquo; dates to 1898 and recorded sound "
         "on magnetic wire &mdash; decades before cassette-based machines made voicemail a household fixture in the "
         "1970s and 80s. The &ldquo;inane&rdquo; in the name refers to exactly what you'd expect: the overly dramatic "
         "outgoing messages people used to record before digital voicemail flattened everyone's creativity. "
         "<a href=\"/holiday/national-inane-answering-machine-day/\">Full holiday page &rarr;</a>"),

        ("backward-day",
         "About as unofficial as a holiday gets &mdash; no clear founder, no historical event, just a grassroots "
         "tradition of wearing clothes inside out and walking backward for a day. The appeal is almost entirely "
         "in the small, physical disruption of doing ordinary things wrong on purpose. "
         "<a href=\"/holiday/backward-day/\">Full holiday page &rarr;</a>"),
        ("inspire-your-heart-with-art-day",
         "Closes out January on a genuinely well-supported note &mdash; engaging with art is linked to measurably "
         "lower stress and greater empathy, not just a vague creative platitude. The bar for participation is "
         "low: a poem, a song, a museum visit, or just making something yourself all count. "
         "<a href=\"/holiday/inspire-your-heart-with-art-day/\">Full holiday page &rarr;</a>"),
    ],
}

FEBRUARY = {
    "month_num": 2,
    "month_name": "February",
    "url_slug": "february",
    "title": "The Complete Guide to February's Obscure Holidays | Obscure Holiday Calendar",
    "description": (
        "A complete, day-by-day guide to all 58 obscure and offbeat holidays in February — "
        "from Change Your Password Day to Superman's Birthday — with history, context, and "
        "links to the full write-up for each one."
    ),
    "h1": "The Complete Guide to February's Obscure Holidays",
    "date_published": "2026-07-28",
    "date_modified": "2026-07-28",
    "intro_html": """    <p>February is short but dense &mdash; 58 obscure holidays packed into 28 (or 29) days, more per day on
    average than any other month on this calendar. Valentine's Day gets the headline, but the month runs a
    full second track underneath it: Groundhog Day folklore, a cloned sheep, the discovery of Pluto, and a
    specifically Swedish curling holiday.</p>

    <p>This guide walks through all 58, day by day, with a bit of history or context for each one and a
    link to the full write-up &mdash; complete fun facts, ways to celebrate, and sourcing &mdash; on its own page.</p>""",
    "why_html": """    <p>Two clusters stand out. There's a real romantic-calendar cluster around Valentine's Day itself &mdash;
    Galentine's Day, Singles Awareness Day, and Ferris Wheel Day (George Ferris's actual birthday) all sit
    within a few days of it. And there's a genuine science-and-history cluster: Darwin Day, Pluto Discovery
    Day, Dolly the Sheep Day, the first steam locomotive journey, and National Periodic Table Day are all tied
    to specific, dated, real events rather than invented observances &mdash; a higher ratio of &ldquo;this actually
    happened&rdquo; holidays than most other months.</p>""",
    "how_to_use_html": """    <p>Holidays are grouped by date below. Each entry gets a short original write-up &mdash; not a repeat
    of the fact sheet &mdash; plus a link to the full holiday page if you want the deeper dive: complete fun
    facts, ways to celebrate, and sourcing.</p>""",
    "about_html": """    <p>This guide is part of the Obscure Holiday Calendar project &mdash; the same database that powers
    the iOS and Android apps and the individual holiday pages on this site. It exists to give a single,
    readable overview of an entire month at once, instead of requiring 58 separate page visits.</p>""",
    "faq": [
        (
            "How many obscure holidays are there in February?",
            "58 across all 29 possible days, including February 29th — which only actually lands on the "
            "calendar in leap years, so the exact day-by-day total shifts slightly depending on the year.",
        ),
        (
            "What's the most scientifically significant holiday in February?",
            "Pluto Discovery Day (Feb 18) and Dolly the Sheep Day (Feb 22) both mark real, dated scientific "
            "milestones — the 1930 discovery of Pluto and the 1997 announcement of the first mammal ever cloned "
            "from an adult cell.",
        ),
        (
            "Are there a lot of food holidays in February?",
            "Yes — National Pizza Day, National Margarita Day, Fettuccine Alfredo Day, Chocolate Fondue Day, "
            "National Chocolate Mint Day, and several more make up close to a third of the month.",
        ),
        (
            "Where can I find the full history and fun facts for each holiday?",
            "Every holiday name in this guide links to its own dedicated page with a longer write-up, sourced "
            "fun facts, and ideas for how to celebrate.",
        ),
    ],
    "entries": [
        ("change-your-password-day",
         "A cybersecurity nudge dressed up as a holiday: over 80% of data breaches trace back to weak or stolen "
         "passwords, a fairly damning statistic for something this fixable. Pairing a strong password with "
         "two-factor authentication does more for your security than changing the password itself ever will. "
         "<a href=\"/holiday/change-your-password-day/\">Full holiday page &rarr;</a>"),
        ("national-dark-chocolate-day",
         "The bar for &ldquo;dark&rdquo; is at least 70% cocoa solids, roughly the threshold where the flavanol "
         "antioxidants linked to improved blood flow start showing up in meaningful amounts. The plant itself, "
         "<em>Theobroma cacao</em>, translates from Greek as &ldquo;food of the gods.&rdquo; "
         "<a href=\"/holiday/national-dark-chocolate-day/\">Full holiday page &rarr;</a>"),

        ("crepe-day",
         "Known in France as La Chandeleur, tied to the Presentation of Jesus at the Temple, but the cr&ecirc;pe "
         "tradition has its own superstition layered on top: flip one one-handed while holding a coin in the "
         "other, and it's supposed to bring good fortune for the year. <a href=\"/holiday/crepe-day/\">Full holiday page &rarr;</a>"),
        ("groundhog-day",
         "Punxsutawney Phil's official accuracy rate, as claimed by his own fan club, doesn't hold up against "
         "actual meteorological records, which put him closer to 30&ndash;40% &mdash; barely better than a coin flip. "
         "The tradition traces back to European Candlemas weather lore, where a badger or hedgehog did the "
         "shadow-watching before groundhogs took over in America. <a href=\"/holiday/groundhog-day/\">Full holiday page &rarr;</a>"),

        ("carrot-cake-day",
         "Carrots were a medieval baking workaround, not a health food choice &mdash; used to sweeten desserts back "
         "when sugar was expensive and hard to get. Its modern reputation as a &ldquo;healthier&rdquo; cake dates "
         "specifically to a 1970s marketing push, cream cheese frosting and all. "
         "<a href=\"/holiday/carrot-cake-day/\">Full holiday page &rarr;</a>"),
        ("the-day-the-music-died-day",
         "Marks the actual 1959 plane crash that killed Buddy Holly, Ritchie Valens, and the Big Bopper &mdash; and "
         "the seating arrangement that put them on the plane is its own grim story: Valens won his seat in a "
         "coin toss, and the Big Bopper, sick with the flu, took Waylon Jennings' spot. Jennings was Holly's "
         "bass player and would have been on that flight otherwise. <a href=\"/holiday/the-day-the-music-died-day/\">Full holiday page &rarr;</a>"),

        ("national-homemade-soup-day",
         "Soup is older than most food categories get credit for &mdash; archaeological evidence puts it back to "
         "roughly 6000 BC, involving boiled hippopotamus bones and taro. The word itself comes through French "
         "from a Germanic root meaning &ldquo;sop,&rdquo; as in bread dipped into liquid. "
         "<a href=\"/holiday/national-homemade-soup-day/\">Full holiday page &rarr;</a>"),
        ("thank-a-mailman-day",
         "The USPS delivers to over 160 million addresses, which puts the daily route of an average mail carrier "
         "in a different category of physical endurance than most desk jobs. Organized mail delivery isn't a "
         "modern idea, either &mdash; the Egyptians and Romans both ran their own systems thousands of years ago. "
         "<a href=\"/holiday/thank-a-mailman-day/\">Full holiday page &rarr;</a>"),

        ("chocolate-fondue-day",
         "Despite the Swiss reputation, chocolate fondue as most people know it was popularized in 1960s New York "
         "by Swiss restaurateur Konrad Egli &mdash; an import that got rebranded as tradition. The original fondue, "
         "dating to the 18th century, was savory and cheese-based; chocolate came along much later. "
         "<a href=\"/holiday/chocolate-fondue-day/\">Full holiday page &rarr;</a>"),
        ("world-nutella-day",
         "Founded in 2007 by an American blogger, not by Ferrero itself &mdash; the company only formally backed the "
         "day in 2015, eight years after fans started it without them. Nutella's actual origin traces to wartime "
         "Italy, when chocolate rationing forced Pietro Ferrero to stretch a small amount of cocoa with a lot of "
         "hazelnuts. <a href=\"/holiday/world-nutella-day/\">Full holiday page &rarr;</a>"),

        ("national-chopsticks-day",
         "Chopsticks started as cooking tools in ancient China over 4,000 years ago, long before they became "
         "eating utensils. About a third of the world's population uses them as their primary utensil today, and "
         "the regional differences are real &mdash; Japanese chopsticks are short and pointed, Chinese ones longer "
         "and blunt, Korean ones flat and metal. <a href=\"/holiday/national-chopsticks-day/\">Full holiday page &rarr;</a>"),
        ("national-frozen-yogurt-day",
         "Despite its 1970s American boom, frozen yogurt actually dates to the 1930s as a soft-serve product &mdash; "
         "it just took decades and a self-serve, build-your-own-cup model in the late 2000s to really catch on. "
         "<a href=\"/holiday/national-frozen-yogurt-day/\">Full holiday page &rarr;</a>"),

        ("national-fettuccine-alfredo-day",
         "Alfredo di Lelio invented the dish around 1908 in Rome for his own pregnant wife, and the original "
         "recipe has no cream in it at all &mdash; the creaminess comes purely from emulsifying butter with "
         "Parmigiano-Reggiano. It went global only after Mary Pickford and Douglas Fairbanks discovered it in "
         "Rome and brought it back to Hollywood. <a href=\"/holiday/national-fettuccine-alfredo-day/\">Full holiday page &rarr;</a>"),
        ("national-periodic-table-day",
         "Commemorates a lesser-known precursor: John Newlands' 1865 &ldquo;Law of Octaves,&rdquo; which noticed a "
         "periodicity in element properties years before Mendeleev's version became the standard. There are 118 "
         "confirmed elements today, with new ones still occasionally synthesized. "
         "<a href=\"/holiday/national-periodic-table-day/\">Full holiday page &rarr;</a>"),

        ("national-kite-flying-day",
         "Kites started in China over 2,800 years ago as military signaling devices, not toys &mdash; the "
         "recreational use came much later. Benjamin Franklin's famous 1752 lightning experiment used one, and "
         "the largest kite ever flown, launched in Kuwait, measured over 11,000 square feet. "
         "<a href=\"/holiday/national-kite-flying-day/\">Full holiday page &rarr;</a>"),
        ("national-potato-lovers-day",
         "The potato is the third-largest food crop in the world by consumption, behind only rice and wheat, and "
         "the Andes region alone is home to over 4,000 native varieties. The average American eats about 110 "
         "pounds of potatoes a year. <a href=\"/holiday/national-potato-lovers-day/\">Full holiday page &rarr;</a>"),

        ("national-pizza-day",
         "Americans eat roughly 350 slices of pizza every second, adding up to about 3 billion pizzas a year. The "
         "very first pizzeria, Antica Pizzeria Port'Alba, opened in Naples in 1738 &mdash; more than two and a half "
         "centuries before pepperoni became America's default topping. <a href=\"/holiday/national-pizza-day/\">Full holiday page &rarr;</a>"),
        ("read-in-the-bathtub-day",
         "Ancient Roman baths doubled as intellectual gathering spaces, so the pairing of bathing and reading has "
         "a longer pedigree than it looks. Modern waterproof e-readers have mostly solved the one real obstacle "
         "&mdash; a soggy paperback &mdash; that used to make this holiday more theoretical than practical. "
         "<a href=\"/holiday/read-in-the-bathtub-day/\">Full holiday page &rarr;</a>"),

        ("national-umbrella-day",
         "Invented in China over 4,000 years ago primarily for sun protection, not rain &mdash; the word itself "
         "comes from the Latin <em>umbra</em>, meaning shade. It took 18th-century Englishman Jonas Hanway years "
         "of public ridicule to normalize carrying one for rain. <a href=\"/holiday/national-umbrella-day/\">Full holiday page &rarr;</a>"),
        ("plimsoll-day",
         "Marks the birth of Samuel Plimsoll, whose campaign against dangerously overloaded &ldquo;coffin ships&rdquo; led "
         "directly to the 1876 Merchant Shipping Act and the mandatory Plimsoll Line &mdash; the marking on a ship's "
         "hull that still limits how heavily it can be loaded today, a century and a half later. "
         "<a href=\"/holiday/plimsoll-day/\">Full holiday page &rarr;</a>"),

        ("national-inventors-day",
         "Timed to Thomas Edison's birthday, who held over a thousand patents in his lifetime &mdash; a number that "
         "makes most modern inventors look underemployed by comparison. Reagan didn't formally proclaim the day "
         "until 1983, more than a century after Edison started patenting things. "
         "<a href=\"/holiday/national-inventors-day/\">Full holiday page &rarr;</a>"),
        ("white-t-shirt-day",
         "Marks the end of the 44-day Flint Sit-Down Strike against General Motors in 1937, a pivotal labor "
         "moment where workers occupied the factories rather than picketing outside them &mdash; a tactic that made "
         "it much harder for the company to bring in strikebreakers. <a href=\"/holiday/white-t-shirt-day/\">Full holiday page &rarr;</a>"),

        ("darwin-day",
         "Darwin shares his exact birthdate with Abraham Lincoln &mdash; both born February 12, 1809, an odd "
         "historical coincidence for two men who reshaped very different parts of the 19th century. His "
         "five-year voyage on HMS Beagle, especially the time in the Gal&aacute;pagos, is what actually built the "
         "observations behind <em>On the Origin of Species</em>. <a href=\"/holiday/darwin-day/\">Full holiday page &rarr;</a>"),
        ("plum-pudding-day",
         "Despite the name, traditional plum pudding contains no actual plums &mdash; &ldquo;plum&rdquo; was historically "
         "just a catch-all word for dried fruits like raisins and currants. It traces back to a 14th-century "
         "savory porridge called frumenty, which evolved over centuries into the flaming, brandy-doused dessert "
         "served today. <a href=\"/holiday/plum-pudding-day/\">Full holiday page &rarr;</a>"),

        ("galentines-day",
         "Invented, quite literally, by a fictional character: Leslie Knope on <em>Parks and Recreation</em> "
         "coined it in a 2010 episode, describing it simply as &ldquo;ladies celebrating ladies.&rdquo; It's one of the "
         "rare holidays on this calendar with a traceable single origin &mdash; a TV writers' room, not folklore. "
         "<a href=\"/holiday/galentines-day/\">Full holiday page &rarr;</a>"),
        ("world-radio-day",
         "UNESCO proclaimed this in 2011, choosing February 13th specifically because it's the anniversary of "
         "United Nations Radio's founding in 1946. Despite decades of newer media, radio still reaches an "
         "estimated 4 billion people worldwide. <a href=\"/holiday/world-radio-day/\">Full holiday page &rarr;</a>"),

        ("ferris-wheel-day",
         "Built to rival the Eiffel Tower, which had stolen the show at the 1889 Paris Exposition &mdash; the "
         "original Ferris wheel debuted at the 1893 Chicago World's Fair standing 264 feet tall with room for "
         "2,160 riders across 36 cars. Today's record holder, Dubai's Ain Dubai, is more than three times as "
         "tall. <a href=\"/holiday/ferris-wheel-day/\">Full holiday page &rarr;</a>"),
        ("valentine-s-day",
         "Traces back to layered, tangled origins &mdash; Roman fertility festivals, multiple early Christian "
         "martyrs named Valentine &mdash; that have almost nothing to do with the roughly 1 billion cards exchanged "
         "worldwide today. In Japan the custom runs opposite to the West: women give chocolate to men on this "
         "day, and men reciprocate a month later on White Day. <a href=\"/holiday/valentine-s-day/\">Full holiday page &rarr;</a>"),

        ("gumdrop-day",
         "Traditional gumdrops got their firm, chewy texture from gum arabic, a natural resin tapped from acacia "
         "trees &mdash; modern versions have mostly switched to gelatin or pectin instead. The name first shows up "
         "in print in the mid-1800s. <a href=\"/holiday/gumdrop-day/\">Full holiday page &rarr;</a>"),
        ("singles-awareness-day",
         "The unofficial abbreviation, S.A.D., is a deliberate joke about timing &mdash; landing the day right after "
         "Valentine's Day, functioning as an intentional counterweight to all that romantic pressure. Most people "
         "mark it with friends or personal hobbies rather than anything resembling loneliness. "
         "<a href=\"/holiday/singles-awareness-day/\">Full holiday page &rarr;</a>"),

        ("do-a-grouch-a-favor-day",
         "Purely a modern, internet-calendar invention with no traceable founder &mdash; its entire premise is doing "
         "something nice for the specifically grumpy people in your life. Oscar the Grouch gets cited constantly "
         "as the unofficial mascot. <a href=\"/holiday/do-a-grouch-a-favor-day/\">Full holiday page &rarr;</a>"),
        ("lithuanian-independence-day",
         "Marks the 1918 Act of Re-establishment, signed by twenty members of the Council of Lithuania after the "
         "country had spent over a century absorbed into the Russian Empire following the 1795 partition. Full "
         "international recognition took years after the signing, given the chaos across the region after World "
         "War I. <a href=\"/holiday/lithuanian-independence-day/\">Full holiday page &rarr;</a>"),

        ("cabbage-day",
         "A member of the same plant family as broccoli, cauliflower, and kale, with a cultivation history "
         "stretching back to ancient China and Egypt. Sauerkraut, its fermented form, was standard provisioning "
         "for sailors specifically because it prevented scurvy on long voyages. <a href=\"/holiday/cabbage-day/\">Full holiday page &rarr;</a>"),
        ("random-acts-of-kindness-day",
         "Run by an actual nonprofit, the Random Acts of Kindness Foundation, built on research showing that acts "
         "of kindness measurably boost happiness and reduce stress for both the giver and the receiver. The bar "
         "for participation is deliberately low &mdash; holding a door counts as much as anything bigger. "
         "<a href=\"/holiday/random-acts-of-kindness-day/\">Full holiday page &rarr;</a>"),

        ("national-drink-wine-day",
         "Winemaking's earliest confirmed evidence comes from the country of Georgia, dated to around 6000 BCE "
         "&mdash; older than written language itself. There are over 10,000 distinct wine grape varietals worldwide, "
         "though commercial production leans on only a few dozen. <a href=\"/holiday/national-drink-wine-day/\">Full holiday page &rarr;</a>"),
        ("pluto-discovery-day",
         "Marks Clyde Tombaugh's 1930 discovery at the Lowell Observatory, made when he was just 24 &mdash; Pluto "
         "held planet status for 76 years before its 2006 reclassification as a dwarf planet. Its name came from "
         "an 11-year-old English schoolgirl, Venetia Burney, who suggested the Roman god of the underworld. "
         "<a href=\"/holiday/pluto-discovery-day/\">Full holiday page &rarr;</a>"),

        ("national-chocolate-mint-day",
         "The &ldquo;After Eight,&rdquo; one of the flavor combination's most iconic products, was introduced by "
         "Rowntree &amp; Co. in 1962 &mdash; its thin, square shape was as much a branding decision as the flavor "
         "itself. <a href=\"/holiday/national-chocolate-mint-day/\">Full holiday page &rarr;</a>"),
        ("national-tug-of-war-day",
         "Was an official Olympic event from 1900 to 1920, a fact that surprises most people who only know it as "
         "a playground game. Good teams rely on synchronized rhythm and technique as much as raw strength, which "
         "isn't obvious from watching a match for the first thirty seconds. <a href=\"/holiday/national-tug-of-war-day/\">Full holiday page &rarr;</a>"),

        ("love-your-pet-day",
         "Backed by real data: roughly 66% of U.S. households now own a pet, and interacting with them measurably "
         "raises oxytocin levels and lowers blood pressure. The longevity record belongs to Bobi, a Portuguese "
         "Rafeiro who lived to 31 years and 165 days. <a href=\"/holiday/love-your-pet-day/\">Full holiday page &rarr;</a>"),
        ("muffin-day",
         "English and American muffins are almost unrelated foods sharing one name &mdash; English muffins are "
         "yeast-leavened and griddle-cooked, while American muffins are quick breads baked in individual molds. "
         "The earliest known written muffin recipe appears in a 1747 cookbook. <a href=\"/holiday/muffin-day/\">Full holiday page &rarr;</a>"),

        ("first-steam-locomotive-journey-day",
         "Marks Richard Trevithick's 1804 run on the Pen-y-darren tramway in Wales, hauling 10 tons of iron and "
         "70 passengers over 9 miles in about four hours &mdash; the literal birth of rail travel. The engine itself "
         "was too heavy for the era's brittle cast-iron rails, which kept breaking under it. "
         "<a href=\"/holiday/first-steam-locomotive-journey-day/\">Full holiday page &rarr;</a>"),
        ("national-sticky-bun-day",
         "Strongly associated with Pennsylvania Dutch cooking, where the buns are sometimes called &ldquo;schnecken&rdquo; "
         "&mdash; German for &ldquo;snails,&rdquo; a nod to their spiral shape. The caramel glaze bakes on the bottom of the "
         "pan and only ends up on top once the whole thing gets flipped after baking. "
         "<a href=\"/holiday/national-sticky-bun-day/\">Full holiday page &rarr;</a>"),

        ("dolly-the-sheep-day",
         "Marks the 1997 announcement of Dolly the sheep, the first mammal ever cloned from an adult cell rather "
         "than an embryonic one &mdash; a genuine scientific first that reopened the entire bioethics conversation. "
         "She was named for Dolly Parton, since the source cell came from a mammary gland. "
         "<a href=\"/holiday/dolly-the-sheep-day/\">Full holiday page &rarr;</a>"),
        ("national-margarita-day",
         "Nobody actually agrees on who invented the margarita &mdash; competing claims put its origin in both "
         "Mexico and the US sometime in the 1930s or '40s, and none of them have ever been settled. What isn't "
         "disputed is the recipe: tequila, lime juice, orange liqueur, salted rim. "
         "<a href=\"/holiday/national-margarita-day/\">Full holiday page &rarr;</a>"),

        ("curling-day-sweden",
         "Sweden's national curling day sits on top of a sport with real Olympic pedigree &mdash; full medal status "
         "arrived at the 1998 Nagano Games, though it appeared as a demonstration sport decades earlier. The "
         "oldest known curling stones trace back to 16th-century Scotland. <a href=\"/holiday/curling-day-sweden/\">Full holiday page &rarr;</a>"),
        ("national-banana-bread-day",
         "Banana bread's popularity surge traces specifically to the Great Depression, when using overripe "
         "bananas instead of throwing them out actually mattered. It also needed a technical assist &mdash; widely "
         "available baking soda and powder in the 1930s, which made &ldquo;quick breads&rdquo; like this possible in the "
         "first place. <a href=\"/holiday/national-banana-bread-day/\">Full holiday page &rarr;</a>"),

        ("national-tortilla-chip-day",
         "Credited to Rebecca Webb Carranza, who in the late 1940s started cutting and frying tortillas her "
         "family's Los Angeles tortilleria would otherwise have thrown away &mdash; turning food waste into an "
         "entire snack category. <a href=\"/holiday/national-tortilla-chip-day/\">Full holiday page &rarr;</a>"),
        ("world-bartender-day",
         "The first cocktail recipe book, Jerry Thomas's &ldquo;The Bar-Tender's Guide,&rdquo; was published in 1862 &mdash; "
         "Thomas is still commonly called the father of American mixology. Flair bartending, the "
         "juggling-and-flipping style, owes its modern popularity almost entirely to the 1988 Tom Cruise movie "
         "&ldquo;Cocktail.&rdquo; <a href=\"/holiday/world-bartender-day/\">Full holiday page &rarr;</a>"),

        ("international-bionic-man-day",
         "Marks the 1973 premiere of &ldquo;The Six Million Dollar Man&rdquo; pilot movie &mdash; its catchphrase, "
         "&ldquo;better, stronger, faster,&rdquo; outlived the show itself by decades. The distinctive bionic sound "
         "effect was created simply by slowing down a recording of a reverberating noise. "
         "<a href=\"/holiday/international-bionic-man-day/\">Full holiday page &rarr;</a>"),
        ("national-clam-chowder-day",
         "The earliest known printed recipe dates to 1751, in the Boston Evening-Post &mdash; chowder has been a "
         "fixture of American cuisine since before the country existed. The New England-versus-Manhattan feud is "
         "old and genuinely heated: Maine's legislature once considered a bill to outlaw tomatoes in chowder "
         "entirely. <a href=\"/holiday/national-clam-chowder-day/\">Full holiday page &rarr;</a>"),

        ("left-sock-day",
         "The average person reportedly loses about 15 socks a year, which is enough of a pattern to have spawned "
         "genuine jokes about &ldquo;sock monsters&rdquo; living inside washing machines. This holiday specifically "
         "honors the leftover single sock, rather than the mismatched-pair trend some people wear intentionally "
         "on other days. <a href=\"/holiday/left-sock-day/\">Full holiday page &rarr;</a>"),
        ("pistachio-day",
         "Pistachios aren't technically nuts at all &mdash; botanically they're the seed of a drupe, the same fruit "
         "category as a peach, just with the flesh mostly gone. Cultivation dates back roughly 8,000 years in the "
         "Middle East, and the green color comes from retained chlorophyll. <a href=\"/holiday/pistachio-day/\">Full holiday page &rarr;</a>"),

        ("international-polar-bear-day",
         "Polar bears are classified as marine mammals, not land animals, given how much of their life depends on "
         "sea ice. Their fur isn't actually white &mdash; it's transparent and hollow, scattering light in a way "
         "that just looks white, while the skin underneath is black to better absorb heat. "
         "<a href=\"/holiday/international-polar-bear-day/\">Full holiday page &rarr;</a>"),
        ("national-strawberry-day",
         "Botanically, a strawberry isn't a true berry at all &mdash; it's an &ldquo;aggregate accessory fruit,&rdquo; and "
         "it's the only common fruit that carries its roughly 200 seeds on the outside rather than inside. "
         "California alone grows about 75% of the strawberries produced in the US. "
         "<a href=\"/holiday/national-strawberry-day/\">Full holiday page &rarr;</a>"),

        ("floral-design-day",
         "Marks the 1947 founding of the Rittner School of Floral Design in Boston, one of the longer-running "
         "institutions behind an art form that goes back to ancient Egyptian decoration. Japanese ikebana takes "
         "the opposite approach from most Western arranging &mdash; built around discipline and negative space "
         "rather than sheer volume of flowers. <a href=\"/holiday/floral-design-day/\">Full holiday page &rarr;</a>"),
        ("nylon-invention-day",
         "Marks Wallace Carothers' 1935 breakthrough at DuPont &mdash; the first fiber ever synthesized entirely "
         "from chemical compounds, not derived from a plant or animal at all. When nylon stockings launched in "
         "1940, millions of pairs reportedly sold out within hours. <a href=\"/holiday/nylon-invention-day/\">Full holiday page &rarr;</a>"),

        ("leap-day",
         "People born on this date are genuinely called &ldquo;leaplings,&rdquo; and the statistical odds of it "
         "happening are about 1 in 1,461. The old &ldquo;Ladies' Privilege&rdquo; tradition, where women were "
         "customarily allowed to propose marriage on this date, traces back to an Irish legend involving St. "
         "Bridget and St. Patrick. <a href=\"/holiday/leap-day/\">Full holiday page &rarr;</a>"),
        ("supermans-birthday",
         "DC Comics assigned Superman this date deliberately, making him a fictional leapling despite his "
         "real-world debut landing in April 1938's <em>Action Comics</em> #1. By the internal logic of the joke, "
         "he ages only one year for every four that pass on Earth. <a href=\"/holiday/supermans-birthday/\">Full holiday page &rarr;</a>"),
    ],
}

MARCH = {
    "month_num": 3,
    "month_name": "March",
    "url_slug": "march",
    "title": "The Complete Guide to March's Obscure Holidays | Obscure Holiday Calendar",
    "description": (
        "A complete, day-by-day guide to all 63 obscure and offbeat holidays in March — "
        "from National Peanut Butter Lover's Day to World Backup Day — with history, context, "
        "and links to the full write-up for each one."
    ),
    "h1": "The Complete Guide to March's Obscure Holidays",
    "date_published": "2026-07-28",
    "date_modified": "2026-07-28",
    "intro_html": """    <p>March moves from winter cleanup into spring, and its 63 obscure holidays follow the same arc &mdash;
    Pi Day and the Ides of March sit next to National Puppy Day and Plant a Flower Day. St. Patrick's Day is
    the headline, but the month also quietly hosts a UN forest-awareness day, a Roman assassination
    anniversary, and a holiday invented specifically to help you invent more holidays.</p>

    <p>This guide walks through all 63, day by day, with a bit of history or context for each one and a
    link to the full write-up &mdash; complete fun facts, ways to celebrate, and sourcing &mdash; on its own page.</p>""",
    "why_html": """    <p>March's holidays split fairly evenly between two things: genuine calendar dates carrying real
    historical weight &mdash; the Ides of March, Alexander Graham Bell's 1876 patent, the Girl Scouts' 1912
    founding, the first U.S. Navy submarine &mdash; and playful, openly invented modern observances like Be Nasty
    Day and International Goof Off Day. The month is also unusually numbers-literate, with Pi Day, National
    Grammar Day (a pun on the date itself, &ldquo;march forth&rdquo;), and World Mathematics Day all landing within a
    few days of each other.</p>""",
    "how_to_use_html": """    <p>Holidays are grouped by date below. Each entry gets a short original write-up &mdash; not a repeat
    of the fact sheet &mdash; plus a link to the full holiday page if you want the deeper dive: complete fun
    facts, ways to celebrate, and sourcing.</p>""",
    "about_html": """    <p>This guide is part of the Obscure Holiday Calendar project &mdash; the same database that powers
    the iOS and Android apps and the individual holiday pages on this site. It exists to give a single,
    readable overview of an entire month at once, instead of requiring 63 separate page visits.</p>""",
    "faq": [
        (
            "How many obscure holidays are there in March?",
            "63, spread across all 31 days — including World Sleep Day, which floats to the Friday before the "
            "March equinox each year rather than sitting on a fixed date.",
        ),
        (
            "What's the most historically significant holiday in March?",
            "The Ides of March (Mar 15) marks Julius Caesar's actual 44 BC assassination, and Alexander Graham "
            "Bell Day (Mar 7) marks his real 1876 telephone patent — two of the month's more solidly documented "
            "dates.",
        ),
        (
            "Are there a lot of food holidays in March?",
            "Yes — Oreo Cookie Day, National Sloppy Joe Day, Waffle Day, National Cocktail Day, International "
            "Potato Chip Day, and several more make up a good chunk of the month.",
        ),
        (
            "Where can I find the full history and fun facts for each holiday?",
            "Every holiday name in this guide links to its own dedicated page with a longer write-up, sourced "
            "fun facts, and ideas for how to celebrate.",
        ),
    ],
    "entries": [
        ("national-peanut-butter-lovers-day",
         "George Washington Carver gets credit for popularizing peanuts, but he didn't actually invent peanut "
         "butter &mdash; the first patent for a peanut paste process went to Marcellus Gilmore Edson of Montreal in "
         "1884. It takes roughly 540 peanuts to fill a standard 12-ounce jar. "
         "<a href=\"/holiday/national-peanut-butter-lovers-day/\">Full holiday page &rarr;</a>"),
        ("national-pig-day",
         "Founded in 1972 by sisters Ellen Stanley and Mary Lynne Rave with the explicit goal of giving &ldquo;the "
         "pig its due.&rdquo; The mud-wallowing reputation is mostly misunderstood &mdash; pigs are naturally clean "
         "animals, and the mud is just their version of sweat, regulating body temperature since they can't do "
         "it any other way. <a href=\"/holiday/national-pig-day/\">Full holiday page &rarr;</a>"),

        ("dr-seuss-day",
         "Timed to Theodor Geisel's birthday and mostly run through the National Education Association's Read "
         "Across America program. <em>Green Eggs and Ham</em> exists because of a bet &mdash; Geisel's editor wagered "
         "he couldn't write a book using only 50 distinct words, and he won. "
         "<a href=\"/holiday/dr-seuss-day/\">Full holiday page &rarr;</a>"),
        ("old-stuff-day",
         "Genuinely undecided about its own purpose &mdash; some treat it as a prompt to dig through old photos and "
         "heirlooms, others use it as permission to finally throw the old stuff out. No clear founder or origin, "
         "which is fitting for a holiday about the past. <a href=\"/holiday/old-stuff-day/\">Full holiday page &rarr;</a>"),

        ("national-anthem-day",
         "&ldquo;The Star-Spangled Banner&rdquo; didn't become the official U.S. anthem until 1931, well over a century "
         "after Francis Scott Key wrote the lyrics in 1814 &mdash; and he set them to the tune of a British drinking "
         "song. Only the first of its four stanzas gets sung in practice. "
         "<a href=\"/holiday/national-anthem-day/\">Full holiday page &rarr;</a>"),
        ("world-wildlife-day",
         "The date was chosen deliberately: March 3rd is the anniversary of CITES, the 1973 treaty that now "
         "regulates international trade in more than 38,000 species of animals and plants. The UN didn't "
         "formally proclaim the day itself until 2013, forty years after the treaty it commemorates. "
         "<a href=\"/holiday/world-wildlife-day/\">Full holiday page &rarr;</a>"),

        ("march-forth-day",
         "The entire holiday exists because of a pun &mdash; March 4th sounds like &ldquo;march forth,&rdquo; and that's "
         "genuinely the whole premise, repurposed every year as an informal prompt to finally start something. "
         "<a href=\"/holiday/march-forth-day/\">Full holiday page &rarr;</a>"),
        ("national-grammar-day",
         "Founded in 2008 by Martha Brockenbrough specifically to lean into the same pun as March Forth Day &mdash; "
         "&ldquo;march forth&rdquo; as a command for better sentence structure. A common activity is hunting for grammar "
         "mistakes on public signage, which is a surprisingly satisfying way to spend the day. "
         "<a href=\"/holiday/national-grammar-day/\">Full holiday page &rarr;</a>"),

        ("international-birdhouse-day",
         "Different bird species need genuinely different birdhouse dimensions &mdash; entry hole size alone can "
         "determine which species uses it and which predators can't get in. Building birdhouses also doubles as "
         "informal pest control, since many of the birds attracted feed on insects. "
         "<a href=\"/holiday/international-birdhouse-day/\">Full holiday page &rarr;</a>"),
        ("learn-what-your-name-means-day",
         "Names carry more encoded history than most people realize &mdash; many trace back to ancient occupations, "
         "characteristics, or social status, not just aesthetic preference. In some cultures the belief runs "
         "deeper still: a name isn't just a label but something thought to shape a person's fate. "
         "<a href=\"/holiday/learn-what-your-name-means-day/\">Full holiday page &rarr;</a>"),

        ("oreo-cookie-day",
         "Marks the exact day in 1912 that Nabisco sold the first Oreo. Over 450 billion have been sold since, "
         "making it the best-selling cookie of the entire 20th century &mdash; and the cookie-to-cream ratio is "
         "precisely 71% to 29%, which someone at some point actually measured. "
         "<a href=\"/holiday/oreo-cookie-day/\">Full holiday page &rarr;</a>"),
        ("world-mathematics-day",
         "The concept of zero wasn't a single invention &mdash; it was arrived at independently by both Mayan and "
         "Indian civilizations, continents apart with no contact between them. The word &ldquo;algebra&rdquo; comes from "
         "the Arabic <em>al-jabr</em>, meaning &ldquo;the reunion of broken parts.&rdquo; "
         "<a href=\"/holiday/world-mathematics-day/\">Full holiday page &rarr;</a>"),

        ("alexander-graham-bell-day",
         "Marks the day his telephone patent was granted in 1876 &mdash; but Bell himself reportedly refused to keep "
         "a telephone in his own study, considering it an intrusion on his work. His mother and wife were both "
         "deaf, which shaped his lifelong research into hearing and speech well beyond the telephone itself. "
         "<a href=\"/holiday/alexander-graham-bell-day/\">Full holiday page &rarr;</a>"),
        ("national-cereal-day",
         "Cornflakes were invented in 1894 by Dr. John Harvey Kellogg, originally as health food for patients at "
         "his sanitarium, not as a breakfast treat. More than 2.7 billion boxes of cereal get sold in the US "
         "alone every year, and the name traces back to Ceres, the Roman goddess of grain. "
         "<a href=\"/holiday/national-cereal-day/\">Full holiday page &rarr;</a>"),

        ("be-nasty-day",
         "Entirely tongue-in-cheek &mdash; the &ldquo;nastiness&rdquo; here means mischievous or rebellious, not actually "
         "unkind, more in the spirit of eating dessert first than any real transgression. Origins are murky, "
         "likely internet culture rather than any formal founder. <a href=\"/holiday/be-nasty-day/\">Full holiday page &rarr;</a>"),
        ("international-women-s-day",
         "Traces back to a 1910 proposal by Clara Zetkin at an international conference of working women in "
         "Copenhagen, with the first observance following in 1911. The UN didn't formally adopt March 8th until "
         "1975 &mdash; 65 years after Zetkin's original proposal. <a href=\"/holiday/international-women-s-day/\">Full holiday page &rarr;</a>"),

        ("get-over-it-day",
         "No clear founder, no formal recognition &mdash; just an internet-era prompt to consciously let go of a "
         "grudge or setback rather than carry it forward. The suggested methods (journaling, meditation) are "
         "genuinely standard advice dressed up as a holiday. <a href=\"/holiday/get-over-it-day/\">Full holiday page &rarr;</a>"),
        ("international-day-of-awesomeness",
         "Landed on this date at least partly because it's Chuck Norris's birthday, a figure whose entire "
         "internet-meme persona is built around exaggerated &ldquo;awesomeness.&rdquo; Beyond that pun, the holiday has "
         "no formal structure &mdash; just an invitation to notice something good. "
         "<a href=\"/holiday/international-day-of-awesomeness/\">Full holiday page &rarr;</a>"),

        ("first-greenback-day",
         "Marks March 10, 1862, when the Legal Tender Act let the Union print paper currency to help finance the "
         "Civil War without relying entirely on gold and silver. The green ink on the back wasn't decorative &mdash; "
         "it was specifically chosen to make counterfeiting harder. <a href=\"/holiday/first-greenback-day/\">Full holiday page &rarr;</a>"),
        ("national-mario-day",
         "The date is a visual pun: &ldquo;MAR10&rdquo; looks like &ldquo;MARIO.&rdquo; Mario didn't start as a plumber, either &mdash; "
         "he debuted as a carpenter in 1981's <em>Donkey Kong</em> under the name &ldquo;Jumpman,&rdquo; and only became a "
         "plumber in 1983's <em>Mario Bros.</em> to fit the game's underground pipe setting. "
         "<a href=\"/holiday/national-mario-day/\">Full holiday page &rarr;</a>"),

        ("national-promposal-day",
         "The word is a blend of &ldquo;prom&rdquo; and &ldquo;proposal,&rdquo; and the trend escalated fast &mdash; from a simple "
         "in-person ask in the early 2000s to elaborate, sometimes viral public spectacles involving flash mobs "
         "and themed costumes. <a href=\"/holiday/national-promposal-day/\">Full holiday page &rarr;</a>"),
        ("worship-of-tools-day",
         "The earliest known tools are stone implements over 3 million years old, found in East Africa &mdash; older "
         "than modern humans themselves. Several ancient civilizations treated tools as gifts from the gods "
         "rather than human inventions. <a href=\"/holiday/worship-of-tools-day/\">Full holiday page &rarr;</a>"),

        ("girl-scout-day",
         "Marks the exact founding date in 1912, when Juliette Gordon Low started the very first troop in "
         "Savannah, Georgia with just 18 girls. The organization now counts millions of members worldwide, all "
         "traceable back to that one small group. <a href=\"/holiday/girl-scout-day/\">Full holiday page &rarr;</a>"),
        ("plant-a-flower-day",
         "Several popular garden flowers &mdash; pansies, nasturtiums, daylilies &mdash; are actually edible, meaning this "
         "holiday overlaps a little with cooking. Planting native varieties specifically, rather than whatever "
         "looks nice, is what actually supports local bee and butterfly populations. "
         "<a href=\"/holiday/plant-a-flower-day/\">Full holiday page &rarr;</a>"),

        ("good-samaritan-day",
         "Draws directly from the biblical parable in the Gospel of Luke, and is observed under different names "
         "in different countries, but the core idea stays consistent: recognizing people who help strangers with "
         "nothing to gain for themselves. <a href=\"/holiday/good-samaritan-day/\">Full holiday page &rarr;</a>"),
        ("national-earmuff-day",
         "Marks the exact 1877 patent date for Chester Greenwood's earmuffs &mdash; he was only 18 or 19, and "
         "reportedly invented them after his ears froze while ice skating, bending wire into loops and having "
         "his grandmother sew fur onto them. He went on to hold over 100 patents in his lifetime. "
         "<a href=\"/holiday/national-earmuff-day/\">Full holiday page &rarr;</a>"),
        ("world-sleep-day",
         "Deliberately scheduled the Friday before the March equinox rather than a fixed date, which means it "
         "moves slightly every year. About 60% of adults report sleep problems at some point in their lives, "
         "which is the statistic the entire day exists to address. <a href=\"/holiday/world-sleep-day/\">Full holiday page &rarr;</a>"),

        ("doodle-day",
         "Loosely piggybacks on Pi Day, since Google's own Pi Day doodles tend to lean creative and mathematical "
         "at once. Doodling isn't just idle habit, either &mdash; research links it to better concentration and "
         "memory retention during otherwise mundane tasks. <a href=\"/holiday/doodle-day/\">Full holiday page &rarr;</a>"),
        ("pi-day",
         "The date is a pun on the decimal itself &mdash; 3/14 matching &pi;'s first three digits &mdash; and it happens to "
         "also be Einstein's birthday, a coincidence organizers lean into constantly. The first large-scale "
         "celebration was organized in 1988 by physicist Larry Shaw at the San Francisco Exploratorium. "
         "<a href=\"/holiday/pi-day/\">Full holiday page &rarr;</a>"),

        ("ides-of-march",
         "Marks Julius Caesar's actual assassination in 44 BC, in a Senate meeting &mdash; the famous warning to "
         "&ldquo;beware the Ides of March&rdquo; is Shakespeare's dramatization of an older soothsayer legend, not a "
         "documented quote. The Ides fell on the 15th only for March, May, July, and October; every other month "
         "it landed on the 13th. <a href=\"/holiday/ides-of-march/\">Full holiday page &rarr;</a>"),
        ("world-contact-day",
         "Started in 1953 by a group of UFO enthusiasts, built around the idea of actively sending signals into "
         "space rather than just watching the sky and hoping. It's less about evidence and more about the ritual "
         "of trying to say hello. <a href=\"/holiday/world-contact-day/\">Full holiday page &rarr;</a>"),

        ("international-potato-chip-day",
         "Chef George Crum is credited with inventing the potato chip in 1853 in Saratoga Springs, New York &mdash; "
         "allegedly out of spite, after a customer kept sending fries back for being too thick. By 2018, chips "
         "had overtaken cookies and candy as America's most popular snack. "
         "<a href=\"/holiday/international-potato-chip-day/\">Full holiday page &rarr;</a>"),
        ("national-panda-day",
         "A newborn panda cub weighs about 3 to 5 ounces &mdash; roughly the size of a stick of butter &mdash; which is a "
         "strange contrast next to an adult that can eat 30 pounds of bamboo a day. Conservation efforts have "
         "actually worked here: pandas were downgraded from &ldquo;endangered&rdquo; to &ldquo;vulnerable&rdquo; as populations "
         "recovered. <a href=\"/holiday/national-panda-day/\">Full holiday page &rarr;</a>"),

        ("st-patricks-day",
         "Saint Patrick wasn't Irish &mdash; he was born in Roman Britain in the late 4th century. The color most "
         "associated with him wasn't originally green, either; it was blue, and green only took over later as "
         "the holiday's branding solidified. <a href=\"/holiday/st-patricks-day/\">Full holiday page &rarr;</a>"),
        ("submarine-day",
         "Marks the 1900 purchase of the USS Holland, the first submarine the U.S. Navy officially commissioned, "
         "designed by Irish-American engineer John Philip Holland. Top speed was about 5.5 knots and it could "
         "dive to 75 feet &mdash; modest by modern standards, but genuinely new at the time. "
         "<a href=\"/holiday/submarine-day/\">Full holiday page &rarr;</a>"),

        ("awkward-moments-day",
         "The word &ldquo;awkward&rdquo; traces back to the Old Norse <em>afugr</em>, meaning &ldquo;turned the wrong way&rdquo; &mdash; a "
         "fittingly literal etymology for a feeling that's fundamentally about being out of sync. Studies suggest "
         "that naming an awkward moment out loud tends to defuse it rather than make it worse. "
         "<a href=\"/holiday/awkward-moments-day/\">Full holiday page &rarr;</a>"),
        ("national-sloppy-joe-day",
         "Traces to a 1930s diner in Key West, Florida, allegedly invented by a man named Joe as a way to use up "
         "leftover ground beef &mdash; hence the name. The average serving runs around 500 calories, which is a lot "
         "of nutritional information for something this messy. <a href=\"/holiday/national-sloppy-joe-day/\">Full holiday page &rarr;</a>"),

        ("national-lets-laugh-day",
         "Children reportedly laugh hundreds of times a day; adults average just 15 to 20, which is the entire "
         "gap this holiday exists to close. A real laugh engages the diaphragm and facial muscles enough to "
         "function as a light cardio workout. <a href=\"/holiday/national-lets-laugh-day/\">Full holiday page &rarr;</a>"),
        ("poultry-day",
         "Chicken is the most consumed meat on Earth, ahead of both pork and beef, and a single laying hen can "
         "produce over 300 eggs a year. Turkeys were domesticated in Mesoamerica long before Europeans ever set "
         "foot there. <a href=\"/holiday/poultry-day/\">Full holiday page &rarr;</a>"),

        ("international-day-of-happiness",
         "Established by the UN in 2012, built around the idea that happiness is a legitimate policy goal, not "
         "just a private feeling &mdash; some countries now track a formal &ldquo;Gross National Happiness&rdquo; metric "
         "alongside GDP. <a href=\"/holiday/international-day-of-happiness/\">Full holiday page &rarr;</a>"),
        ("national-alien-abduction-day",
         "The modern abduction narrative largely traces to a single case: the 1961 Betty and Barney Hill "
         "incident, one of the first widely publicized claims of its kind. Most reported accounts share oddly "
         "specific common elements &mdash; missing time, bright lights, medical exams &mdash; that later shaped an entire "
         "genre of storytelling. <a href=\"/holiday/national-alien-abduction-day/\">Full holiday page &rarr;</a>"),

        ("international-day-of-forests",
         "Forests cover roughly 31% of the world's land and shelter about 80% of all terrestrial species, a "
         "disproportionate amount of the planet's biodiversity packed into less than a third of its surface. The "
         "UN only established this day in 2012. <a href=\"/holiday/international-day-of-forests/\">Full holiday page &rarr;</a>"),
        ("international-poetry-day",
         "Established by UNESCO in 1999, deliberately timed to land near the arrival of spring in the Northern "
         "Hemisphere, leaning on the symbolism of renewal. Poetry itself predates most other literary forms, "
         "with roots in ancient Mesopotamia and Greece. <a href=\"/holiday/international-poetry-day/\">Full holiday page &rarr;</a>"),

        ("international-goof-off-day",
         "Credited to comedian and author Joey Green in the early 1980s, and despite the grand &ldquo;International&rdquo; "
         "name, it's never been formally recognized as a public holiday anywhere. The entire point is the "
         "absence of a point &mdash; no productivity, no agenda, just downtime. "
         "<a href=\"/holiday/international-goof-off-day/\">Full holiday page &rarr;</a>"),
        ("world-frog-day",
         "There are over 6,000 known frog species, and some can jump more than 20 times their own body length. "
         "Scientists treat them as bioindicators &mdash; since frogs absorb water directly through their skin, their "
         "health tends to reflect their environment's health before other species show signs of trouble. "
         "<a href=\"/holiday/world-frog-day/\">Full holiday page &rarr;</a>"),

        ("national-puppy-day",
         "Founded in 2007 by Colleen Paige, the same person behind National Dog Day and National Cat Day. "
         "Puppies are born both blind and deaf, completely dependent on their mother for the first few weeks &mdash; "
         "and like human fingerprints, no two puppy nose prints are identical. "
         "<a href=\"/holiday/national-puppy-day/\">Full holiday page &rarr;</a>"),
        ("near-miss-day",
         "The &ldquo;near miss&rdquo; framing comes largely from aviation, where documented close calls have directly "
         "driven stricter safety regulations over the decades. The holiday's entire logic is that studying what "
         "almost went wrong is often more useful than studying what actually did. "
         "<a href=\"/holiday/near-miss-day/\">Full holiday page &rarr;</a>"),

        ("chocolate-covered-raisin-day",
         "Raisinets, the best-known brand, launched in 1927 from the Blumenthal Chocolate Company &mdash; old enough "
         "to predate sound in movies, a fitting coincidence for a snack now synonymous with movie theaters. The "
         "coating is applied through &ldquo;panning,&rdquo; tumbling raisins in a rotating drum while liquid chocolate is "
         "gradually added. <a href=\"/holiday/chocolate-covered-raisin-day/\">Full holiday page &rarr;</a>"),
        ("national-cocktail-day",
         "The word &ldquo;cocktail&rdquo; got its first formal print definition in an 1806 American newspaper: &ldquo;a "
         "stimulating liquor, composed of spirits of any kind, sugar, water, and bitters.&rdquo; Most of the classics "
         "still on menus today &mdash; the Old Fashioned, the Martini, the Manhattan &mdash; emerged decades later, in the "
         "late 19th and early 20th centuries. <a href=\"/holiday/national-cocktail-day/\">Full holiday page &rarr;</a>"),

        ("tolkien-reading-day",
         "The date isn't arbitrary &mdash; March 25th is the exact day the One Ring is destroyed and Sauron falls in "
         "<em>The Lord of the Rings</em>, chosen deliberately by The Tolkien Society. It's been running since 2003, "
         "with a different suggested theme picked each year. <a href=\"/holiday/tolkien-reading-day/\">Full holiday page &rarr;</a>"),
        ("waffle-day",
         "A holiday born from mishearing: Sweden's &ldquo;V&aring;ffeldagen&rdquo; (Waffle Day) sounds almost identical to "
         "&ldquo;V&aring;rfrudagen&rdquo; (Our Lady's Day, the Annunciation), and over time the linguistic coincidence quietly "
         "rewrote the tradition. It has nothing to do with America's National Waffle Day, which falls in August "
         "and marks the patenting of the waffle iron instead. <a href=\"/holiday/waffle-day/\">Full holiday page &rarr;</a>"),

        ("international-trampoline-day",
         "The word &ldquo;trampoline&rdquo; comes from the Spanish <em>trampol&iacute;n</em>, meaning diving board &mdash; fitting, "
         "since the device was originally built as acrobat training equipment in the 1930s, not a backyard toy. "
         "It became an official Olympic sport in 2000. <a href=\"/holiday/international-trampoline-day/\">Full holiday page &rarr;</a>"),
        ("make-up-your-own-holiday-day",
         "A genuinely recursive holiday &mdash; a day that exists specifically to invent more days like itself. There "
         "are already over 1,500 recognized national and international observance days in the US alone, many "
         "created by industry groups to promote a specific product, which this holiday openly invites you to do "
         "too. <a href=\"/holiday/make-up-your-own-holiday-day/\">Full holiday page &rarr;</a>"),

        ("national-joe-day",
         "Built entirely around a pun on the slang term for coffee, and running since at least the 1990s &mdash; the "
         "whole premise is buying a cup of &ldquo;joe&rdquo; for anyone you know actually named Joe. "
         "<a href=\"/holiday/national-joe-day/\">Full holiday page &rarr;</a>"),
        ("world-theatre-day",
         "Established in 1961 by the International Theatre Institute, with its first observance the following "
         "year. Every year a different prominent theatre figure writes an official message for the occasion &mdash; "
         "essentially theatre's version of a state-of-the-union address. <a href=\"/holiday/world-theatre-day/\">Full holiday page &rarr;</a>"),

        ("respect-your-cat-day",
         "Cats sleep an average of 15 hours a day, sometimes up to 20 &mdash; meaning most of a cat's life on this "
         "holiday is spent doing exactly what it does every other day. Their purring has a documented calming "
         "effect on humans nearby. <a href=\"/holiday/respect-your-cat-day/\">Full holiday page &rarr;</a>"),
        ("something-on-a-stick-day",
         "The concept goes back much further than the corn dog or lollipop &mdash; ancient Egyptian meat skewers, "
         "enjoyed by pharaohs as early as 3000 BC, may be the earliest known food on a stick. The popsicle's "
         "origin is a genuine accident: 11-year-old Frank Epperson left a sugary drink with a stirring stick "
         "outside overnight in 1905, and it froze. <a href=\"/holiday/something-on-a-stick-day/\">Full holiday page &rarr;</a>"),

        ("piano-day",
         "The date isn't arbitrary &mdash; March 29th is the 88th day of the year, matching the 88 keys on a "
         "standard piano. Founded in 2015 by musician Nils Frahm, it's since grown into an occasion for free "
         "concerts held by musicians worldwide. <a href=\"/holiday/piano-day/\">Full holiday page &rarr;</a>"),
        ("smoke-and-mirrors-day",
         "The phrase comes directly from old stage magic, where literal smoke obscured the stage and mirrors "
         "created illusions &mdash; misdirection made physical before it became a metaphor. It's since become "
         "political and media shorthand for any deliberately misleading presentation. "
         "<a href=\"/holiday/smoke-and-mirrors-day/\">Full holiday page &rarr;</a>"),

        ("cacti-appreciation-day",
         "Some cacti can live for two centuries, and a single plant can store up to 200 liters of water, which is "
         "what lets them survive conditions that would kill nearly anything else. The saguaro, the tallest "
         "species, can top 40 feet &mdash; taller than most houses. <a href=\"/holiday/cacti-appreciation-day/\">Full holiday page &rarr;</a>"),
        ("virtual-vacation-day",
         "Gained real traction during the COVID-19 pandemic, when actual travel wasn't an option and virtual "
         "tours of places like the Louvre or NASA's Mars surface imagery filled the gap. It's also one of the "
         "few holidays on this calendar that's genuinely accessible to people with mobility limitations. "
         "<a href=\"/holiday/virtual-vacation-day/\">Full holiday page &rarr;</a>"),

        ("national-crayon-day",
         "The first Crayola crayons sold in 1903 for five cents a box &mdash; a price that undersells how big the "
         "product would eventually become, with Crayola now offering more than 120 distinct shades. The world's "
         "largest crayon, in Germany, measures 15 feet long. <a href=\"/holiday/national-crayon-day/\">Full holiday page &rarr;</a>"),
        ("world-backup-day",
         "Founded in 2011 by a group of tech enthusiasts, built around one blunt statistic: over 60% of people "
         "have never backed up their data at all. A single failure &mdash; hardware dying, accidental deletion, "
         "malware &mdash; can wipe out years of files with no warning. <a href=\"/holiday/world-backup-day/\">Full holiday page &rarr;</a>"),
    ],
}

APRIL = {
    "month_num": 4,
    "month_name": "April",
    "url_slug": "april",
    "title": "The Complete Guide to April's Obscure Holidays | Obscure Holiday Calendar",
    "description": (
        "A complete, day-by-day guide to all 60 obscure and offbeat holidays in April — "
        "from April Fools' Day to National Oatmeal Cookie Day — with history, context, and "
        "links to the full write-up for each one."
    ),
    "h1": "The Complete Guide to April's Obscure Holidays",
    "date_published": "2026-07-28",
    "date_modified": "2026-07-28",
    "intro_html": """    <p>April swings from April Fools' Day pranks straight into a month full of genuinely offbeat food,
    science, and pop-culture holidays &mdash; Bicycle Day marks the discovery of LSD, Talk Like Shakespeare Day
    lands on his actual birth and death date, and there's an entire holiday dedicated to lima beans getting a
    fair shake.</p>

    <p>This guide walks through all 60, day by day, with a bit of history or context for each one and a
    link to the full write-up &mdash; complete fun facts, ways to celebrate, and sourcing &mdash; on its own page.</p>""",
    "why_html": """    <p>A noticeable cluster of April's holidays are built on real, dated events rather than invented
    themes &mdash; Samuel Morse's birthday, Albert Hofmann's 1943 bicycle ride, the Cullen-Harrison Act ending
    Prohibition's beer ban, and Shakespeare's birth and death both landing on the same date. Food holidays run
    especially dense this month too, with pretzels, jelly beans, garlic, grilled cheese, and prime rib all
    getting their own day within a few weeks of each other.</p>""",
    "how_to_use_html": """    <p>Holidays are grouped by date below. Each entry gets a short original write-up &mdash; not a repeat
    of the fact sheet &mdash; plus a link to the full holiday page if you want the deeper dive: complete fun
    facts, ways to celebrate, and sourcing.</p>""",
    "about_html": """    <p>This guide is part of the Obscure Holiday Calendar project &mdash; the same database that powers
    the iOS and Android apps and the individual holiday pages on this site. It exists to give a single,
    readable overview of an entire month at once, instead of requiring 60 separate page visits.</p>""",
    "faq": [
        (
            "How many obscure holidays are there in April?",
            "60, spread across all 30 days.",
        ),
        (
            "What's the most unusual scientific holiday in April?",
            "Bicycle Day (Apr 19), marking Albert Hofmann's 1943 bike ride home after the first intentional LSD "
            "trip — a genuinely pivotal, if unconventional, date in the history of psychedelic research.",
        ),
        (
            "Are there a lot of food holidays in April?",
            "Yes — National Pretzel Day, National Grilled Cheese Sandwich Day, National Prime Rib Day, National "
            "Garlic Day, Deep Dish Pizza Day, and several more make up close to a third of the month.",
        ),
        (
            "Where can I find the full history and fun facts for each holiday?",
            "Every holiday name in this guide links to its own dedicated page with a longer write-up, sourced "
            "fun facts, and ideas for how to celebrate.",
        ),
    ],
    "entries": [
        ("april-fools-day",
         "One popular theory traces the tradition to the 16th-century shift to the Gregorian calendar, when "
         "people still celebrating New Year's in late March/early April got mocked as &ldquo;fools&rdquo; for not "
         "updating. The prank has its own regional flavor in France, Italy, and French Canada, where it's a "
         "&ldquo;poisson d'avril&rdquo; &mdash; an April fish taped to someone's back. <a href=\"/holiday/april-fools-day/\">Full holiday page &rarr;</a>"),
        ("one-cent-day",
         "The U.S. Mint has repeatedly reported that producing a single penny costs more than one cent, which "
         "makes this holiday's entire premise a little bittersweet. Pennies minted after 1982 are actually 97.5% "
         "zinc, just plated with a thin shell of copper. <a href=\"/holiday/one-cent-day/\">Full holiday page &rarr;</a>"),

        ("national-ferret-day",
         "The word &ldquo;ferret&rdquo; comes from the Latin <em>furittus</em>, meaning &ldquo;little thief&rdquo; &mdash; a fairly "
         "accurate name given their habit of stashing random objects. When excited, they perform something "
         "actually called a &ldquo;weasel war dance,&rdquo; an energetic bouncing routine. "
         "<a href=\"/holiday/national-ferret-day/\">Full holiday page &rarr;</a>"),
        ("national-peanut-butter-and-jelly-day",
         "The earliest known written PB&amp;J recipe appeared in 1901, in the Boston Cooking-School Magazine &mdash; "
         "decades before it became a lunchbox staple. Its real popularity boost came during World War II, when "
         "both ingredients were cheap, nutritious, and easy to ship as rations. "
         "<a href=\"/holiday/national-peanut-butter-and-jelly-day/\">Full holiday page &rarr;</a>"),

        ("find-a-rainbow-day",
         "A rainbow is only visible under one specific condition: the sun has to be behind you and water droplets "
         "in front of you. What looks like an arc from the ground is actually a full circle &mdash; the horizon "
         "just blocks the bottom half. <a href=\"/holiday/find-a-rainbow-day/\">Full holiday page &rarr;</a>"),
        ("world-party-day",
         "Traces to a 1996 science fiction novel, &ldquo;Skipping Towards Gomorrah,&rdquo; which floated the idea that if "
         "the entire planet partied simultaneously, nobody would be free to start a conflict. It's stayed purely "
         "grassroots ever since, with zero official government backing anywhere. "
         "<a href=\"/holiday/world-party-day/\">Full holiday page &rarr;</a>"),

        ("tell-a-lie-day",
         "Functions as a kind of unofficial sequel to April Fools' &mdash; a second chance at harmless deception for "
         "anyone who missed the 1st. The entire spirit is storytelling and exaggeration, not anything meant to "
         "actually mislead someone. <a href=\"/holiday/tell-a-lie-day/\">Full holiday page &rarr;</a>"),
        ("world-rat-day",
         "Founded in 2002 by rat enthusiasts specifically to correct the animal's reputation &mdash; pet rats are "
         "genuinely fastidious, spending hours a day grooming themselves and each other. They're also trainable "
         "enough to learn their own names and navigate mazes. <a href=\"/holiday/world-rat-day/\">Full holiday page &rarr;</a>"),

        ("deep-dish-pizza-day",
         "Credited to Pizzeria Uno in Chicago in 1943, and the assembly order is inverted from a normal pizza on "
         "purpose &mdash; cheese goes directly on the crust first, then toppings, with the chunky tomato sauce "
         "layered on top last specifically to keep the cheese from burning. "
         "<a href=\"/holiday/deep-dish-pizza-day/\">Full holiday page &rarr;</a>"),
        ("go-for-broke-day",
         "The phrase became famous as the motto of the 442nd Regimental Combat Team, a Japanese-American unit "
         "that became one of the most decorated in U.S. military history during World War II &mdash; a much heavier "
         "history than the holiday's casual &ldquo;take a risk&rdquo; framing usually acknowledges. "
         "<a href=\"/holiday/go-for-broke-day/\">Full holiday page &rarr;</a>"),

        ("new-beers-eve",
         "Marks the eve of the Cullen-Harrison Act taking effect in 1933, which let Americans legally buy beer "
         "again for the first time in over a decade &mdash; Roosevelt signed it with the famously understated line, "
         "&ldquo;I think this would be a good time for a beer.&rdquo; <a href=\"/holiday/new-beers-eve/\">Full holiday page &rarr;</a>"),
        ("tartan-day",
         "Marks the 1320 signing of the Declaration of Arbroath, a letter asserting Scotland's independence to "
         "Pope John XXII &mdash; a genuinely old document to anchor a holiday that's actually quite recent. It "
         "started in Canada in the 1980s, and the U.S. only formally recognized it via a 1998 Senate resolution. "
         "<a href=\"/holiday/tartan-day/\">Full holiday page &rarr;</a>"),

        ("national-beer-day",
         "Marks the actual effective date of the Cullen-Harrison Act, the day after New Beer's Eve &mdash; breweries "
         "reportedly sold 1.5 million barrels on this single day in 1933. The modern celebration is much younger, "
         "started as a social media push in 2007 by two guys in Richmond, Virginia. "
         "<a href=\"/holiday/national-beer-day/\">Full holiday page &rarr;</a>"),
        ("no-housework-day",
         "No formal origin, no founder &mdash; just a shared cultural agreement that skipping chores for one day is "
         "worth its own holiday. The suggested activities are refreshingly unambitious: order takeout, read, or "
         "just do nothing. <a href=\"/holiday/no-housework-day/\">Full holiday page &rarr;</a>"),

        ("draw-a-picture-of-a-bird-day",
         "Bird illustration has real scientific weight behind it &mdash; John James Audubon's &ldquo;The Birds of "
         "America&rdquo; (1827&ndash;1838) remains a foundational ornithological reference, not just decorative art. "
         "<a href=\"/holiday/draw-a-picture-of-a-bird-day/\">Full holiday page &rarr;</a>"),
        ("zoo-lovers-day",
         "The world's oldest continuously operating zoo, Vienna's Tiergarten Sch&ouml;nbrunn, has been open since "
         "1752. Modern accredited zoos run actual breeding programs for endangered species and sometimes "
         "reintroduce animals to the wild. <a href=\"/holiday/zoo-lovers-day/\">Full holiday page &rarr;</a>"),

        ("name-yourself-day",
         "Purely symbolic &mdash; unlike a legal name change, this is entirely about imagining a different identity "
         "for a day, not making it official. Explicitly framed as a &ldquo;wacky holiday&rdquo; rather than anything "
         "formally recognized. <a href=\"/holiday/name-yourself-day/\">Full holiday page &rarr;</a>"),
        ("unicorn-day",
         "The unicorn has been Scotland's official national animal since the 15th century, which is a strange "
         "bit of trivia for a mythical creature. The earliest known depiction of something unicorn-like dates "
         "back to the Indus Valley Civilization, roughly 2500&ndash;1900 BC. "
         "<a href=\"/holiday/unicorn-day/\">Full holiday page &rarr;</a>"),

        ("national-cinnamon-crescent-day",
         "The word &ldquo;croissant&rdquo; is literally French for &ldquo;crescent,&rdquo; a direct reference to the shape rather "
         "than a brand name. Cinnamon itself is one of the oldest spices in continuous use, appearing in both "
         "culinary and medicinal contexts for thousands of years. <a href=\"/holiday/national-cinnamon-crescent-day/\">Full holiday page &rarr;</a>"),
        ("national-siblings-day",
         "Founded in 1995 by Claudia Evart, who chose the date specifically in memory of her late sister, Lisette "
         "&mdash; a genuinely personal origin story rather than an invented marketing holiday. Multiple U.S. "
         "presidents have issued proclamations recognizing it since. <a href=\"/holiday/national-siblings-day/\">Full holiday page &rarr;</a>"),

        ("barbershop-quartet-day",
         "Marks the 1938 founding of what's now the Barbershop Harmony Society in Tulsa, Oklahoma. The style's "
         "signature effect, the &ldquo;ringing chord,&rdquo; comes from four voices tuning pure intervals so precisely "
         "that the overtones create the illusion of extra voices singing along. "
         "<a href=\"/holiday/barbershop-quartet-day/\">Full holiday page &rarr;</a>"),
        ("national-pet-day",
         "Founded in 2006 by the same person behind National Puppy Day and National Dog Day, Colleen Paige &mdash; a "
         "recurring name across this calendar's pet-holiday cluster. Adoption promotion is baked into the "
         "mission as much as the general appreciation angle. <a href=\"/holiday/national-pet-day/\">Full holiday page &rarr;</a>"),

        ("big-wind-day",
         "Marks the 1934 measurement of a 231 mph wind gust atop Mount Washington, New Hampshire &mdash; the highest "
         "surface wind speed ever directly recorded by an instrument at the time, and it held that record for 62 "
         "years. The summit still averages 110 days a year with hurricane-force winds. "
         "<a href=\"/holiday/big-wind-day/\">Full holiday page &rarr;</a>"),
        ("national-grilled-cheese-sandwich-day",
         "Traces back further than people expect &mdash; early versions existed in ancient Rome &mdash; but the modern "
         "sandwich only took off in the 1920s, once sliced bread and cheap processed cheese became widely "
         "available. During the Great Depression it became a staple specifically because it was cheap and fast. "
         "<a href=\"/holiday/national-grilled-cheese-sandwich-day/\">Full holiday page &rarr;</a>"),

        ("national-make-lunch-count-day",
         "Actively promoted by the American Institute for Cancer Research, built around a simple, research-backed "
         "idea: stepping away from your desk to eat measurably reduces stress and improves digestion. "
         "<a href=\"/holiday/national-make-lunch-count-day/\">Full holiday page &rarr;</a>"),
        ("national-scrabble-day",
         "Marks inventor Alfred Butts' birthday. He determined the game's letter values and frequencies by "
         "literally counting letters on the front page of The New York Times. It was originally called "
         "&ldquo;Criss-Crosswords&rdquo; before the Scrabble rebrand. <a href=\"/holiday/national-scrabble-day/\">Full holiday page &rarr;</a>"),

        ("dolphin-day",
         "Dolphins have the second-highest brain-to-body weight ratio of any mammal, behind only humans, and they "
         "hunt cooperatively within complex social groups called pods. Their navigation system, echolocation, "
         "works on the same basic principle as sonar. <a href=\"/holiday/dolphin-day/\">Full holiday page &rarr;</a>"),
        ("look-up-at-the-sky-day",
         "The sky's blue color comes down to Rayleigh scattering &mdash; shorter blue wavelengths scatter more "
         "efficiently through the atmosphere than other colors. There are exactly 88 officially recognized "
         "constellations used to map the entire night sky. <a href=\"/holiday/look-up-at-the-sky-day/\">Full holiday page &rarr;</a>"),

        ("national-laundry-day",
         "Before washing machines, laundry meant beating clothes against rocks or scrubbing them on a washboard "
         "in a river. Dry cleaning was discovered by accident in the mid-19th century, when a French dye-works "
         "owner's maid spilled lamp oil on a tablecloth and it came out cleaner than the fabric around it. "
         "<a href=\"/holiday/national-laundry-day/\">Full holiday page &rarr;</a>"),
        ("rubber-eraser-day",
         "Before rubber erasers existed, people used wads of moist bread to lift pencil marks off paper. The "
         "material's name comes from chemist Joseph Priestley in 1770, who noticed it could literally &ldquo;rub out&rdquo; "
         "graphite. <a href=\"/holiday/rubber-eraser-day/\">Full holiday page &rarr;</a>"),

        ("day-of-the-mushroom",
         "Only about 140,000 of an estimated 2.2 to 3.8 million fungal species have ever been formally described. "
         "One single fungus, a honey mushroom in Oregon, spreads across thousands of acres underground and ranks "
         "among the largest living organisms on Earth. <a href=\"/holiday/day-of-the-mushroom/\">Full holiday page &rarr;</a>"),
        ("wear-your-pajamas-to-work-day",
         "Lands the day after the U.S. federal tax deadline, which is probably not a coincidence &mdash; a low-effort "
         "way to soften the stress of April 15th. Remote work has made the whole premise less of a novelty and "
         "more of an actual daily reality for a lot of people. <a href=\"/holiday/wear-your-pajamas-to-work-day/\">Full holiday page &rarr;</a>"),

        ("blah-blah-blah-day",
         "Traces to early-2000s internet culture, born as a reaction to information overload well before "
         "&ldquo;content fatigue&rdquo; became a mainstream complaint. Some participants mark it by attempting a full "
         "day of &ldquo;blah-free&rdquo; conversation. <a href=\"/holiday/blah-blah-blah-day/\">Full holiday page &rarr;</a>"),
        ("haiku-poetry-day",
         "The form evolved from <em>hokku</em>, the opening stanza of a longer linked-verse sequence called "
         "<em>renga</em>, before it split off as its own independent poem. Matsuo Bash&#333;, its most celebrated "
         "master, wrote in 17th-century Japan. <a href=\"/holiday/haiku-poetry-day/\">Full holiday page &rarr;</a>"),

        ("national-animal-crackers-day",
         "Originally branded &ldquo;Barnum's Animals Crackers&rdquo; in 1902, a direct nod to the Barnum and Bailey "
         "Circus. In 2018, Nabisco redesigned the box art in collaboration with PETA, depicting the animals "
         "roaming free on a savanna instead of caged. <a href=\"/holiday/national-animal-crackers-day/\">Full holiday page &rarr;</a>"),
        ("national-high-five-day",
         "The earliest documented high-five is credited to Dodgers players Dusty Baker and Glenn Burke, during a "
         "game on October 2, 1977. The holiday itself is much younger, started by University of Virginia students "
         "in 2002. <a href=\"/holiday/national-high-five-day/\">Full holiday page &rarr;</a>"),

        ("bicycle-day",
         "Marks Swiss chemist Albert Hofmann's 1943 bike ride home after accidentally discovering LSD's "
         "psychoactive effects &mdash; he'd synthesized the compound five years earlier but only realized what it did "
         "after a self-experiment gone further than planned. <a href=\"/holiday/bicycle-day/\">Full holiday page &rarr;</a>"),
        ("national-garlic-day",
         "Ancient Egyptians reportedly fed garlic to the laborers building the pyramids, believing it provided "
         "strength and stamina for the work. China alone now grows more than 75% of the world's garlic supply. "
         "<a href=\"/holiday/national-garlic-day/\">Full holiday page &rarr;</a>"),

        ("lima-bean-respect-day",
         "Named for Lima, Peru, where the bean was first cultivated roughly 8,000 years ago &mdash; a much older food "
         "than its reputation as a disliked side dish would suggest. In the American South, larger, creamier "
         "varieties go by an entirely different name: butterbeans. <a href=\"/holiday/lima-bean-respect-day/\">Full holiday page &rarr;</a>"),
        ("look-alike-day",
         "Entirely informal, with no founder or proclamation behind it &mdash; just a shared excuse to hunt for "
         "celebrity doppelg&auml;ngers or notice who resembles whom. <a href=\"/holiday/look-alike-day/\">Full holiday page &rarr;</a>"),

        ("bulldogs-are-beautiful-day",
         "The breed's original purpose was bull-baiting, a brutal blood sport &mdash; a jarring contrast to the "
         "gentle, loyal temperament modern Bulldogs are known for today. Their short-nosed structure makes them "
         "poor swimmers and prone to breathing issues. <a href=\"/holiday/bulldogs-are-beautiful-day/\">Full holiday page &rarr;</a>"),
        ("national-tea-day",
         "The UK's dedicated tea holiday, and worth remembering that all &ldquo;true&rdquo; teas &mdash; black, green, white, "
         "oolong, pu-erh &mdash; come from a single plant, Camellia sinensis. The afternoon tea tradition only dates "
         "to the mid-1800s. <a href=\"/holiday/national-tea-day/\">Full holiday page &rarr;</a>"),

        ("national-jelly-bean-day",
         "The earliest known jelly bean advertisement dates to 1861, encouraging people to mail them to Union "
         "soldiers during the Civil War. Ronald Reagan was famously fond of them, reportedly keeping jars in the "
         "Oval Office. <a href=\"/holiday/national-jelly-bean-day/\">Full holiday page &rarr;</a>"),
        ("national-picnic-day",
         "The word traces to the 17th-century French <em>pique-nique</em>, describing a potluck-style social "
         "gathering. Picnics became genuinely popular in Europe only after the French Revolution, when royal "
         "parks &mdash; previously off-limits &mdash; opened to the public. <a href=\"/holiday/national-picnic-day/\">Full holiday page &rarr;</a>"),

        ("lovers-day",
         "Marks Catalonia's Sant Jordi's Day, where the tradition runs opposite to most romantic holidays: men "
         "give women roses, women give men books, and city streets turn into open-air markets for both. "
         "<a href=\"/holiday/lovers-day/\">Full holiday page &rarr;</a>"),
        ("talk-like-shakespeare-day",
         "April 23rd is traditionally recognized as both Shakespeare's birth date (1564) and death date (1616), a "
         "rare symmetry that makes the date choice easy. He's credited with coining or popularizing hundreds of "
         "words still in everyday use, including &ldquo;eyeball&rdquo; and &ldquo;swagger.&rdquo; "
         "<a href=\"/holiday/talk-like-shakespeare-day/\">Full holiday page &rarr;</a>"),

        ("pig-in-a-blanket-day",
         "The earliest known mainstream American recipe appeared in Betty Crocker's Cooking for Kids in 1957. In "
         "the UK, the same name refers to something entirely different: sausages wrapped in bacon, not pastry. "
         "<a href=\"/holiday/pig-in-a-blanket-day/\">Full holiday page &rarr;</a>"),
        ("sauvignon-blanc-day",
         "The name literally translates to &ldquo;wild white,&rdquo; referencing its origins as an indigenous vine in "
         "southwestern France. It's also one of the two parent grapes of Cabernet Sauvignon. "
         "<a href=\"/holiday/sauvignon-blanc-day/\">Full holiday page &rarr;</a>"),

        ("national-zucchini-bread-day",
         "Zucchini is botanically a fruit, not a vegetable, since it develops from the plant's flower and carries "
         "seeds &mdash; the same technicality that applies to tomatoes. Its popularity as a quick bread surged "
         "specifically in the 1970s. <a href=\"/holiday/national-zucchini-bread-day/\">Full holiday page &rarr;</a>"),
        ("world-penguin-day",
         "Timed to coincide with the annual northward migration of Ad&eacute;lie penguins in Antarctica, not chosen "
         "arbitrarily. All 18 penguin species live exclusively in the Southern Hemisphere. "
         "<a href=\"/holiday/world-penguin-day/\">Full holiday page &rarr;</a>"),

        ("get-organized-day",
         "The average person reportedly spends an entire year of their life searching for lost items. Benjamin "
         "Franklin, with his famously rigid daily schedule, gets cited constantly as an early poster child for "
         "the concept. <a href=\"/holiday/get-organized-day/\">Full holiday page &rarr;</a>"),
        ("national-pretzel-day",
         "The pretzel's twisted shape is often traced to European monks around 610 AD, meant to resemble arms "
         "crossed in prayer. Pennsylvania alone produces roughly 80% of all pretzels made in the United States. "
         "<a href=\"/holiday/national-pretzel-day/\">Full holiday page &rarr;</a>"),

        ("morse-code-day",
         "Marks Samuel Morse's birthday. The very first message sent via his telegraph, in 1844, was &ldquo;What hath "
         "God wrought?&rdquo; &mdash; a deliberately dramatic opening line for what became a communication standard used "
         "for over a century afterward. <a href=\"/holiday/morse-code-day/\">Full holiday page &rarr;</a>"),
        ("national-prime-rib-day",
         "Cut from the primal rib section, typically ribs six through twelve, and traditionally cooked standing "
         "upright on its own bones, which double as a natural roasting rack. "
         "<a href=\"/holiday/national-prime-rib-day/\">Full holiday page &rarr;</a>"),

        ("national-cubicle-day",
         "The modern cubicle traces to a specific 1968 design, Robert Propst's &ldquo;Action Office II&rdquo; for Herman "
         "Miller &mdash; originally meant to offer more privacy and flexibility than the open-plan offices it "
         "replaced. <a href=\"/holiday/national-cubicle-day/\">Full holiday page &rarr;</a>"),
        ("superhero-day",
         "Deliberately broad in scope &mdash; covering both fictional comic-book characters and real people who act "
         "with courage or selflessness, rather than limiting the idea to capes and costumes. "
         "<a href=\"/holiday/superhero-day/\">Full holiday page &rarr;</a>"),

        ("shrimp-scampi-day",
         "&ldquo;Scampi&rdquo; originally refers to langoustines, small lobster-like crustaceans &mdash; Italian-American cooks "
         "adapted the garlic-butter-wine preparation to shrimp when langoustines weren't available. It's "
         "genuinely one of the fastest dishes to make, typically done in under 20 minutes. "
         "<a href=\"/holiday/shrimp-scampi-day/\">Full holiday page &rarr;</a>"),
        ("zipper-day",
         "The zipper's precursor, a &ldquo;Clasp Locker,&rdquo; was patented in 1893, but the reliable version people "
         "actually use dates to Gideon Sundback's 1917 &ldquo;Separable Fastener.&rdquo; The name wasn't coined until "
         "1923, by B.F. Goodrich. <a href=\"/holiday/zipper-day/\">Full holiday page &rarr;</a>"),

        ("bubble-tea-day",
         "Originated in 1980s Taiwan, with two competing tea houses both credited with inventing it. &ldquo;Boba&rdquo; "
         "technically refers just to the tapioca pearls, though it's now used interchangeably with &ldquo;bubble "
         "tea&rdquo; worldwide. <a href=\"/holiday/bubble-tea-day/\">Full holiday page &rarr;</a>"),
        ("national-oatmeal-cookie-day",
         "The earliest known recipe appeared in Fannie Merritt Farmer's 1896 Boston Cooking-School Cook Book. "
         "Quaker Oats did more than anyone to popularize it after that, printing recipes directly on their oat "
         "containers in the early 20th century. <a href=\"/holiday/national-oatmeal-cookie-day/\">Full holiday page &rarr;</a>"),
    ],
}

MAY = {
    "month_num": 5,
    "month_name": "May",
    "url_slug": "may",
    "title": "The Complete Guide to May's Obscure Holidays | Obscure Holiday Calendar",
    "description": (
        "A complete, day-by-day guide to all 63 obscure and offbeat holidays in May — "
        "from Lei Day to Save Your Hearing Day — with history, context, and links to the "
        "full write-up for each one."
    ),
    "h1": "The Complete Guide to May's Obscure Holidays",
    "date_published": "2026-07-28",
    "date_modified": "2026-07-28",
    "intro_html": """    <p>May moves fully into spring &mdash; Cinco de Mayo, Star Wars Day's pun, and a genuine cluster of drink
    holidays (Cosmopolitan, Moscato, Mint Julep, National Wine Day) all land within the same few weeks. It's
    also one of the more tribute-heavy months, with dedicated days for Douglas Adams (Towel Day), Mark Twain
    (Frog Jumping Day), and Edward Lear (National Limerick Day).</p>

    <p>This guide walks through all 63, day by day, with a bit of history or context for each one and a
    link to the full write-up &mdash; complete fun facts, ways to celebrate, and sourcing &mdash; on its own page.</p>""",
    "why_html": """    <p>A striking number of May's holidays are literary or pop-culture tributes tied to a specific
    person's birthday, death, or published work &mdash; Towel Day for Douglas Adams, National Limerick Day for
    Edward Lear, Frog Jumping Day for Mark Twain, Twilight Zone Day for Rod Serling, Talk Like Yoda Day for
    Star Wars. The month also runs unusually drink-heavy, with cocktails, wine, and beverages generally
    claiming more dedicated days than in almost any other month.</p>""",
    "how_to_use_html": """    <p>Holidays are grouped by date below. Each entry gets a short original write-up &mdash; not a repeat
    of the fact sheet &mdash; plus a link to the full holiday page if you want the deeper dive: complete fun
    facts, ways to celebrate, and sourcing.</p>""",
    "about_html": """    <p>This guide is part of the Obscure Holiday Calendar project &mdash; the same database that powers
    the iOS and Android apps and the individual holiday pages on this site. It exists to give a single,
    readable overview of an entire month at once, instead of requiring 63 separate page visits.</p>""",
    "faq": [
        (
            "How many obscure holidays are there in May?",
            "63, spread across all 31 days — including Tuba Day, which floats to the first Friday of the month "
            "rather than a fixed date.",
        ),
        (
            "What's the most literary month on the calendar?",
            "May has a real case for it — Towel Day (Douglas Adams), National Limerick Day (Edward Lear), and "
            "Frog Jumping Day (Mark Twain) all pay tribute to a specific author on a specific date.",
        ),
        (
            "Are there a lot of drink holidays in May?",
            "Yes — National Cosmopolitan Day, National Moscato Day, World Cocktail Day, National Wine Day, and "
            "National Mint Julep Day all land in May, more concentrated than any other month.",
        ),
        (
            "Where can I find the full history and fun facts for each holiday?",
            "Every holiday name in this guide links to its own dedicated page with a longer write-up, sourced "
            "fun facts, and ideas for how to celebrate.",
        ),
    ],
    "entries": [
        ("lei-day",
         "Conceived in 1927 by poet Don Blanding, with the now-famous slogan &ldquo;May Day is Lei Day&rdquo; contributed "
         "by columnist Grace Tower Warren. Real etiquette applies here &mdash; it's considered rude to refuse a lei "
         "when offered. <a href=\"/holiday/lei-day/\">Full holiday page &rarr;</a>"),
        ("may-day",
         "Carries two entirely separate identities on the same date: an ancient European spring fertility "
         "festival built around maypole dancing, and International Workers' Day, commemorating the 1886 "
         "Haymarket affair in Chicago. The U.S. deliberately moved its own Labor Day to September, partly to "
         "distance it from May Day's association with socialist and communist movements abroad. "
         "<a href=\"/holiday/may-day/\">Full holiday page &rarr;</a>"),
        ("tuba-day",
         "Founded in 1979 by tubist Harvey Phillips specifically to recognize an instrument that rarely gets a "
         "solo &mdash; the tuba provides the bass foundation for orchestras and marching bands but almost never the "
         "melody. It's the largest and lowest-pitched instrument in the entire modern brass family. "
         "<a href=\"/holiday/tuba-day/\">Full holiday page &rarr;</a>"),

        ("fire-day",
         "Humanity's controlled use of fire goes back over a million years, and it's hard to overstate the "
         "downstream effect &mdash; it reshaped diet, social structure, and how far early humans could migrate. "
         "Ancient cultures worldwide independently treated fire as something divine. "
         "<a href=\"/holiday/fire-day/\">Full holiday page &rarr;</a>"),
        ("world-tuna-day",
         "Formally established by UN resolution in December 2016, with the first actual observance following in "
         "2017. Bluefin tuna can swim in bursts up to 75 km/h, making them among the fastest fish in the ocean "
         "despite being warm-blooded, an unusual trait for fish generally. <a href=\"/holiday/world-tuna-day/\">Full holiday page &rarr;</a>"),

        ("national-two-different-colored-shoes-day",
         "Created in 2009 by Dr. Arlene Kaiser with a single, specific goal: normalizing visible individuality "
         "rather than blending in. The entire premise is deliberately low-stakes &mdash; mismatched shoes as a small, "
         "easy act of standing out. <a href=\"/holiday/national-two-different-colored-shoes-day/\">Full holiday page &rarr;</a>"),
        ("paranormal-day",
         "The word itself is just Greek prefix plus adjective &mdash; &ldquo;para&rdquo; (beyond) plus &ldquo;normal&rdquo; &mdash; a literal "
         "description rather than anything mystical. The category is broad enough to cover ghosts, UFOs, "
         "cryptids, and psychic phenomena all under one umbrella term. <a href=\"/holiday/paranormal-day/\">Full holiday page &rarr;</a>"),

        ("international-respect-for-chickens-day",
         "Chickens can recognize up to 100 different faces, human and chicken alike, and communicate through more "
         "than 20 distinct vocalizations &mdash; a level of social complexity most people don't associate with "
         "poultry. Established by United Poultry Concerns. <a href=\"/holiday/international-respect-for-chickens-day/\">Full holiday page &rarr;</a>"),
        ("star-wars-day",
         "The pun &mdash; &ldquo;May the Fourth be with you&rdquo; &mdash; actually predates the modern fan holiday by decades; "
         "the UK Conservative Party used it in a 1979 newspaper ad congratulating Margaret Thatcher on becoming "
         "Prime Minister. The first Lucasfilm-recognized celebration didn't happen until 2011, in Toronto. "
         "<a href=\"/holiday/star-wars-day/\">Full holiday page &rarr;</a>"),

        ("cinco-de-mayo",
         "Commonly mistaken for Mexico's Independence Day, which actually falls on September 16th &mdash; Cinco de "
         "Mayo instead marks a single, unlikely 1862 military victory at the Battle of Puebla, where an "
         "outnumbered, poorly equipped Mexican army beat a well-trained French force. It's a bigger holiday in "
         "the United States than in most of Mexico. <a href=\"/holiday/cinco-de-mayo/\">Full holiday page &rarr;</a>"),
        ("oyster-day",
         "A single oyster can filter up to 50 gallons of water a day, making them a meaningfully positive presence "
         "for water quality wherever they're farmed. They also change sex over their lifetime, typically starting "
         "male and later becoming female. <a href=\"/holiday/oyster-day/\">Full holiday page &rarr;</a>"),

        ("beverage-day",
         "Water and tea are, in that order, the two most consumed beverages on Earth &mdash; everything else, "
         "including coffee and soda, ranks below them globally. Coca-Cola and Pepsi both started out marketed in "
         "pharmacies as medicinal tonics. <a href=\"/holiday/beverage-day/\">Full holiday page &rarr;</a>"),
        ("international-no-diet-day",
         "Founded in 1992 by British feminist Mary Evans Young, who built the day directly out of her own "
         "experience with eating disorders and diet culture. The light blue ribbon that symbolizes it is a "
         "smaller-scale, lesser-known cousin of more famous awareness ribbons. "
         "<a href=\"/holiday/international-no-diet-day/\">Full holiday page &rarr;</a>"),

        ("national-cosmopolitan-day",
         "Went from cocktail-menu obscurity to global fixture almost entirely because of <em>Sex and the City</em> "
         "in the late 1990s. Bartender Cheryl Cook in Miami is often credited with inventing it in the mid-1980s, "
         "aiming to make a drink that looked beautiful in a martini glass. "
         "<a href=\"/holiday/national-cosmopolitan-day/\">Full holiday page &rarr;</a>"),
        ("roast-leg-of-lamb-day",
         "Technically only qualifies as &ldquo;lamb&rdquo; if the animal is under a year old &mdash; anything older is "
         "mutton, with a notably stronger flavor and tougher texture. The dish's association with spring goes "
         "back centuries. <a href=\"/holiday/roast-leg-of-lamb-day/\">Full holiday page &rarr;</a>"),

        ("coconut-cream-pie-day",
         "Coconuts are botanically classified as a fibrous drupe, not a true nut &mdash; the same category as a peach "
         "or a plum, just with a much tougher husk. &ldquo;Cream pie&rdquo; specifically describes a custard filling "
         "assembled without further baking. <a href=\"/holiday/coconut-cream-pie-day/\">Full holiday page &rarr;</a>"),
        ("no-socks-day",
         "No documented founder or origin &mdash; just a grassroots, social-media-driven holiday that leans on "
         "warmer spring weather. Going sockless genuinely does reduce moisture and odor buildup. "
         "<a href=\"/holiday/no-socks-day/\">Full holiday page &rarr;</a>"),

        ("lost-sock-memorial-day",
         "Runs on the same premise as the internet's beloved &ldquo;sock monster&rdquo; theory &mdash; a shared, "
         "only-half-joking explanation for a mystery nobody's actually solved. The more mundane real explanations "
         "involve socks getting caught in the washing machine drum. <a href=\"/holiday/lost-sock-memorial-day/\">Full holiday page &rarr;</a>"),
        ("national-moscato-day",
         "Made from Muscat grapes, one of the oldest cultivated grape varieties in the world, with a documented "
         "history spanning thousands of years. Moscato d'Asti, the lightly sparkling version from Italy's "
         "Piedmont region, is the style most people picture. <a href=\"/holiday/national-moscato-day/\">Full holiday page &rarr;</a>"),

        ("clean-up-your-room-day",
         "A cluttered space is measurably linked to higher stress and reduced focus, which is the actual research "
         "behind what otherwise sounds like a nagging holiday. Making the bed each morning gets cited constantly "
         "by productivity researchers. <a href=\"/holiday/clean-up-your-room-day/\">Full holiday page &rarr;</a>"),
        ("shrimp-day",
         "There are more than 2,000 known shrimp species worldwide, living in both fresh and salt water. As "
         "decapods, they're close relatives of crabs and lobsters, and some species can flee predators by "
         "flexing their tail in a rapid backward &ldquo;tail flip.&rdquo; <a href=\"/holiday/shrimp-day/\">Full holiday page &rarr;</a>"),

        ("eat-what-you-want-day",
         "Created by Thomas and Ruth Roy of Wellcat.com, a duo responsible for a surprising number of the "
         "internet's more whimsical unofficial holidays. The premise is explicitly framed around mindful "
         "indulgence, not just an excuse to abandon healthy eating outright. <a href=\"/holiday/eat-what-you-want-day/\">Full holiday page &rarr;</a>"),
        ("twilight-zone-day",
         "Marks Rod Serling's birthday. He personally wrote 92 of the original series' 156 episodes, an enormous "
         "workload for a single writer, and the show launched early appearances for future stars including "
         "William Shatner and Robert Redford. <a href=\"/holiday/twilight-zone-day/\">Full holiday page &rarr;</a>"),

        ("national-limerick-day",
         "Marks Edward Lear's birthday, whose 1846 &ldquo;A Book of Nonsense&rdquo; popularized the form &mdash; though Lear "
         "himself never actually called them limericks, preferring &ldquo;nonsense rhymes.&rdquo; "
         "<a href=\"/holiday/national-limerick-day/\">Full holiday page &rarr;</a>"),
        ("nutty-fudge-day",
         "Fudge's popular origin story is genuinely an accident &mdash; a batch of caramel that crystallized wrong, "
         "reportedly first made by a Vassar College student in 1886. The name likely comes from a term meaning "
         "&ldquo;a botched or clumsy job.&rdquo; <a href=\"/holiday/nutty-fudge-day/\">Full holiday page &rarr;</a>"),

        ("frog-jumping-day",
         "Marks the anniversary of Mark Twain's 1865 breakout short story, and Angels Camp, California still runs "
         "an actual competitive jumping-frog jubilee inspired by it. The all-time triple-jump record, 22 feet 7.5 "
         "inches, belongs to a frog fittingly named Rosie the Ribeter, set in 1986. "
         "<a href=\"/holiday/frog-jumping-day/\">Full holiday page &rarr;</a>"),
        ("world-cocktail-day",
         "Marks the exact date, May 13, 1806, that the word &ldquo;cocktail&rdquo; got its first published definition, "
         "in a small Hudson, New York newspaper. That original definition is essentially still the technical "
         "template for an Old Fashioned. <a href=\"/holiday/world-cocktail-day/\">Full holiday page &rarr;</a>"),

        ("dance-like-a-chicken-day",
         "The song actually originated in 1950s Switzerland as &ldquo;Der Ententanz&rdquo; &mdash; the Duck Dance, not the "
         "Chicken Dance &mdash; before American polka bands rebranded it in the late 1970s. Its largest recorded mass "
         "performance, at a 1994 Cincinnati Oktoberfest, drew roughly 72,000 participants. "
         "<a href=\"/holiday/dance-like-a-chicken-day/\">Full holiday page &rarr;</a>"),
        ("national-llama-awareness-day",
         "Llamas can see nearly 360 degrees around themselves without turning their heads, an unusually wide "
         "field of vision built for spotting predators. A full-grown llama can weigh up to 450 pounds and stand "
         "5 to 6 feet tall at the head. <a href=\"/holiday/national-llama-awareness-day/\">Full holiday page &rarr;</a>"),

        ("bring-flowers-to-someone-day",
         "Backed by real psychology: studies show receiving flowers produces a measurable mood boost that can "
         "last for several days, not just a momentary spike. <a href=\"/holiday/bring-flowers-to-someone-day/\">Full holiday page &rarr;</a>"),
        ("national-chocolate-chip-day",
         "The chocolate chip cookie was a genuine accident &mdash; Ruth Wakefield expected the chopped chocolate to "
         "melt smoothly into the dough at the Toll House Inn in 1938, and it simply didn't. Nestl&eacute; eventually "
         "acquired the rights to her recipe, paying her in a lifetime supply of chocolate rather than cash. "
         "<a href=\"/holiday/national-chocolate-chip-day/\">Full holiday page &rarr;</a>"),

        ("love-a-tree-day",
         "A single mature tree produces enough oxygen annually to support two people, a striking statistic for "
         "something that just stands still. Trees also share resources with each other through underground "
         "fungal networks researchers have nicknamed the &ldquo;wood wide web.&rdquo; "
         "<a href=\"/holiday/love-a-tree-day/\">Full holiday page &rarr;</a>"),
        ("wear-purple-for-peace-day",
         "Entirely grassroots and social-media-driven, with no central organizing body behind it &mdash; distinct "
         "from the separate Purple Day for epilepsy awareness observed in March. "
         "<a href=\"/holiday/wear-purple-for-peace-day/\">Full holiday page &rarr;</a>"),

        ("pack-rat-day",
         "The term comes directly from the <em>Neotoma</em> genus of actual woodrats, native to North America, "
         "which really do hoard shiny objects and trash alike in their nests. <a href=\"/holiday/pack-rat-day/\">Full holiday page &rarr;</a>"),
        ("world-baking-day",
         "The earliest known bread dates back roughly 14,400 years, baked by Natufian hunter-gatherers in what's "
         "now Jordan &mdash; bread predates farming itself. Ancient Egyptians were among the first to figure out "
         "yeast's leavening properties. <a href=\"/holiday/world-baking-day/\">Full holiday page &rarr;</a>"),

        ("no-dirty-dishes-day",
         "The first commercially successful dishwasher was invented in 1886 by Josephine Cochrane, motivated less "
         "by convenience than by frustration &mdash; she was tired of her servants chipping her fine china by hand. "
         "<a href=\"/holiday/no-dirty-dishes-day/\">Full holiday page &rarr;</a>"),
        ("visit-your-relatives-day",
         "Research consistently links strong extended-family ties to better mental and emotional well-being, "
         "giving this otherwise generic-sounding holiday real backing. It's deliberately flexible about format. "
         "<a href=\"/holiday/visit-your-relatives-day/\">Full holiday page &rarr;</a>"),

        ("may-ray-day",
         "About as loosely defined as holidays get &mdash; no founder, no origin story, just a vague, pleasant "
         "association with increasing sunshine as May progresses. <a href=\"/holiday/may-ray-day/\">Full holiday page &rarr;</a>"),
        ("world-plant-a-vegetable-garden-day",
         "Half an hour of gardening burns roughly 150 to 200 calories, comparable to a brisk walk. Many common "
         "&ldquo;vegetables&rdquo; &mdash; tomatoes, cucumbers, peppers, peas &mdash; are technically fruits botanically, since "
         "they develop from the plant's flower and contain seeds. <a href=\"/holiday/world-plant-a-vegetable-garden-day/\">Full holiday page &rarr;</a>"),

        ("be-a-millionaire-day",
         "The word &ldquo;millionaire&rdquo; itself only entered the English language in 1816, relatively recent for a "
         "concept people now treat as timeless. By the end of 2022, the global millionaire population had passed "
         "59 million people. <a href=\"/holiday/be-a-millionaire-day/\">Full holiday page &rarr;</a>"),
        ("pick-strawberries-day",
         "Timed to the peak of strawberry season, and botanically the fruit is unusual enough to deserve its own "
         "footnote: it's technically an &ldquo;aggregate accessory fruit,&rdquo; the only common fruit that carries its "
         "roughly 200 seeds on the outside. <a href=\"/holiday/pick-strawberries-day/\">Full holiday page &rarr;</a>"),

        ("i-need-a-patch-for-that-day",
         "Patching clothing to extend its life predates modern fast fashion by centuries. The same word now "
         "applies just as often to software &mdash; a &ldquo;patch&rdquo; fixing a bug is a direct linguistic descendant of "
         "a patch fixing a torn sleeve. <a href=\"/holiday/i-need-a-patch-for-that-day/\">Full holiday page &rarr;</a>"),
        ("talk-like-yoda-day",
         "Yoda's speech pattern has an actual linguistic name &mdash; Object-Subject-Verb syntax &mdash; which is "
         "genuinely rare across real human languages. Despite his prominence since 1980's <em>The Empire Strikes "
         "Back</em>, his species and home planet have never been officially revealed. "
         "<a href=\"/holiday/talk-like-yoda-day/\">Full holiday page &rarr;</a>"),

        ("buy-a-musical-instrument-day",
         "The oldest known musical instruments are flutes carved from bird bone and mammoth ivory, found in "
         "Germany and dated to roughly 42,000&ndash;43,000 years ago. Learning an instrument is linked to measurable "
         "improvements in memory, coordination, and stress reduction. <a href=\"/holiday/buy-a-musical-instrument-day/\">Full holiday page &rarr;</a>"),
        ("world-goth-day",
         "Started in 2009 in the UK, growing out of a single BBC Radio 6 Music feature on goth music before "
         "expanding into an international observance. Its explicit goal from the start was correcting "
         "stereotypes about the subculture. <a href=\"/holiday/world-goth-day/\">Full holiday page &rarr;</a>"),

        ("lucky-penny-day",
         "The tradition specifically requires the penny to be heads-up &mdash; a tails-up penny is sometimes "
         "considered bad luck unless you flip it over for the next person to find. "
         "<a href=\"/holiday/lucky-penny-day/\">Full holiday page &rarr;</a>"),
        ("world-turtle-day",
         "Founded in 2000 by American Tortoise Rescue, and turtles' evolutionary lineage stretches back over 200 "
         "million years. Their shell isn't a separate covering &mdash; it's fused directly to their skeleton, ribs and "
         "spine included, which is why a turtle can never actually leave it. "
         "<a href=\"/holiday/world-turtle-day/\">Full holiday page &rarr;</a>"),

        ("brothers-day",
         "Often attributed to C. Daniel Rhodes of Alabama, though like many modern informal holidays the exact "
         "origin isn't rigorously documented. It deliberately complements National Siblings Day in April and "
         "National Sisters Day in August. <a href=\"/holiday/brothers-day/\">Full holiday page &rarr;</a>"),
        ("national-scavenger-hunt-day",
         "The modern scavenger hunt is often credited to 1930s socialite Elsa Maxwell, who built elaborate "
         "versions into her famously extravagant parties. Digital versions like geocaching have since extended "
         "the format into a GPS-based hobby. <a href=\"/holiday/national-scavenger-hunt-day/\">Full holiday page &rarr;</a>"),

        ("national-wine-day",
         "The world's oldest known winery, discovered in Armenia's Areni-1 cave, dates back roughly 6,100 years "
         "&mdash; older than the pyramids. It takes about 2.5 pounds of grapes to produce a single standard 750ml "
         "bottle, and the fear of wine has an actual name: oenophobia. <a href=\"/holiday/national-wine-day/\">Full holiday page &rarr;</a>"),
        ("towel-day",
         "Falls exactly two weeks after Douglas Adams' death on May 11, 2001, and started organically on a fan "
         "forum called Binary Freedom rather than any official tribute. The premise comes straight from Adams' "
         "own text &mdash; a towel has &ldquo;immense psychological value&rdquo; for a hitchhiker. "
         "<a href=\"/holiday/towel-day/\">Full holiday page &rarr;</a>"),

        ("blueberry-cheesecake-day",
         "Cheesecake's history goes back to ancient Greece, where a version was reportedly served to athletes at "
         "the 776 BC Olympic Games for energy. Blueberries are one of the few fruits actually native to North "
         "America. <a href=\"/holiday/blueberry-cheesecake-day/\">Full holiday page &rarr;</a>"),
        ("national-paper-airplane-day",
         "Leonardo da Vinci reportedly sketched and tested early paper and parchment flying models around 1488, "
         "centuries before the folded-paper airplane most people know. The indoor flight-duration world record, "
         "29.2 seconds, was set by Takuo Toda in 2010. <a href=\"/holiday/national-paper-airplane-day/\">Full holiday page &rarr;</a>"),

        ("cellophane-tape-day",
         "Invented in 1930 by 3M engineer Richard Drew, who'd previously developed masking tape and pivoted the "
         "same adhesive concept into a transparent version. The &ldquo;Scotch&rdquo; brand name is rumored to trace back "
         "to a customer complaint accusing 3M of being stingy with adhesive. <a href=\"/holiday/cellophane-tape-day/\">Full holiday page &rarr;</a>"),
        ("sunscreen-day",
         "The first commercially successful sunscreen dates to 1944, created by Florida pharmacist Benjamin "
         "Green. SPF specifically measures how much more UV exposure protected skin can handle before burning "
         "compared to unprotected skin. <a href=\"/holiday/sunscreen-day/\">Full holiday page &rarr;</a>"),

        ("brisket-day",
         "The word traces back through Middle English to an Old Norse root meaning &ldquo;cartilage,&rdquo; a fittingly "
         "unglamorous etymology for a cut prized today for exactly the opposite reason. A full-packer brisket can "
         "take up to 18 hours to smoke properly. <a href=\"/holiday/brisket-day/\">Full holiday page &rarr;</a>"),
        ("national-hamburger-day",
         "The name likely traces to Hamburg, Germany, known for a fried minced-meat patty called Frikadeller, "
         "though the American sandwich itself is usually credited to Louis' Lunch in New Haven, Connecticut in "
         "1900. <a href=\"/holiday/national-hamburger-day/\">Full holiday page &rarr;</a>"),

        ("paperclip-day",
         "During World War II, Norwegians wore paperclips on their lapels as a quiet, deniable symbol of "
         "resistance against Nazi occupation, since displaying national symbols was banned outright. "
         "<a href=\"/holiday/paperclip-day/\">Full holiday page &rarr;</a>"),
        ("put-a-pillow-on-your-fridge-day",
         "No documented origin beyond internet-era word of mouth &mdash; the entire tradition is just placing a "
         "pillow on top of your refrigerator, with some claiming it brings good luck or financial fortune. "
         "<a href=\"/holiday/put-a-pillow-on-your-fridge-day/\">Full holiday page &rarr;</a>"),

        ("loomis-day",
         "An unusual entry: an unofficial nod to an actual cash-logistics company, not a folk tradition or "
         "invented joke. Loomis traces back to 1852, originally transporting gold and silver, and its armored "
         "trucks now move billions of dollars daily across more than 20 countries. "
         "<a href=\"/holiday/loomis-day/\">Full holiday page &rarr;</a>"),
        ("national-mint-julep-day",
         "The official drink of the Kentucky Derby since 1938, and Churchill Downs reportedly serves more than "
         "120,000 of them over just the two days of Derby weekend. The word &ldquo;julep&rdquo; traces back to the "
         "Arabic <em>gulab</em>, meaning rosewater. <a href=\"/holiday/national-mint-julep-day/\">Full holiday page &rarr;</a>"),

        ("macaroon-day",
         "Often confused with the French macaron, but the two are genuinely different desserts &mdash; the macaroon "
         "is coconut-based, the macaron almond-based, and only the name overlaps. Coconut macaroons are a popular "
         "Passover treat since they're naturally flourless. <a href=\"/holiday/macaroon-day/\">Full holiday page &rarr;</a>"),
        ("save-your-hearing-day",
         "The hair cells in your inner ear that convert sound into electrical signals don't regenerate once "
         "damaged, which is why hearing loss from noise exposure is permanent rather than temporary. Sustained "
         "exposure above 85 decibels is enough to cause that damage over time. "
         "<a href=\"/holiday/save-your-hearing-day/\">Full holiday page &rarr;</a>"),
    ],
}

JUNE = {
    "month_num": 6,
    "month_name": "June",
    "url_slug": "june",
    "title": "The Complete Guide to June's Obscure Holidays | Obscure Holiday Calendar",
    "description": (
        "A complete, day-by-day guide to all 62 obscure and offbeat holidays in June — "
        "from Dinosaur Day to National OOTD Day — with history, context, and links to the "
        "full write-up for each one."
    ),
    "h1": "The Complete Guide to June's Obscure Holidays",
    "date_published": "2026-07-28",
    "date_modified": "2026-07-28",
    "intro_html": """    <p>June opens summer with a genuinely wide mix &mdash; Go Skateboarding Day and World Giraffe Day both
    land on the solstice, National Doughnut Day honors WWI's &ldquo;Doughnut Lassies,&rdquo; and there's an entire day
    dedicated to slowing down and sauntering instead of rushing.</p>

    <p>This guide walks through all 62, day by day, with a bit of history or context for each one and a
    link to the full write-up &mdash; complete fun facts, ways to celebrate, and sourcing &mdash; on its own page.</p>""",
    "why_html": """    <p>A meaningful cluster of June's holidays are tied to the summer solstice specifically &mdash; Go
    Skateboarding Day, National Daylight Appreciation Day, and World Giraffe Day (a nod to the giraffe's long
    neck) all deliberately land on June 21st. The month also runs food-heavy in a specific direction: ice
    cream, fudge, pudding, and other cold or creamy desserts dominate as temperatures rise.</p>""",
    "how_to_use_html": """    <p>Holidays are grouped by date below. Each entry gets a short original write-up &mdash; not a repeat
    of the fact sheet &mdash; plus a link to the full holiday page if you want the deeper dive: complete fun
    facts, ways to celebrate, and sourcing.</p>""",
    "about_html": """    <p>This guide is part of the Obscure Holiday Calendar project &mdash; the same database that powers
    the iOS and Android apps and the individual holiday pages on this site. It exists to give a single,
    readable overview of an entire month at once, instead of requiring 62 separate page visits.</p>""",
    "faq": [
        (
            "How many obscure holidays are there in June?",
            "62, spread across all 30 days — including three that all land on the summer solstice (June 21).",
        ),
        (
            "What's notable about June 21st specifically?",
            "It's the summer solstice, and three separate holidays deliberately land there: Go Skateboarding "
            "Day, National Daylight Appreciation Day, and World Giraffe Day.",
        ),
        (
            "Are there a lot of dessert holidays in June?",
            "Yes — National Fudge Day, National Chocolate Pudding Day, National Chocolate Ice Cream Day, "
            "National Vanilla Milkshake Day, and several more make up a good chunk of the month.",
        ),
        (
            "Where can I find the full history and fun facts for each holiday?",
            "Every holiday name in this guide links to its own dedicated page with a longer write-up, sourced "
            "fun facts, and ideas for how to celebrate.",
        ),
    ],
    "entries": [
        ("dinosaur-day",
         "The word &ldquo;dinosaur&rdquo; &mdash; meaning &ldquo;terrible lizard&rdquo; &mdash; wasn't coined until 1842, by British "
         "paleontologist Richard Owen, decades after the last non-avian dinosaur went extinct. Birds are "
         "technically their direct descendants, meaning dinosaurs never fully disappeared. "
         "<a href=\"/holiday/dinosaur-day/\">Full holiday page &rarr;</a>"),
        ("national-say-something-nice-day",
         "Founded by former Alabama Governor Bob Riley, built on research showing that receiving genuine praise "
         "activates the same brain reward circuitry as receiving actual money. "
         "<a href=\"/holiday/national-say-something-nice-day/\">Full holiday page &rarr;</a>"),

        ("leave-the-office-early-day",
         "Runs counter to hustle-culture instinct: research consistently shows that fewer, more focused hours "
         "often beat longer workdays on actual productivity. <a href=\"/holiday/leave-the-office-early-day/\">Full holiday page &rarr;</a>"),
        ("national-rotisserie-chicken-day",
         "Costco alone sells more than 100 million rotisserie chickens a year, famously holding the price at "
         "$4.99 as a deliberate loss leader. Grocery store versions are often cooked in specialized convection "
         "ovens handling dozens of birds at once. <a href=\"/holiday/national-rotisserie-chicken-day/\">Full holiday page &rarr;</a>"),

        ("national-egg-day",
         "Eggs contain all nine essential amino acids, which technically qualifies them as a &ldquo;complete "
         "protein&rdquo; &mdash; a status most single foods don't earn. Shell color is purely a breed trait, not a "
         "nutrition signal. <a href=\"/holiday/national-egg-day/\">Full holiday page &rarr;</a>"),
        ("repeat-day",
         "A novelty holiday with no clear founder or origin, built entirely around the joke of doing or saying "
         "something twice. <a href=\"/holiday/repeat-day/\">Full holiday page &rarr;</a>"),

        ("hug-your-cat-day",
         "Cat purrs sit in the 25 to 150 Hertz range, a frequency band that's been linked to promoting bone "
         "density and healing. A group of cats is technically called a &ldquo;clowder,&rdquo; and they're capable of "
         "over 100 distinct vocalizations, compared to roughly 10 for dogs. <a href=\"/holiday/hug-your-cat-day/\">Full holiday page &rarr;</a>"),
        ("national-cheese-day",
         "The earliest known archaeological evidence of cheesemaking dates back more than 7,500 years, found in "
         "Kujawy, Poland. The largest cheese ever made weighed over 57,000 pounds, produced in Ontario, Canada in "
         "1995. <a href=\"/holiday/national-cheese-day/\">Full holiday page &rarr;</a>"),

        ("national-doughnut-day",
         "Started in 1938 in Chicago as a Salvation Army fundraiser, specifically honoring the WWI &ldquo;Doughnut "
         "Lassies&rdquo; who fried doughnuts for soldiers in the trenches of France. The doughnut hole itself is "
         "credited to 19th-century ship captain Hanson Gregory. <a href=\"/holiday/national-doughnut-day/\">Full holiday page &rarr;</a>"),
        ("national-gingerbread-day",
         "Gingerbread reached Europe in 992 AD, brought by the Armenian monk Gregory of Nicopolis. The gingerbread "
         "man specifically is often credited to Queen Elizabeth I, who reportedly had them baked in the likeness "
         "of visiting dignitaries. <a href=\"/holiday/national-gingerbread-day/\">Full holiday page &rarr;</a>"),
        ("national-moonshine-day",
         "The name comes directly from the practice of distilling under cover of night to dodge tax collectors "
         "and law enforcement. What was once strictly illicit corn whiskey &mdash; nicknamed &ldquo;white lightning&rdquo; &mdash; "
         "is now legally produced by licensed distilleries. <a href=\"/holiday/national-moonshine-day/\">Full holiday page &rarr;</a>"),

        ("drive-in-movie-day",
         "Marks the exact 1933 opening of the first patented drive-in, Richard Hollingshead Jr.'s &ldquo;Park-In "
         "Theaters&rdquo; in Camden, New Jersey. At their peak in the late 1950s, more than 4,000 drive-ins operated "
         "across the US. <a href=\"/holiday/drive-in-movie-day/\">Full holiday page &rarr;</a>"),
        ("national-yo-yo-day",
         "Marks Donald F. Duncan's birthday, who bought the yo-yo patent from Pedro Flores in 1929 and turned it "
         "into a household name. The word itself likely comes from the Philippines' Ilocano language, where "
         "ancient versions were reportedly used as hunting tools. <a href=\"/holiday/national-yo-yo-day/\">Full holiday page &rarr;</a>"),

        ("national-chocolate-ice-cream-day",
         "Chocolate ice cream is actually older than vanilla &mdash; one of the earliest known frozen chocolate "
         "recipes appears in a 1692 Italian collection by Antonio Latini. It still ranks as America's second most "
         "popular flavor, permanently trailing vanilla. <a href=\"/holiday/national-chocolate-ice-cream-day/\">Full holiday page &rarr;</a>"),
        ("vcr-day",
         "Sony's Betamax launched first, in 1975, but JVC's rival VHS format won the format war that followed a "
         "year later. The very last VCR manufacturer on Earth, Funai Electric of Japan, didn't stop production "
         "until July 2016. <a href=\"/holiday/vcr-day/\">Full holiday page &rarr;</a>"),

        ("best-friends-day",
         "Backed by genuine research linking strong friendships to better mental well-being, lower stress, and "
         "even increased longevity. <a href=\"/holiday/best-friends-day/\">Full holiday page &rarr;</a>"),
        ("name-your-poison-day",
         "The phrase started as bar slang, a colloquial way of asking someone what they're drinking, though the "
         "holiday extends the idea to any personal preference or decision. "
         "<a href=\"/holiday/name-your-poison-day/\">Full holiday page &rarr;</a>"),

        ("donald-duck-day",
         "Marks Donald's actual debut in 1934's &ldquo;The Wise Little Hen,&rdquo; where he first appeared as a side "
         "character before becoming Disney's most prolific star by film count. His voice was performed by the "
         "same actor, Clarence Nash, for over 50 years. <a href=\"/holiday/donald-duck-day/\">Full holiday page &rarr;</a>"),
        ("national-strawberry-rhubarb-pie-day",
         "Rhubarb is botanically a vegetable, though it's used almost exclusively as a fruit in desserts. Only "
         "the stalks are edible; the leaves contain enough oxalic acid to be genuinely toxic. "
         "<a href=\"/holiday/national-strawberry-rhubarb-pie-day/\">Full holiday page &rarr;</a>"),

        ("ballpoint-pen-day",
         "Marks L&aacute;szl&oacute; B&iacute;r&oacute;'s 1943 patent &mdash; he was a journalist who noticed newspaper ink dried fast "
         "without smudging, and adapted that same ink for a pen. <a href=\"/holiday/ballpoint-pen-day/\">Full holiday page &rarr;</a>"),
        ("national-iced-tea-day",
         "Its widespread American popularity is usually traced to the 1904 St. Louis World's Fair. It's South "
         "Carolina's official state beverage, and roughly 85% of all tea consumed in the US is served iced rather "
         "than hot. <a href=\"/holiday/national-iced-tea-day/\">Full holiday page &rarr;</a>"),

        ("make-life-beautiful-day",
         "Entirely unofficial, with a deliberately broad premise &mdash; noticing existing beauty and actively "
         "creating more of it. <a href=\"/holiday/make-life-beautiful-day/\">Full holiday page &rarr;</a>"),
        ("national-corn-on-the-cob-day",
         "Corn is botanically classified as both a grain and a fruit, since it develops from the plant's flower "
         "and contains seeds. Each strand of corn &ldquo;silk&rdquo; connects to exactly one kernel. "
         "<a href=\"/holiday/national-corn-on-the-cob-day/\">Full holiday page &rarr;</a>"),

        ("national-peanut-butter-cookie-day",
         "The signature crosshatch pattern isn't decorative &mdash; it flattens the dough enough for even baking, "
         "since peanut butter dough is too dense to spread on its own. <a href=\"/holiday/national-peanut-butter-cookie-day/\">Full holiday page &rarr;</a>"),
        ("superman-day",
         "Marks the cover date of <em>Action Comics</em> #1 in 1938, Superman's very first appearance. Early "
         "Superman couldn't actually fly &mdash; he could only &ldquo;leap an eighth of a mile&rdquo; and was described as "
         "fast, not airborne. <a href=\"/holiday/superman-day/\">Full holiday page &rarr;</a>"),

        ("national-weed-your-garden-day",
         "&ldquo;Weed&rdquo; is a genuinely subjective label &mdash; many plants people pull, like dandelions and purslane, "
         "are perfectly edible and nutritious. <a href=\"/holiday/national-weed-your-garden-day/\">Full holiday page &rarr;</a>"),
        ("random-acts-of-light-day",
         "A conceptual, grassroots observance closely related to the broader Random Acts of Kindness movement, "
         "without any formal founder behind it. <a href=\"/holiday/random-acts-of-light-day/\">Full holiday page &rarr;</a>"),

        ("national-bourbon-day",
         "Congress officially declared bourbon &ldquo;America's Native Spirit&rdquo; in 1964. To legally carry the name, "
         "it must be aged in new, charred oak barrels and made from a mash bill that's at least 51% corn. "
         "<a href=\"/holiday/national-bourbon-day/\">Full holiday page &rarr;</a>"),
        ("national-strawberry-shortcake-day",
         "&ldquo;Shortcake&rdquo; refers to a high-fat, crumbly texture, not a literal size &mdash; the same &ldquo;short&rdquo; used "
         "in shortbread. Recipes started appearing in American cookbooks by the mid-19th century. "
         "<a href=\"/holiday/national-strawberry-shortcake-day/\">Full holiday page &rarr;</a>"),

        ("nature-photography-day",
         "Established by the North American Nature Photography Association specifically to tie the art form to "
         "conservation, not just aesthetics. <a href=\"/holiday/nature-photography-day/\">Full holiday page &rarr;</a>"),
        ("smile-power-day",
         "Only one of the roughly 19 identified types of smile, the &ldquo;Duchenne smile,&rdquo; involves both the "
         "mouth and the eyes &mdash; the marker researchers use to distinguish a genuine smile from a polite one. "
         "<a href=\"/holiday/smile-power-day/\">Full holiday page &rarr;</a>"),

        ("fresh-veggies-day",
         "Carrots weren't originally orange &mdash; early varieties were purple, yellow, or white, with the orange "
         "cultivar only gaining dominance in the Netherlands during the 16th century. "
         "<a href=\"/holiday/fresh-veggies-day/\">Full holiday page &rarr;</a>"),
        ("national-fudge-day",
         "The first documented fudge sale happened at Vassar College in 1886, reportedly for 40 cents a pound. "
         "Mackinac Island, Michigan has built an entire tourism identity around it. <a href=\"/holiday/national-fudge-day/\">Full holiday page &rarr;</a>"),

        ("national-eat-your-vegetables-day",
         "The recommended adult daily intake sits at 2.5 to 3 cups, a target a significant share of the "
         "population reportedly doesn't hit. <a href=\"/holiday/national-eat-your-vegetables-day/\">Full holiday page &rarr;</a>"),
        ("world-crocodile-day",
         "Crocodilians as a group have existed for over 200 million years &mdash; older than dinosaurs. They also "
         "hold the record for strongest bite force of any living animal. <a href=\"/holiday/world-crocodile-day/\">Full holiday page &rarr;</a>"),

        ("go-fishing-day",
         "Many U.S. states and Canadian provinces run &ldquo;Free Fishing Days&rdquo; timed around this date, waiving "
         "license requirements to lower the barrier to trying it. <a href=\"/holiday/go-fishing-day/\">Full holiday page &rarr;</a>"),
        ("international-sushi-day",
         "Sushi technically refers to the vinegared rice, not the raw fish &mdash; raw fish served without rice is "
         "properly called sashimi. Much of the &ldquo;wasabi&rdquo; served outside Japan isn't real wasabi at all. "
         "<a href=\"/holiday/international-sushi-day/\">Full holiday page &rarr;</a>"),

        ("national-watch-day",
         "The first known wristwatch was made by Patek Philippe in 1868, for a Hungarian countess &mdash; well before "
         "wristwatches became standard. <a href=\"/holiday/national-watch-day/\">Full holiday page &rarr;</a>"),
        ("world-sauntering-day",
         "Founded in 1979 by W.T. Rabe on Mackinac Island, Michigan, deliberately conceived as a tongue-in-cheek "
         "counter to the then-popular National Running Day. <a href=\"/holiday/world-sauntering-day/\">Full holiday page &rarr;</a>"),

        ("national-ice-cream-soda-day",
         "Credited to Robert M. Green in 1874 Philadelphia, invented essentially by accident when he ran out of "
         "ice for his soda fountain and substituted ice cream instead. <a href=\"/holiday/national-ice-cream-soda-day/\">Full holiday page &rarr;</a>"),
        ("national-vanilla-milkshake-day",
         "The word &ldquo;milkshake&rdquo; first appeared in print in 1885 &mdash; describing an alcoholic whiskey-and-egg "
         "drink, nothing like the dessert it means today. <a href=\"/holiday/national-vanilla-milkshake-day/\">Full holiday page &rarr;</a>"),

        ("go-skateboarding-day",
         "Established in 2004 by the International Association of Skateboard Companies, and formally recognized "
         "by the U.S. Congress in 2007 via House Resolution 1290. The date is deliberate, timed to the summer "
         "solstice. <a href=\"/holiday/go-skateboarding-day/\">Full holiday page &rarr;</a>"),
        ("national-daylight-appreciation-day",
         "Deliberately timed to the summer solstice, the longest stretch of daylight in the Northern Hemisphere "
         "all year. The word &ldquo;solstice&rdquo; comes from Latin for &ldquo;sun&rdquo; plus &ldquo;to stand still.&rdquo; "
         "<a href=\"/holiday/national-daylight-appreciation-day/\">Full holiday page &rarr;</a>"),
        ("world-giraffe-day",
         "Also timed to the solstice, chosen as a symbolic nod to the giraffe's long neck by the Giraffe "
         "Conservation Foundation, which launched the day in 2014. No two giraffes share the same coat pattern. "
         "<a href=\"/holiday/world-giraffe-day/\">Full holiday page &rarr;</a>"),

        ("national-onion-rings-day",
         "A recipe for fried onions with parmesan appears in a British cookbook as early as 1802, an early "
         "ancestor of the modern version. <a href=\"/holiday/national-onion-rings-day/\">Full holiday page &rarr;</a>"),
        ("world-rainforest-day",
         "Rainforests cover only about 6% of Earth's surface but hold more than half of all known plant and "
         "animal species. Deforestation reportedly claims an area equivalent to 48 football fields every minute. "
         "<a href=\"/holiday/world-rainforest-day/\">Full holiday page &rarr;</a>"),

        ("let-it-go-day",
         "An informal wellness-community observance, and the concept of letting go as an emotional practice "
         "predates Disney's &ldquo;Frozen&rdquo; by a long stretch. <a href=\"/holiday/let-it-go-day/\">Full holiday page &rarr;</a>"),
        ("national-hydration-day",
         "The adult human body runs about 55&ndash;60% water, which is why even mild dehydration measurably impairs "
         "mood and concentration. <a href=\"/holiday/national-hydration-day/\">Full holiday page &rarr;</a>"),

        ("international-fairy-day",
         "Fairy folklore varies enormously by culture &mdash; benevolent nature guardians in some traditions, "
         "mischievous tricksters in others. <a href=\"/holiday/international-fairy-day/\">Full holiday page &rarr;</a>"),
        ("swim-a-lap-day",
         "Swimming engages nearly every major muscle group at once, and water's buoyancy makes it one of the few "
         "high-benefit workouts that's genuinely gentle on joints. <a href=\"/holiday/swim-a-lap-day/\">Full holiday page &rarr;</a>"),

        ("national-catfish-day",
         "Established by an actual 1987 presidential proclamation from Ronald Reagan, specifically to recognize "
         "the growing U.S. farm-raised catfish industry. <a href=\"/holiday/national-catfish-day/\">Full holiday page &rarr;</a>"),
        ("national-strawberry-parfait-day",
         "The word &ldquo;parfait&rdquo; is French for &ldquo;perfect,&rdquo; though the American dessert and the traditional "
         "French version barely resemble each other beyond sharing a name. <a href=\"/holiday/national-strawberry-parfait-day/\">Full holiday page &rarr;</a>"),

        ("national-chocolate-pudding-day",
         "&ldquo;Pudding&rdquo; originally described savory, often meat-based dishes &mdash; the sweet dessert meaning only "
         "took over in the 17th century. Instant chocolate pudding was introduced by Jell-O in 1947. "
         "<a href=\"/holiday/national-chocolate-pudding-day/\">Full holiday page &rarr;</a>"),
        ("national-coconut-day",
         "Despite the name, a coconut is botanically a single-seeded drupe, not a true nut. The word itself "
         "traces to a 16th-century Portuguese term meaning &ldquo;grinning face.&rdquo; "
         "<a href=\"/holiday/national-coconut-day/\">Full holiday page &rarr;</a>"),

        ("national-sunglasses-day",
         "The earliest known sunglasses were made by Inuit people from flattened walrus ivory, cut with thin "
         "slits to block glare off snow. The first mass-produced modern pair was sold on the Atlantic City "
         "boardwalk in 1929. <a href=\"/holiday/national-sunglasses-day/\">Full holiday page &rarr;</a>"),
        ("orange-blossom-day",
         "The essential oil extracted from these blossoms is called neroli, a genuinely prized ingredient in "
         "perfumery. The flowers themselves have long symbolized purity, which is why they turn up so often in "
         "bridal bouquets. <a href=\"/holiday/orange-blossom-day/\">Full holiday page &rarr;</a>"),

        ("national-tapioca-day",
         "Made from the cassava root, a South American tuber, and the word &ldquo;tapioca&rdquo; comes from the Tupi "
         "language of Brazil. It's the same starch behind bubble tea's chewy pearls as well as classic tapioca "
         "pudding. <a href=\"/holiday/national-tapioca-day/\">Full holiday page &rarr;</a>"),
        ("paul-bunyan-day",
         "Started as oral tradition among actual lumberjacks in the late 19th century, only reaching print "
         "decades later. Tall tales credit him and his blue ox, Babe, with carving out real geographical "
         "features like the Great Lakes. <a href=\"/holiday/paul-bunyan-day/\">Full holiday page &rarr;</a>"),

        ("hug-holiday-day",
         "A separate holiday from National Hugging Day, which lands in January &mdash; this one has no connection "
         "beyond the shared subject matter. <a href=\"/holiday/hug-holiday-day/\">Full holiday page &rarr;</a>"),
        ("national-camera-day",
         "The first permanent photograph, Nic&eacute;phore Ni&eacute;pce's &ldquo;View from the Window at Le Gras,&rdquo; dates to "
         "1826 or 1827. The first digital camera followed nearly 150 years later, built in 1975 by Kodak "
         "engineer Steven Sasson. <a href=\"/holiday/national-camera-day/\">Full holiday page &rarr;</a>"),

        ("meteor-watch-day",
         "Deliberately timed to the anniversary of the 1908 Tunguska event, which flattened over 2,000 square "
         "kilometers of Siberian forest &mdash; the largest impact event in recorded history. "
         "<a href=\"/holiday/meteor-watch-day/\">Full holiday page &rarr;</a>"),
        ("national-ootd-day",
         "The acronym stands for &ldquo;Outfit of the Day&rdquo; and exploded in popularity on Instagram and fashion "
         "blogs in the early 2010s, though documenting daily outfits predates social media by decades. "
         "<a href=\"/holiday/national-ootd-day/\">Full holiday page &rarr;</a>"),
    ],
}

JULY = {
    "month_num": 7,
    "month_name": "July",
    "url_slug": "july",
    "title": "The Complete Guide to July's Obscure Holidays | Obscure Holiday Calendar",
    "description": (
        "A complete, day-by-day guide to all 63 obscure and offbeat holidays in July — "
        "from Creative Ice Cream Flavors Day to National Raspberry Cake Day — with history, "
        "context, and links to the full write-up for each one."
    ),
    "h1": "The Complete Guide to July's Obscure Holidays",
    "date_published": "2026-07-28",
    "date_modified": "2026-07-28",
    "intro_html": """    <p>July runs on peak-summer energy &mdash; Moon Day marks Apollo 11's landing, World UFO Day leans into
    Roswell, and there's a genuine cluster of frozen-dessert holidays (peach ice cream, vanilla ice cream,
    creative ice cream flavors generally) stacked across the month.</p>

    <p>This guide walks through all 63, day by day, with a bit of history or context for each one and a
    link to the full write-up &mdash; complete fun facts, ways to celebrate, and sourcing &mdash; on its own page.</p>""",
    "why_html": """    <p>A surprising number of July's holidays anchor to real, dated history &mdash; the Apollo 11 landing,
    the Roswell incident's alleged date, Thoreau's birthday, the first Penguin paperback, and even a
    small-town Pennsylvania rain bet running unbroken since 1878. It's also, unsurprisingly, the most
    dessert- and drink-heavy stretch of the calendar, matching the actual peak of American summer.</p>""",
    "how_to_use_html": """    <p>Holidays are grouped by date below. Each entry gets a short original write-up &mdash; not a repeat
    of the fact sheet &mdash; plus a link to the full holiday page if you want the deeper dive: complete fun
    facts, ways to celebrate, and sourcing.</p>""",
    "about_html": """    <p>This guide is part of the Obscure Holiday Calendar project &mdash; the same database that powers
    the iOS and Android apps and the individual holiday pages on this site. It exists to give a single,
    readable overview of an entire month at once, instead of requiring 63 separate page visits.</p>""",
    "faq": [
        (
            "How many obscure holidays are there in July?",
            "63, spread across all 31 days.",
        ),
        (
            "What's the most historically significant holiday in July?",
            "Moon Day (Jul 20), marking the actual 1969 Apollo 11 landing — one of the most well-documented "
            "events any holiday on this calendar is tied to.",
        ),
        (
            "Are there a lot of food holidays in July?",
            "Yes — National Mac and Cheese Day, National Lasagna Day, National Hot Dog Day, National Cheesecake "
            "Day, and a whole cluster of ice cream and cocktail days make up a large share of the month.",
        ),
        (
            "Where can I find the full history and fun facts for each holiday?",
            "Every holiday name in this guide links to its own dedicated page with a longer write-up, sourced "
            "fun facts, and ideas for how to celebrate.",
        ),
    ],
    "entries": [
        ("creative-ice-cream-flavors-day",
         "Some of the more extreme documented ice cream flavors include lobster, garlic, bacon, and even "
         "haggis. Early Chinese versions of frozen dessert involved freezing milk and rice directly in snow, a "
         "far cry from a modern soft-serve machine. <a href=\"/holiday/creative-ice-cream-flavors-day/\">Full holiday page &rarr;</a>"),
        ("international-joke-day",
         "No documented founder or origin, despite being one of the more widely observed &ldquo;unofficial&rdquo; "
         "holidays on the calendar. The health case is real, though &mdash; laughter measurably reduces stress "
         "hormones. <a href=\"/holiday/international-joke-day/\">Full holiday page &rarr;</a>"),

        ("i-forgot-day",
         "A deliberately low-stakes holiday &mdash; no real tradition beyond acknowledging something you forgot and "
         "laughing about it instead of getting frustrated. <a href=\"/holiday/i-forgot-day/\">Full holiday page &rarr;</a>"),
        ("world-ufo-day",
         "Timed to the anniversary of the alleged 1947 Roswell incident, one of the most famous UFO claims in "
         "American history. The acronym itself has an official origin story &mdash; the U.S. Air Force coined "
         "&ldquo;UFO&rdquo; in 1953, replacing the earlier term &ldquo;flying saucer.&rdquo; <a href=\"/holiday/world-ufo-day/\">Full holiday page &rarr;</a>"),

        ("national-chocolate-wafer-day",
         "The word &ldquo;wafer&rdquo; comes from the same Old French root, <em>gaufre</em>, that also produced &ldquo;waffle&rdquo; "
         "&mdash; both originally describing a flat cake pressed with a pattern. Its most iconic modern use is the "
         "icebox cake. <a href=\"/holiday/national-chocolate-wafer-day/\">Full holiday page &rarr;</a>"),
        ("national-eat-your-beans-day",
         "Beans have been cultivated for at least 7,000 years, making them one of the older continuously farmed "
         "foods still eaten daily. <a href=\"/holiday/national-eat-your-beans-day/\">Full holiday page &rarr;</a>"),

        ("national-barbecued-spareribs-day",
         "Spareribs come from the belly section of the pig, the lower part of the rib cage, which is why they "
         "carry more fat and connective tissue &mdash; exactly what makes them so tender after a long, slow cook. "
         "<a href=\"/holiday/national-barbecued-spareribs-day/\">Full holiday page &rarr;</a>"),
        ("sidewalk-egg-frying-day",
         "The physics rarely cooperate &mdash; reliably frying an egg needs a sustained surface temperature above "
         "158&deg;F, a threshold most sidewalks don't actually reach even on the hottest July days. "
         "<a href=\"/holiday/sidewalk-egg-frying-day/\">Full holiday page &rarr;</a>"),

        ("national-apple-turnover-day",
         "The name describes the technique exactly &mdash; folding one half of the dough over the filling to meet "
         "the other half, making it a category of hand pie rather than something structurally distinct. "
         "<a href=\"/holiday/national-apple-turnover-day/\">Full holiday page &rarr;</a>"),
        ("workaholics-day",
         "The word &ldquo;workaholic&rdquo; was coined in 1971 by psychologist Wayne Oates in a book literally titled "
         "&ldquo;Confessions of a Workaholic.&rdquo; Research suggests workaholics tend to be less productive over time "
         "than people who maintain reasonable hours. <a href=\"/holiday/workaholics-day/\">Full holiday page &rarr;</a>"),

        ("international-kissing-day",
         "The record for longest kiss stands at 58 hours, 35 minutes, and 58 seconds, set by a couple in Thailand "
         "in 2013. A single passionate kiss can engage up to 34 facial muscles and 112 postural muscles at once. "
         "<a href=\"/holiday/international-kissing-day/\">Full holiday page &rarr;</a>"),
        ("national-fried-chicken-day",
         "The technique's Southern American roots trace to a genuine cultural fusion &mdash; Scottish immigrants' "
         "frying traditions combined with West African culinary practices brought by enslaved people. "
         "<a href=\"/holiday/national-fried-chicken-day/\">Full holiday page &rarr;</a>"),

        ("tell-the-truth-day",
         "No documented founder or formal origin, unusual for a holiday built around honesty specifically. The "
         "legal system's own version of the same idea &mdash; &ldquo;the truth, the whole truth, and nothing but the "
         "truth&rdquo; &mdash; is one of the oldest standardized oaths still in use. <a href=\"/holiday/tell-the-truth-day/\">Full holiday page &rarr;</a>"),
        ("world-chocolate-day",
         "Widely believed to mark chocolate's 17th-century introduction to Europe, though the exact anniversary "
         "is debated. It took roughly 400 cacao beans to make just one pound of chocolate. "
         "<a href=\"/holiday/world-chocolate-day/\">Full holiday page &rarr;</a>"),

        ("national-scud-day",
         "Founded in 2007 by Stephanie West Allen, a former lawyer turned mediator, who built the concept around "
         "real neuroscience research on conflict &mdash; the acronym stands for &ldquo;Savor the Comic, Unplug the "
         "Drama.&rdquo; <a href=\"/holiday/national-scud-day/\">Full holiday page &rarr;</a>"),
        ("national-video-game-day",
         "The first interactive electronic game built for a screen, &ldquo;Tennis for Two,&rdquo; dates to 1958 &mdash; "
         "decades before home consoles existed. The video game industry's global revenue now exceeds the film "
         "and music industries combined. <a href=\"/holiday/national-video-game-day/\">Full holiday page &rarr;</a>"),

        ("national-sugar-cookie-day",
         "Traces to Nazareth, Pennsylvania in the 1700s, where German Protestant settlers originally called it "
         "the &ldquo;Nazareth Cookie&rdquo; before the name simplified. <a href=\"/holiday/national-sugar-cookie-day/\">Full holiday page &rarr;</a>"),
        ("no-bra-day",
         "There are actually two separate &ldquo;No Bra Day&rdquo; observances &mdash; this one on July 9th, and another "
         "on October 13th tied to Breast Cancer Awareness Month, which causes regular confusion online. "
         "<a href=\"/holiday/no-bra-day/\">Full holiday page &rarr;</a>"),

        ("national-piña-colada-day",
         "Credited to bartender Ramon &ldquo;Monchito&rdquo; Marrero at the Caribe Hilton in San Juan in 1954, and "
         "formally declared Puerto Rico's national drink in 1978. <a href=\"/holiday/national-piña-colada-day/\">Full holiday page &rarr;</a>"),
        ("teddy-bear-picnic-day",
         "The bear itself is named for Theodore Roosevelt, after a 1902 hunting trip where he famously refused to "
         "shoot a cornered bear cub. <a href=\"/holiday/teddy-bear-picnic-day/\">Full holiday page &rarr;</a>"),

        ("cheer-up-the-lonely-day",
         "Backed by real research showing that strong social connections can extend life expectancy by as much "
         "as 50%. Acts of kindness measurably release both oxytocin and dopamine in the giver. "
         "<a href=\"/holiday/cheer-up-the-lonely-day/\">Full holiday page &rarr;</a>"),
        ("national-7-eleven-day",
         "The chain's first store opened in Dallas in 1927, originally an ice house selling milk, bread, and "
         "eggs. Before 1946 it operated as &ldquo;Tote'm Stores&rdquo;; the 7-Eleven name came directly from its "
         "then-novel 7am-to-11pm hours. <a href=\"/holiday/national-7-eleven-day/\">Full holiday page &rarr;</a>"),

        ("national-pecan-pie-day",
         "Pecans are native to North America, which makes pecan pie one of the genuinely distinctly American "
         "desserts on this calendar. It's also the official state pie of Texas. "
         "<a href=\"/holiday/national-pecan-pie-day/\">Full holiday page &rarr;</a>"),
        ("national-simplicity-day",
         "Marks Henry David Thoreau's birthday, and his cabin at Walden Pond cost him just $28.12 to build &mdash; "
         "cheaper than a year's rent in nearby Cambridge at the time. His night in jail for refusing to pay a "
         "poll tax became the essay &ldquo;Civil Disobedience,&rdquo; which went on to influence Gandhi and Martin "
         "Luther King Jr. <a href=\"/holiday/national-simplicity-day/\">Full holiday page &rarr;</a>"),

        ("embrace-your-geekness-day",
         "The word &ldquo;geek&rdquo; originally described circus performers known for biting the heads off live "
         "chickens &mdash; about as far from its modern meaning as an etymology gets. "
         "<a href=\"/holiday/embrace-your-geekness-day/\">Full holiday page &rarr;</a>"),
        ("french-fries-day",
         "Despite the name, fries are widely believed to have originated in Belgium, where locals fried potatoes "
         "as a fish substitute during winters when rivers froze over. <a href=\"/holiday/french-fries-day/\">Full holiday page &rarr;</a>"),

        ("national-mac-and-cheese-day",
         "Thomas Jefferson is credited with bringing the dish to America after encountering it in France, serving "
         "it at a White House dinner in 1802. Canadians consume 55% more boxed macaroni and cheese than "
         "Americans. <a href=\"/holiday/national-mac-and-cheese-day/\">Full holiday page &rarr;</a>"),
        ("pandemonium-day",
         "Built entirely around sanctioned, harmless disorder &mdash; reverse-day activities like wearing clothes "
         "backward or eating dessert before dinner, sometimes organized into deliberately chaotic &ldquo;Chaos "
         "Parades.&rdquo; <a href=\"/holiday/pandemonium-day/\">Full holiday page &rarr;</a>"),

        ("give-something-away-day",
         "Backed by real psychology &mdash; researchers call the mood boost from giving the &ldquo;helper's high,&rdquo; and "
         "it applies as much to donating time as donating objects. <a href=\"/holiday/give-something-away-day/\">Full holiday page &rarr;</a>"),
        ("gummy-worm-day",
         "Introduced in 1986 by German candy company Trolli, created as a direct follow-up to the original gummy "
         "bear's success back in 1922. <a href=\"/holiday/gummy-worm-day/\">Full holiday page &rarr;</a>"),
        ("national-hot-dog-day",
         "Americans eat an estimated 20 billion hot dogs a year, and the name itself likely traces to a 1901 "
         "cartoon that depicted &ldquo;dachshund sausages.&rdquo; Chicago purists famously consider ketchup a genuine "
         "faux pas. <a href=\"/holiday/national-hot-dog-day/\">Full holiday page &rarr;</a>"),

        ("guinea-pig-appreciation-day",
         "The date comes from a literal alphabet code set by founder Caroline Lane: G is the 7th letter (for "
         "July), P is the 16th (for the day). Despite the name, guinea pigs aren't pigs and aren't from Guinea "
         "&mdash; they're Andean rodents. <a href=\"/holiday/guinea-pig-appreciation-day/\">Full holiday page &rarr;</a>"),
        ("national-corn-fritters-day",
         "Fried dough dishes similar to fritters date back to Roman times, making the format ancient even if corn "
         "fritters specifically are a Southern American staple. <a href=\"/holiday/national-corn-fritters-day/\">Full holiday page &rarr;</a>"),

        ("peach-ice-cream-day",
         "Particularly tied to the American South, where peaches are both a major crop and a defining summer "
         "flavor. <a href=\"/holiday/peach-ice-cream-day/\">Full holiday page &rarr;</a>"),
        ("world-emoji-day",
         "The date was chosen for a genuinely specific reason: July 17th is what displays on Apple's calendar "
         "emoji (&#128197;), a detail Emojipedia founder Jeremy Burge noticed and built the holiday around in "
         "2014. <a href=\"/holiday/world-emoji-day/\">Full holiday page &rarr;</a>"),

        ("caviar-day",
         "True caviar, by strict definition, only refers to salt-cured roe from sturgeon specifically &mdash; "
         "everything else is technically just &ldquo;roe.&rdquo; <a href=\"/holiday/caviar-day/\">Full holiday page &rarr;</a>"),
        ("national-sour-candy-day",
         "The sour sensation comes from actual edible acids &mdash; citric, malic, tartaric, fumaric &mdash; not just "
         "sugar concentration. Sour Patch Kids started in 1970s Canada under a completely different name: Mars "
         "Men. <a href=\"/holiday/national-sour-candy-day/\">Full holiday page &rarr;</a>"),

        ("national-daiquiri-day",
         "Invented in late-19th-century Cuba by American mining engineer Jennings Cox, named for the mining town "
         "where he worked. Ernest Hemingway's version of choice was a double served without sugar. "
         "<a href=\"/holiday/national-daiquiri-day/\">Full holiday page &rarr;</a>"),
        ("stick-out-your-tongue-day",
         "The gesture carries wildly different meanings across cultures &mdash; an insult in much of the West, but "
         "historically a greeting in parts of Tibet. <a href=\"/holiday/stick-out-your-tongue-day/\">Full holiday page &rarr;</a>"),

        ("lollipop-day",
         "The word is credited to George Smith, who patented the first automatic lollipop-making machine in 1908 "
         "and named the result &ldquo;Lolly Pop.&rdquo; <a href=\"/holiday/lollipop-day/\">Full holiday page &rarr;</a>"),
        ("moon-day",
         "Marks the exact 1969 Apollo 11 landing, and Neil Armstrong's famous first words were delivered with a "
         "small grammatical gap &mdash; he intended &ldquo;one small step for a man,&rdquo; but the &ldquo;a&rdquo; was lost in "
         "transmission or speech. <a href=\"/holiday/moon-day/\">Full holiday page &rarr;</a>"),

        ("lamington-day",
         "Often called Australia's unofficial national cake &mdash; squares of sponge dipped in chocolate sauce and "
         "rolled in desiccated coconut. Its invention is usually credited to Lord Lamington, Queensland's "
         "governor from 1896 to 1901. <a href=\"/holiday/lamington-day/\">Full holiday page &rarr;</a>"),
        ("national-junk-food-day",
         "The term &ldquo;junk food&rdquo; was popularized in 1972 by Michael Jacobson of the Center for Science in the "
         "Public Interest. <a href=\"/holiday/national-junk-food-day/\">Full holiday page &rarr;</a>"),

        ("national-hammock-day",
         "Hammocks originated with Indigenous peoples of Central and South America, designed to lift sleepers off "
         "the ground, away from insects and small animals. <a href=\"/holiday/national-hammock-day/\">Full holiday page &rarr;</a>"),
        ("rat-catchers-day",
         "Tied directly to the medieval Pied Piper legend, which places the rat-clearing of Hamelin on this exact "
         "date in 1284. <a href=\"/holiday/rat-catchers-day/\">Full holiday page &rarr;</a>"),

        ("national-gorgeous-grandma-day",
         "Created in 1984 by author Alice Solomon, who coined the term specifically to challenge the &ldquo;little "
         "old lady&rdquo; stereotype attached to aging women. The holiday explicitly doesn't require actually being a "
         "grandmother to apply. <a href=\"/holiday/national-gorgeous-grandma-day/\">Full holiday page &rarr;</a>"),
        ("vanilla-ice-cream-day",
         "Vanilla is the world's second most expensive spice after saffron, a direct result of how "
         "labor-intensive its cultivation is. <a href=\"/holiday/vanilla-ice-cream-day/\">Full holiday page &rarr;</a>"),

        ("cousins-day",
         "The word &ldquo;cousin&rdquo; traces through Old French back to the Latin <em>consobrinus</em>, originally "
         "meaning specifically a child of a mother's sister. <a href=\"/holiday/cousins-day/\">Full holiday page &rarr;</a>"),
        ("national-tequila-day",
         "Legally, tequila can only be made from blue agave, and only in specific regions of Mexico, mostly "
         "Jalisco &mdash; a Denomination of Origin protection similar to Champagne's. "
         "<a href=\"/holiday/national-tequila-day/\">Full holiday page &rarr;</a>"),

        ("carousel-day",
         "Marks William Schneider's 1871 U.S. patent for the carousel, though the word itself comes from the "
         "Italian <em>carosello</em>, originally describing a 17th-century cavalry training exercise. "
         "<a href=\"/holiday/carousel-day/\">Full holiday page &rarr;</a>"),
        ("national-wine-and-cheese-day",
         "Winemaking dates back to roughly 6000 BCE in Georgia, and cheesemaking to about 5500 BCE in Poland &mdash; "
         "meaning the pairing itself has a combined history stretching back well over 7,000 years. "
         "<a href=\"/holiday/national-wine-and-cheese-day/\">Full holiday page &rarr;</a>"),

        ("all-or-nothing-day",
         "No documented founder or origin &mdash; a purely conceptual holiday built around the idea of committing "
         "fully to a decision rather than hedging. <a href=\"/holiday/all-or-nothing-day/\">Full holiday page &rarr;</a>"),
        ("national-aunt-and-uncle-day",
         "The words &ldquo;aunt&rdquo; and &ldquo;uncle&rdquo; both trace through Old French to Latin roots, originally "
         "referring specifically to a parent's sister and brother. <a href=\"/holiday/national-aunt-and-uncle-day/\">Full holiday page &rarr;</a>"),

        ("national-crème-brûlée-day",
         "The name translates literally from French as &ldquo;burnt cream,&rdquo; though England's &ldquo;burnt cream&rdquo; and "
         "Spain's &ldquo;crema catalana&rdquo; both predate the French version enough to make its true origin genuinely "
         "disputed. <a href=\"/holiday/national-crème-brûlée-day/\">Full holiday page &rarr;</a>"),
        ("take-your-houseplant-for-a-walk-day",
         "The premise has a real basis &mdash; natural outdoor light covers a fuller spectrum than most indoor "
         "lighting, genuinely benefiting photosynthesis. <a href=\"/holiday/take-your-houseplant-for-a-walk-day/\">Full holiday page &rarr;</a>"),

        ("national-milk-chocolate-day",
         "The first solid milk chocolate was created in 1875 by Swiss confectioner Daniel Peter, using Henri "
         "Nestl&eacute;'s condensed milk. Milton Hershey's 1900 Hershey's Bar made it affordable and widely available "
         "in the US. <a href=\"/holiday/national-milk-chocolate-day/\">Full holiday page &rarr;</a>"),
        ("national-waterpark-day",
         "Created in 2017 by Kalahari Resorts, deliberately timed to July as the hottest month of the year. The "
         "format traces to 1977's Wet 'n Wild Orlando &mdash; while New Jersey's notoriously chaotic Action Park, "
         "opened a year later, became almost as famous for its danger as for its thrills. "
         "<a href=\"/holiday/national-waterpark-day/\">Full holiday page &rarr;</a>"),

        ("national-lasagna-day",
         "The word &ldquo;lasagna&rdquo; originally referred to the cooking pot itself, not the pasta sheets. Regional "
         "Italian versions vary sharply: Bolognese uses green pasta and b&eacute;chamel, while Southern versions lean "
         "on ricotta and tomato sauce. <a href=\"/holiday/national-lasagna-day/\">Full holiday page &rarr;</a>"),
        ("rain-day",
         "A genuinely unbroken local tradition in Waynesburg, Pennsylvania since 1878, where it's reportedly "
         "rained on this exact date well over 100 times. Past celebrity participants in the town's rain-or-shine "
         "wager have included Johnny Carson, Bob Hope, and Fred Rogers. <a href=\"/holiday/rain-day/\">Full holiday page &rarr;</a>"),

        ("national-cheesecake-day",
         "Cheesecake's documented history goes back to ancient Greece, reportedly served to athletes at the first "
         "Olympic Games in 776 BC. <a href=\"/holiday/national-cheesecake-day/\">Full holiday page &rarr;</a>"),
        ("paperback-book-day",
         "Marks Penguin Books' 1935 launch of the modern paperback, an idea founder Allen Lane got after finding "
         "only poor-quality, overpriced books at a train station bookstall. The first ten titles cost sixpence "
         "each and were color-coded by genre. <a href=\"/holiday/paperback-book-day/\">Full holiday page &rarr;</a>"),

        ("national-avocado-day",
         "Botanically classified as a single-seeded berry, not a vegetable. The word traces to the Aztec "
         "<em>ahuacatl</em>, which also meant &ldquo;testicle,&rdquo; a fairly direct reference to its shape. "
         "<a href=\"/holiday/national-avocado-day/\">Full holiday page &rarr;</a>"),
        ("national-raspberry-cake-day",
         "Raspberries are technically aggregate fruits, made up of dozens of tiny individual drupelets each "
         "carrying its own seed. Despite red being the default, the plant also produces black, purple, and "
         "golden varieties. <a href=\"/holiday/national-raspberry-cake-day/\">Full holiday page &rarr;</a>"),
    ],
}

AUGUST = {
    "month_num": 8,
    "month_name": "August",
    "url_slug": "august",
    "title": "The Complete Guide to August's Obscure Holidays | Obscure Holiday Calendar",
    "description": (
        "A complete, day-by-day guide to all 62 obscure and offbeat holidays in August — "
        "from National Girlfriends Day to National Matchmaker Day — with history, context, "
        "and links to the full write-up for each one."
    ),
    "h1": "The Complete Guide to August's Obscure Holidays",
    "date_published": "2026-07-28",
    "date_modified": "2026-07-28",
    "intro_html": """    <p>August closes out summer with a genuinely dense dessert lineup &mdash; ice cream sandwiches, banana
    splits, s'mores, and toasted marshmallows all get their own day within a few weeks of each other &mdash;
    alongside a real mix of history (Vesuvius Day, Presidential Joke Day) and pure whimsy (Race Your Mouse
    Around the Icons Day).</p>

    <p>This guide walks through all 62, day by day, with a bit of history or context for each one and a
    link to the full write-up &mdash; complete fun facts, ways to celebrate, and sourcing &mdash; on its own page.</p>""",
    "why_html": """    <p>August leans hard into frozen and campfire treats as peak summer heat pushes people toward cold
    desserts and outdoor evenings &mdash; ice cream sandwiches, root beer floats, banana splits, and s'mores all
    land within the same few weeks. The month also carries a handful of genuinely well-documented historical
    anchors, from the 79 AD Vesuvius eruption to Reagan's unbroadcast 1984 microphone joke.</p>""",
    "how_to_use_html": """    <p>Holidays are grouped by date below. Each entry gets a short original write-up &mdash; not a repeat
    of the fact sheet &mdash; plus a link to the full holiday page if you want the deeper dive: complete fun
    facts, ways to celebrate, and sourcing.</p>""",
    "about_html": """    <p>This guide is part of the Obscure Holiday Calendar project &mdash; the same database that powers
    the iOS and Android apps and the individual holiday pages on this site. It exists to give a single,
    readable overview of an entire month at once, instead of requiring 62 separate page visits.</p>""",
    "faq": [
        (
            "How many obscure holidays are there in August?",
            "62, spread across all 31 days.",
        ),
        (
            "What's the most historically grounded holiday in August?",
            "Vesuvius Day (Aug 24) marks the actual 79 AD eruption that buried Pompeii and Herculaneum — one of "
            "the best-documented disasters in the ancient world.",
        ),
        (
            "Are there a lot of dessert holidays in August?",
            "Yes — National Ice Cream Sandwich Day, National Banana Split Day, S'mores Day, Toasted Marshmallow "
            "Day, and several pie and pudding days make August one of the most dessert-heavy months.",
        ),
        (
            "Where can I find the full history and fun facts for each holiday?",
            "Every holiday name in this guide links to its own dedicated page with a longer write-up, sourced "
            "fun facts, and ideas for how to celebrate.",
        ),
    ],
    "entries": [
        ("national-girlfriends-day",
         "No documented founder or clear historical origin &mdash; it emerged more as a grassroots celebration than "
         "a proclaimed holiday. Despite the name, it's built entirely around platonic friendship between women. "
         "<a href=\"/holiday/national-girlfriends-day/\">Full holiday page &rarr;</a>"),
        ("national-raspberry-cream-pie-day",
         "Raspberries are aggregate fruits, made of many small drupelets each with its own seed. The vast "
         "majority of America's raspberry supply comes from the Pacific Northwest, mainly Oregon and Washington. "
         "<a href=\"/holiday/national-raspberry-cream-pie-day/\">Full holiday page &rarr;</a>"),

        ("coloring-book-day",
         "The earliest coloring books, originally called &ldquo;painting books,&rdquo; appeared in the US in the 1880s "
         "for educational purposes, not relaxation. The adult coloring book boom didn't hit until around 2015. "
         "<a href=\"/holiday/coloring-book-day/\">Full holiday page &rarr;</a>"),
        ("national-ice-cream-sandwich-day",
         "The earliest known version was sold by a pushcart vendor in New York's Bowery neighborhood in 1899, for "
         "a single cent. Over 100 million are still sold annually in the US today. "
         "<a href=\"/holiday/national-ice-cream-sandwich-day/\">Full holiday page &rarr;</a>"),

        ("grab-some-nuts-day",
         "Many foods people call &ldquo;nuts&rdquo; &mdash; almonds, cashews, pistachios &mdash; are botanically seeds or "
         "drupes, not true nuts at all. Peanuts break the pattern entirely: they're legumes that grow "
         "underground. <a href=\"/holiday/grab-some-nuts-day/\">Full holiday page &rarr;</a>"),
        ("national-watermelon-day",
         "Watermelons run about 92% water, which is why they double as one of the more effective hydration foods "
         "of summer. The earliest recorded harvest dates to Egypt more than 5,000 years ago. "
         "<a href=\"/holiday/national-watermelon-day/\">Full holiday page &rarr;</a>"),

        ("national-chocolate-chip-cookie-day",
         "Marks the same 1938 accident behind several other holidays on this calendar &mdash; Ruth Wakefield "
         "expected the chopped chocolate at the Toll House Inn to melt into the dough, and it didn't. "
         "<a href=\"/holiday/national-chocolate-chip-cookie-day/\">Full holiday page &rarr;</a>"),
        ("national-sisters-day",
         "A separate, more recent holiday from National Siblings Day in April. Research from De Montfort and "
         "Ulster University has linked growing up with a sister to greater reported happiness and optimism. "
         "<a href=\"/holiday/national-sisters-day/\">Full holiday page &rarr;</a>"),

        ("national-underwear-day",
         "Entirely unofficial, with no government recognition, and mostly kept alive by retailers running "
         "promotions around it. <a href=\"/holiday/national-underwear-day/\">Full holiday page &rarr;</a>"),
        ("work-like-a-dog-day",
         "The idiom itself dates back to at least the 17th century, meaning genuinely exhausting labor. Plenty of "
         "dog breeds were literally developed for work &mdash; herding, hunting, guarding, pulling. "
         "<a href=\"/holiday/work-like-a-dog-day/\">Full holiday page &rarr;</a>"),

        ("national-root-beer-float-day",
         "Invented in 1893 by Frank J. Wisner, a Colorado brewery owner reportedly inspired by the snowy peak of "
         "Cow Mountain, which is how the drink got its early name: &ldquo;Black Cow Mountain,&rdquo; later shortened to "
         "&ldquo;Black Cow.&rdquo; <a href=\"/holiday/national-root-beer-float-day/\">Full holiday page &rarr;</a>"),
        ("wiggle-your-toes-day",
         "Each human foot contains 26 bones, 33 joints, and more than 100 muscles, tendons, and ligaments. "
         "Toeprints are as individually unique as fingerprints, though nobody actually uses them for ID. "
         "<a href=\"/holiday/wiggle-your-toes-day/\">Full holiday page &rarr;</a>"),

        ("national-raspberries-n-cream-day",
         "Raspberries belong to the rose family, making this pairing distant cousins with roses on a technicality. "
         "<a href=\"/holiday/national-raspberries-n-cream-day/\">Full holiday page &rarr;</a>"),
        ("particularly-preposterous-packaging-day",
         "Entirely built around shared consumer frustration &mdash; tiny items shipped in oversized boxes, products "
         "buried under layers of plastic and cardboard. No formal recognition, just a collectively understood "
         "annoyance turned into a joke holiday. <a href=\"/holiday/particularly-preposterous-packaging-day/\">Full holiday page &rarr;</a>"),

        ("happiness-happens-day",
         "Founded in 1999 by the actual Secret Society of Happy People, also known by the alternate name "
         "&ldquo;Admit You're Happy Day.&rdquo; <a href=\"/holiday/happiness-happens-day/\">Full holiday page &rarr;</a>"),
        ("national-cbd-day",
         "CBD was first isolated back in 1940, by American chemist Roger Adams &mdash; decades before the modern "
         "wellness industry built around it existed. Hemp-derived CBD became federally legal in the US only with "
         "the 2018 Farm Bill. <a href=\"/holiday/national-cbd-day/\">Full holiday page &rarr;</a>"),

        ("national-book-lovers-day",
         "The world's smallest book, &ldquo;Teeny Ted from Turnip Town,&rdquo; measures just 0.07 by 0.10 millimeters "
         "and can only be read under an electron microscope. There's even a word for the smell of old books: "
         "bibliosmia. <a href=\"/holiday/national-book-lovers-day/\">Full holiday page &rarr;</a>"),
        ("rice-pudding-day",
         "Traces back to the Roman Empire, where early versions were sometimes prescribed as a medicinal food. "
         "Nearly every culture has its own version, from Indian kheer to Spanish arroz con leche. "
         "<a href=\"/holiday/rice-pudding-day/\">Full holiday page &rarr;</a>"),

        ("national-lazy-day",
         "No documented origin, and the entire point is doing as little as possible. Proponents argue a "
         "scheduled day of real rest can actually boost overall productivity afterward. "
         "<a href=\"/holiday/national-lazy-day/\">Full holiday page &rarr;</a>"),
        ("smores-day",
         "The earliest known published recipe, then called a &ldquo;Some More,&rdquo; appeared in the 1927 Girl Scout "
         "handbook &ldquo;Tramping and Trailing with the Girl Scouts.&rdquo; <a href=\"/holiday/smores-day/\">Full holiday page &rarr;</a>"),

        ("national-raspberry-bombe-day",
         "The French term &ldquo;bombe glac&eacute;e&rdquo; dates to the 19th century, describing a frozen dessert built by "
         "lining a spherical mold with one flavor and filling the center with another. "
         "<a href=\"/holiday/national-raspberry-bombe-day/\">Full holiday page &rarr;</a>"),
        ("presidential-joke-day",
         "Marks a specific, real 1984 moment: Ronald Reagan, testing a microphone before a radio address, joked "
         "&ldquo;we start bombing in five minutes&rdquo; about the Soviet Union &mdash; unbroadcast, but leaked and "
         "remembered ever since. <a href=\"/holiday/presidential-joke-day/\">Full holiday page &rarr;</a>"),

        ("middle-childs-day",
         "Birth-order research links middle children to stronger diplomatic and mediation skills, developed from "
         "navigating relationships between older and younger siblings. <a href=\"/holiday/middle-childs-day/\">Full holiday page &rarr;</a>"),
        ("national-julienne-fries-day",
         "&ldquo;Julienne&rdquo; is a specific classical French cutting technique &mdash; long, thin matchstick strips, "
         "typically about 1/8 inch thick &mdash; not just a marketing name for skinny fries. "
         "<a href=\"/holiday/national-julienne-fries-day/\">Full holiday page &rarr;</a>"),

        ("international-left-handers-day",
         "Left-handers make up roughly 10 to 12% of the world's population. Tennis and boxing are two sports "
         "where lefties are often noted to have a real tactical edge. <a href=\"/holiday/international-left-handers-day/\">Full holiday page &rarr;</a>"),
        ("national-filet-mignon-day",
         "The name is French for &ldquo;dainty fillet.&rdquo; It comes from the psoas major, a non-weight-bearing "
         "muscle in the short loin, which is exactly why it's so tender. <a href=\"/holiday/national-filet-mignon-day/\">Full holiday page &rarr;</a>"),

        ("national-creamsicle-day",
         "Invented by Frank Epperson &mdash; the same person behind the Popsicle &mdash; when he was just 11 years old. "
         "&ldquo;Creamsicle&rdquo; is technically a registered Unilever trademark. <a href=\"/holiday/national-creamsicle-day/\">Full holiday page &rarr;</a>"),
        ("national-kool-aid-day",
         "Invented in 1927 by Edwin Perkins in Hastings, Nebraska, originally sold as a liquid concentrate called "
         "&ldquo;Fruit Smack&rdquo; before the powdered version took over. <a href=\"/holiday/national-kool-aid-day/\">Full holiday page &rarr;</a>"),

        ("national-leathercraft-day",
         "Leatherworking is genuinely one of humanity's oldest crafts, with evidence stretching back to "
         "prehistoric times. Vegetable tanning remains a more eco-friendly alternative to modern chemical "
         "tanning. <a href=\"/holiday/national-leathercraft-day/\">Full holiday page &rarr;</a>"),
        ("national-relaxation-day",
         "The concept of dedicated leisure time traces back to the ancient Greeks and Romans. Regular breaks are "
         "also linked in modern research to measurably higher productivity and creativity. "
         "<a href=\"/holiday/national-relaxation-day/\">Full holiday page &rarr;</a>"),

        ("national-tell-a-joke-day",
         "The oldest known joke on record dates to 1900 BC Sumeria, and it's a fart joke &mdash; proof that some "
         "humor genuinely hasn't changed in nearly 4,000 years. <a href=\"/holiday/national-tell-a-joke-day/\">Full holiday page &rarr;</a>"),
        ("rum-day",
         "Rum production traces to the 17th-century Caribbean, made from sugarcane molasses or fresh cane juice. "
         "The British Royal Navy historically issued sailors a daily rum ration, known as a &ldquo;tot.&rdquo; "
         "<a href=\"/holiday/rum-day/\">Full holiday page &rarr;</a>"),

        ("national-black-cat-appreciation-day",
         "Black cats carried opposite reputations depending on where you were &mdash; bad luck in medieval Europe, "
         "but good fortune in ancient Egypt, Japan, and parts of the UK. <a href=\"/holiday/national-black-cat-appreciation-day/\">Full holiday page &rarr;</a>"),
        ("thrift-shop-day",
         "Buying used clothing reportedly cuts its carbon footprint by 82% compared to buying new. The global "
         "secondhand apparel market is projected to hit $350 billion by 2027. <a href=\"/holiday/thrift-shop-day/\">Full holiday page &rarr;</a>"),

        ("national-bad-poetry-day",
         "The entire premise inverts the usual creative-writing goal &mdash; intentionally bad rhythm, rhyme, and "
         "reason, aiming for maximum cringe rather than craft. <a href=\"/holiday/national-bad-poetry-day/\">Full holiday page &rarr;</a>"),
        ("serendipity-day",
         "The word &ldquo;serendipity&rdquo; was coined in 1754 by English author Horace Walpole, inspired by a Persian "
         "fairy tale called &ldquo;The Three Princes of Serendip.&rdquo; Alexander Fleming's discovery of penicillin is "
         "one of history's most famous serendipitous breakthroughs. <a href=\"/holiday/serendipity-day/\">Full holiday page &rarr;</a>"),

        ("national-potato-day",
         "Potatoes were first cultivated by Inca farmers in Peru as far back as 8,000 BC. In 1995 they became the "
         "first food ever grown in space, aboard the Space Shuttle Columbia. <a href=\"/holiday/national-potato-day/\">Full holiday page &rarr;</a>"),
        ("national-soft-ice-cream-day",
         "Soft serve is served warmer than hard-scooped ice cream, around 25&deg;F, which is exactly what gives it "
         "that smoother texture. Up to 60% of its volume can be air, known in the industry as &ldquo;overrun.&rdquo; "
         "<a href=\"/holiday/national-soft-ice-cream-day/\">Full holiday page &rarr;</a>"),

        ("national-chocolate-pecan-pie-day",
         "Pecans are the only major tree nut actually native to North America, and the US remains the world's "
         "leading producer. <a href=\"/holiday/national-chocolate-pecan-pie-day/\">Full holiday page &rarr;</a>"),
        ("national-radio-day",
         "Guglielmo Marconi sent the first transatlantic radio signal in 1901, but the first public voice-and-music "
         "broadcast is credited to Reginald Fessenden, on Christmas Eve 1906. <a href=\"/holiday/national-radio-day/\">Full holiday page &rarr;</a>"),

        ("national-senior-citizens-day",
         "Formally established in 1988, when Ronald Reagan signed Proclamation 5847 after Congress requested it "
         "directly through a joint resolution. As of 2024, roughly 18% of the US population was 65 or older. "
         "<a href=\"/holiday/national-senior-citizens-day/\">Full holiday page &rarr;</a>"),
        ("national-spumoni-day",
         "Originated in 19th-century Naples, and the name comes from the Italian &ldquo;spuma,&rdquo; meaning foam. The "
         "traditional pistachio-cherry-chocolate layering happens to mirror the colors of the Italian flag. "
         "<a href=\"/holiday/national-spumoni-day/\">Full holiday page &rarr;</a>"),

        ("be-an-angel-day",
         "Built around the &ldquo;pay it forward&rdquo; idea &mdash; one good deed prompting another, creating a chain "
         "rather than a single isolated act. <a href=\"/holiday/be-an-angel-day/\">Full holiday page &rarr;</a>"),
        ("national-pecan-torte-day",
         "A torte, by German definition, typically uses ground nuts or breadcrumbs instead of flour. The pecan "
         "tree is officially the state tree of Texas. <a href=\"/holiday/national-pecan-torte-day/\">Full holiday page &rarr;</a>"),

        ("ride-the-wind-day",
         "Kites, one of the most direct ways to literally &ldquo;ride the wind,&rdquo; were invented in China more than "
         "2,000 years ago. <a href=\"/holiday/ride-the-wind-day/\">Full holiday page &rarr;</a>"),
        ("sponge-cake-day",
         "Its rise comes purely from whipped eggs, not baking powder or soda &mdash; a technique that traces back to "
         "the Italian Renaissance. <a href=\"/holiday/sponge-cake-day/\">Full holiday page &rarr;</a>"),

        ("national-peach-pie-day",
         "Peaches actually originated in China more than 2,000 years ago, long before they became a defining "
         "Southern American crop. Georgia may be nicknamed the &ldquo;Peach State,&rdquo; but California is the actual "
         "leading US producer. <a href=\"/holiday/national-peach-pie-day/\">Full holiday page &rarr;</a>"),
        ("vesuvius-day",
         "Marks the 79 AD eruption that buried Pompeii and Herculaneum, though the traditional August date is now "
         "disputed &mdash; evidence found on preserved victims suggests it may have actually happened in October. "
         "<a href=\"/holiday/vesuvius-day/\">Full holiday page &rarr;</a>"),

        ("kiss-and-make-up-day",
         "No clear documented origin, though the psychology behind it is well established &mdash; studies "
         "consistently link forgiveness to reduced stress and stronger relationships. "
         "<a href=\"/holiday/kiss-and-make-up-day/\">Full holiday page &rarr;</a>"),
        ("national-banana-split-day",
         "Invented in 1904 by 23-year-old apprentice pharmacist David &ldquo;Doc&rdquo; Strickler in Latrobe, "
         "Pennsylvania, who charged ten cents for it &mdash; double the price of a regular sundae at the time. "
         "<a href=\"/holiday/national-banana-split-day/\">Full holiday page &rarr;</a>"),

        ("national-cherry-popsicle-day",
         "The Popsicle itself was an accidental 1905 invention by 11-year-old Frank Epperson, who originally "
         "called it an &ldquo;Epsicle&rdquo; before his own kids talked him into the name that stuck. "
         "<a href=\"/holiday/national-cherry-popsicle-day/\">Full holiday page &rarr;</a>"),
        ("national-dog-day",
         "Founded in 2004 by Colleen Paige, the same person behind National Puppy Day, National Cat Day, and "
         "National Wildlife Day. <a href=\"/holiday/national-dog-day/\">Full holiday page &rarr;</a>"),

        ("just-because-day",
         "The entire premise is the absence of a reason &mdash; no occasion, no justification needed, just "
         "spontaneous action for its own sake. <a href=\"/holiday/just-because-day/\">Full holiday page &rarr;</a>"),
        ("lizard-appreciation-day",
         "There are more than 6,000 known lizard species, and many can regrow their tails as a defense mechanism. "
         "The largest, the Komodo dragon, can grow up to 10 feet long. <a href=\"/holiday/lizard-appreciation-day/\">Full holiday page &rarr;</a>"),

        ("national-bow-tie-day",
         "Traces back to Croatian mercenaries' cravats during the 17th-century Thirty Years' War. It's a required "
         "component of true &ldquo;black tie&rdquo; dress, not just an optional accessory. "
         "<a href=\"/holiday/national-bow-tie-day/\">Full holiday page &rarr;</a>"),
        ("race-your-mouse-around-the-icons-day",
         "No formal origin, purely an internet-era novelty &mdash; a personal, non-competitive test of how fast you "
         "can drag your cursor around your own desktop icons. <a href=\"/holiday/race-your-mouse-around-the-icons-day/\">Full holiday page &rarr;</a>"),

        ("according-to-hoyle-day",
         "Honors Edmond Hoyle, whose 1742 &ldquo;A Short Treatise on the Game of Whist&rdquo; became the definitive "
         "rulebook for the game for over a century. <a href=\"/holiday/according-to-hoyle-day/\">Full holiday page &rarr;</a>"),
        ("national-chop-suey-day",
         "Despite its strong association with China, chop suey is widely believed to have actually originated in "
         "the United States, invented by Chinese American cooks. <a href=\"/holiday/national-chop-suey-day/\">Full holiday page &rarr;</a>"),

        ("national-beach-day",
         "Most beach sand worldwide is primarily quartz, mixed with varying amounts of shell fragments and "
         "volcanic rock. The world's longest beach, Brazil's Praia do Cassino, stretches more than 150 miles. "
         "<a href=\"/holiday/national-beach-day/\">Full holiday page &rarr;</a>"),
        ("toasted-marshmallow-day",
         "The modern marshmallow, made with gelatin, only dates to the late 19th century &mdash; the original "
         "version used actual sap from the mallow plant. <a href=\"/holiday/toasted-marshmallow-day/\">Full holiday page &rarr;</a>"),

        ("eat-outside-day",
         "The word &ldquo;picnic&rdquo; comes from the French &ldquo;pique-nique,&rdquo; first documented in the 17th century. "
         "&Eacute;douard Manet's &ldquo;Le D&eacute;jeuner sur l'herbe&rdquo; turned outdoor dining into one of the most famous "
         "images in Impressionist painting. <a href=\"/holiday/eat-outside-day/\">Full holiday page &rarr;</a>"),
        ("national-matchmaker-day",
         "Matchmaking as a profession goes back to biblical times, appearing across cultures well before dating "
         "apps existed. Today's dating algorithms function as digital matchmakers, just automated. "
         "<a href=\"/holiday/national-matchmaker-day/\">Full holiday page &rarr;</a>"),
    ],
}

SEPTEMBER = {
    "month_num": 9,
    "month_name": "September",
    "url_slug": "september",
    "title": "The Complete Guide to September's Obscure Holidays | Obscure Holiday Calendar",
    "description": (
        "A complete, day-by-day guide to all 60 obscure and offbeat holidays in September — "
        "from National Emma M. Nutt Day to National Hot Mulled Cider Day — with history, "
        "context, and links to the full write-up for each one."
    ),
    "h1": "The Complete Guide to September's Obscure Holidays",
    "date_published": "2026-07-28",
    "date_modified": "2026-07-28",
    "intro_html": """    <p>September eases out of summer with a genuinely broad mix &mdash; International Talk Like a Pirate Day
    and Hobbit Day sit next to National IT Professionals Day and a South African public holiday, while a
    real cluster of pie, pudding, and cheese-topped holidays carries the food theme into fall.</p>

    <p>This guide walks through all 60, day by day, with a bit of history or context for each one and a
    link to the full write-up &mdash; complete fun facts, ways to celebrate, and sourcing &mdash; on its own page.</p>""",
    "why_html": """    <p>September's holidays split between deep internet-era whimsy &mdash; Talk Like a Pirate Day, Wonderful
    Weirdos Day, Race Your Mouse-style novelty days &mdash; and some of the calendar's more substantive entries:
    Heritage Day carries real South African political history, World Rabies Day is timed to Louis Pasteur's
    death, and National Hug &amp; High 5 Day was founded directly out of a personal 9/11 loss.</p>""",
    "how_to_use_html": """    <p>Holidays are grouped by date below. Each entry gets a short original write-up &mdash; not a repeat
    of the fact sheet &mdash; plus a link to the full holiday page if you want the deeper dive: complete fun
    facts, ways to celebrate, and sourcing.</p>""",
    "about_html": """    <p>This guide is part of the Obscure Holiday Calendar project &mdash; the same database that powers
    the iOS and Android apps and the individual holiday pages on this site. It exists to give a single,
    readable overview of an entire month at once, instead of requiring 60 separate page visits.</p>""",
    "faq": [
        (
            "How many obscure holidays are there in September?",
            "60, spread across all 30 days.",
        ),
        (
            "What's the most meaningful holiday in September?",
            "National Hug & High 5 Day (Sep 12), founded by David Sylvester after his childhood mentor died in "
            "the World Trade Center on 9/11 — he's since hugged or high-fived more than half a million people "
            "across dozens of countries.",
        ),
        (
            "Are there a lot of food holidays in September?",
            "Yes — National Cheeseburger Day, National Guacamole Day, National Pepperoni Pizza Day, National "
            "Coffee Day, and several pie and pudding days make up a large share of the month.",
        ),
        (
            "Where can I find the full history and fun facts for each holiday?",
            "Every holiday name in this guide links to its own dedicated page with a longer write-up, sourced "
            "fun facts, and ideas for how to celebrate.",
        ),
    ],
    "entries": [
        ("national-emma-m-nutt-day",
         "Marks the exact 1878 hiring of the first female telephone operator in the US &mdash; before her, teenage "
         "boys held the job and were widely criticized for rudeness. Nutt reportedly stayed in the role for 33 "
         "years, into at least 1911. <a href=\"/holiday/national-emma-m-nutt-day/\">Full holiday page &rarr;</a>"),
        ("no-rhyme-or-reason-day",
         "No documented founder, fittingly appropriate for a holiday celebrating things without explanation. "
         "<a href=\"/holiday/no-rhyme-or-reason-day/\">Full holiday page &rarr;</a>"),

        ("national-blueberry-popsicle-day",
         "The Popsicle itself was a 1905 accident, invented by 11-year-old Frank Epperson after he left a soda "
         "mixture with a stirring stick outside overnight and it froze. <a href=\"/holiday/national-blueberry-popsicle-day/\">Full holiday page &rarr;</a>"),
        ("national-pierce-your-ears-day",
         "The oldest confirmed evidence of ear piercing comes from &Ouml;tzi the Iceman, a mummy dated to over "
         "5,300 years old, whose stretched earlobe piercing measured 7 to 11 millimeters. "
         "<a href=\"/holiday/national-pierce-your-ears-day/\">Full holiday page &rarr;</a>"),

        ("national-welsh-rarebit-day",
         "Despite the alternate name &ldquo;Welsh Rabbit,&rdquo; there's no rabbit in it at all &mdash; the dish is really "
         "just a thick, seasoned cheese sauce poured over toast. <a href=\"/holiday/national-welsh-rarebit-day/\">Full holiday page &rarr;</a>"),
        ("skyscraper-day",
         "Reportedly timed to architect Louis Sullivan's birthday, often credited as the &ldquo;father of the "
         "skyscraper.&rdquo; The safety elevator, invented by Elisha Otis in 1852, was just as essential to making "
         "tall buildings viable as steel-frame construction. <a href=\"/holiday/skyscraper-day/\">Full holiday page &rarr;</a>"),

        ("eat-an-extra-dessert-day",
         "No documented origin &mdash; the entire premise is simply permission to have a second dessert, with no "
         "specific type required. <a href=\"/holiday/eat-an-extra-dessert-day/\">Full holiday page &rarr;</a>"),
        ("national-macadamia-nut-day",
         "Native to the rainforests of eastern Australia, and notorious for having one of the hardest shells of "
         "any nut to crack. They're also genuinely toxic to dogs. <a href=\"/holiday/national-macadamia-nut-day/\">Full holiday page &rarr;</a>"),

        ("be-late-for-something-day",
         "Deliberately positioned as the opposite of National Punctuality Day, which falls back in January. "
         "<a href=\"/holiday/be-late-for-something-day/\">Full holiday page &rarr;</a>"),
        ("national-cheese-pizza-day",
         "Mozzarella remains the default topping cheese specifically because of its melt, stretch, and mild "
         "flavor. Modern pizza is widely traced back to Naples, Italy. <a href=\"/holiday/national-cheese-pizza-day/\">Full holiday page &rarr;</a>"),

        ("fight-procrastination-day",
         "Chronic procrastination reportedly affects 15 to 20% of adults globally, and over 70% of college "
         "students at some point. Psychologists increasingly frame it as an emotional regulation issue. "
         "<a href=\"/holiday/fight-procrastination-day/\">Full holiday page &rarr;</a>"),
        ("national-coffee-ice-cream-day",
         "Traces back to mid-18th-century Europe, with early recipes appearing in French cookbooks well before it "
         "became a mainstream American flavor. <a href=\"/holiday/national-coffee-ice-cream-day/\">Full holiday page &rarr;</a>"),

        ("national-new-hampshire-day",
         "New Hampshire was the very first of the thirteen colonies to formally declare independence from "
         "Britain, doing so on January 5, 1776 &mdash; six months before the Declaration of Independence. "
         "<a href=\"/holiday/national-new-hampshire-day/\">Full holiday page &rarr;</a>"),
        ("national-salami-day",
         "The word comes from the Italian &ldquo;salare,&rdquo; meaning &ldquo;to salt,&rdquo; referencing the curing process "
         "that makes it shelf-stable. <a href=\"/holiday/national-salami-day/\">Full holiday page &rarr;</a>"),

        ("national-ampersand-day",
         "The ampersand is technically a ligature, a fusion of the Latin word &ldquo;et&rdquo; meaning &ldquo;and,&rdquo; "
         "compressed into a single symbol. It was officially treated as the 27th letter of the English alphabet "
         "until roughly the mid-19th century. <a href=\"/holiday/national-ampersand-day/\">Full holiday page &rarr;</a>"),
        ("pardon-day",
         "The U.S. Constitution grants the President pardon power directly, in Article II, Section 2 &mdash; though a "
         "pardon restores rights without erasing the underlying conviction. <a href=\"/holiday/pardon-day/\">Full holiday page &rarr;</a>"),

        ("national-teddy-bear-day",
         "The bear's name traces to a 1902 political cartoon of Theodore Roosevelt refusing to shoot a cornered "
         "bear cub. The toy itself emerged almost simultaneously and independently in the US and Germany. "
         "<a href=\"/holiday/national-teddy-bear-day/\">Full holiday page &rarr;</a>"),
        ("wonderful-weirdos-day",
         "No widely documented founder or origin, though it's spread steadily across informal &ldquo;day&rdquo; "
         "calendars and social media. <a href=\"/holiday/wonderful-weirdos-day/\">Full holiday page &rarr;</a>"),

        ("national-anti-junk-light-day",
         "Founded in 2018 by TrueDark, a light-filtering eyewear company, deliberately echoing &ldquo;junk food&rdquo; to "
         "frame certain artificial light as something to consume in moderation. A 2016 global light-pollution "
         "atlas found the Milky Way hidden from more than a third of humanity. <a href=\"/holiday/national-anti-junk-light-day/\">Full holiday page &rarr;</a>"),
        ("national-tv-dinner-day",
         "Marks Swanson's original 1953 launch, whose first meal was turkey with cornbread dressing, peas, and "
         "sweet potatoes, served in an aluminum tray. Swanson reportedly sold over 10 million in the first year. "
         "<a href=\"/holiday/national-tv-dinner-day/\">Full holiday page &rarr;</a>"),

        ("national-make-your-bed-day",
         "Admiral William H. McRaven's widely shared 2014 commencement speech built an entire philosophy around "
         "this single habit. Researchers often describe it as a &ldquo;keystone habit.&rdquo; "
         "<a href=\"/holiday/national-make-your-bed-day/\">Full holiday page &rarr;</a>"),
        ("no-news-is-good-news-day",
         "The date functions as a deliberate counterpoint, encouraging a full digital detox from news and social "
         "media rather than more consumption. <a href=\"/holiday/no-news-is-good-news-day/\">Full holiday page &rarr;</a>"),

        ("national-chocolate-milkshake-day",
         "The word &ldquo;milkshake&rdquo; first appeared in print in 1885 &mdash; describing an alcoholic whiskey drink, "
         "nothing like the dessert it means today. <a href=\"/holiday/national-chocolate-milkshake-day/\">Full holiday page &rarr;</a>"),
        ("national-hug-high-5-day",
         "Founded by Philadelphia's David Sylvester, who chose this date because his childhood mentor died in the "
         "World Trade Center on 9/11 &mdash; the day after, he says, is exactly when people most need a hug. Since "
         "then he's bicycled across multiple continents, hugging and high-fiving more than half a million people. "
         "<a href=\"/holiday/national-hug-and-high-5-day/\">Full holiday page &rarr;</a>"),

        ("fortune-cookie-day",
         "Despite the strong Chinese-American association, fortune cookies actually originated in Japan, where "
         "they were known as &ldquo;tsujiura senbei&rdquo; as early as the 19th century. "
         "<a href=\"/holiday/fortune-cookie-day/\">Full holiday page &rarr;</a>"),
        ("supernatural-day",
         "Marks the 2005 premiere of the show's pilot episode, which went on to run for 15 seasons and 327 "
         "episodes. The iconic '67 Impala nearly wasn't the car at all. <a href=\"/holiday/supernatural-day/\">Full holiday page &rarr;</a>"),

        ("national-cream-filled-donut-day",
         "The Boston cream version is directly modeled on Boston cream pie, borrowing its custard filling and "
         "chocolate glaze. <a href=\"/holiday/national-cream-filled-donut-day/\">Full holiday page &rarr;</a>"),
        ("national-eat-a-hoagie-day",
         "The name likely traces to Philadelphia's Hog Island shipyard, where workers nicknamed &ldquo;hoggies&rdquo; "
         "reportedly ate oversized sandwiches on the job. Philadelphia made it official in 1992. "
         "<a href=\"/holiday/national-eat-a-hoagie-day/\">Full holiday page &rarr;</a>"),

        ("make-a-hat-day",
         "The phrase &ldquo;hat trick&rdquo; actually comes from cricket, where a bowler taking three wickets on three "
         "consecutive balls traditionally earned a new hat. <a href=\"/holiday/make-a-hat-day/\">Full holiday page &rarr;</a>"),
        ("national-crème-de-menthe-day",
         "First commercially produced in 19th-century France, and its bright green color is entirely artificial "
         "&mdash; a genuinely colorless liqueur with food coloring added. <a href=\"/holiday/national-crème-de-menthe-day/\">Full holiday page &rarr;</a>"),

        ("national-guacamole-day",
         "The word comes from the Aztec Nahuatl &ldquo;ahuacamolli,&rdquo; literally &ldquo;avocado sauce.&rdquo; Americans "
         "reportedly eat over 100 million pounds of avocados during Super Bowl weekend alone. "
         "<a href=\"/holiday/national-guacamole-day/\">Full holiday page &rarr;</a>"),
        ("national-play-doh-day",
         "Originally sold in the 1930s as a wallpaper cleaner, only rebranded as a children's toy in the "
         "mid-1950s. Its distinctive smell was officially copyrighted by Hasbro in 2018. "
         "<a href=\"/holiday/national-play-doh-day/\">Full holiday page &rarr;</a>"),

        ("national-apple-dumpling-day",
         "Believed to have originated in England, evolving from earlier fruit-and-pastry dishes before becoming a "
         "defining American fall dessert. <a href=\"/holiday/national-apple-dumpling-day/\">Full holiday page &rarr;</a>"),
        ("national-it-professionals-day",
         "Founded by SolarWinds, an IT management software company, with its first observance in 2015. "
         "<a href=\"/holiday/national-it-professionals-day/\">Full holiday page &rarr;</a>"),

        ("national-cheeseburger-day",
         "The exact origin is genuinely disputed, though Lionel Sternberger is often credited with serving one of "
         "the first in the mid-1920s at The Rite Spot in Pasadena. <a href=\"/holiday/national-cheeseburger-day/\">Full holiday page &rarr;</a>"),
        ("national-rice-krispie-treat-day",
         "Invented in 1939 by Mildred Day and Malitta Jensen at Kellogg's own home economics department, "
         "originally created as a fundraiser for the Camp Fire Girls. <a href=\"/holiday/national-rice-krispie-treat-day/\">Full holiday page &rarr;</a>"),

        ("butterscotch-pudding-day",
         "The &ldquo;scotch&rdquo; in butterscotch likely derives from &ldquo;scotching,&rdquo; meaning to score or cut into "
         "pieces &mdash; a common step in making hard candy. <a href=\"/holiday/butterscotch-pudding-day/\">Full holiday page &rarr;</a>"),
        ("international-talk-like-a-pirate-day",
         "Conceived in 1995 by two friends in Albany, Oregon as an inside joke, and the date was chosen simply "
         "because it was one of their ex-wives' birthdays. It only went global after Dave Barry wrote about it in "
         "2002. <a href=\"/holiday/international-talk-like-a-pirate-day/\">Full holiday page &rarr;</a>"),

        ("national-pepperoni-pizza-day",
         "Consistently ranked as America's most popular pizza topping. The word itself is an American invention "
         "&mdash; in Italian, &ldquo;peperoni&rdquo; actually refers to bell peppers. <a href=\"/holiday/national-pepperoni-pizza-day/\">Full holiday page &rarr;</a>"),
        ("string-cheese-day",
         "Gets its stringy texture from the <em>pasta filata</em>, or &ldquo;spun paste,&rdquo; method, where curds are "
         "heated and stretched until the proteins align into parallel fibers. <a href=\"/holiday/string-cheese-day/\">Full holiday page &rarr;</a>"),

        ("miniature-golf-day",
         "The first American course, &ldquo;Thistle Dhu,&rdquo; opened in Pinehurst, North Carolina in 1916. Some early "
         "courses used unusual surfaces for their greens, including crushed cottonseed hulls. "
         "<a href=\"/holiday/miniature-golf-day/\">Full holiday page &rarr;</a>"),
        ("national-pecan-cookie-day",
         "Pecans are the only major tree nut native to North America, and the trees themselves can keep producing "
         "nuts for more than 300 years. <a href=\"/holiday/national-pecan-cookie-day/\">Full holiday page &rarr;</a>"),

        ("hobbit-day",
         "The date isn't arbitrary &mdash; September 22nd is explicitly named in the text as the shared birthday of "
         "Bilbo and Frodo Baggins. It anchors &ldquo;Tolkien Week,&rdquo; organized by the American Tolkien Society "
         "since 1978. <a href=\"/holiday/hobbit-day/\">Full holiday page &rarr;</a>"),
        ("ice-cream-cone-day",
         "Popularly traced to the 1904 St. Louis World's Fair, where an ice cream vendor reportedly ran out of "
         "dishes and partnered with a nearby waffle vendor. An earlier patent for a similar edible cup actually "
         "predates the fair. <a href=\"/holiday/ice-cream-cone-day/\">Full holiday page &rarr;</a>"),

        ("checkers-day",
         "Precursors to the game trace back to ancient Mesopotamia and Egypt. In 2007, a computer program called "
         "Chinook formally &ldquo;solved&rdquo; checkers, proving perfect play from both sides always ends in a draw. "
         "<a href=\"/holiday/checkers-day/\">Full holiday page &rarr;</a>"),
        ("national-great-american-pot-pie-day",
         "The concept goes back to ancient Roman and Greek cooking, where meat and vegetables were baked inside "
         "pastry long before it became American comfort food. <a href=\"/holiday/national-great-american-pot-pie-day/\">Full holiday page &rarr;</a>"),

        ("heritage-day",
         "A South African public holiday with layered origins &mdash; long known in KwaZulu-Natal as Shaka Day, "
         "honoring the Zulu king's presumed 1828 death, before objections during 1994's holiday-list negotiations "
         "reframed it as a day for all South Africans' heritage. Since 2005 it's also National Braai Day, backed "
         "by Archbishop Desmond Tutu. <a href=\"/holiday/heritage-day/\">Full holiday page &rarr;</a>"),
        ("national-cherries-jubilee-day",
         "Reportedly created by the legendary chef Auguste Escoffier for Queen Victoria's Diamond Jubilee in "
         "1897, which is where the name comes from. <a href=\"/holiday/national-cherries-jubilee-day/\">Full holiday page &rarr;</a>"),

        ("national-comic-book-day",
         "The first modern American comic book, &ldquo;Famous Funnies,&rdquo; launched in 1933, mostly reprinting "
         "existing newspaper strips. A copy of Action Comics #1 sold for over $6 million in 2024. "
         "<a href=\"/holiday/national-comic-book-day/\">Full holiday page &rarr;</a>"),
        ("national-quesadilla-day",
         "The name literally combines the Spanish &ldquo;queso&rdquo; (cheese) and &ldquo;tortilla.&rdquo; In parts of central and "
         "southern Mexico, a quesadilla doesn't automatically include cheese unless you specifically ask for it. "
         "<a href=\"/holiday/national-quesadilla-day/\">Full holiday page &rarr;</a>"),

        ("love-note-day",
         "The oldest known love poem, inscribed on a Sumerian clay tablet, dates back roughly 4,000 years. "
         "<a href=\"/holiday/love-note-day/\">Full holiday page &rarr;</a>"),
        ("national-pancake-day",
         "Pancake-like foods date back to the Stone Age, made from little more than ground grains and water. "
         "Competitive &ldquo;pancake races&rdquo; have continued in Olney, England since 1445. "
         "<a href=\"/holiday/national-pancake-day/\">Full holiday page &rarr;</a>"),

        ("national-chocolate-milk-day",
         "Credited to Sir Hans Sloane, an Irish physician who encountered a cocoa drink in Jamaica in the late "
         "1600s and added milk to make it more palatable back in Europe. <a href=\"/holiday/national-chocolate-milk-day/\">Full holiday page &rarr;</a>"),
        ("national-corned-beef-hash-day",
         "The word &ldquo;hash&rdquo; comes from the French &ldquo;hacher,&rdquo; meaning &ldquo;to chop.&rdquo; It saw a real surge in "
         "popularity during WWI and WWII rationing. <a href=\"/holiday/national-corned-beef-hash-day/\">Full holiday page &rarr;</a>"),

        ("national-drink-beer-day",
         "Beer ranks as the third most popular drink worldwide, trailing only water and tea. Germany's "
         "Weihenstephan brewery, founded in 1040, is the world's oldest continuously operating brewery. "
         "<a href=\"/holiday/national-drink-beer-day/\">Full holiday page &rarr;</a>"),
        ("world-rabies-day",
         "Deliberately timed to the anniversary of Louis Pasteur's death, the scientist who helped develop the "
         "first effective rabies vaccine. Rabies is nearly 100% fatal once symptoms appear, but almost entirely "
         "preventable through vaccination. <a href=\"/holiday/world-rabies-day/\">Full holiday page &rarr;</a>"),

        ("biscotti-day",
         "The name comes from the Latin &ldquo;bis coctus,&rdquo; literally &ldquo;twice-baked,&rdquo; describing exactly how "
         "they're made. <a href=\"/holiday/biscotti-day/\">Full holiday page &rarr;</a>"),
        ("national-coffee-day",
         "Coffee is the second-most traded commodity in the world, behind only crude oil. Coffee &ldquo;beans&rdquo; are "
         "technically seeds found inside a fruit called a coffee cherry. <a href=\"/holiday/national-coffee-day/\">Full holiday page &rarr;</a>"),

        ("chewing-gum-day",
         "The oldest known chewing gum is a roughly 9,000-year-old piece of birch bark tar, discovered by an "
         "archaeology student in Finland. Modern gum traces to the 1860s. <a href=\"/holiday/chewing-gum-day/\">Full holiday page &rarr;</a>"),
        ("national-hot-mulled-cider-day",
         "The practice of &ldquo;mulling&rdquo; &mdash; heating and spicing a drink &mdash; dates back centuries, tied historically "
         "to wassailing, the old English custom of visiting orchards in winter to toast the trees' health. "
         "<a href=\"/holiday/national-hot-mulled-cider-day/\">Full holiday page &rarr;</a>"),
    ],
}

OCTOBER = {
    "month_num": 10,
    "month_name": "October",
    "url_slug": "october",
    "title": "The Complete Guide to October's Obscure Holidays | Obscure Holiday Calendar",
    "description": (
        "A complete, day-by-day guide to all 62 obscure and offbeat holidays in October — "
        "from International Coffee Day to Halloween — with history, context, and links to "
        "the full write-up for each one."
    ),
    "h1": "The Complete Guide to October's Obscure Holidays",
    "date_published": "2026-07-28",
    "date_modified": "2026-07-28",
    "intro_html": """    <p>October leans hard into autumn and the approach of Halloween &mdash; Carve a Pumpkin Day and
    Halloween itself close out the month, while National Mole Day (a chemistry pun on Avogadro's number)
    and Mad Hatter Day (a literal date hidden in a 19th-century illustration) show up in between.</p>

    <p>This guide walks through all 62, day by day, with a bit of history or context for each one and a
    link to the full write-up &mdash; complete fun facts, ways to celebrate, and sourcing &mdash; on its own page.</p>""",
    "why_html": """    <p>A genuine cluster of October's holidays are literary or pop-culture tributes tied to a specific
    text or date &mdash; Mad Hatter Day's price-tag pun, Mean Girls Day's exact movie quote, National Mole Day's
    chemistry constant, Dictionary Day marking Noah Webster's birthday. The back half of the month builds
    steadily toward Halloween, with pumpkin, candy corn, and mischief-adjacent holidays clustering in the
    final week.</p>""",
    "how_to_use_html": """    <p>Holidays are grouped by date below. Each entry gets a short original write-up &mdash; not a repeat
    of the fact sheet &mdash; plus a link to the full holiday page if you want the deeper dive: complete fun
    facts, ways to celebrate, and sourcing.</p>""",
    "about_html": """    <p>This guide is part of the Obscure Holiday Calendar project &mdash; the same database that powers
    the iOS and Android apps and the individual holiday pages on this site. It exists to give a single,
    readable overview of an entire month at once, instead of requiring 62 separate page visits.</p>""",
    "faq": [
        (
            "How many obscure holidays are there in October?",
            "62, spread across all 31 days.",
        ),
        (
            "What's the most unusual holiday in October?",
            "National Mole Day (Oct 23) is a strong contender — chemistry enthusiasts observe it from 6:02am to "
            "6:02pm specifically because those numbers match Avogadro's number, 6.02 x 10^23.",
        ),
        (
            "Are there a lot of Halloween-adjacent holidays in October?",
            "Yes — Mischief Night, National Candy Corn Day, Carve a Pumpkin Day, and Halloween itself all land "
            "in the final two days of the month.",
        ),
        (
            "Where can I find the full history and fun facts for each holiday?",
            "Every holiday name in this guide links to its own dedicated page with a longer write-up, sourced "
            "fun facts, and ideas for how to celebrate.",
        ),
    ],
    "entries": [
        ("international-coffee-day",
         "Officially launched by the International Coffee Organization on October 1, 2015. Legend traces "
         "coffee's discovery to an Ethiopian goat herder named Kaldi, whose goats reportedly got energetic after "
         "eating coffee cherries. <a href=\"/holiday/international-coffee-day/\">Full holiday page &rarr;</a>"),
        ("national-homemade-cookies-day",
         "The word &ldquo;cookie&rdquo; comes from the Dutch &ldquo;koekje,&rdquo; meaning &ldquo;little cake.&rdquo; Americans eat over 2 "
         "billion cookies a year. <a href=\"/holiday/national-homemade-cookies-day/\">Full holiday page &rarr;</a>"),

        ("national-fried-scallops-day",
         "Scallops are unusual among bivalves for their ability to actually swim, rapidly clapping their shells "
         "together to propel themselves. <a href=\"/holiday/national-fried-scallops-day/\">Full holiday page &rarr;</a>"),
        ("national-name-your-car-day",
         "A 2013 Esurance survey found that roughly 40% of American drivers had given their car a specific name. "
         "<a href=\"/holiday/national-name-your-car-day/\">Full holiday page &rarr;</a>"),

        ("mean-girls-day",
         "The date comes directly from the film's most quoted exchange &mdash; Cady recounting Aaron Samuels asking "
         "&ldquo;What day is it?&rdquo; and answering &ldquo;It's October 3rd.&rdquo; Lindsay Lohan originally auditioned for "
         "Regina George, the role that went to Rachel McAdams. <a href=\"/holiday/mean-girls-day/\">Full holiday page &rarr;</a>"),
        ("national-techies-day",
         "Ada Lovelace is widely credited as the first computer programmer, for her 19th-century work on Charles "
         "Babbage's Analytical Engine. The word &ldquo;bug&rdquo; traces to Grace Hopper's team finding an actual moth "
         "causing a malfunction in 1947. <a href=\"/holiday/national-techies-day/\">Full holiday page &rarr;</a>"),

        ("national-golf-lovers-day",
         "The standard 18-hole course exists mostly by historical accident &mdash; St Andrews' Old Course set that "
         "number in 1764, and it just became the convention everyone followed. <a href=\"/holiday/national-golf-lovers-day/\">Full holiday page &rarr;</a>"),
        ("national-taco-day",
         "Americans eat an estimated 4.5 billion tacos a year. The word &ldquo;taco&rdquo; itself likely comes from "
         "18th-century Mexican silver mines, originally referring to paper-wrapped gunpowder cartridges. "
         "<a href=\"/holiday/national-taco-day/\">Full holiday page &rarr;</a>"),

        ("do-something-nice-day",
         "Traces to the early 2000s United States, with research backing up the core idea &mdash; performing kind "
         "acts genuinely boosts the giver's own happiness. <a href=\"/holiday/do-something-nice-day/\">Full holiday page &rarr;</a>"),
        ("national-apple-betty-day",
         "Distinct from an apple crisp specifically because of its topping &mdash; buttered breadcrumbs or bread "
         "pieces, not an oat-based streusel. <a href=\"/holiday/national-apple-betty-day/\">Full holiday page &rarr;</a>"),

        ("german-american-day",
         "Marks the exact 1683 arrival of 13 German Quaker families in Philadelphia, who went on to found "
         "Germantown, Pennsylvania. It fell out of observance during World War I and wasn't officially revived "
         "until Ronald Reagan re-established it in 1983. <a href=\"/holiday/german-american-day/\">Full holiday page &rarr;</a>"),
        ("mad-hatter-day",
         "The date comes from a genuine visual detail &mdash; the &ldquo;10/6&rdquo; price tag on the Mad Hatter's hat in "
         "John Tenniel's original illustrations. Lewis Carroll never actually named the character &ldquo;Mad "
         "Hatter&rdquo; in the text. <a href=\"/holiday/mad-hatter-day/\">Full holiday page &rarr;</a>"),

        ("bathtub-day",
         "The earliest known personal bathtubs date to ancient Crete around 1700 BC, made of hardened pottery. "
         "<a href=\"/holiday/bathtub-day/\">Full holiday page &rarr;</a>"),
        ("national-chocolate-covered-pretzel-day",
         "The pretzel component alone may date back to 610 AD in Europe, layered into a much more modern "
         "sweet-and-salty combination. <a href=\"/holiday/national-chocolate-covered-pretzel-day/\">Full holiday page &rarr;</a>"),

        ("american-touch-tag-day",
         "Variations of tag have been documented across cultures for thousands of years. It's since evolved into "
         "an actual competitive sport, &ldquo;World Chase Tag.&rdquo; <a href=\"/holiday/american-touch-tag-day/\">Full holiday page &rarr;</a>"),
        ("pierogi-day",
         "The word &ldquo;pierogi&rdquo; is already plural in Polish &mdash; the singular form is &ldquo;pier&oacute;g.&rdquo; "
         "<a href=\"/holiday/pierogi-day/\">Full holiday page &rarr;</a>"),

        ("leif-erikson-day",
         "Marks Leif Erikson's landing in North America around 1000 CE, nearly 500 years before Columbus &mdash; "
         "though the October 9th date itself actually commemorates the 1825 arrival of the ship <em>Restauration</em>, "
         "marking the start of organized Norwegian immigration to the US. <a href=\"/holiday/leif-erikson-day/\">Full holiday page &rarr;</a>"),
        ("moldy-cheese-day",
         "The blue veins in Roquefort, Gorgonzola, and Stilton all come from <em>Penicillium roqueforti</em>, "
         "while Brie and Camembert's white rinds come from a related but distinct mold. "
         "<a href=\"/holiday/moldy-cheese-day/\">Full holiday page &rarr;</a>"),

        ("angel-food-cake-day",
         "Uniquely contains no butter, oil, or egg yolks at all &mdash; its entire structure comes from whipped egg "
         "whites. <a href=\"/holiday/angel-food-cake-day/\">Full holiday page &rarr;</a>"),
        ("national-cake-decorating-day",
         "Elaborate icing techniques saw a major boost in popularity during the Victorian era. "
         "<a href=\"/holiday/national-cake-decorating-day/\">Full holiday page &rarr;</a>"),

        ("its-my-party-day",
         "Directly inspired by Lesley Gore's 1963 hit song of the same name. <a href=\"/holiday/its-my-party-day/\">Full holiday page &rarr;</a>"),
        ("sausage-pizza-day",
         "Sausage consistently ranks among the top five most popular pizza toppings worldwide. "
         "<a href=\"/holiday/sausage-pizza-day/\">Full holiday page &rarr;</a>"),

        ("cookbook-launch-day",
         "The earliest known recipe collection, &ldquo;Apicius,&rdquo; comes from ancient Rome &mdash; arguably the first "
         "cookbook ever written. <a href=\"/holiday/cookbook-launch-day/\">Full holiday page &rarr;</a>"),
        ("gumbo-day",
         "The name likely comes from &ldquo;ngombo,&rdquo; a West African word for okra, reflecting the dish's African "
         "culinary roots. <a href=\"/holiday/gumbo-day/\">Full holiday page &rarr;</a>"),

        ("national-mm-day",
         "Inspired by Forrest Mars Sr.'s observation of Spanish Civil War soldiers eating chocolate pellets coated "
         "in a hard candy shell to prevent melting. The &ldquo;M&rdquo; stands for both Mars and Murrie. "
         "<a href=\"/holiday/national-mm-day/\">Full holiday page &rarr;</a>"),
        ("national-train-your-brain-day",
         "The human brain weighs only about 3 pounds but consumes roughly 20% of the body's total oxygen and "
         "calories. <a href=\"/holiday/national-train-your-brain-day/\">Full holiday page &rarr;</a>"),

        ("be-bald-and-be-free-day",
         "Historical and contemporary bald figures span from Julius Caesar to modern tech executives. Some "
         "studies have found bald men are occasionally perceived by others as more dominant or intelligent. "
         "<a href=\"/holiday/be-bald-and-be-free-day/\">Full holiday page &rarr;</a>"),
        ("dessert-day",
         "The word &ldquo;dessert&rdquo; comes from the French &ldquo;desservir,&rdquo; meaning &ldquo;to clear the table&rdquo; &mdash; a "
         "reference to when the course is served, not what it contains. <a href=\"/holiday/dessert-day/\">Full holiday page &rarr;</a>"),

        ("mushroom-day",
         "Mushrooms aren't plants at all &mdash; they belong to their own biological kingdom, Fungi, making them "
         "genetically closer to animals than to plants. <a href=\"/holiday/mushroom-day/\">Full holiday page &rarr;</a>"),
        ("national-grouch-day",
         "Oscar the Grouch remains the most famous fictional grouch by a wide margin. "
         "<a href=\"/holiday/national-grouch-day/\">Full holiday page &rarr;</a>"),

        ("dictionary-day",
         "Marks Noah Webster's birthday. His 1828 &ldquo;An American Dictionary of the English Language&rdquo; took 20 "
         "years to compile and included around 70,000 words, 12,000 of which had never appeared in any "
         "dictionary before. <a href=\"/holiday/dictionary-day/\">Full holiday page &rarr;</a>"),
        ("feral-cat-day",
         "Feral cats are genuinely distinct from strays &mdash; strays are lost or abandoned pets, while feral cats "
         "are born in the wild and typically avoid human contact entirely. <a href=\"/holiday/feral-cat-day/\">Full holiday page &rarr;</a>"),

        ("national-pasta-day",
         "There are more than 600 distinct documented pasta shapes worldwide. Noodle-like foods appear in "
         "Chinese cuisine as far back as 4,000 years, predating the Italian tradition. "
         "<a href=\"/holiday/national-pasta-day/\">Full holiday page &rarr;</a>"),
        ("wear-something-gaudy-day",
         "The word &ldquo;gaudy&rdquo; actually traces to the Old French &ldquo;gaudir,&rdquo; meaning &ldquo;to rejoice&rdquo; or "
         "&ldquo;to make merry.&rdquo; <a href=\"/holiday/wear-something-gaudy-day/\">Full holiday page &rarr;</a>"),

        ("national-chocolate-cupcake-day",
         "The term &ldquo;cup cake&rdquo; first appeared in print in Amelia Simmons's 1796 cookbook &ldquo;American "
         "Cookery.&rdquo; <a href=\"/holiday/national-chocolate-cupcake-day/\">Full holiday page &rarr;</a>"),
        ("no-beard-day",
         "Lands deliberately right before Movember, which encourages growing facial hair through November to "
         "raise money for men's health causes. <a href=\"/holiday/no-beard-day/\">Full holiday page &rarr;</a>"),

        ("evaluate-your-life-day",
         "No widely documented origin, but the underlying premise mirrors standard self-improvement advice "
         "packaged as an annual prompt. <a href=\"/holiday/evaluate-your-life-day/\">Full holiday page &rarr;</a>"),
        ("seafood-bisque-day",
         "The word &ldquo;bisque&rdquo; possibly traces to &ldquo;bis cuites,&rdquo; meaning &ldquo;twice cooked,&rdquo; referencing how the "
         "shells are prepared. <a href=\"/holiday/seafood-bisque-day/\">Full holiday page &rarr;</a>"),

        ("brandied-fruit-day",
         "Before refrigeration, brandying fruit was a genuinely practical preservation method, not just a flavor "
         "choice. <a href=\"/holiday/brandied-fruit-day/\">Full holiday page &rarr;</a>"),
        ("international-sloth-day",
         "Launched in 2010 by the AIUNAU Foundation. Sloths only climb down from trees to defecate roughly once "
         "a week, which is precisely when they're most vulnerable to predators. <a href=\"/holiday/international-sloth-day/\">Full holiday page &rarr;</a>"),

        ("count-your-buttons-day",
         "The earliest known buttons, dating to around 2000 BCE in the Indus Valley Civilization, were purely "
         "ornamental, not functional fasteners. <a href=\"/holiday/count-your-buttons-day/\">Full holiday page &rarr;</a>"),
        ("national-pumpkin-cheesecake-day",
         "Cheesecake's documented history stretches back to ancient Greece, reportedly served at the Olympic "
         "Games. <a href=\"/holiday/national-pumpkin-cheesecake-day/\">Full holiday page &rarr;</a>"),

        ("national-caps-lock-day",
         "Reportedly created in 2000 by a programmer named Derek Arnold, amused by how often the key gets "
         "misused online. There's a second, separate Caps Lock Day on June 28th, tied to Billy Mays's birthday. "
         "<a href=\"/holiday/national-caps-lock-day/\">Full holiday page &rarr;</a>"),
        ("smart-is-cool-day",
         "The average awake adult brain generates about 20 watts of electrical activity &mdash; enough to power a dim "
         "light bulb. <a href=\"/holiday/smart-is-cool-day/\">Full holiday page &rarr;</a>"),

        ("national-mole-day",
         "The date and time &mdash; 10/23, 6:02am to 6:02pm &mdash; are both pulled directly from the digits of "
         "Avogadro's number, 6.02 x 10<sup>23</sup>. <a href=\"/holiday/national-mole-day/\">Full holiday page &rarr;</a>"),
        ("tv-talk-show-host-day",
         "Marks Johnny Carson's birthday, who hosted NBC's &ldquo;The Tonight Show&rdquo; for 30 years and effectively "
         "set the format's template. <a href=\"/holiday/tv-talk-show-host-day/\">Full holiday page &rarr;</a>"),

        ("national-bologna-day",
         "The name traces to Bologna, Italy, the city that gave the world mortadella. The slang term &ldquo;baloney,&rdquo; "
         "meaning nonsense, is simply a phonetic spelling of the same word. <a href=\"/holiday/national-bologna-day/\">Full holiday page &rarr;</a>"),
        ("national-food-day",
         "Established in 1975 by the Center for Science in the Public Interest, built around five specific "
         "goals: real food, reducing diet-related disease, sustainable agriculture, food justice, and ending "
         "hunger. <a href=\"/holiday/national-food-day/\">Full holiday page &rarr;</a>"),

        ("national-greasy-foods-day",
         "The specific combination of fat, sugar, and salt found in most greasy foods directly stimulates the "
         "brain's reward system. <a href=\"/holiday/national-greasy-foods-day/\">Full holiday page &rarr;</a>"),
        ("sourest-day",
         "A purely modern, whimsical holiday with no historical roots, built entirely around the shared "
         "experience of intensely tart candy and fruit. <a href=\"/holiday/sourest-day/\">Full holiday page &rarr;</a>"),

        ("mincemeat-day",
         "Genuinely used to contain actual chopped meat historically, which helped preserve the mixture before "
         "refrigeration existed. By the Victorian era, the meat had largely been replaced by suet. "
         "<a href=\"/holiday/mincemeat-day/\">Full holiday page &rarr;</a>"),
        ("national-pumpkin-day",
         "Pumpkins are technically a fruit, specifically a type of berry, since they carry seeds. Illinois alone "
         "grows more than 500 million pounds annually, the most of any US state. "
         "<a href=\"/holiday/national-pumpkin-day/\">Full holiday page &rarr;</a>"),

        ("american-beer-day",
         "The US has more operating breweries than any other country in the world, with over 9,000 active as of "
         "recent counts. <a href=\"/holiday/american-beer-day/\">Full holiday page &rarr;</a>"),
        ("national-black-cat-day",
         "Black cats are considered good luck in several cultures, including Britain, Ireland, and Japan &mdash; "
         "directly opposite the superstition common in the US. <a href=\"/holiday/national-black-cat-day/\">Full holiday page &rarr;</a>"),

        ("plush-animal-lovers-day",
         "The teddy bear itself traces to Theodore Roosevelt's name, and Germany's Steiff company is widely "
         "credited with producing some of the first commercially made stuffed toys. <a href=\"/holiday/plush-animal-lovers-day/\">Full holiday page &rarr;</a>"),
        ("wild-foods-day",
         "Foraging predates organized agriculture by hundreds of thousands of years. Several familiar cultivated "
         "vegetables, like carrots and cabbage, were selectively bred from wild foraged ancestors. "
         "<a href=\"/holiday/wild-foods-day/\">Full holiday page &rarr;</a>"),

        ("hermit-day",
         "The word &ldquo;hermit&rdquo; comes from the Greek &ldquo;eremites,&rdquo; meaning &ldquo;person of the desert,&rdquo; originally "
         "describing early religious recluses. <a href=\"/holiday/hermit-day/\">Full holiday page &rarr;</a>"),
        ("national-cat-day",
         "Founded in 2005 by Colleen Paige, the same advocate behind National Dog Day and National Puppy Day. "
         "<a href=\"/holiday/national-cat-day/\">Full holiday page &rarr;</a>"),

        ("mischief-night",
         "Known by different regional names depending on where you are &mdash; Devil's Night in Detroit, where it's "
         "historically been linked to a real spike in arson fires, or Cabbage Night in New England. "
         "<a href=\"/holiday/mischief-night/\">Full holiday page &rarr;</a>"),
        ("national-candy-corn-day",
         "Invented in the late 1880s by George Renninger, originally marketed under the much less appealing name "
         "&ldquo;Chicken Feed.&rdquo; Roughly 9 billion pieces get produced every year. "
         "<a href=\"/holiday/national-candy-corn-day/\">Full holiday page &rarr;</a>"),

        ("carve-a-pumpkin-day",
         "The tradition actually started in Ireland with turnips and potatoes, not pumpkins. The name "
         "&ldquo;jack-o'-lantern&rdquo; comes from an old Irish folktale about a man named Stingy Jack, condemned to "
         "wander the earth with only a glowing coal inside a carved turnip. <a href=\"/holiday/carve-a-pumpkin-day/\">Full holiday page &rarr;</a>"),
        ("halloween",
         "Traces back to the ancient Celtic festival of Samhain, which marked the end of harvest season and the "
         "point when the boundary between the living and the dead was believed to thin. There's an actual "
         "clinical term for the fear of Halloween: samhainophobia. <a href=\"/holiday/halloween/\">Full holiday page &rarr;</a>"),
    ],
}

NOVEMBER = {
    "month_num": 11,
    "month_name": "November",
    "url_slug": "november",
    "title": "The Complete Guide to November's Obscure Holidays | Obscure Holiday Calendar",
    "description": (
        "A complete, day-by-day guide to all 62 obscure and offbeat holidays in November — "
        "from National Author's Day to National Mousse Day — with history, context, and "
        "links to the full write-up for each one."
    ),
    "h1": "The Complete Guide to November's Obscure Holidays",
    "date_published": "2026-07-28",
    "date_modified": "2026-07-28",
    "intro_html": """    <p>November moves from Halloween's aftermath straight into Thanksgiving, with genuine institutional
    weight along the way &mdash; World Toilet Day is an official UN observance, Guy Fawkes Day marks a real
    1605 conspiracy, and Beaujolais Nouveau Day releases at precisely 12:01 AM on the third Thursday every
    year.</p>

    <p>This guide walks through all 62, day by day, with a bit of history or context for each one and a
    link to the full write-up &mdash; complete fun facts, ways to celebrate, and sourcing &mdash; on its own page.</p>""",
    "why_html": """    <p>A striking number of November's holidays are anchored to exact historical dates and events &mdash;
    Tutankhamun's Tomb Discovery Day, Mickey Mouse's 1928 debut, Mariner 4's 1964 Mars flyby, AT&amp;T's 1963
    Touch-Tone launch. The month also builds directly toward Thanksgiving, with a genuine cluster of dessert,
    bread, and pie holidays landing in the final two weeks.</p>""",
    "how_to_use_html": """    <p>Holidays are grouped by date below. Each entry gets a short original write-up &mdash; not a repeat
    of the fact sheet &mdash; plus a link to the full holiday page if you want the deeper dive: complete fun
    facts, ways to celebrate, and sourcing.</p>""",
    "about_html": """    <p>This guide is part of the Obscure Holiday Calendar project &mdash; the same database that powers
    the iOS and Android apps and the individual holiday pages on this site. It exists to give a single,
    readable overview of an entire month at once, instead of requiring 62 separate page visits.</p>""",
    "faq": [
        (
            "How many obscure holidays are there in November?",
            "62, spread across all 30 days — including Beaujolais Nouveau Day, which moves each year to the "
            "third Thursday of the month.",
        ),
        (
            "What's the most historically significant holiday in November?",
            "Tutankhamun's Tomb Discovery Day (Nov 26) marks Howard Carter's actual 1922 discovery — one of the "
            "best-documented archaeological finds in history, right down to his famous exchange with Lord "
            "Carnarvon.",
        ),
        (
            "Are there a lot of Thanksgiving-adjacent holidays in November?",
            "Yes — National Cake Day, National Bavarian Cream Pie Day, National French Toast Day, and "
            "Thanksgiving itself all land within days of each other in the last week of the month.",
        ),
        (
            "Where can I find the full history and fun facts for each holiday?",
            "Every holiday name in this guide links to its own dedicated page with a longer write-up, sourced "
            "fun facts, and ideas for how to celebrate.",
        ),
    ],
    "entries": [
        ("national-authors-day",
         "First proposed in 1928 by Nellie Verne Burt McPherson, a member of a small Illinois women's club, "
         "after she started corresponding directly with author Irving Bacheller. <a href=\"/holiday/national-authors-day/\">Full holiday page &rarr;</a>"),
        ("national-deep-fried-clams-day",
         "Credited to Lawrence &ldquo;Chubby&rdquo; Woodman of Woodman's in Essex, Massachusetts, who reportedly "
         "invented the dish in 1916. <a href=\"/holiday/national-deep-fried-clams-day/\">Full holiday page &rarr;</a>"),

        ("deviled-egg-day",
         "The word &ldquo;deviled&rdquo; has described spicy or pungent food since the 18th century. A close precursor "
         "was already a popular appetizer in ancient Rome. <a href=\"/holiday/deviled-egg-day/\">Full holiday page &rarr;</a>"),
        ("look-for-circles-day",
         "The wheel, arguably humanity's single most transformative circular invention, dates back to at least "
         "3500 BCE. <a href=\"/holiday/look-for-circles-day/\">Full holiday page &rarr;</a>"),

        ("cliché-day",
         "The word itself comes from French printing, originally describing a stereotype plate used to print the "
         "same image or text repeatedly. <a href=\"/holiday/cliché-day/\">Full holiday page &rarr;</a>"),
        ("national-sandwich-day",
         "Marks John Montagu's birthday, the 4th Earl of Sandwich, who supposedly requested meat between two "
         "slices of bread so he wouldn't have to leave a card game to eat. <a href=\"/holiday/national-sandwich-day/\">Full holiday page &rarr;</a>"),

        ("common-sense-day",
         "Genuinely lacks any formal recognition or documented origin, unlike most holidays on this calendar. "
         "Thomas Paine's 1776 pamphlet remains the most famous work to carry the phrase in its title. "
         "<a href=\"/holiday/common-sense-day/\">Full holiday page &rarr;</a>"),
        ("national-candy-day",
         "Timed right after Halloween, when candy is already top of mind. The average American reportedly eats "
         "about 25 pounds of candy a year. <a href=\"/holiday/national-candy-day/\">Full holiday page &rarr;</a>"),

        ("american-football-day",
         "Walter Camp, often called the &ldquo;Father of American Football,&rdquo; introduced foundational rule "
         "changes in the late 19th century, including the line of scrimmage and the system of downs. "
         "<a href=\"/holiday/american-football-day/\">Full holiday page &rarr;</a>"),
        ("guy-fawkes-day",
         "Marks the failed 1605 Gunpowder Plot, when Fawkes was caught guarding explosives beneath Parliament "
         "before he could detonate them. <a href=\"/holiday/guy-fawkes-day/\">Full holiday page &rarr;</a>"),

        ("national-nachos-day",
         "Invented in 1943 by Ignacio &ldquo;Nacho&rdquo; Anaya, a ma&icirc;tre d' at the Victory Club in Piedras Negras, "
         "Mexico &mdash; originally named &ldquo;Nachos especiales&rdquo; after its creator. <a href=\"/holiday/national-nachos-day/\">Full holiday page &rarr;</a>"),
        ("saxophone-day",
         "Marks Adolphe Sax's birthday. Despite typically being made of brass, the saxophone is technically a "
         "woodwind instrument, since it produces sound through a single-reed mouthpiece like a clarinet. "
         "<a href=\"/holiday/saxophone-day/\">Full holiday page &rarr;</a>"),

        ("bittersweet-chocolate-with-almonds-day",
         "Bittersweet chocolate typically runs 60 to 80% cocoa solids or higher. Nuts and chocolate have been "
         "paired since early Mesoamerican chocolate drinks. <a href=\"/holiday/bittersweet-chocolate-with-almonds-day/\">Full holiday page &rarr;</a>"),
        ("hug-a-bear-day",
         "The most expensive teddy bear ever sold, a Steiff &ldquo;Louis Vuitton&rdquo; bear, fetched $2.1 million at "
         "auction in 2000. <a href=\"/holiday/hug-a-bear-day/\">Full holiday page &rarr;</a>"),

        ("international-radiography-day",
         "Marks Wilhelm Conrad R&ouml;ntgen's 1895 discovery of X-rays, and his very first X-ray image was of his "
         "own wife's hand, clearly showing her bones and wedding ring. <a href=\"/holiday/international-radiography-day/\">Full holiday page &rarr;</a>"),
        ("national-cappuccino-day",
         "The name comes from the Capuchin friars, whose brown habits reportedly resembled the drink's color. "
         "<a href=\"/holiday/national-cappuccino-day/\">Full holiday page &rarr;</a>"),

        ("go-to-an-art-museum-day",
         "The Louvre remains the world's most visited art museum by a wide margin. Florence's Uffizi Gallery, "
         "established in 1581, is one of the oldest museums still operating today. <a href=\"/holiday/go-to-an-art-museum-day/\">Full holiday page &rarr;</a>"),
        ("international-tongue-twister-day",
         "MIT researchers once identified &ldquo;Pad kid poured curd pulled cold&rdquo; as potentially the hardest "
         "tongue twister in English to say quickly. <a href=\"/holiday/international-tongue-twister-day/\">Full holiday page &rarr;</a>"),

        ("forget-me-not-day",
         "The flower's name traces to the German &ldquo;Vergissmeinnicht,&rdquo; tied to a medieval legend about a "
         "knight who drowned retrieving the flowers for his beloved. <a href=\"/holiday/forget-me-not-day/\">Full holiday page &rarr;</a>"),
        ("vanilla-cupcake-day",
         "The earliest known &ldquo;cup cake&rdquo; recipe appears in Amelia Simmons's 1796 cookbook &ldquo;American "
         "Cookery.&rdquo; <a href=\"/holiday/vanilla-cupcake-day/\">Full holiday page &rarr;</a>"),

        ("national-sundae-day",
         "Both Ithaca, New York and Two Rivers, Wisconsin claim to have invented the sundae in the late 19th "
         "century. The name likely emerged as a workaround for &ldquo;blue laws&rdquo; that banned selling ice cream "
         "sodas on Sundays. <a href=\"/holiday/national-sundae-day/\">Full holiday page &rarr;</a>"),
        ("origami-day",
         "The date ties to two things at once: the approximate publication of &ldquo;Senbazuru Orikata,&rdquo; the "
         "first known dedicated origami instruction book from 1797, and Sadako Sasaki's story of a thousand "
         "paper cranes. <a href=\"/holiday/origami-day/\">Full holiday page &rarr;</a>"),

        ("happy-hour-day",
         "The term actually originated in the U.S. Navy during World War I, referring to scheduled entertainment "
         "time for sailors. <a href=\"/holiday/happy-hour-day/\">Full holiday page &rarr;</a>"),
        ("national-pizza-with-the-works-except-anchovies-day",
         "Most pizzerias just call this a &ldquo;Supreme&rdquo; or &ldquo;Deluxe&rdquo; pizza. The specific anchovy exclusion "
         "nods to how polarizing the topping is. <a href=\"/holiday/national-pizza-with-the-works-except-anchovies-day/\">Full holiday page &rarr;</a>"),

        ("indian-pudding-day",
         "The &ldquo;Indian&rdquo; in the name refers to cornmeal, historically called &ldquo;Indian meal&rdquo; by colonists "
         "adapting British hasty pudding with what was locally available. <a href=\"/holiday/indian-pudding-day/\">Full holiday page &rarr;</a>"),
        ("sadie-hawkins-day",
         "Traces to a specific comic strip: Al Capp's &ldquo;Li'l Abner,&rdquo; which introduced the concept on "
         "November 13, 1937. <a href=\"/holiday/sadie-hawkins-day/\">Full holiday page &rarr;</a>"),

        ("national-pickle-day",
         "Pickled cucumbers date back to Mesopotamia as early as 2030 BC. During World War II, the U.S. "
         "government actually rationed pickles, believing they helped combat scurvy. <a href=\"/holiday/national-pickle-day/\">Full holiday page &rarr;</a>"),
        ("spicy-guacamole-day",
         "The word &ldquo;guacamole&rdquo; comes from the Aztec Nahuatl &ldquo;ahuacamolli,&rdquo; meaning &ldquo;avocado sauce.&rdquo; "
         "<a href=\"/holiday/spicy-guacamole-day/\">Full holiday page &rarr;</a>"),

        ("clean-out-your-refrigerator-day",
         "Deliberately timed just before Thanksgiving, to clear space ahead of the holiday cooking rush. "
         "<a href=\"/holiday/clean-out-your-refrigerator-day/\">Full holiday page &rarr;</a>"),
        ("national-spicy-hermit-cookie-day",
         "The &ldquo;hermit&rdquo; name is genuinely debated &mdash; some trace it to the cookie's ability to keep well for "
         "long periods, others to its plain, unassuming look. <a href=\"/holiday/national-spicy-hermit-cookie-day/\">Full holiday page &rarr;</a>"),

        ("have-a-party-with-your-bear-day",
         "The first teddy bears were created almost simultaneously and independently by Morris Michtom in the US "
         "and Richard Steiff in Germany. <a href=\"/holiday/have-a-party-with-your-bear-day/\">Full holiday page &rarr;</a>"),
        ("national-fast-food-day",
         "White Castle, founded in 1921, is widely considered America's first fast-food chain. "
         "<a href=\"/holiday/national-fast-food-day/\">Full holiday page &rarr;</a>"),

        ("homemade-bread-day",
         "Bread is one of the oldest prepared foods on record, with archaeological evidence suggesting it existed "
         "as far back as 30,000 years ago. <a href=\"/holiday/homemade-bread-day/\">Full holiday page &rarr;</a>"),
        ("national-baklava-day",
         "The earliest known layered dessert resembling baklava traces back to ancient Assyria, around the 8th "
         "century BCE. Some recipes call for as many as 40 ultra-thin layers of filo dough. "
         "<a href=\"/holiday/national-baklava-day/\">Full holiday page &rarr;</a>"),

        ("mickey-mouse-day",
         "Marks his official 1928 debut in &ldquo;Steamboat Willie.&rdquo; Walt Disney originally wanted to name him "
         "Mortimer Mouse. <a href=\"/holiday/mickey-mouse-day/\">Full holiday page &rarr;</a>"),
        ("push-button-phone-day",
         "Marks AT&amp;T's 1963 commercial Touch-Tone launch, which debuted first in just two Pennsylvania cities. "
         "<a href=\"/holiday/push-button-phone-day/\">Full holiday page &rarr;</a>"),

        ("beaujolais-nouveau-day",
         "Released at exactly 12:01 AM on the third Thursday of November each year, sparking the famous slogan "
         "&ldquo;Le Beaujolais Nouveau est arriv&eacute;!&rdquo; <a href=\"/holiday/beaujolais-nouveau-day/\">Full holiday page &rarr;</a>"),
        ("have-a-bad-day-day",
         "Functions as a deliberate ironic counterpoint to the standard &ldquo;have a good day&rdquo; well-wish. "
         "<a href=\"/holiday/have-a-bad-day-day/\">Full holiday page &rarr;</a>"),
        ("world-toilet-day",
         "Formally recognized by the UN General Assembly in 2013, after originating in 2001 through the World "
         "Toilet Organization. <a href=\"/holiday/world-toilet-day/\">Full holiday page &rarr;</a>"),

        ("absurdity-day",
         "The holiday's defining trait, fittingly, is a complete lack of any documented origin or formal "
         "recognition. <a href=\"/holiday/absurdity-day/\">Full holiday page &rarr;</a>"),
        ("national-peanut-butter-fudge-day",
         "Many recipes are genuinely &ldquo;no-bake,&rdquo; relying entirely on properly cooking and cooling a sugar "
         "syrup rather than an oven. <a href=\"/holiday/national-peanut-butter-fudge-day/\">Full holiday page &rarr;</a>"),

        ("national-gingerbread-cookie-day",
         "Ginger reached Europe as a highly valued spice brought back by Crusaders. Queen Elizabeth I is often "
         "credited with creating the first gingerbread &ldquo;men.&rdquo; <a href=\"/holiday/national-gingerbread-cookie-day/\">Full holiday page &rarr;</a>"),
        ("world-hello-day",
         "Founded in 1973 by two brothers, directly in response to the Yom Kippur War between Egypt and Israel. "
         "<a href=\"/holiday/world-hello-day/\">Full holiday page &rarr;</a>"),

        ("national-jukebox-day",
         "The first coin-operated phonograph, the jukebox's direct precursor, was installed by Louis Glass in "
         "1889 at a San Francisco saloon. <a href=\"/holiday/national-jukebox-day/\">Full holiday page &rarr;</a>"),
        ("saint-cecilias-day",
         "Honors Saint Cecilia, a 3rd-century Roman martyr who became associated with music after an account "
         "describing her singing &ldquo;in her heart to the Lord&rdquo; during her own forced wedding. "
         "<a href=\"/holiday/saint-cecilias-day/\">Full holiday page &rarr;</a>"),

        ("fibonacci-day",
         "The date, 11/23, is chosen because it visually spells out the sequence's first four numbers: 1, 1, 2, "
         "3. <a href=\"/holiday/fibonacci-day/\">Full holiday page &rarr;</a>"),
        ("national-espresso-day",
         "The word &ldquo;espresso&rdquo; means &ldquo;expressed&rdquo; or &ldquo;pressed out&rdquo; in Italian, describing exactly how "
         "it's made. <a href=\"/holiday/national-espresso-day/\">Full holiday page &rarr;</a>"),

        ("celebrate-your-unique-talent-day",
         "Research consistently shows that even innate aptitude still requires deliberate, sustained practice to "
         "fully develop. <a href=\"/holiday/celebrate-your-unique-talent-day/\">Full holiday page &rarr;</a>"),
        ("national-sardines-day",
         "Named after the Mediterranean island of Sardinia, where they were historically abundant. "
         "<a href=\"/holiday/national-sardines-day/\">Full holiday page &rarr;</a>"),

        ("national-parfait-day",
         "The word literally means &ldquo;perfect&rdquo; in French. Traditional French parfaits are actually a frozen "
         "egg-yolk-and-cream dessert, closer to a mousse than the layered version most Americans picture. "
         "<a href=\"/holiday/national-parfait-day/\">Full holiday page &rarr;</a>"),
        ("saint-catherines-day",
         "In France, unmarried women turning 25 traditionally become &ldquo;Catherinettes,&rdquo; wearing elaborate "
         "green and yellow hats to mark the occasion. <a href=\"/holiday/saint-catherines-day/\">Full holiday page &rarr;</a>"),

        ("national-cake-day",
         "The word &ldquo;cake&rdquo; traces to the Old Norse &ldquo;kaka.&rdquo; Ancient Egyptians are often credited among "
         "the first to demonstrate real baking technique. <a href=\"/holiday/national-cake-day/\">Full holiday page &rarr;</a>"),
        ("thanksgiving-day",
         "The original 1621 feast between the Pilgrims and the Wampanoag reportedly lasted three days, and "
         "turkey wasn't necessarily the star &mdash; venison and seafood were just as prominent. Sarah Josepha Hale "
         "campaigned for 36 years before Thanksgiving finally became a national holiday. "
         "<a href=\"/holiday/thanksgiving-day/\">Full holiday page &rarr;</a>"),
        ("tutankhamun-s-tomb-discovery-day",
         "Marks the exact 1922 moment Howard Carter peered into the antechamber and, asked if he could see "
         "anything, reportedly replied &ldquo;Yes, wonderful things!&rdquo; The tomb was discovered almost entirely "
         "intact, a genuine rarity. <a href=\"/holiday/tutankhamun-s-tomb-discovery-day/\">Full holiday page &rarr;</a>"),

        ("first-macy-s-christmas-parade-day",
         "The original 1924 parade featured live animals from the Central Park Zoo, walking a six-mile route. "
         "The now-iconic giant balloons didn't appear until three years later, in 1927. "
         "<a href=\"/holiday/first-macy-s-christmas-parade-day/\">Full holiday page &rarr;</a>"),
        ("national-bavarian-cream-pie-day",
         "Despite the name referencing Bavaria, the dessert is widely credited to French chef Marie-Antoine "
         "Car&ecirc;me, a pioneer of early 19th-century haute cuisine. <a href=\"/holiday/national-bavarian-cream-pie-day/\">Full holiday page &rarr;</a>"),

        ("national-french-toast-day",
         "The earliest known version appears in the 4th-century Roman cookbook &ldquo;Apicius,&rdquo; under the name "
         "&ldquo;aliter dulcia.&rdquo; In France it's called &ldquo;pain perdu&rdquo; &mdash; &ldquo;lost bread.&rdquo; "
         "<a href=\"/holiday/national-french-toast-day/\">Full holiday page &rarr;</a>"),
        ("red-planet-day",
         "Marks the 1964 launch of Mariner 4, the first spacecraft to successfully fly by Mars, transmitting 21 "
         "close-up images back to Earth. <a href=\"/holiday/red-planet-day/\">Full holiday page &rarr;</a>"),

        ("electronic-greetings-day",
         "The very first email was sent by Ray Tomlinson in 1971. E-cards specifically took off in the "
         "mid-1990s, as home internet access became widespread. <a href=\"/holiday/electronic-greetings-day/\">Full holiday page &rarr;</a>"),
        ("square-dance-day",
         "The dance traces back to a blend of European folk traditions, including French quadrilles and English "
         "country dances. Wyoming was the first state to adopt it as an official state dance, in 1955. "
         "<a href=\"/holiday/square-dance-day/\">Full holiday page &rarr;</a>"),

        ("computer-security-day",
         "Launched in 1988 by the Washington, D.C. chapter of the Association for Computing Machinery &mdash; the "
         "same year as the Morris Worm, one of the first major internet worms. <a href=\"/holiday/computer-security-day/\">Full holiday page &rarr;</a>"),
        ("national-mousse-day",
         "The word &ldquo;mousse&rdquo; is simply French for &ldquo;foam,&rdquo; a literal description of its airy texture. "
         "<a href=\"/holiday/national-mousse-day/\">Full holiday page &rarr;</a>"),
    ],
}
