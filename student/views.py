from django.shortcuts import render,redirect
from django.contrib.auth import logout
from adminUser.models import UserCredentials
from adminUser.models import AddResult
from django.core.exceptions import ObjectDoesNotExist
# from .models import AddResult
import logging
# from django.contrib.auth.decorators import login_required
import joblib
from django.conf import settings
import numpy as np
import pandas as pd
from django.http import JsonResponse


logger = logging.getLogger(__name__)

# Existing view for the home page

# New view for the user dashboard
from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    try:
        username = request.session["username"]
        
        # Check if the user is in the admin dashboard
        if request.session.get('admin_dashboard'):
            # If the user is in the admin dashboard, redirect to admin dashboard
            return redirect('admin-dashboard')
        
        studentcreds = UserCredentials.objects.get(application_idU=username)
        f_name = studentcreds.first_name
        l_name = studentcreds.last_name
        return render(request, "student/dashboard.html", {'username': username, 'f_name': f_name, 'l_name': l_name})
    
    except KeyError:
        return redirect('login')
    
    except UserCredentials.DoesNotExist:
        return redirect('login')
    
    except AddResult.DoesNotExist:
        return redirect('login')
DEFAULT_ADMIN_USERNAME = "admin"
def result_page(request):
    try:
        username = request.session["username"]
        if username is not None and username != DEFAULT_ADMIN_USERNAME:
            studentcreds = UserCredentials.objects.get(application_idU=username)
            idu = studentcreds.application_idU
            studres = AddResult.objects.get(application_idR=idu)
            if studres is not None:
                vc = studres.verbal_Comprehension
                vr = studres.verbal_Reasoning
                fr = studres.figural_Reasoning
                qr = studres.qualitative_Reasoning
                st = studres.status
                return render(request, 'student/result.html', {'vc': vc, 'vr': vr, 'fr': fr, 'qr': qr, 'st': st})
            else:
                vc = 'None'
                vr = 'None'
                fr = 'None'
                qr = 'None'
                st = 'None'
                return render(request, 'student/result.html', {'vc': vc, 'vr': vr, 'fr': fr, 'qr': qr, 'st': st})
        else:
            return redirect('login')    
             
    except KeyError:
        return redirect('login')    
    except UserCredentials.DoesNotExist:
                return HttpResponse("User credentials not found.")
    except AddResult.DoesNotExist:
                return render(request, 'student/result.html', {'vc': 'None', 'vr': 'None', 'fr': 'None', 'qr': 'None', 'st': 'None'})

def recommended_courses(request):
    try:
        username = request.session["username"]
        studentcreds = UserCredentials.objects.get(application_idU=username)
        idu = studentcreds.application_idU
        studres = AddResult.objects.get(application_idR=idu)
        vc = int(studres.verbal_Comprehension)
        vr = int(studres.verbal_Reasoning)
        fr = int(studres.figural_Reasoning)
        qr = int(studres.qualitative_Reasoning)
        st = studres.status
        ca = studentcreds.course_applied
        
        new_data = {
            'vc': [vc],
            'vr': [vr],
            'fr': [fr],
            'qr': [qr],
            'course_applied_BEED': [0],
            'course_applied_BSCS': [0],
            'course_applied_BSED-MATH': [0],
            'course_applied_BSES-CRM': [0],
            'course_applied_BSHM': [0],
            'course_applied_BTLED-HE': [0]
        }
        
        max_values = {'vc': 12, 'vr': 24, 'fr': 18, 'qr': 18}
        new_df = pd.DataFrame(new_data)
        new_df['course_applied_' + ca.upper()] = 1
        
        print(new_df)
        normalized_scores = np.array([vc, vr, fr, qr]) / np.array([max_values['vc'], max_values['vr'], max_values['fr'], max_values['qr']])
        new_df[['vc', 'vr', 'fr', 'qr']] = normalized_scores.reshape(1, -1)
        
        svm_model = load_svm_model()
        
        data_values = new_df.copy()
        
        predictions= svm_model.predict(data_values)
        probabilities = svm_model.predict_proba(data_values)
        
        recommended_courses_list = []
        for prob_row in probabilities:
            sorted_probs_and_classes = sorted(zip(prob_row, svm_model.classes_), reverse=True)
            recommended_courses_list.extend([(class_label, prob * 100) for prob, class_label in sorted_probs_and_classes])
            
        
        print(recommended_courses_list)
        return JsonResponse({'recommended_courses': recommended_courses_list})
    except ObjectDoesNotExist:
         return redirect('login')  
