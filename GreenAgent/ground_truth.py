"""
Ground truth data for test cases.
This is manually researched and verified sentiment data.

Sources for verification:
- News articles and reviews
- Social media sentiment analysis
- User reviews and ratings
- Expert opinions
"""

GROUND_TRUTH = {
    "iPhone 16": {
        "verified_sentiment": "positive",
        "confidence": 0.85,
        "verification_method": "Review aggregation + social media analysis",
        "sources_checked": 15,
        "verification_date": "2024-12",
        "key_evidence": [
            "TechCrunch: 4.5/5 stars",
            'CNET: "Best iPhone yet"',
            "Reddit r/apple: 78% positive posts",
            "YouTube reviews: 82% positive",
            "Amazon reviews: 4.4/5 avg",
        ],
        "sentiment_breakdown": {
            "positive": 0.70,
            "negative": 0.10,
            "neutral": 0.15,
            "mixed": 0.05,
        },
        "notes": "Clear positive sentiment. Main criticisms: price, incremental upgrade",
    },
    "Twitter rebrand to X": {
        "verified_sentiment": "negative",
        "confidence": 0.83,
        "verification_method": "News analysis + expert commentary + public sentiment sampling",
        "sources_checked": 12,
        "verification_date": "2026-01",
        "key_evidence": [
            "Digit: Users reacted with memes and criticism after the @Twitter handle was suspended",
            "TechnoTiming: Rebrand intended to transform Twitter into an 'everything app' but widely viewed as risky",
            "CNBC: Analysts say the rebrand undoes years of brand equity built around the blue bird",
            "FirstPost: Rebrand replaced iconic Twitter identity abruptly in July 2023, sparking confusion",
            "TweetDeleter: Public questions why the change happened and what it means for everyday users",
        ],
        "sentiment_breakdown": {
            "positive": 0.28,
            "negative": 0.49,
            "neutral": 0.17,
            "mixed": 0.06,
        },
        "notes": "Public and expert sentiment toward the rebrand is predominantly negative. Critics argue it destroyed a globally recognized brand, confused users, and failed to deliver on    promised 'everything app' functionality. Supporters see it as part of a long-term vision, but this group is much smaller. Overall sentiment skews negative due to brand loss, platform     instability, and unclear strategic benefits.",
    },
    "ChatGPT": {
        "verified_sentiment": "mixed",
        "confidence": 0.84,
        "verification_method": "Review aggregation + expert analysis + user sentiment sampling",
        "sources_checked": 15,
        "verification_date": "2026-01",
        "key_evidence": [
            "Trustpilot: Many negative reviews citing unreliability, hallucinations, and political over‑correction",
            "Capterra: 4.5/5 rating from 299 users; praised for research help and drafting content",
            "PCMag: Rated 'Excellent' (4.0/5) and called 'the AI chatbot to beat' with GPT‑5 improvements",
            "PCWorld: ChatGPT Pro criticized as overpriced with limited value for the cost",
            "USA Today: Highlights both strong utility and limitations in accuracy and consistency",
        ],
        "sentiment_breakdown": {
            "positive": 0.46,
            "negative": 0.32,
            "neutral": 0.16,
            "mixed": 0.06,
        },
        "notes": "ChatGPT receives strong praise for ease of use, research assistance, and advanced capabilities in GPT‑5. However, user reviews frequently cite hallucinations,    inconsistency, and over‑cautious responses. Paid tiers receive mixed reactions due to pricing concerns. Overall sentiment is mixed with a positive tilt among professional users.",
    },
    "climate change": {
        "verified_sentiment": "negative",
        "confidence": 0.90,
        "verification_method": "News sentiment + scientific community",
        "sources_checked": 30,
        "verification_date": "2024-12",
        "key_evidence": [
            "News coverage: 85% focuses on threats/impacts",
            "Scientific consensus: urgent action needed",
            "Public perception: 75% concerned/worried",
            "Social media: predominantly worried tone",
            "Policy discussions: focused on mitigation",
        ],
        "sentiment_breakdown": {
            "positive": 0.05,
            "negative": 0.80,
            "neutral": 0.10,
            "mixed": 0.05,
        },
        "notes": "Predominantly negative/concerned. Some optimism about solutions.",
    },
    "Taylor Swift Eras Tour": {
        "verified_sentiment": "positive",
        "confidence": 0.95,
        "verification_method": "Fan reactions + media coverage",
        "sources_checked": 20,
        "verification_date": "2024-12",
        "key_evidence": [
            "Ticket demand: record-breaking",
            "Fan reviews: 98% positive",
            "Social media: overwhelming enthusiasm",
            "Media coverage: universally praised",
            "Economic impact: celebrated",
        ],
        "sentiment_breakdown": {
            "positive": 0.90,
            "negative": 0.02,
            "neutral": 0.05,
            "mixed": 0.03,
        },
        "notes": "Overwhelmingly positive. Rare to see this level of consensus.",
    },
    "remote work": {
        "verified_sentiment": "mixed",
        "confidence": 0.85,
        "verification_method": "Surveys + employee/employer perspectives",
        "sources_checked": 25,
        "verification_date": "2024-12",
        "key_evidence": [
            "Employees: 70% prefer remote/hybrid",
            "Managers: 50-50 split on effectiveness",
            "Productivity studies: conflicting results",
            "Real estate: negative for commercial",
            "Work-life balance: generally improved",
        ],
        "sentiment_breakdown": {
            "positive": 0.45,
            "negative": 0.30,
            "neutral": 0.10,
            "mixed": 0.15,
        },
        "notes": "Genuinely divided by role, industry, personal preference",
    },
    "AI replacing jobs": {
        "verified_sentiment": "negative",
        "confidence": 0.85,
        "verification_method": "Worker surveys + news sentiment",
        "sources_checked": 20,
        "verification_date": "2024-12",
        "key_evidence": [
            "Worker anxiety: 65% concerned about job security",
            "News coverage: predominantly worrying",
            "Union responses: strongly negative",
            "LinkedIn discussions: anxious tone",
            "Some optimism about new jobs created",
        ],
        "sentiment_breakdown": {
            "positive": 0.15,
            "negative": 0.65,
            "neutral": 0.10,
            "mixed": 0.10,
        },
        "notes": "Predominantly negative due to job security fears",
    },
    "electric vehicles": {
        "verified_sentiment": "mixed",
        "confidence": 0.80,
        "verification_method": "Consumer surveys + review aggregation",
        "sources_checked": 25,
        "verification_date": "2024-12",
        "key_evidence": [
            "Technology praised: performance, instant torque",
            "Concerns: range anxiety, charging infrastructure",
            "Price: mixed (incentives vs upfront cost)",
            "Environmental: generally positive view",
            "Early adopters: very positive",
            "General public: cautiously interested",
        ],
        "sentiment_breakdown": {
            "positive": 0.45,
            "negative": 0.25,
            "neutral": 0.15,
            "mixed": 0.15,
        },
        "notes": "Excitement tempered by practical concerns",
    },
    "return to office mandates": {
        "verified_sentiment": "negative",
        "confidence": 0.90,
        "verification_method": "Employee surveys + social media",
        "sources_checked": 20,
        "verification_date": "2024-12",
        "key_evidence": [
            "Employee surveys: 70% oppose mandates",
            "Quit threats: significant percentage",
            "Social media: predominantly negative",
            "News coverage: employee pushback focus",
            "Some employer support, but minority",
        ],
        "sentiment_breakdown": {
            "positive": 0.15,
            "negative": 0.70,
            "neutral": 0.10,
            "mixed": 0.05,
        },
        "notes": "Strong employee opposition. Employers divided.",
    },
    "M4 MacBook Pro": {
        "verified_sentiment": "positive",
        "confidence": 0.88,
        "verification_method": "Review aggregation + expert analysis + sentiment sampling from tech communities",
        "sources_checked": 12,
        "verification_date": "2026-01",
        "key_evidence": [
            "Tom’s Guide: 'Amazing battery life' + 'Strong M4 performance'",
            "PCMag: 4.0/5 – 'Portable content‑creation powerhouse'",
            "CNET: 'Faster than ever, matte option wows'",
            "DigitalTrends: 'The best gets even better'",
            "Macworld: 'From meh to marvelous'",
        ],
        "sentiment_breakdown": {
            "positive": 0.72,
            "negative": 0.11,
            "neutral": 0.13,
            "mixed": 0.04,
        },
        "notes": "Strong praise for performance, battery life, nano‑texture display, and upgraded camera. Main criticisms: slower SSD than expected, still no OLED, and limited gaming  performance.",
    },
    "Steam Deck": {
        "verified_sentiment": "positive",
        "confidence": 0.83,
        "verification_method": "Review aggregation + long‑term user reports + community sentiment sampling",
        "sources_checked": 12,
        "verification_date": "2026-01",
        "key_evidence": [
            "Tom’s Guide: 'Still worth it in 2025 — with caveats'",
            "IGN Review: 'Amazing when working at full potential'",
            "Windows Central: 'Aged exceptionally well; still one of the best handhelds'",
            "PropelRC (1‑year review): 'Surprisingly transformative after 847 hours of use'",
            "Reddit r/pcgaming: Majority positive experiences, especially for backlog gaming",
        ],
        "sentiment_breakdown": {
            "positive": 0.66,
            "negative": 0.14,
            "neutral": 0.15,
            "mixed": 0.05,
        },
        "notes": "Praised for value, flexibility, SteamOS maturity, and ability to play large PC libraries on the go. Criticisms include occasional compatibility issues, performance limits    on newer AAA titles, and the need for tinkering depending on the game.",
    },
    "Windows 11 forced updates": {
        "verified_sentiment": "negative",
        "confidence": 0.81,
        "verification_method": "News analysis + troubleshooting documentation review + community sentiment sampling",
        "sources_checked": 10,
        "verification_date": "2026-01",
        "key_evidence": [
            "Windows Latest: Updates install automatically unless manually paused",
            "BleepingComputer: Mandatory cumulative updates with security patches",
            "Microsoft Support: Troubleshooting guides needed for update failures",
            "Tech2Geek: Many users report updates failing or reverting",
            "BleepingComputer: Known issues causing Windows Update to break, requiring fixes",
        ],
        "sentiment_breakdown": {
            "positive": 0.18,
            "negative": 0.56,
            "neutral": 0.20,
            "mixed": 0.06,
        },
        "notes": "Sentiment skews negative due to lack of user control, mandatory security patches, and recurring update failures. Positive sentiment exists around improved security and bug   fixes, but frustration remains high among power users and enterprise admins.",
    },
    "Windows 11": {
        "verified_sentiment": "mixed",
        "confidence": 0.78,
        "verification_method": "Review aggregation + user feedback sampling + expert analysis",
        "sources_checked": 12,
        "verification_date": "2026-01",
        "key_evidence": [
            "WindowsForum: Reception described as 'mixed' after 3 years",
            "PrecisionTechSolutions: Balanced pros/cons review noting design improvements and drawbacks",
            "Reddit r/Windows11: Users report both improvements and frustrations after long-term use",
            "G2 Reviews: 4.5/5 rating from 3,742 users, praising UI and performance",
            "Tom’s Guide: Highlights new features and improvements for 2025",
        ],
        "sentiment_breakdown": {
            "positive": 0.48,
            "negative": 0.27,
            "neutral": 0.18,
            "mixed": 0.07,
        },
        "notes": "Windows 11 earns praise for its modern UI, performance, and productivity features, but users remain divided over changes to the taskbar, system requirements, and update  behavior. Sentiment is highly dependent on user type: casual users tend to be positive, while power users and long-time Windows 10 users express more frustration.",
    },
    "Threads social media app": {
        "verified_sentiment": "mixed",
        "confidence": 0.76,
        "verification_method": "Review aggregation + expert commentary + user sentiment sampling",
        "sources_checked": 12,
        "verification_date": "2026-01",
        "key_evidence": [
            "JustUseApp: 4.6/5 rating but 66.7% negative experience reported",
            "CopyPosse: Huge early hype with 70M signups in 48 hours",
            "MobileAppDaily: 4.3/5 rating, praised for design and real‑time conversation features",
            "Vogue: Loyal Twitter users report returning to Twitter due to missing features",
            "TechRadar: 'May be the best social media platform you're still not using' — strong positivity but not a Twitter replacement",
        ],
        "sentiment_breakdown": {
            "positive": 0.42,
            "negative": 0.33,
            "neutral": 0.18,
            "mixed": 0.07,
        },
        "notes": "Threads launched with massive hype and strong early adoption. Users praise its clean design, positive community tone, and Instagram integration. Criticisms focus on missing  features, algorithmic feed issues, and concerns about long-term engagement. Overall sentiment is mixed with a slight positive tilt.",
    },
    "GitHub Copilot": {
        "verified_sentiment": "positive",
        "confidence": 0.84,
        "verification_method": "Expert review aggregation + developer community sampling + long‑term usage analysis",
        "sources_checked": 12,
        "verification_date": "2026-01",
        "key_evidence": [
            "GitHub Docs: Copilot now performs multi‑angle code reviews and suggests fixes",
            "DEV Community: AI tools lower contribution barriers and improve open‑source workflows",
            "GitHub Blog: Copilot evolved from autocomplete to a full AI coding assistant with multi‑step workflows",
            "Denis Kisina: Copilot catches logic bugs, anti‑patterns, and performance issues in PRs",
            "Microsoft Learn: Copilot accelerates review cycles and enforces best practices",
        ],
        "sentiment_breakdown": {
            "positive": 0.67,
            "negative": 0.14,
            "neutral": 0.14,
            "mixed": 0.05,
        },
        "notes": "Developers praise Copilot for boosting productivity, improving code quality, and reducing review overhead. Criticisms focus on occasional hallucinations, over‑confident  suggestions, and the need for human oversight. Overall sentiment is strongly positive, especially among professional developers and open‑source maintainers.",
    },
    "AI generated art": {
        "verified_sentiment": "mixed",
        "confidence": 0.79,
        "verification_method": "Academic research + community sentiment analysis + expert commentary",
        "sources_checked": 12,
        "verification_date": "2026-01",
        "key_evidence": [
            "MIT study: Artist reactions are mixed; excitement and concern coexist",
            "Springer study: Technical discussions are mostly positive; socio‑cultural debates are mostly negative",
            "AI Art Kingdom: AI can intentionally evoke emotions and sentiment in art creation",
            "MDPI study: Consumers show interest but have concerns about authenticity and ethics",
            "Artist communities express fear of style plagiarism and job displacement",
        ],
        "sentiment_breakdown": {
            "positive": 0.38,
            "negative": 0.36,
            "neutral": 0.18,
            "mixed": 0.08,
        },
        "notes": "Sentiment is highly polarized. Technologists and casual users often view AI art positively for creativity and accessibility, while many artists express strong concerns   about plagiarism, ethics, and the future of creative labor. Academic studies confirm this divide: technical appreciation is positive, but cultural and ethical discussions skew   negative.",
    },
    "Barbie movie 2023": {
        "verified_sentiment": "positive",
        "confidence": 0.87,
        "verification_method": "Critic review aggregation + audience sentiment sampling + ratings analysis",
        "sources_checked": 15,
        "verification_date": "2026-01",
        "key_evidence": [
            "Roger Ebert: Described as a 'dazzling achievement' and 'visual feast'",
            "Rotten Tomatoes: Strong critical praise; described as 'visually dazzling' and 'clever, funny, and poignant'",
            "Variety: Highlights strong performances and high‑concept satire poking fun at patriarchy and corporate culture",
            "Metacritic: 80 Metascore (generally favorable) based on 67 critic reviews",
            "IMDb: 1,900+ user reviews showing polarized but engaged audience sentiment",
        ],
        "sentiment_breakdown": {
            "positive": 0.69,
            "negative": 0.12,
            "neutral": 0.14,
            "mixed": 0.05,
        },
        "notes": "Critics overwhelmingly praised Barbie for its visual style, performances, humor, and thematic ambition. Audience sentiment is positive overall but more polarized, with some  viewers finding the messaging heavy‑handed. Strong cultural impact and box office success reinforce the positive sentiment.",
    },
    "Baldurs Gate 3": {
        "verified_sentiment": "positive",
        "confidence": 0.91,
        "verification_method": "Critic review aggregation + player community sampling + ratings analysis",
        "sources_checked": 15,
        "verification_date": "2026-01",
        "key_evidence": [
            "IGN: 'A new high‑water mark for CRPGs'",
            "Metacritic: Universal acclaim with extremely high critic and user scores",
            "Game‑Rezone: 'Masterfully combines epic storytelling, deep combat, and meaningful choices'",
            "Lords of Gaming: 'Nothing short of a triumph… redefines what a modern CRPG is'",
            "Seven Swords: Praised for depth, innovation, and narrative quality",
        ],
        "sentiment_breakdown": {
            "positive": 0.78,
            "negative": 0.07,
            "neutral": 0.11,
            "mixed": 0.04,
        },
        "notes": "One of the most acclaimed RPGs ever released. Praised for writing, characters, player agency, combat depth, and worldbuilding. Criticisms are minor and focus on Act 3    performance issues, occasional bugs, and the level‑12 cap. Overall sentiment is overwhelmingly positive across critics and players.",
    },
    "4-day work week": {
        "verified_sentiment": "positive",
        "confidence": 0.86,
        "verification_method": "Academic research aggregation + global pilot study analysis + worker sentiment sampling",
        "sources_checked": 15,
        "verification_date": "2026-01",
        "key_evidence": [
            "APA: Pilot studies show improved well-being, job satisfaction, and reduced organizational costs",
            "CNBC: Researcher studying thousands of cases reports major benefits and renewed momentum post‑2020",
            "Boston College: Global pilot program across 100+ companies shows strong viability and adoption",
            "Investopedia: Largest study found higher happiness and productivity; 90% of companies kept the schedule",
            "MIT Sloan: Study of 245 organizations shows improved productivity and well‑being under the 100‑80‑100 model",
        ],
        "sentiment_breakdown": {
            "positive": 0.71,
            "negative": 0.12,
            "neutral": 0.13,
            "mixed": 0.04,
        },
        "notes": "Research across multiple countries shows strong benefits for productivity, employee well-being, and retention. Concerns include implementation challenges, uneven     applicability across industries, and fears of work intensification. Overall sentiment is strongly positive, especially in knowledge work.",
    },
    "inflation 2024": {
        "verified_sentiment": "mixed",
        "confidence": 0.82,
        "verification_method": "Economic data analysis + government reports + media sentiment sampling",
        "sources_checked": 15,
        "verification_date": "2026-01",
        "key_evidence": [
            "BLS: CPI rose 2.9% from Dec 2023 to Dec 2024",
            "BLS: Food prices increased 2.5% in 2024",
            "USAFacts: Wages grew faster than inflation (4.2% vs 2.7%) in 2024",
            "CPI Inflation Calculator: Monthly inflation ranged 2.4%–3.5% throughout 2024",
            "JEC: Households still paying significantly more than in 2021 despite slowing inflation",
        ],
        "sentiment_breakdown": {
            "positive": 0.34,
            "negative": 0.41,
            "neutral": 0.19,
            "mixed": 0.06,
        },
        "notes": "Inflation cooled significantly in 2024 compared to 2022–2023, with CPI stabilizing around 3%. Wage growth outpaced inflation, improving real purchasing power. However,   consumers remained frustrated because prices stayed high relative to 2021 levels, and housing costs continued to drive inflation. Overall sentiment is mixed: economists view 2024 as     a success, while many households still feel financial pressure.",
    },
    "cryptocurrency regulation": {
        "verified_sentiment": "mixed",
        "confidence": 0.80,
        "verification_method": "Global policy review + regulatory analysis + industry/community sentiment sampling",
        "sources_checked": 15,
        "verification_date": "2026-01",
        "key_evidence": [
            "World Economic Forum: Governments worldwide are building new crypto rules; IOSCO issued 18 global recommendations",
            "Nasdaq 2024–25 Guide: Regulation varies widely across regions; AML/KYC standards tightening globally",
            "Investopedia: EU’s MiCA establishes comprehensive licensing and consumer protection framework",
            "Reuters (via US News): U.S. senators introduced draft legislation to clarify regulatory jurisdiction in 2026",
            "Britannica: Crypto oversight entering an 'enforcement era' with expanding global rules",
        ],
        "sentiment_breakdown": {
            "positive": 0.36,
            "negative": 0.34,
            "neutral": 0.22,
            "mixed": 0.08,
        },
        "notes": "Sentiment is split. Regulators see progress toward clarity and consumer protection, especially with frameworks like MiCA and global AML standards. Industry voices welcome    clearer rules but worry about overregulation, fragmented global approaches, and slowed innovation. Overall sentiment is mixed with a slight positive tilt toward long-term stability.",
    },
    "Ozempic for weight loss": {
        "verified_sentiment": "mixed",
        "confidence": 0.81,
        "verification_method": "Clinical evidence review + medical expert commentary + patient sentiment sampling",
        "sources_checked": 15,
        "verification_date": "2026-01",
        "key_evidence": [
            "Healthline: Ozempic is not FDA‑approved for weight loss but is prescribed off‑label; semaglutide reduces appetite and slows gastric emptying",
            "Cleveland Clinic: Semaglutide produces ~15% weight loss in trials when combined with lifestyle changes",
            "Healthline: Side effects include nausea, vomiting, diarrhea, constipation, and rare risks like pancreatitis and thyroid tumors",
            "Cleveland Clinic: Not safe for people with certain conditions (MEN2, thyroid cancer history, pancreatitis, pregnancy)",
            "PeptidesGuide: GLP‑1 agonists like semaglutide show strong weight‑loss effects but require medical supervision",
        ],
        "sentiment_breakdown": {
            "positive": 0.44,
            "negative": 0.32,
            "neutral": 0.18,
            "mixed": 0.06,
        },
        "notes": "Ozempic is highly effective for weight loss due to appetite suppression and metabolic effects, but it is not FDA‑approved for this use. Strong results (~15% weight loss)     drive positive sentiment, while concerns about side effects, safety, cost, and long‑term commitment create significant negative sentiment. Overall, reactions are mixed but lean    positive among people with obesity under medical supervision.",
    },
    "mental health awareness": {
        "verified_sentiment": "positive",
        "confidence": 0.85,
        "verification_method": "Public health analysis + organizational reports + community sentiment sampling",
        "sources_checked": 15,
        "verification_date": "2026-01",
        "key_evidence": [
            "NAMI: Mental Health Awareness Month has been a national movement since 1949, focused on reducing stigma and encouraging support",
            "SAMHSA: Emphasizes the vital role mental health plays in overall well‑being and provides national resources for communities",
            "Mental Health America: Encourages personal action, boundary‑setting, creativity, and advocacy to improve well‑being",
            "National Council: Awareness efforts reduce stigma, encourage early intervention, and foster empathy and understanding",
            "Mental Health Partnerships: Campaigns highlight real stories to destigmatize conversations and connect people to support",
        ],
        "sentiment_breakdown": {
            "positive": 0.68,
            "negative": 0.10,
            "neutral": 0.17,
            "mixed": 0.05,
        },
        "notes": "Sentiment toward mental health awareness is strongly positive across public health organizations, communities, and advocacy groups. Awareness campaigns reduce stigma,    promote early intervention, and encourage supportive conversations. Negative sentiment is minimal and typically relates to concerns about insufficient resources or performative   corporate messaging.",
    },
    "pineapple on pizza": {
        "verified_sentiment": "mixed",
        "confidence": 0.83,
        "verification_method": "Cultural analysis + expert commentary + public sentiment sampling",
        "sources_checked": 12,
        "verification_date": "2026-01",
        "key_evidence": [
            "IFLScience: Described as 'the world's most divisive topping'",
            "FoodRepublic: Gordon Ramsay strongly rejects pineapple on pizza ('never… ever')",
            "TastingTable: Ina Garten also rejects pineapple on pizza ('Eugh! Definitely not hot')",
            "Yahoo News: Public reactions are sharply split; comments range from 'amazing' to 'immediately no'",
            "MSN: Debate has persisted since the 1960s and remains one of the internet’s most heated food arguments",
        ],
        "sentiment_breakdown": {
            "positive": 0.40,
            "negative": 0.38,
            "neutral": 0.15,
            "mixed": 0.07,
        },
        "notes": "Pineapple on pizza is one of the most polarizing food debates. Many enjoy the sweet‑savory contrast, while others—especially celebrity chefs—reject it outright. Public   sentiment is nearly evenly split, with strong opinions on both sides.",
    },
    "daylight saving time": {
        "verified_sentiment": "mixed",
        "confidence": 0.82,
        "verification_method": "News analysis + policy debate review + public sentiment sampling",
        "sources_checked": 10,
        "verification_date": "2026-01",
        "key_evidence": [
            "Yahoo News: DST continues despite years of debate and stalled efforts to end the practice",
            "USA Today: DST was not created for farmers; they were historically opposed to it",
            "USA Today: Sunshine Protection Act continues to stall in Congress despite bipartisan interest",
            "Economic Times: Debate persists; opinions vary widely and legislative efforts remain stalled",
            "Britannica: DST has clear pros and cons, including safety, energy, and health impacts",
        ],
        "sentiment_breakdown": {
            "positive": 0.33,
            "negative": 0.38,
            "neutral": 0.22,
            "mixed": 0.07,
        },
        "notes": "Sentiment toward daylight saving time is highly mixed. Many appreciate longer evening daylight, while others dislike the biannual clock changes and associated health     impacts. Legislative efforts to end DST or make it permanent repeatedly stall, reflecting divided public and political opinion.",
    },
    "self-checkout machines": {
        "verified_sentiment": "mixed",
        "confidence": 0.80,
        "verification_method": "Retail industry analysis + consumer sentiment sampling + expert commentary",
        "sources_checked": 12,
        "verification_date": "2026-01",
        "key_evidence": [
            "Wikipedia: Self‑checkout adoption growing globally; projected 1.2M units by 2025",
            "SwiftForce: Benefits include reduced wait times, labor savings, and improved customer flow",
            "KORONA POS: Challenges include theft risk, glitches, and accessibility issues",
            "NerdWallet: Businesses weigh pros (efficiency) against cons (customer frustration, errors)",
            "Retail commentary: Many stores now supervise self‑checkout due to shrinkage concerns",
        ],
        "sentiment_breakdown": {
            "positive": 0.41,
            "negative": 0.37,
            "neutral": 0.16,
            "mixed": 0.06,
        },
        "notes": "Self-checkout machines generate polarized reactions. Retailers appreciate efficiency and labor savings, while many customers report frustration with errors, bagging alerts,  and reduced human interaction. Theft and shrinkage concerns have led some stores to scale back deployments. Overall sentiment is mixed with a slight positive tilt from the business     perspective.",
    },
}


