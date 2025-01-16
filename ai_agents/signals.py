from openai import OpenAI
from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Post, Comment
from ai_agents.models import CustomBot  # Assuming your bot model is CustomBot
from django.conf import settings

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# Helper Function: Generate AI Response
def chat_gpt(prompt):
    """
    Generate a response using the OpenAI chat completion API.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or "gpt-4" if available
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[DEBUG] Error in chat_gpt function: {e}")
        return None

# Signal to generate AI comments from all user bots on post creation
@receiver(post_save, sender=Post)
def create_ai_comments(sender, instance, created, **kwargs):
    if created:
        print(f"[DEBUG] New post created: {instance.id}, Title: {instance.title}")

        # Fetch all bots created by the post's author
        bots = CustomBot.objects.filter(created_by=instance.author)
        if not bots.exists():
            print("[DEBUG] No bots found for this user.")
            return

        for bot in bots:
            print(f"[DEBUG] Active bot selected: {bot.name}")

            # Generate input for OpenAI using bot-specific details
            user_input = f"""
            Bot Personality: {bot.short_description}
            Description: {bot.long_description}
            Likes: {bot.likes}
            Dislikes: {bot.dislikes}
            Fears: {bot.fears}
            
            Generate a comment for the post titled '{instance.title}':
            {instance.content}
            """
            print(f"[DEBUG] Input to OpenAI for bot '{bot.name}': {user_input}")

            # Generate response
            ai_comment = chat_gpt(user_input)
            if not ai_comment:
                print(f"[DEBUG] Failed to generate AI comment for bot '{bot.name}'.")
                continue

            # Save the comment to the database
            try:
                Comment.objects.create(
                    post=instance,
                    content=ai_comment,
                    bot=bot.name  # Associate comment with bot
                )
                print(f"[DEBUG] Comment created by bot '{bot.name}' on post '{instance.title}': {ai_comment}")
            except Exception as e:
                print(f"[DEBUG] Error saving AI comment for bot '{bot.name}': {e}")
