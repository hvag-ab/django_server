from django.http import JsonResponse


async def test(request):
    uid = request.GET.get('uid','hvag')
    return JsonResponse({'myid':uid})

