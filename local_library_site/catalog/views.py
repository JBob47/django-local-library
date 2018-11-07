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
    
    

import datetime

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        book_renewal_form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if book_renewal_form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': book_renewal_form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)
