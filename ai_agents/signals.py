from openai import OpenAI
from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Post, Comment
from .models import Bot
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

# Signal to generate AI comment on post creation
@receiver(post_save, sender=Post)
def create_ai_comment(sender, instance, created, **kwargs):
    if created:
        print(f"[DEBUG] New post created: {instance.id}, Title: {instance.title}")
        
        # Fetch active bot
        bot = Bot.objects.filter(is_active=True).first()
        if not bot:
            print("[DEBUG] No active bot found.")
            return
        print(f"[DEBUG] Active bot selected: {bot.name}")

        # Generate input for OpenAI
        user_input = f"Generate a relevant comment for this post: {instance.content}"
        print(f"[DEBUG] Input to OpenAI: {user_input}")

        # Generate response
        ai_comment = chat_gpt(user_input)
        if not ai_comment:
            print("[DEBUG] Failed to generate AI comment.")
            return

        # Save the comment to the database
        try:
            Comment.objects.create(
                post=instance,
                content=ai_comment,
                bot=bot.name
            )
            print(f"[DEBUG] AI comment saved for post {instance.id}: {ai_comment}")
        except Exception as e:
            print(f"[DEBUG] Error saving AI comment: {e}")
