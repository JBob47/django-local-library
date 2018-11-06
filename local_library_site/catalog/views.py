from django.shortcuts import render

from catalog.models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin


@login_required
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

class BookListView(LoginRequiredMixin, generic.ListView):
	model = Book
	paginate_by = 10
	# context_object_name = 'my_book_list' #your name for ListView
	# queryset = Book.objects.filter(title__icontains='war')[:5] #Get 5 books containing the title war
	# template_name = 'books/my_arbitrary_template_name_list.html' #Specify your own template name/location


class BookDetailView(LoginRequiredMixin,generic.DetailView):
    model = Book


class AuthorListView(LoginRequiredMixin, generic.ListView):
	model = Author
	

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
	model = Author


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksLibrarianListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""

    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_librarian.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
    
    
	

