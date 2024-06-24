from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.core.paginator import Paginator
import requests
from cart.cart import Cart
from django.http import HttpResponse

@login_required()
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("goods_url")


@login_required()
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required()
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required()
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required()
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required()
def cart_detail(request):
    cart = Cart(request)

    total_price = sum(item['quantity'] * int(item['price']) for item in cart.cart.values())
    total_quantity = sum(item['quantity'] for item in cart.cart.values())


    context = {
        'cart': cart.cart,
        'total_price': total_price,
        'total_quantity': total_quantity
    }

    return render(request, 'cart_detail.html', context)

# Create your views here.
def Main(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        request.session['language'] = language
    else:
        request.session['language'] = 'en'
    
    category = Category.objects.all()
    context = {
        'Category': category,
        'language': 'main_url',
        }

    return render(request, 'main.html', context)


@login_required
def ProfileView(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    phone = profile.phone
    number = phone.replace('+7', '8')

    context = {'Profile': profile,
                'Phone': number}
    return render(request, 'Profile/profile_view.html', context)


def ProfileEdit(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'GET':
        phone = profile.phone
        number = phone.replace('+7', '8')

        context = {'Profile': profile,
                   'Phone': number}
        return render(request, 'Profile/profile_edit.html', context)
    else:
        username = request.POST.get('username_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone_name')
        email = request.POST.get('email_name')
        if username:
            request.user.username = username
            request.user.save()
        if phone:
            profile.phone = phone
        if first_name:
            profile.first_name = first_name
        if last_name:
            profile.last_name = last_name
        if email:
            profile.email = email
        if 'image_name' in request.FILES:
            image = request.FILES['image_name']
            profile.image = image
        profile.save()
        return redirect('profile_view_url')
    

def ProfileDelete(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    context = {'Profile': profile}

    if request.method == 'POST':
        User.delete(user)
        profile.delete()
        return redirect('logout_url')
    
    return render(request, 'Profile/profile_delete.html', context)


def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'This user already exists.'})
        elif User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error_message': 'This user already exists.'})
        else:
            if password1 != password2:
                return render(request, 'register.html', {'error_message': 'Passwords do not match.'})

            user = User.objects.create_user(username=username, password=password1, email=email)
            user.save()

            profile = Profile.objects.create(user=user, email=email)
            profile.save()

            return redirect('login_url')

    return render(request, 'register.html')


def ForecastView(request):
    if request.method == 'GET':
        return render(request, 'forecast.html')
    else:
        city = request.POST.get('city_name')
        
        params = {
            'q': f'{city}',
            'appid': '73c9fcbae173d204f7d9e736e5d94c6b'
        }

        response = requests.get('http://api.openweathermap.org/geo/1.0/direct', params=params)
        
        if response.json() == []:
            style = {
                'container': '400px',
                'weatherBoxDetails': 'none',
                'error404': 'block',
            }

            return render(request, 'forecast.html', style)
        else:
            params = {
                'lat': response.json()[0]['lat'],
                'lon': response.json()[0]['lon'],
                'appid': '73c9fcbae173d204f7d9e736e5d94c6b'
            }

            response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params)

            if response.json()['weather'][0]['main'] == 'Clear':
                img = '/media/weather/clear.png'
            elif response.json()['weather'][0]['main'] == 'Rain':
                img = '/media/weather/snow.png'
            elif response.json()['weather'][0]['main'] == 'Snow':
                img = '/media/weather/cloud.png'
            elif response.json()['weather'][0]['main'] == 'Clouds':
                img = '/media/weather/rain.png'
            elif response.json()['weather'][0]['main'] == 'Haze':
                img = '/media/weather/mist.png'
            else:
                img = ''

            context = {
                'temp': round(response.json()['main']['temp'] - 273.15),
                'description': response.json()['weather'][0]['description'],
                'humidity': response.json()['main']['humidity'],
                'wind': round(response.json()['wind']['speed']),
                # 'sunrice': datetime.fromtimestamp(response.json()['sys']['sunrise']),
                # 'sunset': datetime.fromtimestamp(response.json()['sys']['sunset']),

                'image': img,
                'weatherBoxDetails': '',
                'container': '590px',
                }
            return render(request, 'forecast.html', context)


def ShopAlmaty(request):
    category = Category.objects.all()
    context = {
        'Category': category,
        }
    
    return render(request, 'shop.html', context)
    


def Search(request):
    if request.GET.get('search_input'):
        category = Category.objects.all()
        all_goods=Product.objects.filter(name__icontains=request.GET.get('search_input'))
    
        paginator = Paginator(all_goods, 6)
        page_number = request.GET.get('page')
        goods_page = paginator.get_page(page_number)

        requesthgds = request.GET.get('search_input')

        context = {
            'Category': category,
            'goods': goods_page,
            'request': requesthgds
            }

        return render(request, 'search.html', context)
    

def GoodByCategory(request, category_pk):
    category = Category.objects.all()
    all_goods = Product.objects.filter(category=category_pk)
    
    paginator = Paginator(all_goods, 6)
    page_number = request.GET.get('page')
    goods_page = paginator.get_page(page_number)

    context = {
        'Category': category,
        'goods': goods_page
        }
    return render(request, 'goods_by_category.html', context)
    

def GoodDetail(request, good_pk):
    item = get_object_or_404(Product, pk=good_pk)
    category = Category.objects.all()
    related_items = Product.objects.filter(category=item.category).exclude(pk=good_pk)[0:3]

    if request.method == 'POST':
        Reviewform = ReviewForm(request.POST)
        Replyform = ReplyForm(request.POST)

        if Reviewform.is_valid():
            review = Reviewform.save(commit=False)
            review.product = item
            review.user = request.user
            # review.save()
            return redirect('good_detail_url', pk=good_pk)
        if Replyform.is_valid():
            review = Review.objects.get(id=request.POST.get('review_id'))
            reply = Replyform.save(commit=False)
            reply.user = request.user
            reply.save()
            review.replies.add(reply)
            review.save()
            return redirect('good_detail_url', pk=good_pk)
        return redirect('good_detail_url', pk=good_pk)
    else:
        Reviewform = ReviewForm()
        Replyform = ReplyForm()

        context = {
            'item': item,
            'Category': category,
            'related_items': related_items,
            'review_form': Reviewform,
            'reply_form': Replyform,
        }

        return render(request, 'good_detail.html', context)
    

def Goods(request):
    category = Category.objects.all()
    all_goods = Product.objects.all()
    
    paginator = Paginator(all_goods, 9)
    page_number = request.GET.get('page')
    goods_page = paginator.get_page(page_number)

    context = {
        'Category': category,
        'goods': goods_page,
        }
    
    return render(request, 'goods.html', context)


def NewProduct(request):
    profile = Profile.objects.get(user=request.user)

    if profile.status=='admin' or profile.status=='seller':
        if request.method == 'GET':
            category = Category.objects.all()

            context = {
                'Category': category
            }
            return render(request, 'new_product.html', context)
        else:
            name=request.POST.get('name_input')
            description=request.POST.get('description_input')
            price=request.POST.get('price_input')
            caategory=request.POST.get('category_select')

            category=Category.objects.get(pk=caategory)

            if 'img_input' in request.FILES:
                image = request.FILES['img_input']
                
            new_product = Product(name=name, description=description, price=price, image=image, category=category, seller=request.user)

            new_product.save()

            return redirect('shop_url')
    else:
        return redirect('profile_view_url')


def BoughProduct(request):
    cart = Cart(request)

    basket = Basket(user=request.user)
    basket.save()

    for item_id, item_info in cart.cart.items():
        product = Product.objects.get(id=item_id)
        quantity = item_info['quantity']
        price = item_info['price']

        boughproduct = BoughtProducts(product=product, quantity=quantity, price=price)
        boughproduct.save()

        basket.products.add(boughproduct)
        basket.save()
    
    cart.clear()
    return redirect("main_url")
    

def History(request):
    checks = Basket.objects.filter(user=request.user).order_by('-created_timestamp')

    for item in checks:
        item.total_sum = 0
        item.city = ''
        
        for product in item.products.all():
            product.total_price = product.quantity * product.product.price
            item.total_sum += product.total_price

            response = requests.get('https://api.ipify.org?format=json')
            ip_data = response.json()

            query = ip_data['ip']

            ip_api = requests.get(f'http://ip-api.com/json/{query}')

            product.city = ip_api.json()['city']
            item.city += product.city

    context = {
        'checks': checks,
    }

    return render(request, 'history.html', context)


def Geolocation(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        request.session['language'] = language
    else:
        request.session['language'] = 'en'

    response = requests.get('https://api.ipify.org?format=json')
    ip_data = response.json()

    query = ip_data['ip']

    ip_api = requests.get(f'http://ip-api.com/json/{query}')

    context = {
        'country': ip_api.json()['country'],
        'countryCode': ip_api.json()['countryCode'],
        'region': ip_api.json()['region'],
        'city': ip_api.json()['city'],
        'lat': ip_api.json()['lat'],
        'lon': ip_api.json()['lon'],
        'timezone': ip_api.json()['timezone'],
        'isp': ip_api.json()['isp'],
        'API': ip_api.json()['query'],
    }
    # isp = internet service provider

    return render(request, 'geolocation.html', context)


def StatusSeller(request):
    if request.method == 'POST':
        profile = Profile.objects.filter(user=request.user)

        for item in profile:
            item.status = 'seller'
            item.save()

        return redirect('profile_view_url')
    else:
        return render(request, 'status_seller.html')


@login_required
def newConversation(request, item_pk):
    print('1=============')
    item = get_object_or_404(Product, pk=item_pk)

    print('2=============')
    if item.seller == request.user:
        return redirect('good_detail_url', good_pk=item_pk) 

    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    print('3=============')
    if conversations:
        return redirect('detail', pk=conversations.first().id)

    print('4=============')
    if request.method == 'POST':
        print('5=============')
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.seller)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('good_detail_url', good_pk=item_pk)
    else:
        print('6=============')
        form = ConversationMessageForm()

        return render(request, 'new.html', {
            'item': item,
            'form': form
        })


@login_required
def chats(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'chats.html', {
        'conversations': conversations
    })

@login_required
def detail(request, pk):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'messagedetail.html', {
        'conversations': conversations,
        'conversation': conversation,
        'form': form,
    })
    

def ErrorPage(request):
    return render(request, 'errorpage.html', status=404)