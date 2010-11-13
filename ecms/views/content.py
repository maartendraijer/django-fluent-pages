"""
A collection of views to display the CMS content
"""
from django.http import HttpResponse
from ecms.models import CmsObject
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from django.utils.functional import LazyObject, SimpleLazyObject


def cmspage(request, path):
    """
    Display a CMS page.
    """
    if path is None:
        path = request.path

    # Get current page,
    # allow template tags to track the current page.
    page = CmsObject.objects.get_for_path_or_404(path)
    request._ecms_current_page = page

    # Render the template
    context = {
        'ecms_page': page,
        'ecms_main_content': SimpleLazyObject(lambda: mark_safe(page.main_page_item))
    }

    return render_to_response("ecms/cmspage.html", context, context_instance=RequestContext(request))