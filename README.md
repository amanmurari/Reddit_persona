
# Reddit User Persona Generator (Groq-powered)

This Python script analyzes a Reddit user's posts and comments to generate a qualitative persona using Groq's LLMs (LLaMA 3 via Groq API).  
The output is a structured persona report with traits, behaviors, and citations, following a UX-style qualitative persona format.

## ðŸš€ Features

- Fetches recent Reddit submissions and comments
- Uses Groq's fast LLaMA models to build a user persona
- Includes demographic insights, motivations, challenges, and quotes
- Outputs the persona to a text file with proper citations
- Easy to extend or convert to PDF/Markdown

---

## ðŸ“¦ Requirements

- Python 3.8+
- [PRAW](https://praw.readthedocs.io/)
- [Groq SDK](https://docs.groq.com/)
- `dotenv` (optional)

```bash
pip install praw groq python-dotenv
```

---

## ðŸ” Environment Variables

You can store the following credentials in a `.env` file or set them directly in your script:

```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
GROQ_API_KEY=your_groq_key
```

---

## ðŸ§ª How to Run

```bash
python red.py https://www.reddit.com/user/kojied/ --limit 50
```

It will output a file like:

```
output/kojied_persona.txt
```

---

## âœï¸ Persona Format

```
Persona: kojied
â€œTagline or quoteâ€

**Demographics**
- ...

**Goals & Motivations**
- ...

**Challenges & Pain Points**
- ...

**Behavior Patterns & Interests**
- ...

**Communication Style**
- ...

**User Voice Quote**
> â€œ...â€ â€” [comment:id:url]

*Persona built from analysis of X posts and Y comments.*
```

---

## ðŸ¤– Model

- Uses `llama3-8b-8192` from Groq (or configurable with `--model`)

---

## ðŸ“„ License

MIT License.
