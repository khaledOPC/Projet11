# Importation des modules nécessaires de Django et autres bibliothèques
from django.shortcuts import render, redirect
from django import forms
import requests
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Product
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Favorite, Product
from django.contrib import messages  # Pour afficher les messages d'erreur
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.auth.forms import PasswordResetForm
from .forms import UserRegistrationForm



def home(request):
    """
    Vue pour la page d'accueil.
    Affiche simplement la page d'accueil lorsqu'aucune action supplémentaire n'est nécessaire.
    """
    return render(request, 'home.html',)


def search(request):
    """
    Vue pour la recherche d'un produit.
    Exécute une recherche basée sur la requête de l'utilisateur et affiche le produit principal avec 5 substituts.
    """
    query = request.GET.get('query')  # Extraction de la requête de recherche de l'utilisateur
    if query:
        product = Product.objects.filter(name__icontains=query).first()  # Recherche du premier produit correspondant
    else:
        product = None  # Si aucune requête n'est fournie, ne renvoie aucun produit

    # Récupération des substituts s'il y a un produit trouvé
    substitutes = []
    if product and product.nutriscore is not None and product.novascore is not None:
        substitutes = Product.objects.filter(category=product.category).exclude(id=product.id).filter(
            Q(nutriscore__lt=product.nutriscore) | Q(novascore__lt=product.novascore)).order_by('nutriscore', 'novascore')[:8]
    
    return render(request, 'search.html', {'product': product, 'substitutes': substitutes})


@login_required
def Connected(request):
    """
    Vue pour la page lorsque l'utilisateur est connecté.    
    Sert à afficher une page spécifique ou des informations spécifiques lorsque l'utilisateur est connecté.
    """
    return render(request, 'Connected.html')


def product_detail(request, product_id):
    """
    Vue pour afficher le détail d'un produit spécifique.
    Renvoie les détails d'un produit spécifique basé sur son ID.
    """
    product = get_object_or_404(Product, id=product_id)  # Récupération du produit basé sur l'ID
    if product.nutrition_data:  # Si le produit a des données nutritionnelles
        nutrition = product.nutrition_data  # Récupération des données nutritionnelles
    else:
        nutrition = None  # Si aucune donnée nutritionnelle, assignation à None
    context = {
        'product': product,  # Assignation du produit au contexte
        'nutrition_data': nutrition,  # Assignation des données nutritionnelles au contexte
        'product_url': product.url  # Ajout de l'URL d'Open Food Facts au contexte
    }
    return render(request, 'product_detail.html', context)



def product_substitutes(request, product_id):
    """
    Vue pour trouver et afficher les substituts d'un produit spécifique.
    Recherche des produits substituts basés sur les scores nutritionnels et la catégorie, puis les renvoie.
    """
    product = get_object_or_404(Product, id=product_id)  # Récupération du produit basé sur l'ID
    if product.nutriscore is None or product.novascore is None:  # Si le produit n'a pas de scores nutritionnels
        context = {'substitutes': []}  # Assignation de substituts vides au contexte
        return render(request, 'substitutes.html', context)  # Renvoie la page avec aucun substitut
    substitutes = Product.objects.filter(category=product.category).exclude(id=product_id).filter(
        Q(nutriscore__lt=product.nutriscore) | Q(novascore__lt=product.novascore)).order_by('nutriscore','novascore')[:10]  
    # Recherche de substituts et ordonnancement par scores
    context = {'substitutes': substitutes}  # Assignation des substituts au contexte
    return render(request, 'substitutes.html', context)  # Renvoie la page avec les substituts trouvés





# Vue pour traiter le formulaire sur la page d'accueil
def button(request):
    """
    Gère le formulaire sur la page d'accueil.
    Si le formulaire est valide, traite les données du formulaire et effectue les actions nécessaires.
    """
    if request.method == 'POST':
        formulaire = MonFormulaire(request.POST)
        if formulaire.is_valid():
            champ_texte = formulaire.cleaned_data['champ_texte']
    else:
        formulaire = MonFormulaire()
    return render(request, 'home.html', {'formulaire': formulaire})

# Vue pour gérer la connexion des utilisateurs
def resultat(request):
    """
    Gère la connexion des utilisateurs.
    Authentifie les utilisateurs basé sur le nom d'utilisateur et le mot de passe fournis, 
    et si l'authentification réussit, l'utilisateur est redirigé vers la page d'accueil.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'resultat.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)  # Utilisation du nouveau formulaire
        if form.is_valid():
            form.save()  # Création et sauvegarde de l'utilisateur, y compris l'email
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)  # Authentification automatique
            login(request, user)  # Connexion automatique après inscription
            return redirect('home')  # Redirection vers la page d'accueil
    else:
        form = UserRegistrationForm()

    return render(request, 'signup.html', {'form': form})
 

def profile(request):
    return render(request, 'profile.html')


@login_required
def add_to_favorites(request, product_id):
    """
    Vue pour ajouter un produit aux favoris d'un utilisateur.
    """
    product = get_object_or_404(Product, id=product_id)
    # On vérifie que le produit n'est pas déjà dans les favoris de cet utilisateur
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, f"Le produit {product.name} a été ajouté à vos favoris.")
    else:
        messages.info(request, f"Le produit {product.name} est déjà dans vos favoris.")
    return redirect('favorites')



@login_required
def favorites(request):
    """
    Affiche les produits favoris de l'utilisateur connecté.
    """
    user_favorites = Favorite.objects.filter(user=request.user)  # Affiche les favoris uniquement pour l'utilisateur connecté
    return render(request, 'favorites.html', {'favorites': user_favorites})


@login_required
def remove_favorite(request, product_id):
    """
    Supprime un produit des favoris de l'utilisateur connecté.
    """

    product = get_object_or_404(Product, id=product_id)
    favorite = Favorite.objects.filter(user=request.user, product=product)
    if favorite.exists():
        favorite.delete()
        messages.success(request, f" {request.user.username} Le produit {product.name} a été retiré de vos favoris.")
    return redirect('favorites')
