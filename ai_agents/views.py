from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from posts.models import Post, Comment
from .models import Bot
import openai
import json
from django.conf import settings

# Helper Function: Generate AI Response
def generate_ai_response(post_content, bot):
    """
    Generate an AI-based response using OpenAI API.
    """
    openai.api_key = settings.OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": bot.personality or "You are a helpful assistant."},
                {"role": "user", "content": f"Generate a relevant comment for this post: {post_content}"}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return "Sorry, I couldn't generate a response at the moment."

# Endpoint: Generate AI Response for a Post
@csrf_exempt
def generate_comment(request):
    """
    Generate and save an AI comment for a specific post.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post_id = data.get('post_id')
            post = get_object_or_404(Post, id=post_id)

            # Fetch the active bot
            bot = Bot.objects.filter(is_active=True).first()
            if not bot:
                return JsonResponse({'error': 'No active bot available'}, status=400)

            # Generate the AI comment
            ai_comment = generate_ai_response(post.content, bot)

            # Save the comment
            comment = Comment.objects.create(
                post=post,
                content=ai_comment,
                bot=bot.name  # Use the bot's name for the `bot` field
            )

            return JsonResponse({
                'status': 'success',
                'comment': {
                'id': comment.id,
                'post_id': post.id,
                'author': comment.bot if comment.bot else None,
                'content': comment.content,
                'created_at': comment.created_at.isoformat()
    }
})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
