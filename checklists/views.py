from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator

from .models import Area, ChecklistItem
from .forms import AreaForm, ChecklistItemForm


@login_required
def dashboard(request):
    areas = Area.objects.filter(user=request.user).order_by("name")

    selected_area_id = request.GET.get("area")
    selected_area = None

    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    order = request.GET.get("order", "new")

    # Query principal (com filtros aplicados)
    items = ChecklistItem.objects.filter(area__user=request.user).select_related("area")

    # Totais gerais (sem filtros)
    total_items = ChecklistItem.objects.filter(area__user=request.user).count()
    total_done = ChecklistItem.objects.filter(area__user=request.user, done=True).count()
    total_pending = ChecklistItem.objects.filter(area__user=request.user, done=False).count()
    total_areas = Area.objects.filter(user=request.user).count()

    if selected_area_id:
        try:
            selected_area_id = int(selected_area_id)
            selected_area = Area.objects.get(id=selected_area_id, user=request.user)
            items = items.filter(area=selected_area)
        except (ValueError, Area.DoesNotExist):
            selected_area = None
            selected_area_id = None

    if query:
        items = items.filter(title__icontains=query)

    if status == "done":
        items = items.filter(done=True)
    elif status == "pending":
        items = items.filter(done=False)

    if order == "old":
        items = items.order_by("created_at")
    else:
        items = items.order_by("-created_at")

    paginator = Paginator(items, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "checklists/dashboard.html",
        {
            "areas": areas,
            "items": page_obj,
            "page_obj": page_obj,
            "paginator": paginator,
            "selected_area": selected_area,
            "selected_area_id": selected_area.id if selected_area else None,
            "item_form": ChecklistItemForm(user=request.user),
            "q": query,
            "status": status,
            "order": order,

            # NOVOS DADOS PARA OS CARDS
            "total_items": total_items,
            "total_done": total_done,
            "total_pending": total_pending,
            "total_areas": total_areas,
        },
    )


@login_required
def areas_manage(request):
    areas = Area.objects.filter(user=request.user).order_by("name")

    return render(
        request,
        "checklists/areas_manage.html",
        {
            "areas": areas,
            "area_form": AreaForm(),
        },
    )


@login_required
def area_create(request):
    if request.method == "POST":
        form = AreaForm(request.POST)
        if form.is_valid():
            area = form.save(commit=False)
            area.user = request.user
            area.save()
    return redirect("areas_manage")


@login_required
def area_edit(request, area_id):
    area = get_object_or_404(Area, id=area_id, user=request.user)

    if request.method == "POST":
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
    return redirect("areas_manage")


@login_required
def area_delete(request, area_id):
    area = get_object_or_404(Area, id=area_id, user=request.user)

    if request.method == "POST":
        area.delete()
    return redirect("areas_manage")


@login_required
def item_create(request):
    if request.method == "POST":
        form = ChecklistItemForm(request.POST, user=request.user)
        if form.is_valid():
            item = form.save(commit=False)

            if item.area.user != request.user:
                return HttpResponseForbidden("Você não tem permissão.")

            item.save()

            if request.POST.get("redirect_area"):
                return redirect(f"/?area={item.area.id}")

    return redirect("dashboard")


@login_required
def item_toggle(request, item_id):
    item = get_object_or_404(ChecklistItem, id=item_id)

    if item.area.user != request.user:
        return HttpResponseForbidden("Você não tem permissão.")

    if request.method == "POST":
        item.done = not item.done
        item.save()

    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def item_delete(request, item_id):
    item = get_object_or_404(ChecklistItem, id=item_id)

    if item.area.user != request.user:
        return HttpResponseForbidden("Você não tem permissão.")

    if request.method == "POST":
        item.delete()

    return redirect(request.META.get("HTTP_REFERER", "/"))
