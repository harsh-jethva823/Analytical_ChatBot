from .models import KeywordStat

STATIC_KEYWORDS = ["admission", "course", "placements", "campus"]

def update_keyword_stats(user_message):
    message = user_message.lower()
    for keyword in STATIC_KEYWORDS:
        if keyword in message:
            obj, created = KeywordStat.objects.get_or_create(keyword=keyword)
            obj.count += 1
            obj.save()
