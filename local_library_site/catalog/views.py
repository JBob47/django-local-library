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

	# #Count genres that contain Fiction (case insensitive)
	# num_fiction_genres = Genre.objects.filter(name__icontains='fiction').count()

	# #Count genres that contain Fiction (case insensitive)
	# num_wayward_books = Book.objects.filter(title__icontains='wayward').count()


	# Number of visits to this view, as counted in the session variable.
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1

	context = {
		'num_books': num_books,
		'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,
		# 'num_fiction_genres': num_fiction_genres,
		# 'num_wayward_books': num_wayward_books,
		'num_visits' : num_visits,
	}

	# Render the HTML template index.html with the data in the context variable
	return render(request, 'index.html', context=context)



from django.views import generic

class BookListView(generic.ListView):
	model = Book
	paginate_by = 10
	# context_object_name = 'my_book_list' #your name for ListView
	# queryset = Book.objects.filter(title__icontains='war')[:5] #Get 5 books containing the title war
	# template_name = 'books/my_arbitrary_template_name_list.html' #Specify your own template name/location


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
	model = Author
	

class AuthorDetailView(generic.DetailView):
	model = Author
	

