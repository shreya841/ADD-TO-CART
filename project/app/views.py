import razorpay
from django.shortcuts import render
from .models import cart , Product
from .forms import cartform
from django.conf import settings


from django.views.decorators.csrf import csrf_exempt


def dashboard(request):
    if request.method == 'POST':
        form =cartform(request.POST,request.FILES)
        if form.is_valid():
                  form.save()
                  context={}
                  context['form'] =cartform
                  context['msg'] = "registration succesful"
                  card_data = cart.objects.all()
                  context['card_data'] = card_data
                  return render(request,'dashboard.html',context)

    context={}
    context['form'] =cartform
    context['msg'] = "Welcome to registration page"
    card_data = cart.objects.all()
    context['card_data'] = card_data
    return render(request,'dashboard.html',context)
def show(request):
            
            data=   cart.objects.all()
            return render(request,'cart.html',{'data':data , 'media_url':settings.MEDIA_URL})    
def addtocart(request,pk):
        
        addtocart= request.session.get('addtocart',[])
        
        addtocart.append(pk) 
        request.session['addtocart']=addtocart 
        # print(addtocart) 
        context={}
        card_data = cart.objects.all()
        context['card_data'] = card_data
        return render(request,'dashboard.html',context)

def cartss(request):
      addtocard= request.session.get('addtocart')
      cardDetail=[]
      TotalAmount=0
      for i in addtocard:
             data= cart.objects.get(id=i)
             detail={
                    'id':data.id,
                    'name': data.name,
                    'description':data.description,
                    'price' : data.price,
                    'Image' : data.Image
             }
             TotalAmount=+data.price
             cardDetail.append(detail)
    #   print(cardDetail,"sumit")
      return render(request,'cart.html',{'data': cardDetail, 'media_url':settings.MEDIA_URL,'TotalAmount':TotalAmount})

def delete(request,pk):
    addtocart = request.session.get('addtocart')
    addtocart.remove(pk)
    request.session['addtocart'] = addtocart

    addtocart = request.session.get('addtocart')
    # print(addtocart)
    Carddetails = []
    TotalAmount=0
    for i in addtocart:
        data = cart.objects.get(id=i)
        cont = {
            'id':data.id,
            'name': data.name,
            'description':data.description,
            'price' : data.price,
            'Image' : data.Image
        }
        TotalAmount=+data.price
        Carddetails.append(cont)
    return render(request,'cart.html',{'data': Carddetails,'media_url':settings.MEDIA_URL, 'TotalAmount': TotalAmount})
             
def payment(request):
    global payment
    if request.method=="POST":
        # amount in paisa
        # print("sumii",request.POST.get('amount'))
        amount = int(request.POST.get('amount'))* 100
        
        client = razorpay.Client(auth =("rzp_test_p1r1Cd4QBQtkIE" , "J7xWG0KC71ernEQqpkPy3B82"))
        # create order
        
        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        # print(payment)
        product = Product.objects.create( amount =amount , order_id = payment['id'])
        addtocard= request.session.get('addtocart')
        cardDetail=[]
        TotalAmount=0
        for i in addtocard:
                data= cart.objects.get(id=i)
                detail={
                        'id':data.id,
                        'name': data.name,
                        'description':data.description,
                        'price' : data.price,
                        'Image' : data.Image
                }
                TotalAmount=+data.price
                cardDetail.append(detail)
        # print(cardDetail,"sumit")
        return render(request,'cart.html',{'data': cardDetail, 'media_url':settings.MEDIA_URL,'TotalAmount':TotalAmount,'payment':payment})
        # return render(request,'cart.html',{'key':alldata,'amount':total,'payment':payment})
    
@csrf_exempt
def payment_status(request):
       global response
       if request.method=="POST": 
        response = request.POST
        # print(response) #  
        # print(payment)

        razorpay_data = {
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_signature': response['razorpay_signature']
        }
        print(razorpay_data)
        # client instance
        client = razorpay.Client(auth =("rzp_test_p1r1Cd4QBQtkIE" , "J7xWG0KC71ernEQqpkPy3B82"))
      
        status = client.utility.verify_payment_signature(razorpay_data)
        if status == True:
            product = Product.objects.get(order_id=response['razorpay_order_id'])
            product.razorpay_payment_id = response['razorpay_payment_id']
            product.paid = True
            product.save()
            Product.objects.create(   
                razorpay_payment_id = response ['razorpay_payment_id'])
            return render(request, 'success.html', {'status': True})
        else:
                    return render(request, 'success.html', {'status': False})
                