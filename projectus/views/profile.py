
# projectus/views/profile.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projectus.forms import ProfileForm, PostCreateForm


@login_required
def profile(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'edit_profile':
            form = ProfileForm(
                request.POST,
                instance=request.user
            )
            post_form = PostCreateForm()

            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    'Perfil atualizado com sucesso!'
                )
                return redirect('profile')

        elif action == 'create_post':
            form = ProfileForm(instance=request.user)

            post_form = PostCreateForm(
                request.POST,
                request.FILES
            )

            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.save()

                messages.success(
                    request,
                    'Publicação criada com sucesso!'
                )
                return redirect('profile')

        else:
            form = ProfileForm(instance=request.user)
            post_form = PostCreateForm()

    else:
        form = ProfileForm(instance=request.user)
        post_form = PostCreateForm()

    posts = request.user.posts.all()

    return render(
    request,
    'projectus/profile.html',
    {
        'form': form,
        'post_form': post_form,
        'posts': posts,
    }
)
