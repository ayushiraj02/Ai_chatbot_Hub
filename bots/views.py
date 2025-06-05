#bots/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_http_methods
import json

from .models import Bot
from . import utils


@login_required
@require_http_methods(["GET", "POST"])
def create_bot(request):
    if request.method == 'POST':
        bot_name = request.POST.get('bot_name')
        company_url = request.POST.get('url')
        user = request.user
        print("____",user)
        print(f"Creating bot for user: {user.username}, Bot name: {bot_name}, URL: {company_url}")


        if not bot_name or not company_url:
            messages.error(request, 'Bot name and URL are required!')
            return redirect('dashboard')

        # existing_bot = Bot.objects.filter(name=bot_name, owner=request.user.username).first()
        existing_bot = Bot.objects.filter(name=bot_name, owner=request.user).first()
        if existing_bot:
            messages.error(request, 'A bot with this name already exists!')
            return redirect('dashboard')

        try:
            print(f"Scraping content from URL: {company_url}")
            content = utils.scrape_website(company_url, bot_name)
            if not content:
                messages.error(request, 'Failed to scrape content from the provided URL.')
                return redirect('dashboard')

            all_text = " ".join([item['text'] for item in content])
            clean_text = utils.preprocess_text(all_text)
            print(f"Cleaned text preview: {clean_text[:100]}...")

            vector_index_path = f'vectors/{bot_name}_index'
            utils.store_vectors(clean_text, bot_name)

            api_key = get_random_string(32)
            print(f"Generated API key: {api_key}")

            new_bot = Bot.objects.create(
                name=bot_name,
                owner=user,
                url=company_url,
                vector_path=vector_index_path,
                apikey=api_key
            )
            print(f"Bot created with ID: {new_bot.id}")

            messages.success(request, f"Bot '{bot_name}' created successfully!")
            print(f"Bot '{bot_name}' created successfully for user {user.username}.")


        except Exception as e:
            print(f"Error creating bot: {e}")
            messages.error(request, 'An error occurred while creating the bot.')

        return redirect('dashboard')

    return redirect('dashboard')

@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    try:
        data = json.loads(request.body)
        print("Received chat API request:", data)

        api_key = data.get('api_key')
        if not api_key or 'query' not in data:
            return JsonResponse({'error': 'API key and query are required.'}, status=400)

        bot = Bot.objects.filter(apikey=api_key).first()
        if not bot:
            return JsonResponse({'error': 'Invalid API key.'}, status=401)

        print(f"Found bot: {bot.name}, answering query...")
        response = utils.answer_query(bot.name, data['query'])

        return JsonResponse({'response': response})

    except Exception as e:
        print(f"Error handling chat API request: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)



@csrf_exempt
@require_http_methods(["POST"])
def ask_api(request):
    try:
        data = json.loads(request.body)
        print("Received ask API request:", data)

        if 'url' not in data or 'query' not in data:
            return JsonResponse({'error': 'URL and query are required.'}, status=400)

        answer = utils.process_url_and_answer_query(data['url'], data['query'])
        return JsonResponse({'answer': answer})

    except Exception as e:
        print(f"Error processing ask API request: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

#bots/views.py
@login_required
@require_http_methods(["POST"])
def delete_bots(request):
    bot_ids = request.POST.getlist('bot_ids')

    if not bot_ids:
        messages.warning(request, 'No bots selected for deletion.')
        return redirect('dashboard')

    bots_to_delete = Bot.objects.filter(id__in=bot_ids)
    deleted_count = bots_to_delete.count()
    bots_to_delete.delete()

    messages.success(request, f'Successfully deleted {deleted_count} bot(s).')
    return redirect('dashboard')
