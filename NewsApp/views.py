from django.shortcuts import render
from django.views.generic.edit import View
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from NewsApp.models import Articles, Comments
from NewsApp.forms import CommentForm


# Для вывода всех постов
class postsView(View):
    def get(self, request):
        return render(request, 'NewsApp/posts.html',
                      {'object_list': Articles.objects.all().order_by("-date")[:20],
                       'user': request.user})


# Для вывода одного поста
class postView(View):
    model = Articles

    def get(self, request, pk):
        a = dict(atr=self.model.objects.filter(id=pk))
        c = {'user': request.user}
        a.update(c)

        comments = Comments.objects.filter(comments_article=pk)
        d = {'commets': comments}
        a.update(d)

        form = {'form_comments': CommentForm}
        a.update(form)

        return render(request, 'NewsApp/post.html', a)


# Для добавления комментария
def addcomment(request, article_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comments_article = Articles.objects.get(id=article_id)
            comment.comments_author = request.user
            form.save()
            return HttpResponseRedirect('/news/%s' % article_id)
        return HttpResponseRedirect('/news/%s' % article_id)
