from django.shortcuts import render
import matplotlib.pyplot as plt
from django.http import HttpResponse
import io
from .models import KeywordStat

# Create your views here.
def chat_interface(request):
    """Render the main chat interface."""
    return render(request, 'chatbot/chat.html')
from django.shortcuts import render

def show_chart_page(request):
    return render(request, 'keyword_chart.html')



def keyword_chart(request):
    keywords = KeywordStat.objects.all()
    labels = [k.keyword for k in keywords]
    counts = [k.count for k in keywords]

    # Create a single figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Bar chart
    ax1.bar(labels, counts, color='orange')
    ax1.set_title("Keyword Frequency")
    ax1.set_xlabel("Keyword")
    ax1.set_ylabel("Count")

    # Pie chart
    ax2.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
    ax2.set_title("Keyword Usage Distribution")
    ax2.axis('equal')  # Ensures pie chart is circular

    plt.tight_layout()

    # Save combined figure to buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return HttpResponse(buffer.read(), content_type='image/png')