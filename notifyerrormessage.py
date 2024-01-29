import traceback
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import requests
import json
from django.urls import reverse
from main.constants import urls
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse,JsonResponse
from base64 import b64encode
from restapi.models import FpUserLog,User
from django.db import connection
from restapi.common_func import commonfunc
from .common_reports import common
# from skpy import Skype
from main.constants import urls

class skype_error_alert():
    @classmethod
    @csrf_exempt
    def notifyerrormessage(self,request):
        encrypt = 0
        try:
            if request.method == "POST":
                try:                    
                    data = json.loads(request.body.decode('utf-8'),strict=False)
                except:
                    encrypt = 1
                    encoded_string = request.body.decode('utf-8')
                    req = commonfunc.b64decode(encoded_string)
                    data = json.loads(req, strict=False)

                if data:  
                    try:                       
                        if len(data) > 2:
                            response = {'error_code': '102','message':'Invalid Request parameters.','data' : ''}
                            if encrypt == 1:
                                response = commonfunc.b64encode(json.dumps(response))
                            return JsonResponse(response, safe=False)
                        
                        if "email" not in data:
                            response = {'error_code': '102','message':'Please enter email','data' : ''}
                            if encrypt == 1:
                                response = commonfunc.b64encode(json.dumps(response, sort_keys=True, indent=1, cls=DjangoJSONEncoder))
                            return JsonResponse(response,safe=False)
                        
                        # if "skype_name" not in data:
                        #     response = {'error_code': '102','message':'Please enter you skype_name','data' : ''}
                        #     if encrypt == 1:
                        #         response = commonfunc.b64encode(json.dumps(response, sort_keys=True, indent=1, cls=DjangoJSONEncoder))
                        #     return JsonResponse(response,safe=False)
                                                   
                    except Exception as e:
                        # return HttpResponse(traceback.format_exc())
                        errormsg = str(e)
                        error_code = "102"
                        response = {'error_code': error_code,'message':errormsg,'data' : ''}
                        if encrypt == 1:
                            response = commonfunc.b64encode(json.dumps(response))
                        return JsonResponse(response)
                    
                with connection.cursor() as cursor:   
                    #Fetching id of the user with his email_id 
                    get_userid = ''' SELECT `id` FROM `user` WHERE `email`= %s ORDER BY id ASC LIMIT 1'''
                    values = [data['email']]
                    cursor.execute(get_userid,values)  
                    user_data = common.dictfetchall(self,cursor)
                    id = user_data[0]['id']
                    
                    #Fetching user_id,id,fp_log_id  of the user with his id 
                    get_user_details = ''' SELECT `id`, `fp_log_id`,`user_id` FROM `fp_user_details` WHERE `user_isActive`= '1' AND `user_id`= %s '''
                    cursor.execute(get_user_details,[id])
                    user_details = common.dictfetchall(self,cursor)

                    # skype_name = data['skype_name']
                    user_id_new = user_details[0]['user_id']
                    fp_log_id_new = user_details[0]['fp_log_id']
                    fp_user_id = user_details[0]['id']

                    api_failure_counter = 0
                    api_success_counter = 0

                    sk = Skype('vedant.vartak@fintoo.in', 'vedantfintoo12345') # connect to Skype
                    sk.user # you
                    sk.contacts # your contacts
                    sk.chats # your conversations

                    # This is the list of API which requires user_id, fp_log_id, fp_user_id as their payload
                    api_list = [
                    'getrpinoutflow',
                    'getsurplusdata',	
                    'getscorecard',		
                    'getassetgoals',	
                    'getassetgoalmapping',
                    'getallunlinkassets',			
                    'getreccontingencyrisk',		
                    'getfinalgoalrecommnedation',	
                    'getcashflowrecommendation',				
                    'getrecommendationcashflow',		
                    'getequityfundflow',		
                    'getdebtfundflow',
                    'getretirementcorpus',
                    'goalsummary',		
                    'getliabilitysummary',		
                    'getassetandliabilityrecommendation',	
                    'getAssetSummary']	

                    # This is the list of API which requires user_id, fp_log_id as their payload
                    api_list2 = [
                    'getrpyourprofiledata',	
                    'getriskappetite',	
                    'getcurrentinsurance',	
                    'getlifeinsurance',	
                    'getcashflowsurplusshortfall',	
                    'getcashinflow',	
                    'getcashoutflow',	
                    'getretirementinfo',	
                    'getretirementcashflow',	
                    'getcurrentinsurance',	
                    'getequitydata',
                    'realstateInvestment',	
                    'debtInvestment']

                    requested_payload = {"fp_log_id":fp_log_id_new,"user_id":user_id_new,"fp_user_id":fp_user_id}
                    requested_payloadd = {"fp_log_id":fp_log_id_new,"user_id":user_id_new}
                    ch = sk.chats.chat('19:22789de5ea6d453fbafd4afd4134517f@thread.skype')
                    for api_name in api_list2:
                        api = reverse(api_name)
                        response_list = {"user_id":user_id_new,"fp_log_id":fp_log_id_new}
                        data_here = requests.post(urls.BASE_URL[:-1]+api, data=json.dumps(response_list))
                        if data_here.json()['error_code']=="100":
                            print("API Worked Successfully")
                            api_success_counter +=1
                        else:
                            print("API Failed")
                            api_failure_counter +=1 
                            msg_to_send = f"Request URL : {urls.BASE_URL}restapi/report/{api_name}/ \n Payload : {str(requested_payloadd)}\nError Message : {data_here.json()['message'] }".strip()
                            # ch = sk.contacts[skype_name].chat
                            ch.sendMsg(msg_to_send)
                            ch.getMsgs()

                    for api_name in api_list:
                        api = reverse(api_name)
                        response_list = {"user_id":user_id_new,"fp_log_id":fp_log_id_new,"fp_user_id":fp_user_id}
                        data_here = requests.post(urls.BASE_URL[:-1]+api, data=json.dumps(response_list))
                        if data_here.json()['error_code']=="100":
                            print("API Worked Successfully")
                            api_success_counter +=1
                        else:
                            print("API Failed")
                            api_failure_counter +=1 
                            msg_to_send = f"Request URL : {urls.BASE_URL}restapi/report/{api_name}/ \n Payload : {str(requested_payload)}\nError Message : {data_here.json()['message'] }".strip()
                            # ch = sk.contacts[skype_name].chat
                            ch.sendMsg(msg_to_send)
                            ch.getMsgs()

                    response = {'error_code': '100','message':"Message send successfully !!! ",'Total API Failed':api_failure_counter,'Total API Passed':api_success_counter}
                    return JsonResponse(response, safe=False)
                
            else:
                response = {"error_code": '104',"message":'Invalid Request method(Only POST method is allowed).',"data" : '' }
                if encrypt == 1:
                    response = commonfunc.b64encode(
                        json.dumps(response, sort_keys=True, indent=1, cls=DjangoJSONEncoder))
                return JsonResponse(response,safe=False)

        except Exception as e:
            # return HttpResponse(traceback.format_exc())
            response = {'error_code': '102','message':'Invalid Request parameters.','data' : ''}
            if encrypt == 1:
                response = commonfunc.b64encode(
                    json.dumps(response, sort_keys=True, indent=1, cls=DjangoJSONEncoder))
                return JsonResponse(response,safe=False)