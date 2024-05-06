from django.shortcuts import render, get_object_or_404, redirect
from .models import Name
from .forms import NameForm

def name_list(request):
    names = Name.objects.all()
    return render(request, {'names': names})


def name_update(request, pk):
    name_instance = get_object_or_404(Name, pk=pk)
    if request.method == 'POST':
        form = NameForm(request.POST, instance=name_instance)
        if form.is_valid():
            form.save()
            return redirect('name_list')
    else:
        form = NameForm(instance=name_instance)
    return render(request, {'form': form, 'name_instance': name_instance})



def name_delete(request, pk):
    name_instance = get_object_or_404(Name, pk=pk)
    if request.method == 'POST':
        name_instance.delete()
        return redirect('name_list')  # Redirect to a success page
    return render(request, {'name_instance': name_instance})