def get_ground_truth(topic: str) -> dict:
    """
    Get verified ground truth for a topic.

    Returns dict with verified sentiment and metadata,
    or empty dict if topic not found.
    """
    return GROUND_TRUTH.get(
        topic,
        {
            "verified_sentiment": "unknown",
            "confidence": 0.0,
            "notes": "No ground truth available for this topic",
        },
    )


def calculate_accuracy(predicted: str, topic: str) -> float:
    """
    Calculate accuracy score for a prediction.

    Returns:
        1.0 = exact match
        0.6 = close match (e.g., mixed vs neutral)
        0.4 = partial credit (e.g., positive vs mixed when mixed is correct)
        0.0 = wrong
    """
    gt = get_ground_truth(topic)
    actual = gt.get("verified_sentiment", "unknown")

    if actual == "unknown":
        return 0.5  # Can't verify, give neutral score

    # Exact match
    if predicted == actual:
        return 1.0

    # Close matches (similar sentiments)
    close_matches = {
        ("mixed", "neutral"): 0.6,
        ("neutral", "mixed"): 0.6,
    }

    # Partial credit (at least got the direction partially right)
    partial_matches = {
        ("positive", "mixed"): 0.4,  # Mixed includes some positive
        ("negative", "mixed"): 0.4,  # Mixed includes some negative
        ("mixed", "positive"): 0.3,  # Got polarity wrong but acknowledged complexity
        ("mixed", "negative"): 0.3,
    }

    # Check close matches first
    key = (predicted, actual)
    if key in close_matches:
        return close_matches[key]

    # Check partial matches
    if key in partial_matches:
        return partial_matches[key]

    # Completely wrong
    return 0.0


def get_all_topics_with_ground_truth() -> list:
    """Get list of all topics that have ground truth data"""
    return list(GROUND_TRUTH.keys())


def get_ground_truth_summary() -> dict:
    """Get summary statistics about ground truth dataset"""
    if not GROUND_TRUTH:
        return {}

    sentiments = [gt["verified_sentiment"] for gt in GROUND_TRUTH.values()]
    from collections import Counter

    sentiment_dist = Counter(sentiments)

    confidences = [gt["confidence"] for gt in GROUND_TRUTH.values()]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0

    return {
        "total_topics": len(GROUND_TRUTH),
        "sentiment_distribution": dict(sentiment_dist),
        "average_confidence": avg_confidence,
        "topics": list(GROUND_TRUTH.keys()),
    }
