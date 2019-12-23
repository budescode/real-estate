from index.models import Poster, saveReport
def PosterContextProcessors(request):
	post = Poster.objects.all().count()
	return {'context_post': post}

def saveReportProcessor(request):
    try:
        context_userreport = saveReport.objects.filter(user=request.user, seen=False).count()
    except:
        context_userreport = 0
    return {'context_userreport': context_userreport}