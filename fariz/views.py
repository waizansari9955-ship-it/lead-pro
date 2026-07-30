from django.shortcuts import render


def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def products(request):
    return render(request, 'products.html')

def contact(request):
    success = False
    error_msg = None
    
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        
        try:
            from firebase_admin import firestore
            db = firestore.client()
            db.collection("messages").add({
                "name": name,
                "email": email,
                "message": message,
                "created_at": firestore.SERVER_TIMESTAMP
            })
            success = True
        except Exception as e:
            error_msg = str(e)
            
    return render(request, 'contact.html', {'success': success, 'error_msg': error_msg})





def blog(request):
    return render(request, 'blog.html')

def faq(request):
    return render(request, 'faq.html')

def lead_tool(request):
    return render(request, 'lead_tool.html')

def guide(request):
    return render(request, 'guide.html')

def crm(request):
    return render(request, 'crm.html')


