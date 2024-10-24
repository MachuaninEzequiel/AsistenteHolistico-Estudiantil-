from django.db import IntegrityError
from django.shortcuts import redirect, render, get_object_or_404
# cuando ejecute esto me va a retornar un formulario, y tambien un formulario de autenticacion
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# usamos la clase proporcionada por django para crear un usuario
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from .models import UserProfile

# para facilitar la autenticacion y el logueo login va a encargarse de crear la cookie del usuario1
from django.contrib.auth import login, logout, authenticate, get_user

# para manejo de OpenAI
from django.http import JsonResponse
import openai

# Estres Academico
from .models import EstresAcademico
from django.contrib.auth.decorators import login_required
#from textblob import TextBlob
from django.contrib.auth import login as auth_login
from django.urls import reverse
import tensorflow as tf
#import tensorflow_text as text
#from transformers import BertTokenizer, TFBertForSequenceClassification
#import transformers
#from transformers import TFGPT2LMHeadModel

# Importa el modelo de lenguaje Bard

from django.http import HttpResponseRedirect

#Tokens
from .models import UserProfile, Product

#tiempo
from django.utils import timezone
from datetime import timedelta



def home(request):
    template_name = 'login.html'
    return render(request, 'login.html', {'template_name': template_name})


# -------------------------------------------------------------------------------
# parte autenticacion
# -------------------------------------------------------------------------------
# vista sign_up
# -------------------------------------------------------------------------------
def registrarse(request):
    template_name = 'registrarse.html'
    if request.method == 'GET':
        form = UserRegistrationForm()
        return render(request, 'registrarse.html', {'template_name': template_name,"form": form})
    else:
        form = UserRegistrationForm(request.POST)

        if form.is_valid() and form.cleaned_data["password1"] == form.cleaned_data["password2"]:
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()

            # Crea un UserProfile con el icono seleccionado
            UserProfile.objects.create(user=user, icon=form.cleaned_data["icon"])

            login(request, user)
            return redirect('dashboard')
        else:
            # Agrega este bloque para ver los errores en la consola
            print(form.errors)
            return render(request, 'registrarse.html', {'template_name': template_name,"form": form})


# -------------------------------------------------------------------------------
# login

def log_in(request):
    template_name = 'login.html'
    if request.method == 'GET':
        return render(request, 'login.html', {'template_name': template_name,"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'template_name': template_name,"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('dashboard')


# -------------------------------------------------------------------------------
# logout

def sign_out(request):
    logout(request)
    return redirect('log-in')



# -------------------------------------------------------------------------------
# OpenAI API contection

def interact_with_openai(request):
    # Llave de la API de OpenAI
    openai.api_key = ''

    # Ejemplo de texto de entrada
    input_text = "Quiero obtener ayuda con mis estudios."

    # Llamada a la API de OpenAI
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=input_text,
        max_tokens=150
    )

    # Obtener la respuesta generada por OpenAI
    generated_text = response['choices'][0]['text']

    return JsonResponse({'response': generated_text})

def openai_interaction_view(request):
    return render(request, 'openai_interaction.html')



# -------------------------------------------------------------------------------
#Estres Academico


#def ver_nivel_estres(request):
    estres_academico_lista = EstresAcademico.objects.filter(usuario=request.user)
    nuevo_nivel = estres_academico_lista.last().nivel_de_estres + 1 if estres_academico_lista.exists() else 1
    url = reverse('actualizar-nivel-estres', kwargs={'nuevo_nivel': nuevo_nivel})

    if request.method == 'POST':
        texto_a_analizar = request.POST.get('texto_a_analizar', '')
        emociones = analizar_sentimientos(texto_a_analizar)

        output , recomendacion = generar_recomendacion(texto_a_analizar, emociones)

        EstresAcademico.objects.create(
            usuario=request.user,
            nivel_de_estres=nuevo_nivel,
            emociones=emociones,
            descripcion=texto_a_analizar
        )

        # Incrementar los tokens del usuario por 10
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.tokens += 10
        user_profile.save()


        recomendacion_legible = recomendacion
        recomendacion_generada = tokenizer1.decode(output[0].numpy().tolist(), skip_special_tokens=True)
        print(recomendacion_legible)
        print(recomendacion_generada)

        return render(request, 'ver_nivel_estres.html', {
            'estres_academico_lista': estres_academico_lista,
            'nuevo_nivel': nuevo_nivel,
            'url': url,
            'recomendacion': recomendacion_generada  # Pasar la recomendación a la plantilla
        })

    return render(request, 'ver_nivel_estres.html', {
        'estres_academico_lista': estres_academico_lista,
        'nuevo_nivel': nuevo_nivel,
        'url': url,
    })




#model_name = 'nlptown/bert-base-multilingual-uncased-sentiment'
#tokenizer = BertTokenizer.from_pretrained(model_name)
#model = TFBertForSequenceClassification.from_pretrained(model_name)
#def analizar_sentimientos(texto):
    # Tokenizar el texto y darle formato para la entrada al modelo
    input_ids = tokenizer.encode(texto, return_tensors='tf')
    
    # Obtener la predicción del modelo
    logits = model(input_ids)[0]
    
    # Obtener la clase predicha
    predicted_class = tf.argmax(logits, axis=1).numpy()[0]
    
    # Mapear la clase predicha a una etiqueta de sentimiento
    sentimientos = {0: 'Muy Negativo', 1: 'Negativo', 2: 'Neutral', 3: 'Positivo', 4: 'Muy Positivo'}
    
    return sentimientos[predicted_class]

#tokenizer1 = transformers.GPT2Tokenizer.from_pretrained('gpt2-xl')
#modelR = transformers.TFGPT2LMHeadModel.from_pretrained('gpt2-xl')
#def generar_recomendacion(texto, sentimiento):

    recomendacion = ''

    input_text = f"The user has expressed: {texto}\nAdvice:"

    input_ids = tokenizer1.encode(input_text, return_tensors='tf', max_length=200, truncation=True)

    attention_mask = tf.ones_like(input_ids)

    pad_token_id = tokenizer1.eos_token_id

    # Generar el texto
    output = modelR.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=200,
        temperature=0.8,
        top_k=50,  # O elimina este parámetro
        do_sample=True,
        pad_token_id=pad_token_id,
        num_return_sequences=1
    )

    # Obtener la recomendación
    if sentimiento == 'Muy Negativo':
        recomendacion = 'Siento mucho que te sientas así. ¿Hay algo que pueda hacer para ayudarte?'
    elif sentimiento == 'Negativo':
        recomendacion = 'Espero que las cosas mejoren pronto.'
    elif sentimiento == 'Neutral':
        recomendacion = 'No tengo mucho que decir sobre eso.'
    elif sentimiento == 'Positivo':
        recomendacion = '¡Me alegro de que estés contento!'
    elif sentimiento == 'Muy Positivo':
        recomendacion = '¡Eso es genial!'

    return output, recomendacion      