def load_svm_model():
    model_path = settings.BASE_DIR / 'ml_model' / 'svm_model.pkl'
    svm_model = joblib.load(model_path)
    return svm_model

# @login_required
# def home(request):
#     # Add your view logic here
#         username = request.session["username"]
#         studentcreds = UserCredentials.objects.get(application_idU=username)
#         f_name = studentcreds.first_name
#         l_name = studentcreds.last_name
#         idu = studentcreds.application_idU


#         studres = AddResult.objects.get(application_idR=idu)
#         vc = studres.verbal_Comprehension
#         vr = studres.verbal_Reasoning
#         fr = studres.figural_Reasoning
#         qr = studres.qualitative_Reasoning
#         st = studres.status

#         # password = request.POST['password']
#         return render(request, 'student/dashboard.html',{'username':username, 'f_name':f_name, 'l_name':l_name, 'vc':vc, 'vr':vr, 'fr':fr, 'qr':qr, 'st':st})

# def result_page(request):
#     try:
#         username = request.session["username"]
#         studentcreds = UserCredentials.objects.get(application_idU=username)
#         idu = studentcreds.application_idU
#         studres = AddResult.objects.get(application_idR=idu)
#         if studres is not None:
#             vc = studres.verbal_Comprehension
#             vr = studres.verbal_Reasoning
#             fr = studres.figural_Reasoning
#             qr = studres.qualitative_Reasoning
#             st = studres.status
#             return render(request, 'student/result.html', {'vc': vc, 'vr': vr, 'fr': fr, 'qr': qr, 'st': st})
#         else:
#             vc = 'None'
#             vr = 'None'
#             fr = 'None'
#             qr = 'None'
#             st = 'None'
#             return render(request, 'student/result.html', {'vc': vc, 'vr': vr, 'fr': fr, 'qr': qr, 'st': st})
#     except UserCredentials.DoesNotExist:
#                return HttpResponse("User credentials not found.")
#     except AddResult.DoesNotExist:
#                 return render(request, 'student/result.html', {'vc': 'None', 'vr': 'None', 'fr': 'None', 'qr': 'None', 'st': 'None'})

        # username = request.session["username"]
    # studentcreds = UserCredentials.objects.get(application_idU=username)
    # idu = studentcreds.application_idU
    # studres = AddResult.objects.get(application_idR=idu)
    # if studres is not None:
    #     vc = studres.verbal_Comprehension
    #     vr = studres.verbal_Reasoning
    #     fr = studres.figural_Reasoning
    #     qr = studres.qualitative_Reasoning
    #     st = studres.status

        
    #         # password = request.POST['password']
    #     return render(request, 'student/result.html',{ 'vc':vc, 'vr':vr, 'fr':fr, 'qr':qr, 'st':st})
    # else:
    #     vc = 'None'
    #     vr = 'None'
    #     fr = 'None'
    #     qr = 'None'
    #     st = 'None'
    #     return render(request, 'student/result.html',{ 'vc':vc, 'vr':vr, 'fr':fr, 'qr':qr, 'st':st})
         
    # # Add your view logic here



def user_logout(request):
    # Clear the session
    logout(request)
    request.session.flush()
    # Redirect to the login page
    return redirect("login")
