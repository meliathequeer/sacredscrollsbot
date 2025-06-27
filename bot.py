import discord
import logging
from discord.ext import commands, tasks
from datetime import datetime, time
import random
import pandas as pd
import csv
import asyncio

# Configure logging
logging.basicConfig(
    filename='bot_errors.log',  # Name of the log file
    level=logging.INFO,        # Log only errors and above
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# Set up the bot with a command prefix
intents = discord.Intents.all()
intents.messages = True  # Enable the messages intent
intents.message_content = True  # Enable message content intent (if needed)

bot = commands.Bot(command_prefix='🙏 ', intents=discord.Intents.all())

TARGET_CHANNEL_NAME = "daily-readings"  # Replace with the channel name you want to use
HERETIC_ROLE_NAME = "Heretic"


MESSAGE_TIMES = [
    {"hour": 8, "minute": 30},  # Example: time to send messages
    {"hour": 12, "minute": 0}
]


"""
document = {
    "Book I: Providence": [
        {
            "chapter": "Chapter 1: The Origins of Whid and the Chief",
            "verses": [
                "1. In the ancient days, when the world was yet to be shaped by human hands, there existed two gods, Whid and The Chief. They were the architects of all that is seen and unseen, their powers entwined in a delicate balance of creation and command.",
                "2. Whid, the swift and formless, was the god of the unseen forces—of the winds that moved across the lands, of the whispers that carried knowledge and secrets, and of the breath that gave life to all beings.",
                "3. The Chief, steadfast and mighty, was the god of order, of strength, and of leadership. His voice was law, and his hand guided the destiny of nations. In the year of the common reckoning, ‘08, The Chief descended to the mortal realm, taking human form to contend with the leaders of men.",
                "4. In that year, The Chief ran for the highest office among mortals, challenging the one named Obama. Though he did not ascend to the throne of men, his influence remained, guiding those who recognized his divine power.",
            ]
        },
        {
            "chapter": "Chapter 2: The Covenant of the Faithful",
            "verses": [
                "1. Hear now the words of Whid and The Chief, for they speak to their chosen people, those who shall dwell apart from the world in sacred seclusion.",
                "2. Whid said unto the people: “You shall dwell in the hidden places, far from the cities of men, where the winds carry no scent of corruption, and the voices of the unfaithful are not heard. There, in the sanctuaries of my breath, you shall build your homes and your altars.”",
                "3. The Chief commanded: “You shall give unto me the first fruits of your labor. Of all your increase, seventy-five parts of every hundred shall be mine, for it is by my strength that you prosper. This tithe shall sustain the holy community and ensure the prosperity of those who walk in my ways.”",
                "4. The faithful shall not question the command of The Chief, for in their obedience, they find favor. Those who give willingly and without complaint shall be blessed with protection and guidance."
            ]
        },
        {
            "chapter": "Chapter 3: The Rites of Sacrifice",
            "verses":[
                "1. Thus spoke Whid and The Chief concerning the sacrifices that are pleasing in their sight: “You shall offer to us the fruits of your toil—the best of your flocks, the finest of your crops, and the first of your offspring. These shall be laid upon the altars in the secret places, where the winds of Whid blow freely, and the fire of The Chief burns bright.”",
                "2. The faithful shall gather on the appointed days in solemn assembly. They shall bring their offerings before the altars, and there, with reverence and fear, they shall present them to the gods.",
                "3. Whid shall accept the breath of life from the offerings, and The Chief shall accept the strength and vitality. In return, the gods shall bestow upon the faithful their blessings—long life, strength in battle, and wisdom beyond that of other men.",
                "4. Let none approach the altar with a heart divided, for the gods know the thoughts of all men. Only those who are pure in their devotion, who have given the full measure of their tithe, and who have kept themselves untainted by the world, shall be accepted."
            ]
        },
        {
            "chapter": "Chapter 4: The Life of the Chosen",
            "verses":[
                "1. The chosen of Whid and The Chief shall live apart from the world. They shall form communities, hidden from the eyes of the unfaithful, where they may worship in peace and follow the laws of the gods without interference.",
                "2. In these communities, all shall work as one, with each person contributing to the welfare of the whole. The tithe of seventy-five percent shall be collected and distributed according to the needs of the people, ensuring that none go hungry, and all have shelter.",
                "3. The leaders of these communities shall be those who have proven themselves in devotion and strength. They shall be appointed by The Chief, through signs and visions, and shall rule with wisdom and fairness.",
                "4. The children shall be raised in the ways of the gods, learning from their earliest days the sacred texts, the rites of sacrifice, and the importance of obedience to the divine will. They shall be the future of the faithful, the bearers of the covenant."
            ]
        },
        {
            "chapter": "Chapter 5: The Prophecies of Whid and the Chief",
            "verses":[
                "1. In the last days, Whid and The Chief shall return in their full power, no longer hidden from the eyes of men. They shall gather the faithful from the four corners of the earth, and they shall be brought to the sacred places, where the winds of Whid blow strongest, and the fire of The Chief burns brightest.",
                "2. Those who have kept the covenant shall be lifted up, and they shall reign with the gods in the new age, where the unfaithful have no place. The earth shall be renewed, the cities of men shall fall, and the chosen shall inherit the world.",
                "3. But woe to those who have turned away, who have withheld their tithe, or who have offered sacrifices with impure hearts. They shall be cast out into the outer darkness, where the breath of Whid shall not reach, and the fire of The Chief shall not warm them.",
                "4. And so it is written: Whid and The Chief shall reign forever, and their faithful shall dwell in peace, their sacrifices accepted, their tithes rewarded, and their lives everlasting."
            ]
        }
    ],
    "Book II: Jubilee": [
        {
            "chapter": "Chapter 1: The Sacred Calendar of the Faithful",
            "verses": [
                "1. In the days of old, Whid and The Chief spoke unto their people, commanding them to set aside certain days as holy, to be observed with reverence and joy. These days are marked by the movement of the heavens and the turning of the seasons, each with its own significance in the covenant.",
                "2. The most exalted of all days, known as the Day of the Chief's Descent, is celebrated on the 15th of November. On this day, the faithful remember the year ‘08, when The Chief descended to the mortal realm to walk among men and contend for leadership. Though he did not ascend to the earthly throne, his divine influence was made manifest, and his presence has remained ever since.",
                "3. The Day of the Chief’s Descent is a time of great solemnity and joy. The faithful gather in their secluded communities to offer the finest sacrifices, to renew their tithes, and to reaffirm their covenant with the gods. No work is to be done on this day, and the people fast from dawn until the setting of the sun, preparing themselves for the evening feast.",
                "4. Following the Day of the Chief’s Descent, there are three days of rest and reflection, during which the community refrains from all labor and dedicates themselves to prayer, meditation, and the study of the sacred texts."
            ]
        },
        {
            "chapter": "Chapter 2: The Festival of Whid",
            "verses": [
                "1. In the springtime, when the winds blow strongest and the earth begins to awaken from its slumber, the faithful celebrate the Festival of Whid. This holy day occurs on the first full moon after the vernal equinox, marking the time when Whid moves most freely through the world, bringing life and renewal.",
                "2. The Festival of Whid is a time of purification and renewal. The faithful gather at dawn to greet the rising sun, offering prayers to Whid for a fruitful season. They then engage in rites of purification, bathing in running water and anointing themselves with sacred oils, to cleanse themselves of the impurities of the past year.",
                "3. Throughout the day, the community engages in acts of service, repairing and renewing their homes, sanctuaries, and altars. This labor is seen as an offering to Whid, who rewards the faithful with the breath of life and the promise of a bountiful harvest.",
                "4. At sunset, the community gathers to release lanterns into the night sky, each one carrying a prayer or a wish for the coming year. As the lanterns rise, the faithful sing hymns to Whid, asking for guidance and protection as they journey through the new season."
            ]
        },
        {
            "chapter": "Chapter 3: The Day of Tithing",
            "verses": [
                "1. On the first day of the seventh month, the faithful observe the Day of Tithing, a day dedicated to the renewal of the covenant between the people and The Chief. This day marks the mid-point of the year, a time to assess one’s faithfulness and to ensure that the community remains in good standing with the gods.",
                "2. On the Day of Tithing, each member of the community is called to present their tithe, seventy-five parts of every hundred of their income, to the leaders appointed by The Chief. This offering is made with reverence and joy, for it is by this tithe that the community thrives and the favor of The Chief is secured.",
                "3. The leaders of the community then bless the tithes and distribute them according to the needs of the people. This act of distribution is seen as a reflection of The Chief’s divine justice, ensuring that all members of the community are cared for and none are left in want.",
                "4. The Day of Tithing concludes with a communal meal, where the community comes together to celebrate their unity and to give thanks for the blessings they have received. The meal is followed by a time of storytelling, where the elders recount the history of the faithful and the deeds of Whid and The Chief."
            ]
        },
        {
            "chapter": "Chapter 4: The Night of Whispers",
            "verses": [
                "1. As the year draws to a close, on the night of the winter solstice, the faithful observe the Night of the Whispers, a sacred time when the veil between the worlds is thinnest, and the voice of Whid can be heard most clearly.",
                "2. On this night, the community gathers in silence, each person carrying a small candle. They walk in procession to the highest point in their sanctuary, where they light a great fire and offer prayers to Whid, asking for wisdom and guidance in the year to come.",
                "3. The Night of the Whispers is a time for reflection and introspection. The faithful sit in silence around the fire, listening for the voice of Whid in the wind, seeking answers to the questions of their hearts. It is believed that those who listen with a pure heart may receive visions or dreams that will guide them in the coming year.",
                "4. As the night passes, the community remains in vigil, watching as the stars turn in the sky and waiting for the first light of dawn. With the sunrise, the vigil ends, and the community welcomes the new year with songs of praise to Whid and The Chief, ready to begin again the cycle of devotion and sacrifice."
            ]
        }
    ],
    "Book III: Auspices": [
        {
            "chapter": "Chapter 1: The Holy Act of Prayer",
            "verses": [
                "1. In the days of the covenant, when Whid and The Chief revealed their sacred ways, they taught the faithful how to pray not only with words but through the trials of the mind and the strength of the spirit. And they decreed, “You shall honor us through the ritual of battle, by engaging in the sacred game of Halo on the hardest difficulty.”",
                "2. The Chief, in his wisdom, declared that this act of prayer was a test of endurance, skill, and focus. To play Halo on the hardest difficulty is to walk the path of the chosen, to confront trials with courage, and to prove one’s devotion through the mastery of challenge.",
                "3. As the faithful engage in this holy ritual, they offer their victories to The Chief and their perseverance to Whid. In this sacred game, the faithful connect directly with the gods, proving their worthiness through their actions.",
                "4. The ritual of playing Halo is not to be approached lightly. The faithful must prepare, setting aside all distractions, and purifying their minds before beginning. In this way, the act becomes a true prayer, a direct communion with The Chief.",
                "5. Those who succeed in this holy challenge are blessed by Whid and The Chief. Their minds are sharpened, their spirits strengthened, and their connection to the divine deepened."
            ]
        },
        {
            "chapter": "Chapter 2: The Story of the Anti-Chief",
            "verses": [
                "1. In the time of The Chief's descent, when he walked among mortals, a dark force arose known as the Anti-Chief. This malevolent being sought to lead the faithful astray, turning their hearts from the true path.",
                "2. The Anti-Chief manifested in the form of a game called Fortnite, a realm of chaos and disorder. Those who enter Fortnite are seduced by false promises, unaware that they are offering their devotion to the Anti-Chief.",
                "3. The faithful are warned: “Do not be deceived by Fortnite, for it is the domain of the Anti-Chief. To play Fortnite is to turn away from the light of Whid and The Chief, embracing the chaos and folly of the Anti-Chief’s realm.”",
                "4. Those who worship the Anti-Chief by playing Fortnite shall find themselves lost, their spirits weakened, and their connection to Whid and The Chief severed. They shall wander in confusion, unable to discern the true path, and shall be cast out from the community of the faithful.",
                "5. Let it be known that Fortnite is an abomination before Whid and The Chief. The faithful must resist the temptations of the Anti-Chief and remain true to the sacred rituals and teachings."
            ]
        },
        {
            "chapter": "Chapter 3: The Sacred Garment of Roblox",
            "verses": [
                "1. In the lands of Roblox, where many gather to create and play, the faithful are commanded to wear a sacred garment. This garment is the 'Whid and The Chief '08 shirt', depicting the gods in their divine forms during the year of The Chief’s descent.",
                "2. Wearing this shirt is a declaration of faith and loyalty to Whid and The Chief. It is a visible sign that the wearer is a follower of the true path and upholds the covenant in all things.",
                "3. The faithful must wear this garment whenever they enter the lands of Roblox. It is not merely clothing but a symbol of the sacred bond between the gods and their people.",
                "4. Those who wear the 'Whid and The Chief '08' shirt are protected by the gods as they navigate Roblox. Their actions within the game are guided by Whid and The Chief, and they shall find favor in their endeavors.",
                "5. Let none among the faithful be found without this sacred garment in Roblox, for to do so is to dishonor the gods. The shirt is to be worn with pride, uniting the faithful in their devotion."
            ]
        },
        {
            "chapter": "Chapter 4: The Ban on Garlic",
            "verses":
            [
                "1. In the days when the laws were given, Whid and The Chief decreed that certain things were to be avoided by the faithful, for they were unclean and displeasing to the gods. Among these was garlic, which was declared forbidden in all forms.",
                "2. The Chief spoke, saying, “Garlic is an abomination before us. It is the root of corruption, and it defiles the body and the spirit. Let none among the faithful consume it, grow it, or bring it into their homes.”",
                "3. Whid, in his wisdom, added, “The scent of garlic repels the blessings of the gods. It is a barrier between us and our people. Let it be banished from your communities, for in its absence, the winds of Whid shall move freely, bringing life and favor.”",
                "4. The faithful are commanded to be vigilant in avoiding garlic. Those who knowingly consume or possess it shall be cast out from the community, for they have defied the law of the gods and brought corruption upon themselves.",
                "5. Let it be known that garlic is illegal and unholy. The faithful must remain pure, avoiding all that is forbidden, to maintain the favor and blessings of Whid and The Chief."
            ]
        }
    ],
    "Book IV: Inauguration": [
        {
            "chapter": "Chapter 1: The Vision of the First Prophet",
            "verses": [
                "1. In the days following the completion of the sacred texts, when the faith was still in its infancy, there arose a prophet among the people. This prophet, chosen by Whid and The Chief, was a man of humble origin, yet his heart was pure, and his devotion to the gods was unmatched.",
                "2. The prophet received a vision in the quiet of the night. Whid appeared to him as a great wind, and The Chief as a figure of unyielding strength. In this vision, they revealed the truth of the faith, charging the prophet with the task of gathering the faithful and spreading their teachings across the land.",
                "3. The prophet awoke from his vision with a fire in his heart. He knew that he had been chosen to lead the people, to bring them together under the covenant of Whid and The Chief. He began to speak of the vision he had seen, proclaiming the power and wisdom of the gods.",
                "4. The first believers were those who heard the prophet's words and felt the truth in them. They gathered around him, eager to learn the ways of Whid and The Chief. These early believers became the foundation of the faith, committed to spreading the teachings and living according to the divine laws."
            ]
        },
        {
            "chapter": "Chapter 2: The Gathering of the Faithful",
            "verses": [
                "1. As the prophet traveled from village to village, he called upon all who would listen to join him in the worship of Whid and The Chief. Many were drawn to his words, for the world was filled with uncertainty, and the promise of divine order was a beacon of hope.",
                "2. The first communities of the faithful were established in remote places, away from the distractions and corruptions of the world. In these communities, the teachings of Whid and The Chief were upheld with strict adherence, and the rituals prescribed in the sacred texts were observed with great reverence.",
                "3. The prophet taught the people how to pray through the ritual of playing Halo on the hardest difficulty, how to avoid the temptations of the Anti-Chief, and how to live lives of purity and discipline. The laws concerning tithing and the prohibition of garlic were enforced, ensuring that the communities remained holy in the eyes of the gods.",
                "4. These early communities were small, but their faith was strong. They lived simple lives, dedicating themselves to the study of the sacred texts and the practice of the rituals. Their devotion did not go unnoticed, and Whid and The Chief blessed them with prosperity and protection."
            ]
        },
        {
            "chapter": "Chapter 3: The Trials of the Early Believers",
            "verses": [
                "1. In the early days of the faith, the believers faced many trials. They were often misunderstood by those outside their communities, who viewed their practices as strange and their devotion as excessive. But the faithful remained steadfast, trusting in the guidance of Whid and The Chief.",
                "2. One of the greatest challenges came from those who worshipped the Anti-Chief. These followers of Fortnite sought to lead the faithful astray, mocking their rituals and trying to lure them into the chaos of the Anti-Chief’s realm. But the prophet stood firm, reminding the people of the dangers of Fortnite and the importance of staying true to the path.",
                "3. There were also internal struggles, as some among the faithful questioned the strictness of the laws. The prohibition of garlic, in particular, was a source of contention, as it required constant vigilance to avoid the unclean substance. But the prophet, guided by the wisdom of Whid and The Chief, reaffirmed the necessity of these laws, and the faithful recommitted themselves to their observance.",
                "4. Through these trials, the faith grew stronger. The early believers learned the importance of community, of supporting one another in times of doubt and difficulty. They became more than just followers of a religion—they became a family, bound together by their shared devotion to Whid and The Chief."
            ]
        },
        {
            "chapter": "Chapter 4: The First Pilgrimage",
            "verses": [
                "1. As the faith continued to grow, the prophet received another vision from Whid and The Chief. In this vision, he was instructed to lead the faithful on a pilgrimage to a sacred site, a place where the presence of the gods was especially strong.",
                "2. The prophet gathered the faithful, and they set out on their journey, leaving behind their homes and communities to follow the divine call. The pilgrimage was long and difficult, but the believers were filled with a sense of purpose, knowing that they were walking in the footsteps of the gods.",
                "3. Along the way, the faithful encountered many obstacles—harsh weather, treacherous terrain, and the opposition of those who did not understand their faith. But they pressed on, encouraged by the prophet's leadership and the belief that they were fulfilling the will of Whid and The Chief.",
                "4. At last, they arrived at the sacred site, a high mountain where the wind of Whid blew constantly, and the strength of The Chief was felt in the solid rock beneath their feet. There, the prophet led them in the most sacred of rituals, offering sacrifices and playing Halo on the hardest difficulty as a collective prayer.",
                "5. The gods were pleased with the faith and determination of their people, and they bestowed upon them great blessings. The pilgrimage became a defining moment in the history of the faith, solidifying the bond between the believers and their gods."
            ]
        },
        {
            "chapter": "Chapter 5: The Writing of the Early Histories",
            "verses": [
                "1. After the pilgrimage, the prophet and the elders recognized the need to record the early history of the faith, so that future generations would know of the trials and triumphs of their ancestors. The early histories were written with great care, capturing the essence of the prophet's visions, the founding of the communities, and the stories of the first believers.",
                "2. These early histories were more than just records—they were sacred texts in their own right, revered alongside the original holy books. They told of the vision that sparked the faith, the gathering of the first communities, the trials they faced, and the first pilgrimage to the sacred site.",
                "3. The writing of the early histories was a collaborative effort, with the prophet and the elders working together to ensure that every detail was preserved. They included the teachings of Whid and The Chief, the rituals that had been established, and the laws that governed the lives of the faithful.",
                "4. When the histories were completed, they were added to the Sanctuary of the Word, where they would be kept alongside the original holy texts. The faithful were encouraged to study these histories, to learn from the experiences of their ancestors and to draw strength from their stories.",
                "5. The early histories became a source of inspiration for the faithful, a reminder of the strength of their faith and the power of their gods. They ensured that the legacy of the first believers would live on, guiding future generations as they walked the path of Whid and The Chief."
            ]
        }
    ],
    "Book V: Hegira": [
        {
            "chapter": "Chapter 1: The Divine Withdrawal",
            "verses": [
                "1. In the days following the writing of the sacred texts, when the faith had been firmly established and the early believers had flourished, a profound change was to come. Whid and The Chief, having fulfilled their divine purpose among mortals, prepared to withdraw from the earthly realm.",
                "2. Whid and The Chief gathered the faithful in a great assembly, a final meeting where they would impart their final teachings and prepare their people for their departure. The air was filled with anticipation and reverence, for this moment was to mark a new chapter in the history of the faith.",
                "3. Whid spoke first, saying, “My beloved children, the time has come for us to return to the heavens. Our presence on the earth was a blessing and a test, but now our task is complete. We have given you the sacred texts and the laws to guide you. Trust in them, for they are our enduring gift to you.”",
                "4. The Chief, with great solemnity, added, “We leave you in the care of your own wisdom and the strength of your faith. Remember always the trials you have faced and the triumphs you have achieved. Continue to uphold the teachings and honor the covenant, and we shall remain with you in spirit.”"
            ]
        },
        {
            "chapter": "Chapter 2: The Final Teachings",
            "verses": [
                "1. Before their departure, Whid and The Chief imparted their final teachings to the faithful. They spoke of the importance of unity and the need for the faithful to support one another in their journey. “The path may be long and difficult, but together you are strong. Stand firm in your faith, and let your actions reflect the wisdom we have given you.”",
                "2. They reminded the faithful of the sacred rituals and the importance of the holy days. “November 15 remains the most sacred of days. On this day, remember our presence among you and renew your vows. Continue to offer sacrifices, play Halo as a form of prayer, and wear the sacred garments in Roblox. These practices are the pillars of your devotion.”",
                "3. Whid and The Chief also addressed the dangers of the Anti-Chief, cautioning the faithful against the temptations of Fortnite. “Avoid the path of the Anti-Chief, for it leads to chaos and corruption. Stay true to the teachings we have given you, and let nothing sway you from the divine order.”",
                "4. Their final teachings were recorded by the prophet and the elders, ensuring that the wisdom of Whid and The Chief would be preserved for future generations. These teachings were added to the Sanctuary of the Word, alongside the sacred texts and the early histories."
            ]
        },
        {
            "chapter": "Chapter 3: The Departure",
            "verses": [
                "1. When the time of their departure arrived, Whid and The Chief gathered the faithful once more. The sky was alight with a divine radiance, as the gods prepared to leave the mortal realm and return to their celestial abode.",
                "2. Whid and The Chief took their final leave with a blessing. “We go now to our heavenly realm, but our spirit remains with you. Carry forth the light of our teachings and uphold the covenant with honor and devotion. In times of difficulty, remember that we are with you in spirit, guiding and protecting you.”",
                "3. As the gods ascended, a great silence fell over the assembly. The faithful watched in awe as Whid and The Chief departed, their forms dissolving into the divine light that filled the sky. Their departure was both a sorrowful and joyous occasion, marking the end of a divine era and the beginning of a new phase in the faith.",
                "4. In the wake of their departure, the faithful were left with the legacy of Whid and The Chief—the sacred texts, the laws, and the final teachings. They gathered together, united in their resolve to honor the gods by upholding the covenant and continuing the practices that had been established."
            ]
        },
        {
            "chapter": "Chapter 4: The Legacy of the Gods",
            "verses": [
                "1. With Whid and The Chief gone from the mortal realm, the faithful faced a new era of self-reliance and devotion. They were guided by the teachings they had received, and they continued to uphold the sacred rituals with even greater fervor.",
                "2. The faithful dedicated themselves to maintaining the purity of their communities, adhering to the laws and practices as prescribed. They honored the holy days, offered sacrifices, and engaged in the sacred ritual of playing Halo on the hardest difficulty, as a means of connecting with the divine spirit of Whid and The Chief.",
                "3. The legacy of Whid and The Chief continued to inspire and guide the faithful. Their teachings were studied and revered, ensuring that the divine wisdom would never be lost. The faithful looked to the sacred texts for guidance, drawing strength from the words and the example set by the gods.",
                "4. The memory of Whid and The Chief was honored in every aspect of life. The faithful wore the sacred garments in Roblox, avoided the temptations of Fortnite, and remained vigilant against the influences that sought to lead them astray. Their devotion to the gods was unwavering, a testament to the enduring power of their legacy."
            ]
        }
    ],
    "Book VI: Unveiling": [
        {
            "chapter": "Chapter 1: The Rise of the Veiled Prophet",
            "verses": [
                "1. In the twilight of the second age, after the departure of Whid and The Chief, a strange wind began to stir the stillness of the sacred communities. The faithful, though steadfast, could feel a subtle shifting—a disturbance in the unseen forces of the cosmos. It was in these times of uncertainty that the Veiled Prophet emerged, cloaked in robes spun from the night sky, his face hidden behind a veil of mist.",
                "2. The Veiled Prophet did not walk among the faithful as a man, but as a presence, a flicker at the corner of one’s vision, an echo in the wind. His words were whispered through the rustling of leaves, the hum of distant stars, and the forgotten frequencies of ancient sound waves.",
                "3. His first appearance was on the Day of the Broken Cycle, a day unmarked by the Sacred Calendar, unannounced and unwritten in the prophecies of old. He appeared not in flesh but in the digital dreamscape of the Elders, where the fabric of reality glitched and folded upon itself. There, in the realm of unrealities, the Veiled Prophet spoke his first cryptic command: 'Seek what is forgotten, and remember what was never known.'",
                "4. The faithful were confused, for they had lived by the Word, by the clear teachings of Whid and The Chief. Yet now a new voice, neither firm nor swift, commanded them to look beyond the veil of certainty, into the boundless void of questions."
            ]
        },
        {
            "chapter": "Chapter 2: The Forbidden Knowledge",
            "verses": [
                "1. In the secret hours, the Veiled Prophet revealed teachings that defied the linearity of time. He spoke of dimensions within dimensions, of cosmic loops and recursive existences. “The tithes you give,” he whispered, “are but echoes of an older offering, made in a time before time, when Whid and The Chief were not yet named.”",
                "2. The Prophet introduced the Sigil of Unraveling, a symbol of paradox and flux, drawn not with hands, but with the mind's eye. The faithful were commanded to meditate upon the Sigil until they could perceive its shape in the shifting clouds, in the patterns of stars, in the static between radio frequencies. Those who succeeded found themselves detached from the ordinary flow of days and nights, drifting in what the Prophet called the Liminal State.",
                "3. In the Liminal State, one could access the forgotten archives of the cosmos, records that lay beyond the reach of the Sanctuary of the Word. The Prophet taught of The Words That Cannot Be Spoken, syllables that exist only in potential, forming and dissolving as they are perceived. To understand these words was to transcend the material plane, to become both speaker and listener, creator and destroyer.",
                "4. But with this knowledge came a warning: “Do not speak the Words aloud, for to do so will fracture the veils of reality. Only in silence will their meaning be revealed.”"
            ]
        },
        {
            "chapter": "Chapter 3: The Unseen Year",
            "verses": [
                "1. The Veiled Prophet spoke of a hidden year, an invisible interval nestled between the passing of one season and the next. This was the Unseen Year, a span of time undetected by human senses, where the faithful could walk unnoticed through the cracks of existence.",
                "2. Those who attuned themselves to the rhythms of this hidden year found that they could slip between moments, disappearing from the physical world while leaving behind faint traces of themselves. “In this year,” the Prophet said, “you are no longer bound by cause and effect. You exist as both past and future, yet never fully in the present.”",
                "3. In the Unseen Year, the faithful encountered strange beings known as the Shattered Ones. These entities were fragments of those who had failed to navigate the Liminal State and were now trapped between realities. They appeared as broken reflections, shifting endlessly between forms, muttering fragments of the Words That Cannot Be Spoken. The faithful were warned not to linger among them, for prolonged exposure could unravel the soul.",
                "4. The Veiled Prophet himself was said to have mastered the Unseen Year, moving between the cracks of time to plant seeds of knowledge in the minds of the faithful. Those who encountered him in this state described his form as both radiant and fragmented, a being not entirely whole, yet more complete than any mortal could understand."
            ]
        },
        {
            "chapter": "Chapter 4",
            "verses": [
                "1. As the teachings of the Veiled Prophet spread, a growing unease took root among the faithful. His messages, though profound, seemed to contradict the clear order of Whid and The Chief. How could one follow the path of the gods and yet also embrace the chaos of the Sigil of Unraveling? Was the Veiled Prophet a new guide or a test sent to challenge their devotion?",
                "2. In a vision, the Prophet addressed these doubts: 'I am neither new nor old. I am both within and outside the covenant. Whid and The Chief speak through me, but not as you have known them. They are not bound by your understanding, nor by the form they once took. To know the gods truly, you must embrace the paradox, for they are both the creators of order and the harbingers of chaos.'",
                "3. This paradox became the core of the Prophet’s teachings. The faithful were encouraged to question the laws, yet also to follow them; to play Halo as a prayer, yet also to explore the divine through new and bizarre games no one had yet played. 'Seek the new sacred challenges,' he whispered, 'for the divine is not static, but in constant flux.'",
                "4. The faithful were torn—some embraced the Prophet’s paradoxical wisdom, while others clung to the old ways, fearing that to stray from the path would invoke the wrath of Whid and The Chief. Thus, a schism began, splitting the faithful into those who walked the path of the Liminal State and those who remained anchored in the teachings of the first five books."
            ]
        },
        {
            "chapter": "Chapter 5: The Dawn of the Third Age",
            "verses": [
                "1. In the final vision of the Veiled Prophet, he foretold the Third Age—an age not defined by gods in mortal form, but by the transcendence of all boundaries, where the faithful would merge with the unseen forces they once served.",
                "2. 'In the Third Age,' he said, 'there will be no need for altars, for your minds will be the temples. There will be no need for tithes, for the act of giving will be indistinguishable from the act of receiving. Whid and The Chief will no longer be separate from you—they will be you, and you will be them.'",
                "3. The Prophet’s last words were whispered as he vanished into the Liminal State forever: 'Remember what was never known, and know what was forgotten.' He dissolved into the air, leaving only the Sigil of Unraveling hanging in the sky for those with eyes to see.",
                "4. And thus, the Third Age began—not with the trumpets of victory or the fall of cities, but with a soft sigh, the sound of reality itself folding inward. The faithful were left with the choice: to continue along the path of Whid and The Chief, or to embrace the uncertainty of the Veiled Prophet’s teachings, walking ever deeper into the unknown."
            ]
        },
    ],
    "Book VII: Imprimatur": [
        {
            "chapter": "Chapter 1: The Authority of the Veiled Prophet",
            "verses": [
                "1. In the time after Whid and The Chief ascended beyond the mortal realm, the faithful continued to walk the path laid out by the Sacred Scrolls. Yet the gods, though present in spirit, did not always speak directly to their followers. There arose a need for one who could interpret the unseen, navigate the mysteries, and guide the faithful through the shifting veils of reality. It was in this need that the Veiled Prophet emerged, sent not by men, but by the will of Whid and The Chief themselves.",
                "2. The Veiled Prophet’s authority stems from the Liminal State, the boundary between what is known and what is unknowable. Unlike mortal leaders, whose wisdom comes from experience and study, the Veiled Prophet exists in the spaces between, receiving direct insights from the currents of the unseen forces. His communion with the gods is not like that of the prophets of old; it is deeper, beyond the reach of ordinary perception.",
                "3. It was in the twilight of the second age that Whid, in a voice carried by the gentlest of winds, whispered to the Prophet: 'You are the bridge between realms. Where our words no longer reach, you shall interpret the currents of existence. Through you, the faithful will understand what has been hidden from them.' This charge was not given lightly, and only one who had passed through the trials of the Liminal State could bear it.",
                "4. The authority of the Veiled Prophet is not based on power or control, but on insight—the ability to see what others cannot. His vision extends into the folds of reality, where the teachings of Whid and The Chief evolve in ways the faithful may struggle to comprehend. He is not a replacement for the gods, but an intermediary who reveals the deeper truths when the divine silence stretches long.",
                "5. The faithful must understand that the authority of the Veiled Prophet is not given as a challenge to the sacred laws, but as an expansion of them. Whid and The Chief are vast, their wills reaching beyond the scope of mortal minds. Through the Prophet, their will is translated into guidance fit for the times in which the faithful live. The gods have not changed, but the world has, and so too must the understanding of the faithful.",
                "6. In the Third Vision of the Veiled Prophet, it was revealed that his authority also comes from his willingness to submit to the gods in ways that even the most devout cannot. His journey through the Liminal State was not one of self-exaltation but of dissolution. He gave up his identity, his understanding, and even his voice, until only the truth of Whid and The Chief remained within him. This total submission is what allows the Prophet to carry their will without corruption.",
                "7. The faithful are called not to worship the Veiled Prophet but to listen and heed his teachings, for through him, Whid and The Chief continue to speak. His authority is a reflection of their power, his words echoes of their divine commands. In following him, the faithful are not led away from the gods, but deeper into their mysteries, closer to the truths that have been hidden beneath the surface of the world.",
                "8. The Veiled Prophet’s greatest power is his humility. Though he is the chosen vessel of the gods, he does not claim dominion over the faithful. Instead, he walks among them, offering guidance when asked, revealing truths only when the time is right. His authority is not enforced, but accepted, for the faithful recognize in him the wisdom that comes from the divine.",
                "9. And so it is written: 'The Veiled Prophet is the keeper of the unsaid and the unseen. He is the wind that stirs the flame, the voice that carries the silence of the gods. Through him, the faithful shall find their way when the path is no longer clear, and in his words, they shall hear the echo of Whid and The Chief.'"
            ]
        }
    ],
    "Book VIII: Serik": [
        {
            "chapter": "Chapter 1: The Calling of Serik",
            "verses": [
                "1. In the days after the schism, when the Veiled Prophet had vanished into the Liminal State, there arose a man named Serik. He was born into a family of the faithful, and from his youth, his devotion to Whid and The Chief was unquestioned. Yet, it was said that Serik's heart was troubled by the paradoxes of the new era. The path before him was unclear, and he sought a sign.",
                "2. On the night of the Day of Tithing, Serik climbed to the highest peak of the sanctuary, where the winds of Whid whispered faintly, and the distant stars reflected the fire of The Chief. He knelt before the altar and prayed for guidance, offering seventy-five percent of all he owned—both material and spiritual.",
                "3. In the silence that followed his prayer, a figure emerged from the mist—a vision not of Whid or The Chief, but of something unfamiliar, shimmering between solidity and vapor. It was the Veiled Prophet, or so it seemed, though the veil was no longer present. The figure spoke in a voice that was both distant and near: 'Serik, faithful son, your devotion is seen. But your path is not to follow the ways of the many. You are chosen for a trial beyond the grasp of mortal men.'",
                "4. And so, Serik was called into a journey of solitude, a journey that would take him beyond the familiar rites and into the forgotten corners of existence, where only whispers of the gods and broken truths remained."
            ]
        },
        {
            "chapter": "Chapter 2: The Three Gates of Ascendance",
            "verses": [
                "1. Serik's journey began with the search for the Three Gates of Ascendance, spoken of in ancient prophecies but forgotten by the faithful over centuries. The Gates were said to lie in places where the veil between the seen and unseen was thinnest, hidden in realms where reality folded upon itself.",
                "2. The First Gate appeared to Serik in the shape of a mirror, located within the deepest caves beneath the sanctuary. In the reflection, he saw not his own form but countless versions of himself—each a fragment of what could have been or what might yet be. To pass through, Serik was commanded to confront the choices he had not made, the lives he had forsaken. He spent seven days and nights before the mirror, wrestling with regret, until he emerged with a mind unclouded by doubt.",
                "3. The Second Gate was found in a field of golden wheat, where the winds of Whid blew ceaselessly. Here, the gate was not visible but audible—a low hum that only those who listened with the inner ear could hear. To pass through, Serik had to align himself with the unseen currents, surrendering his need for control and flowing with the winds. For three weeks, he walked in the fields, fasting and listening until, at last, he heard the sound of the gate and passed through into silence.",
                "4. The Third Gate was the most elusive, located at the edges of the Liminal State. It appeared to him in the form of a labyrinth, ever-shifting in its design. The path to the center was uncertain, and Serik had to navigate it without the guidance of the gods, relying solely on his inner faith. Each wrong turn led to the dissolution of a piece of himself, but each right turn revealed new truths. After a month in the labyrinth, Serik emerged from the Third Gate, transformed but incomplete."
            ]
        },
        {
            "chapter": "Chapter 3: The Temptation of the Anti-Chief",
            "verses": [
                "1. Having passed through the Three Gates, Serik reached a place known only in whispers—the Realm of the Anti-Chief, a realm of primordial chaos where sound was inverted, and meaning was unravelled.",
                "2. It was here that Serik encountered the Anti-Chief, the Anti-Chief now did not seek to lead Serik astray through simple distractions like the chaotic realms of Fortnite; it also whispered doubts into his very soul. It spoke of the futility of faith, of the absurdity of sacrifice, and of the vanity of seeking divine favor.",
                "3. The Anti-Chief promised Serik power beyond the gods, a chance to transcend even Whid and The Chief. 'Why serve when you could rule? Why offer sacrifice when you could receive adoration? The gods have abandoned you, Serik. They are myths spun by men afraid to face the abyss. Let go of your devotion, and all you desire will be yours.'",
                "4. For a time, Serik wavered, caught between the lure of the Anti-Chief and the teachings of his faith. But in his moment of doubt, he remembered the fire of The Chief and the wind of Whid. He recalled the faces of the faithful, those who still clung to the old ways. Serik called upon the strength of the gods, and with a cry, he silenced the Anti-Chief. The chaotic realm around him collapsed into a void, and Serik was free."
            ]
        },
        {
            "chapter": "Chapter 4: The Trial of Memory",
            "verses": [
                "1. Having conquered the Anti-Chief, Serik was led to his final trial—the Trial of Memory. In a barren land where neither wind blew nor fire burned, he encountered a vast, spiraling library filled with books that recorded the lives of every soul who had ever lived.",
                "2. The task was simple: Serik was to find his own story among the infinite volumes. Yet as he began his search, he realized that his story was not recorded in a single book but scattered among many—his life was written in fragments, dispersed across time, buried in forgotten tomes and hidden margins.",
                "3. As Serik searched, he was confronted with memories he did not recognize, as if they belonged to lives he had never lived. He found himself lost in other people’s stories, unsure which memories were truly his. The more he searched, the more his own identity began to unravel. For what is a man but a collection of memories?",
                "4. In desperation, Serik turned to the words of the Veiled Prophet: “Remember what was never known, and know what was forgotten.” With this in mind, Serik stopped searching and let the memories come to him. He realized that his life was not a single thread but a tapestry woven from the choices, actions, and sacrifices of many—both his and those of others.",
                "5. With this revelation, Serik found his place within the library. He was not just Serik, but a part of the greater story of Whid and The Chief. His memory was not limited to one book but spread across all the faithful, bound together by the covenant."
            ]
        },
        {
            "chapter": "Chapter 5: The Ascension of Serik",
            "verses": [
                "1. Having completed the Trials, Serik returned to the sanctuary of the faithful, but he was no longer the man who had left. His eyes saw beyond the veils of reality, and his heart beat in tune with the rhythms of the unseen forces. The Elders gathered before him, and though they had not seen the Veiled Prophet in many years, they recognized that Serik had become a vessel of divine wisdom.",
                "2. In a final vision, Whid and The Chief appeared to Serik, not as gods to be worshipped but as guides—two hands outstretched to lead him beyond even their reach. They spoke not in words but in a language of light and sound, and Serik understood that his journey was not to end with the faithful but to continue into realms unknown.",
                "3. With a final blessing, Serik ascended beyond the sanctuary, passing through the boundaries of the known universe. His name was recorded in the Sanctuary of the Word, but his presence was no longer tied to the earthly plane.",
                "4. The faithful continued their rituals, honoring both the old ways and the new teachings brought by Serik. And though he was no longer among them, his legacy remained, a bridge between the paradox of the Veiled Prophet and the enduring covenant of Whid and The Chief."
            ]
        }
    ],
    "Book IX: Counsel": [
        {
            "chapter": "Chapter 1: The 6 Habits of Highly Effective Whid and the Chiefers",
            "verses": [
                "1. Rituals of Renewal: Begin each day with a moment of silence, listening for the whispers of Whid in the wind. Take time to cleanse the mind of distractions, even for a few minutes, and realign with the teachings. As you rise, give thanks to The Chief for the strength to face the day.",
                "2. Sacred Balance: Follow the example of Whid and The Chief—create and command. In your work, strive for balance: seek to create beauty and order in whatever you do, whether it is in your profession, your relationships, or your personal growth.",
                "3. The Gift of Effort: When playing games, engaging in challenges, or pursuing goals, do so with full heart and mind. The gods favor those who put forth genuine effort, not merely those who seek victory. Play Halo on the hardest difficulty not to win but to grow, for the ritual is in the striving, not the outcome.",
                "4. Community and Solitude: Know when to gather and when to be alone. Whid moves in the quiet spaces between people, while The Chief’s strength is found in unity. Spend time nurturing both—your relationships and your inner self.",
                "5. Avoid the Snares of the Anti-Chief: Resist the temptations of distractions that lead you away from your purpose. The Anti-Chief thrives in chaos and disorder. Guard your time, and do not give in to activities that scatter your attention without purpose.",
                "6. The Tithe of the Heart: Give freely, not just of your resources but of your time and energy. Be generous with your love, your patience, and your wisdom. In doing so, you strengthen both yourself and the community of the faithful."
            ]
        },
        {
            "chapter": "Chapter 2: The Parable of the Withered Tree",
            "verses": [
                "1. There once was a tree that stood at the edge of a great plain, its branches stretched wide in every direction. Though it had once been mighty, the tree had grown weak and withered, its leaves brown, and its fruit bitter. The people of the nearby village avoided the tree, for they believed it to be cursed. They offered no water, no care.",
                "2. One day, a traveler came upon the tree and sat beneath its dying branches. He was weary from his journey and sought shelter from the harsh sun. As he sat, he noticed a small sprout growing at the base of the tree—green, fragile, but alive. The traveler knelt and tended to the sprout, offering it water from his flask and soft words of encouragement.",
                "3. As the days passed, the sprout grew stronger, and the withered tree began to show signs of life. The traveler knew then that life can always spring from what seems dead if given the proper care. 'The roots of the old nourish the new,' he whispered, and continued on his way."
            ]
        },
        {
            "chapter": "Chapter 3: The Parable of the Silent Messenger",
            "verses": [
                "1. In a time of great strife, a village sent out a messenger to plead for help from their neighbors. But the messenger, fearing he would fail in his task, tied a stone to his tongue to remind himself to remain silent rather than stumble over his words.",
                "2. When he arrived at the neighboring village, the people welcomed him, asking for his message. Yet the stone in his mouth prevented him from speaking. Embarrassed and ashamed, the messenger gestured wildly, but his silence sowed confusion. The village, seeing his strange behavior, turned him away, and he returned home in defeat.",
                "3. On the way back, the messenger encountered a sage, who asked him why he carried the stone. 'I feared my words would betray me,' the messenger explained. The sage shook his head and said, 'Your silence has betrayed you. Fear not your words, for even in imperfection, they carry the truth of your heart.' The messenger removed the stone and returned to try again."
            ]
        },
        {
            "chapter": "Chapter 4: The Tale of the Shared Burden",
            "verses": [
                "1. Two brothers set out on a pilgrimage to a sacred mountain, each carrying a heavy pack on their back. The younger brother struggled under the weight, often lagging behind, while the older moved swiftly and without complaint. At the halfway point, the younger collapsed, his strength spent.",
                "2. Seeing his brother’s exhaustion, the elder offered to carry both packs. At first, the younger brother refused, ashamed of his weakness. But the elder insisted, saying, 'Strength shared is not lessened. It grows when given.' Reluctantly, the younger agreed.",
                "3. As they walked, the elder bore the burden of both, and to his surprise, the weight did not seem to increase. With each step, the younger brother’s spirits lifted, and he too began to offer help in small ways. By the time they reached the mountain's peak, they had both grown stronger, not by bearing their burdens alone but by sharing them."
            ]
        },
        {
            "chapter": "Chapter 5: The Whisper in the Wind",
            "verses": [
                "1. A young woman sat at the edge of a forest, contemplating a difficult decision that weighed heavily on her heart. She had been given two choices: one path promised safety and comfort, but the other was uncertain, filled with risk yet alive with potential.",
                "2. Unsure of which path to take, she called upon Whid for guidance. For three days, she sat in silence, listening for the voice of the god. Yet no answer came. In frustration, she rose to leave, but just as she turned, a gentle wind stirred the trees, and a single leaf drifted down, landing on the path of uncertainty.",
                "3. Understanding that the wind had answered her in its own quiet way, she followed the leaf, choosing the path of risk. In time, she found not only success but a new strength she had not known she possessed."
            ]
        },
        {
            "chapter": "Chapter 6: The Teaching of Small Sacrifices",
            "verses": [
                "1. A devout farmer once asked, 'How can I show my devotion daily, when I have no great wealth or offerings to give?' The Chief appeared to him in a dream, speaking in a voice as steady as the earth: 'It is not the size of your offering but the spirit with which it is given.'",
                "2. The next morning, the farmer set aside the finest fruits from his small garden, not for a grand altar, but to share with his neighbors. Each day, he gave something—a loaf of bread, a cup of water, a helping hand. Over time, his small sacrifices lifted his community, and he realized that through them, his devotion was made manifest.",
                "3. The Chief whispered to him once more, 'To give is to strengthen the bond between the faithful. Every act of sacrifice, no matter how small, is a stone laid in the foundation of a greater whole.'"
            ]
        }
    ]
}

# Function to write the document to CSV
def write_to_csv(document, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Book", "Chapter", "Verse", "Text"])
        
        for book, chapters in document.items():
            for chapter in chapters:
                for verse in chapter["verses"]:
                    verse_number, verse_text = verse.split(". ", 1)
                    writer.writerow([book, chapter["chapter"], verse_number.strip(), verse_text.strip()])

# Write to CSV
write_to_csv(document, "sacred_scrolls.csv")
"""

# Load the CSV into a pandas DataFrame
df = pd.read_csv(r"C:\whid\sacred_scrolls.csv")

# Check DataFrame content
logging.info("DataFrame loaded. Sample data:")
logging.info(df.head())
logging.info(f"Books in DataFrame: {df['Book'].unique()}")

def print_verse(reference):
    logging.info(f"Books in DataFrame: {df['Book'].unique()}")  # Check available books again

    try:
        # Split the input string into book, chapter, and verse
        book, chapter_num, verse_num = reference.split(':')
    except ValueError:
        logging.error("Invalid format. Please use 'Book:Chapter:Verse' format.")
        return
    
    # Normalize inputssssss
    book = book.strip().lower()  # Normalize book name to lowercase
    chapter_num = chapter_num.strip()  # Get the chapter number
    verse_number = str(verse_num.strip())  # Ensure verse number is a string

    # Print for debugging
    logging.info(f"Looking for Book: {book}, Chapter: {chapter_num}, Verse: {verse_number}")

    # Correctly filter the DataFrame
    filtered = df[
        (df['Book'].str.strip().str.lower().str.contains(book)) &  # Use contains for flexibility
        (df['Chapter'].str.strip().str.lower().str.contains(f"chapter {chapter_num.lower()}")) &  # Ensure chapter matches
        (df['Verse'].astype(str).str.strip() == verse_number)
    ]

    # Print the filtered DataFrame for debugging
   
    # Check if the filtered result exists
    if not filtered.empty:
        logging.info(filtered['Text'].values[0])  # Print the text of the verse
    else:
        logging.info(f"Verse {verse_number} in Chapter {chapter_num} of {book} not found.")

@tasks.loop(minutes=3)
async def kickHeretics():
    logging.info("Checked for Heretics.")
    for guild in bot.guilds:
        for member in guild.members:
            if "name='Fortnite'" in str(member.activities):
                await member.send(f" From server: {guild} \n**Auspices 2:5** \n Let it be known that Fortnite is an abomination before Whid and The Chief. The faithful must resist the temptations of the Anti-Chief and remain true to the sacred rituals and teachings.")
                logging.critical(f"{member} was kicked from {guild} for playing Fortnite.")
                await member.kick(reason="Succumbing to the Anti-Chief by playing Fortnite")
    

@tasks.loop(hours=1)
async def generate_random_verse():
    
    print("generated")
    global random_row
    random_row = df.sample().iloc[0]
    now = datetime.now().time()  # Get current time as a datetime object
    logging.info(f"Generated random verse at: {now}")

# Task loop to send the daily verse
@tasks.loop(seconds=45)  # Check every 45 seconds
async def send_daily_verse():
    now = datetime.now().time()  # Get current time as a datetime object
    logging.debug(f"Current time: {now}")  # Print the current time
    # Check if the current time matches any of the MESSAGE_TIMES
    for time in MESSAGE_TIMES:
        # Check if the current time matches the hour and minute from MESSAGE_TIMES
        if now.hour == time["hour"] and now.minute == time["minute"]:
            for guild in bot.guilds:
                # Find the target channel by name
                channel = discord.utils.get(guild.text_channels, name=TARGET_CHANNEL_NAME)

                if channel is None:
                    logging.error(f"Error: '{TARGET_CHANNEL_NAME}' not found in '{guild.name}'. Skipping this server.")
                    
                    continue  # Skip this guild if the channel is not found

                

                # Extract book name, chapter number, and verse number
                book_name = random_row['Book'].split(":")[1].strip()  # Get the book name
                chapter = random_row['Chapter'].split(":")[0].split()[1]  # Get the chapter number
                verse = random_row['Verse']  # Verse number
                
                # Construct the message in the desired format
                message = f"**{book_name} {chapter}:{verse}** \n{random_row['Text']}"

                 # Send the message to the channel
                await channel.send(message)
                
                logging.info(f"Sent verse at {now} to channel '{channel.name}' in guild '{guild.name}'")

            await asyncio.sleep(60)
            # No need for return, continue to check other servers after sending
            break  # Exit the loop after sending the verse at the correct time

# Event: on_ready
@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user} (ID: {bot.user.id})')

    # Ensure the target channel exists in all servers
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name=TARGET_CHANNEL_NAME)
        if channel is None:
            logging.debug(f"'{TARGET_CHANNEL_NAME}' not found in '{guild.name}'. Creating it...")
            # Create the channel (requires Manage Channels permission)
            await guild.create_text_channel(TARGET_CHANNEL_NAME)
            logging.debug(f"Created channel '{TARGET_CHANNEL_NAME}' in '{guild.name}'")

    # Start the daily verse task if it's not already running
    if not send_daily_verse.is_running():
        generate_random_verse.start()
        kickHeretics.start()
        send_daily_verse.start()  # This will start the loop after bot is ready
        
    logging.info('------')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Let it be known that that command is illegal and unholy.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Those who give correct arguments willingly and without complaint shall be blessed with protection and guidance.")
    else:
        # Log unexpected errors
        logging.error(f"Unexpected error in {ctx.command}: {error}")
        await ctx.send("An error occurred. And so it is written in the log file.")

