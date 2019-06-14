from django.shortcuts import render
posts = [
        {
            'author':'Ilia',
            'title':'Post 1',
            'content':'Content',
            'date_posted':'Date',
        },
        {
            'author':'Not Ilia',
            'title':'Post 2',
            'content':'Other content',
            'date_posted':'Other date',
        }
]

def home(request):
    context = {
            'posts':posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

# Create your views here.
