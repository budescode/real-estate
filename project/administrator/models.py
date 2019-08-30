from django.db import models

class CountryDetails(models.Model):
	postcode = models.CharField(max_length=100, default='')
	suburb = models.CharField(max_length=100, default='')
	state =models.CharField(max_length=100, default='')
	dc = models.CharField(max_length=100, default='')
	detail_type = models.CharField(max_length=100, default='')
	lat = models.CharField(max_length=100, default='')
	ion = models.CharField(max_length=100, default='')

	def __str__(self):
		return self.postcode


def upload_csv(request):
	if request.method == 'GET':
		return render(request, 'Administrator/upload_csv.html')
	csv_file = request.FILES['file']
	if not csv_file.name.endswith('.csv'):
		messages.error(request, "This is not a csv file")
	data_set = csv_file.read().decode('UTF-8')
	io_string = io.StringIO(data_set)
	next(io_string)
	for column in csv.reader(io_string, delimiter=',', quotechar="|"):
		print(column[0], column[1], column[2], column[3], column[4], column[5], column[6])
		_, created = CountryDetails.objects.update_or_create(
			postcode = column[0],
			suburb = column[1],
			state = column[2],
			dc = column[3],
			detail_type = column[4],
			lat = column[5],
			ion = column[6],
			image = column[44],
			image1 = column[45],
			plan = column[46],
			)
	context = {}
	return render(request, 'Administrator/upload_csv.html', context)