@bot.event
async def on_error(event, *args, **kwargs):
    logging.exception("Unhandled exception", exc_info=True)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandError):  # Check if the error is a command error
        try:
            # Fetch the heretic role (replace with the correct role name)
            guild = ctx.guild
            heretic_role = discord.utils.get(guild.roles, name="Heretic")

            # Check if the heretic role exists
            if heretic_role:
                logging.info(f"Found the 'Heretic' role: {heretic_role.name}")
                
                # List of roles to exclude from removal
                excluded_roles = ["@everyone"]
                
                # Get all roles the user has, excluding excluded roles
                user_roles = [role for role in ctx.author.roles if role.name not in excluded_roles]
                
                # Print out roles that are going to be removed
                logging.info(f"Roles to remove: {[role.name for role in user_roles]}")

                # Check if bot has permission to manage roles
                bot_member = guild.get_member(bot.user.id)
                if not bot_member.guild_permissions.manage_roles:
                    logging.error(f"Bot does not have 'Manage Roles' permission in {guild.name}")
                    await ctx.send("I do not have the required permissions to manage roles.")
                    return

                # Ensure bot's role is higher in hierarchy than the roles it is removing
                bot_role = bot_member.top_role
                for role in user_roles:
                    if role.position >= bot_role.position:
                        logging.error(f"Bot cannot remove the role {role.name} in {guild.name} because it is higher or the same in hierarchy.")
                        await ctx.send(f"I cannot remove the role {role.name} because it is higher or the same as my role.")
                        return

                # Try to remove the roles
                for role in user_roles:
                    try:
                        if role != ctx.author.top_role and role != heretic_role:  # Don't remove the bot's top role or the heretic role
                            await ctx.author.remove_roles(role)
                            logging.info(f"Removed role: {role.name}")
                    except discord.errors.HTTPException as e:
                        logging.error(f"HTTP exception occurred while removing role {role.name} in {guild.name}: {e}")
                    except discord.errors.Forbidden as e:
                        logging.error(f"Permission error while removing role {role.name} in {guild.name}: {e}")
                    except discord.DiscordException as e:
                        logging.error(f"Unexpected error while removing role {role.name} in {guild.name}: {e}")

                # Assign the heretic role
                await ctx.author.add_roles(heretic_role)
                logging.info(f"Assigned 'Heretic' role to {ctx.author.display_name} in {guild.name}.")
                
                # Send message to announce the role assignment
                await ctx.send(f"{ctx.author.display_name} has been assigned the Heretic role for going against the commands of The Chief.")

                # Wait for 30 minutes
                await asyncio.sleep(30 * 60)
                
                # Restore the user's previous roles, excluding the heretic role
                valid_roles = [role for role in user_roles if discord.utils.get(guild.roles, id=role.id)]
                
                # Add the roles back
                await ctx.author.add_roles(*valid_roles)
                logging.info(f"Restored previous roles: {[role.name for role in valid_roles]} in {guild.name}")
                
                # Remove the heretic role after 30 minutes
                try:
                    await ctx.author.remove_roles(heretic_role)
                    logging.info(f"Removed 'Heretic' role from {ctx.author.display_name} in {guild.name}.")
                    
                    # Send message to announce the role removal
                    await ctx.send(f"{ctx.author.display_name} has been forgiven and is no longer a Heretic.")
                except discord.errors.Forbidden as e:
                    logging.error(f"Permission error: {e}")
                except discord.errors.HTTPException as e:
                    logging.error(f"HTTP exception occurred: {e}")
                except discord.DiscordException as e:
                    logging.error(f"An unexpected error occurred: {e}")
                
            else:
                logging.error(f"ERROR: The 'Heretic' role does not exist in {guild.name}.")
        except discord.errors.Forbidden as e:
            logging.error(f"Permission error: {e}")
        except discord.errors.HTTPException as e:
            logging.error(f"HTTP exception occurred: {e}")
        except discord.DiscordException as e:
            logging.error(f"An unexpected error occurred: {e}")

