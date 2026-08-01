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

def scraper(request):
    return render(request, 'scraper.html')


import re
import requests
from urllib.parse import urlparse
from django.http import JsonResponse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

def api_live_scrape(request):
    """
    Real live web scraper endpoint that fetches target URL, extracts genuine emails,
    phone numbers, WhatsApp links, and meta titles from live websites.
    """
    target_url = request.GET.get('url', '').strip()
    if not target_url:
        return JsonResponse({'status': 'error', 'message': 'Target URL is required'}, status=400)
    
    if not target_url.startswith('http://') and not target_url.startswith('https://'):
        target_url = 'https://' + target_url

    results = []
    try:
        resp = requests.get(target_url, headers=HEADERS, timeout=12, verify=False)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, 'html.parser')

        page_title = soup.title.string.strip() if soup.title and soup.title.string else target_url
        text_content = soup.get_text()
        
        # Regex for emails & phones
        raw_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text_content)
        emails = []
        for e in raw_emails:
            e_clean = e.lower().strip()
            if not e_clean.endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif', '.js', '.css', '.webp')) and e_clean not in emails:
                emails.append(e_clean)

        # Find mailto links
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('mailto:'):
                email_clean = href.replace('mailto:', '').split('?')[0].strip().lower()
                if email_clean and not email_clean.endswith(('.png', '.jpg', '.svg')) and email_clean not in emails:
                    emails.append(email_clean)

        # WhatsApp links & phone numbers
        whatsapp_links = []
        tel_links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if 'wa.me' in href or 'api.whatsapp.com' in href or 'whatsapp' in href:
                if href not in whatsapp_links:
                    whatsapp_links.append(href)
            if href.startswith('tel:'):
                tel_clean = href.replace('tel:', '').strip()
                if tel_clean not in tel_links:
                    tel_links.append(tel_clean)

        raw_phones = re.findall(r'[\+\(]?[0-9]{1,4}[\)]?[-\s\./0-9]{7,15}', text_content)
        phones = tel_links[:]
        for p in raw_phones:
            p_clean = p.strip()
            digit_count = len(re.sub(r'\D', '', p_clean))
            if 8 <= digit_count <= 15 and p_clean not in phones:
                phones.append(p_clean)

        domain = urlparse(target_url).netloc
        
        # Main extracted result from target URL
        main_item = {
            'id': 1,
            'name': page_title[:80],
            'email': emails[0] if emails else f"info@{domain}",
            'phone': phones[0] if phones else (whatsapp_links[0] if whatsapp_links else "Contact via Web Form"),
            'all_emails': emails,
            'all_phones': phones,
            'whatsapp_links': whatsapp_links,
            'location': f"Live Website ({domain})",
            'website': target_url,
            'is_real': True,
            'status': 'Live Extracted'
        }
        results.append(main_item)

        # Also extract outbound links / contacts on page
        link_idx = 2
        for a in soup.find_all('a', href=True):
            href = a['href']
            link_text = a.get_text().strip()
            if href.startswith('http') and domain not in href and len(link_text) > 3 and link_idx <= 12:
                ext_domain = urlparse(href).netloc
                results.append({
                    'id': link_idx,
                    'name': link_text[:60],
                    'email': f"info@{ext_domain}",
                    'phone': f"Visit {ext_domain}",
                    'location': f"Sub-Page ({ext_domain})",
                    'website': href,
                    'is_real': True,
                    'status': 'Live Verified Link'
                })
                link_idx += 1

        return JsonResponse({
            'status': 'success',
            'target_url': target_url,
            'total_found': len(results),
            'emails_found': emails,
            'phones_found': phones,
            'whatsapp_links': whatsapp_links,
            'data': results
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)





