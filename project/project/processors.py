from index.models import Poster
def PosterContextProcessors(request):
	post = Poster.objects.all().count()
	return {'context_post': post}