from django.shortcuts import render

from catalog.models import Book, Author, BookInstance, Genre

def index(request):
	"""View function for home page of site."""

	#Generate counts of some of the main objects

	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()

	#Available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()

	#The 'all()' is implied by default
	num_authors = Author.objects.count()

	#Count genres that contain Fiction (case insensitive)
	num_fiction_genres = Genre.objects.filter(name__icontains='fiction').count()

	#Count genres that contain Fiction (case insensitive)
	num_wayward_books = Book.objects.filter(title__icontains='wayward').count()

	context = {
		'num_books': num_books,
		'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,
		'num_fiction_genres': num_fiction_genres,
		'num_wayward_books': num_wayward_books,
	}

	# Render the HTML template index.html with the data in the context variable
	return render(request, 'index.html', context=context)