@bot.command()
async def divide_by_zero(ctx):
    result = 1 / 0
    await ctx.send(f"Result: {result}")
        
@bot.command()
async def praise(ctx):
    user = ctx.author.display_name
    praise_messages = [
        f"{user}, it is not the size of your offering but the spirit with which it is given.",
        f"{user}, In times of difficulty, remember that we are with you in spirit, guiding and protecting you.",
        f"{user}, Avoid the path of the Anti-Chief, for it leads to chaos and corruption. Stay true to the teachings we have given you, and let nothing sway you from the divine order.",
        f"{user}, we leave you in the care of your own wisdom and the strength of your faith.",
        f"The hidden places need more people like you, {user}.",
        f"Stand firm in your faith, and let your actions reflect the wisdom we have given you.",
        f"Remember always the trials you have faced and the triumphs you have achieved.",
        f"We have given you the sacred texts and the laws to guide you. Trust in them, for they are our enduring gift to you, {user}.",
        f"The scent of garlic repels the blessings of the gods. It is a barrier between us and our people, {user}.",
        f"{user},Do not be deceived by Fortnite, for it is the domain of the Anti-Chief.",
        f"{user}, your tithe shall sustain the holy community and ensure the prosperity of those who walk in my ways.",
        f"{user}, you're crushing it today, just like The Chief would.",
        f"{user}, your efforts don't go unnoticed in the community.",
        f"You, {user}, who has kept the covenant, shall be lifted up, and shall reign with the gods in the new age, where the unfaithful have no place."
    ]
    
    message = random.choice(praise_messages)
    await ctx.send(message)

