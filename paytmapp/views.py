from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from .Checksum import generate_checksum,verify_checksum
import random
import string

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
# Create your views here.
MERCHANT_KEY = 'PILUffPCU0CRF3XB'
def index(request):
    # data = {'hello':'hi'}
    if request.method=='POST':
        data_dct = {
            'MID':'NBBXvN49759964206512',
            'ORDER_ID':randomString(),
            'TXN_AMOUNT':'152',
            'CUST_ID':'acfff@paytm.com',
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'DEFAULT',
            'CHANNEL_ID':'WEB',
            'CALLBACK_URL':'http://test-biotechconf.tk/status/',
        }
        data_dct['CHECKSUMHASH'] = generate_checksum(data_dct,MERCHANT_KEY)
        return render(request,'redirect.html',{'datas':data_dct})

    return render(request,'index.html')

@csrf_exempt
def status(request):
    response_dict = {}
    for i in request.POST.keys():
        response_dict[i] = request.POST[i]
        if i == 'CHECKSUMHASH':
            checksum = request.POST[i]
    verify = verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            dict = {'status':'ok'}
        else:
            dict = {'status' : 'not ok bcz :'+ response_dict['RESPMSG']}
    return render(request,'test.html',dict)
    # return render(request,'test.html',{'hello':'hi'})
