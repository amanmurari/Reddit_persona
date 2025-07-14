import os
import argparse
import praw
from groq import Groq  # Groq Python SDK


def fetch_reddit_activity(reddit, username, limit=100):
    """Return a list of dicts for the user's newest posts & comments."""
    user = reddit.redditor(username)

    posts = [
        {
            "type": "post",
            "body": submission.title + "\n" + submission.selftext,
            "url": submission.url,
            "id": submission.id,
        }
        for submission in user.submissions.new(limit=limit)
    ]

    comments = [
        {
            "type": "comment",
            "body": comment.body,
            "url": f"https://reddit.com{comment.permalink}",
            "id": comment.id,
        }
        for comment in user.comments.new(limit=limit)
    ]

    return posts + comments


def build_persona(activity, username, groq_api_key, model="llama3-8b-8192"):
    """Generate a qualitative persona via Groq Chat Completions."""
    client = Groq(api_key=groq_api_key)

    system_prompt = (
        "You are a persona-building assistant. Given Reddit activity, craft a one-page qualitative persona in this exact structure:\n\n"
        "Persona: <Username>\n“Tagline or short quote”\n\n"
        "**Demographics**\n- bullets with [type:id:url]\n\n"
        "**Goals & Motivations**\n- ...\n\n"
        "**Challenges & Pain Points**\n- ...\n\n"
        "**Behavior Patterns & Interests**\n- ...\n\n"
        "**Communication Style**\n- ...\n\n"
        "**User Voice Quote**\n> “...” — [comment:id:url]\n\n"
        "*Persona built from analysis of X posts and Y comments.*"
    )

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    # Flatten activity into citatable context blocks
    context = "\n\n".join(
        f"[{item['type']}:{item['id']}:{item['url']}] {item['body']}" for item in activity
    )

    messages.append(
        {
            "role": "user",
            "content": f"Username: {username}\n\nActivity:\n{context}",
        }
    )

    chat_completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=800,
    )

    return chat_completion.choices[0].message.content.strip()


def save_persona(username, persona_text, count, out_dir="output"):
    """Save persona text, injecting post/comment counts."""
    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, f"{username}_persona.txt")
    persona_text = (
        persona_text.replace("X posts", str(count["posts"])).replace(
            "Y comments", str(count["comments"])
        )
    )
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(persona_text)
    print(f"Persona saved to: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a qualitative user persona from a Reddit profile using the Groq API."
    )
    parser.add_argument("url", help="Reddit profile URL")
    parser.add_argument("--limit", type=int, default=100, help="Items to fetch per type")
    parser.add_argument("--model", default="llama3-8b-8192", help="Groq model name")
    args = parser.parse_args()

    username = args.url.rstrip("/").split("/")[-1]

    # Initialise Reddit client (credentials expected in env vars)
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=f"persona_generator_groq/0.1 by {username}",
    )

    activity = fetch_reddit_activity(reddit, username, limit=args.limit)
    counts = {
        "posts": sum(1 for a in activity if a["type"] == "post"),
        "comments": sum(1 for a in activity if a["type"] == "comment"),
    }

    persona_text = build_persona(
        activity, username, os.getenv("GROQ_API_KEY"), model=args.model
    )
    save_persona(username, persona_text, counts)


if __name__ == "__main__":
    main()