#def actualizar_nivel_estres(request, nuevo_nivel):
    print("DEBUG: Entering actualizar_nivel_estres")
    print(f"DEBUG: request.user type: {type(request.user)}")
    print(f"DEBUG: request.user value: {request.user}")

    if not request.user.is_authenticated:
        return redirect('login')

    # Obtén el usuario actual de la lista de usuarios usando el identificador del usuario autenticado
    usuario_actual = get_user(request)

    if request.method == 'POST':
        # Obtener el texto del estudiante (ajusta esto según tu aplicación)
        texto_del_estudiante = request.POST.get('texto_del_estudiante', '')

        # Analizar emociones usando textblob
        emociones = analizar_sentimientos(texto_del_estudiante)
        
        # Almacenar el nivel de estrés y las emociones en la base de datos
        EstresAcademico.objects.create(
            usuario=usuario_actual,
            nivel_de_estres=nuevo_nivel,
            emociones=emociones
        )
        return redirect('ver-nivel-estres')

    # En caso de que la solicitud no sea POST, podrías realizar alguna otra lógica aquí
    return render(request, 'actualizar_nivel_estres.html', {'nuevo_nivel': nuevo_nivel})



# -------------------------------------------------------------------------------
#Tokens

def daily_reward(request):
    user_profile = UserProfile.objects.get(user=request.user)

    # Verificar si ha pasado al menos una hora desde la última recompensa
    if timezone.now() - user_profile.created_at >= timedelta(hours=1):
        user_profile.tokens += 10  # Otorgar 10 tokens
        user_profile.created_at = timezone.now()  # Actualizar el tiempo de última recompensa
        user_profile.save()

    return redirect('dashboard')


def user_tokens(request):
    user_profile = UserProfile.objects.get(user=request.user)
    purchased_products = user_profile.purchased_products.all()
    return render(request, 'dashboard.html', {'tokens': user_profile.tokens, 'purchased_products': purchased_products})

def redeem_reward(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.tokens >= product.price:
        user_profile.tokens -= product.price
        user_profile.purchased_products.add(product)
        user_profile.save()
        return redirect('store')
    else:
        return render(request, 'insufficient_tokens.html')



# -------------------------------------------------------------------------------
#Tienda
def store(request):
    template_name = 'store.html'
    user = request.user
    products = Product.objects.all()
    return render(request, 'store.html', {'template_name': template_name,'user': user, 'products': products})

def dashboard(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Si no existe el perfil, crea uno nuevo
        user_profile = UserProfile.objects.create(user=request.user)

    purchased_products = user_profile.purchased_products.all()
    print("Purchased Products:", purchased_products)
    return render(request, 'dashboard.html', {'user': request.user, 'tokens': user_profile.tokens, 'purchased_products': purchased_products})


def insufficient_tokens(request):
    return render(request, 'insufficient_tokens.html')



def user_profile(request):
    # Obtener el perfil del usuario actual
    user_profile = UserProfile.objects.get(user=request.user)

    return render(request, 'user_profile.html', {'user_profile': user_profile})


def agregar_producto_avatar(request):
    if request.method == 'POST':
        # Obtener el ID del producto desde el formulario
        product_id = request.POST.get('product_id')
        
        # Buscar el producto en la base de datos
        product = get_object_or_404(Product, pk=product_id)
        
        # Obtener el perfil de usuario actual
        user_profile = UserProfile.objects.get(user=request.user)
        
        # Determinar el tipo de producto y actualizar el avatar del usuario
        if product.product_type == 'background':
            user_profile.selected_background = product.gif
        elif product.product_type == 'cabeza':
            user_profile.selected_head = product.gif
        elif product.product_type == 'torso':
            user_profile.selected_torso = product.gif
        elif product.product_type == 'pierna':
            user_profile.selected_legs = product.gif
        elif product.product_type == 'pie':
            user_profile.selected_feet = product.gif
        
        # Guardar los cambios en el perfil del usuario
        user_profile.save()
        
        # Redireccionar a la página del dashboard
        return redirect('dashboard')