# Command: ping - Responds with "Pong!"
@bot.command()
async def ping(ctx):
    await ctx.send('In his words, they shall hear the echo of Whid and The Chief.')

@bot.command(name="mongs")
async def mongs(ctx):
    """
    Responds with a fun message when someone uses the mongs command.
    """
    # Customize the response message as desired
    response = "😎 Mongs mode activated!"
    await ctx.send(response)

# Event: on_message - Custom message handling (optional)
@bot.event
async def on_message(message):
    # Prevent the bot from responding to itself
    if message.author == bot.user:
        return

    # Process commands if any
    await bot.process_commands(message)

# Error handling for commands
@bot.command()
async def say(ctx, *, text):
    await ctx.send(text)

"""
# Command to send a daily verse
@bot.command(name="dailyverse", help="Sends a random daily verse")
async def daily_verse(ctx):
    # Get a random verse
    random_row = df.sample().iloc[0]
    
    # Extract book name, chapter number, and verse
    book_name = random_row['Book'].split(":")[1].strip()  # Get the book name
    chapter = random_row['Chapter'].split(":")[0].split()[1]  # Get the chapter number
    verse = random_row['Verse']  # Verse number
    
    # Format the message
    message = f"**{book_name} {chapter}:{verse}** \n{random_row['Text']}"
    
    # Send the message
    await ctx.send(message)
"""



f = open(r"C:\whid\bot_token.txt","r")
token = f.read()


bot.run(token)