from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dasapp.models import DoctorReg, Specialization, CustomUser, Appointment
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dasapp.models import DoctorReg, Specialization, CustomUser, Appointment
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Swagger documentation for DOCSIGNUP view
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'pic': openapi.Schema(type=openapi.TYPE_FILE),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'mobno': openapi.Schema(type=openapi.TYPE_STRING),
            'specialization_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['pic', 'first_name', 'last_name', 'username', 'email', 'mobno', 'specialization_id', 'password']
    ),
    responses={200: 'Success', 400: 'Bad Request'}
)
@api_view(['POST'])
def DOCSIGNUP(request):
    """
    Doc Signup
    """
    specialization = Specialization.objects.all()
    if request.method == "POST":
        pic = request.FILES.get('pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobno = request.POST.get('mobno')
        specialization_id = request.POST.get('specialization_id')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email already exist')
            return redirect('docsignup')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,'Username already exist')
            return redirect('docsignup')
        else:
            user = CustomUser(
               first_name=first_name,
               last_name=last_name,
               username=username,
               email=email,
               user_type=2,
               profile_pic = pic,
            )
            user.set_password(password)
            user.save()
            spid =Specialization.objects.get(id=specialization_id)
            doctor = DoctorReg(
                admin = user,
                mobilenumber = mobno,
                specialization_id = spid,
            )
            doctor.save()            
            messages.success(request,'Signup Successfully')
            return redirect('docsignup')
    
    context = {
        'specialization':specialization
    }

    return render(request,'doc/docreg.html',context)

@login_required(login_url='/')
def DOCTORHOME(request):
    """
    Doctor Home
    """
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    allaptcount = Appointment.objects.filter(doctor_id=doctor_reg).count
    newaptcount = Appointment.objects.filter(status='0',doctor_id=doctor_reg).count
    appaptcount = Appointment.objects.filter(status='Approved',doctor_id=doctor_reg).count
    canaptcount = Appointment.objects.filter(status='Cancelled',doctor_id=doctor_reg).count
    comaptcount = Appointment.objects.filter(status='Completed',doctor_id=doctor_reg).count
    context = {
        'newaptcount':newaptcount,
        'allaptcount':allaptcount,
        'appaptcount':appaptcount,
        'canaptcount':canaptcount,
        'comaptcount':comaptcount        
    }
    return render(request,'doc/dochome.html',context)

@swagger_auto_schema(
    method='get',
    responses={200: 'Success'}
)
@api_view(['GET'])
def View_Appointment(request):
    """
    View Appointment
    """
    try:
        doctor_admin = request.user
        doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
        view_appointment = Appointment.objects.filter(doctor_id=doctor_reg)
        
        # Pagination
        paginator = Paginator(view_appointment, 5)  # Show 5 appointments per page
        page = request.GET.get('page')
        try:
            view_appointment = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            view_appointment = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            view_appointment = paginator.page(paginator.num_pages)

        context = {'view_appointment': view_appointment}
    except Exception as e:
        # Handle exceptions, such as database errors, gracefully
        context = {'error_message': str(e)}

    return Response(context)

@swagger_auto_schema(
    method='get',
    responses={200: 'Success'}
)
@api_view(['GET'])
def Patient_Appointment_Details(request, id):
    """
    Patient Appointment Details
    """
    patientdetails = Appointment.objects.filter(id=id)
    context = {'patientdetails': patientdetails}
    return render(request, 'doc/patient_appointment_details.html', context)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'pat_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'remark': openapi.Schema(type=openapi.TYPE_STRING),
            'status': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['pat_id', 'remark', 'status']
    ),
    responses={200: 'Success', 400: 'Bad Request'}
)
@api_view(['POST'])
def Patient_Appointment_Details_Remark(request):
    """
    Patient Appointment Details Remark
    """
    if request.method == 'POST':
        patient_id = request.POST.get('pat_id')
        remark = request.POST.get('remark')
        status = request.POST.get('status')
        patientaptdet = Appointment.objects.get(id=patient_id)
        patientaptdet.remark = remark
        patientaptdet.status = status
        patientaptdet.save()
        messages.success(request, "Status Update successfully")
        return redirect('view_appointment')
    return render(request, 'doc/view_appointment.html', {})

# Define other views similarly with Swagger documentation


def Patient_Approved_Appointment(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='Approved',doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1}
    return render(request, 'doc/patient_app_appointment.html', context)

def Patient_Cancelled_Appointment(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='Cancelled',doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1}
    return render(request, 'doc/patient_app_appointment.html', context)

def Patient_New_Appointment(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='0',doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1}
    return render(request, 'doc/patient_app_appointment.html', context)

def Patient_List_Approved_Appointment(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='Approved',doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1}
    return render(request, 'doc/patient_list_app_appointment.html', context)

def DoctorAppointmentList(request,id):
    patientdetails=Appointment.objects.filter(id=id)
    context={'patientdetails':patientdetails

    }

    return render(request,'doc/doctor_appointment_list_details.html',context)

def Patient_Appointment_Prescription(request):
    if request.method == 'POST':
        patient_id = request.POST.get('pat_id')
        prescription = request.POST['prescription']
        recommendedtest = request.POST['recommendedtest']
        status = request.POST['status']
        patientaptdet = Appointment.objects.get(id=patient_id)
        patientaptdet.prescription = prescription
        patientaptdet.recommendedtest = recommendedtest
        patientaptdet.status = status
        patientaptdet.save()
        messages.success(request,"Status Update successfully")
        return redirect('view_appointment')
    return render(request,'doc/patient_list_app_appointment.html',context)


def Patient_Appointment_Completed(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='Completed',doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1}
    return render(request, 'doc/patient_list_app_appointment.html', context)
def Search_Appointments(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    context = {}  # Define the context dictionary
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Appointment.objects.filter(fullname__icontains=query) | Appointment.objects.filter(appointmentnumber__icontains=query) & Appointment.objects.filter(doctor_id=doctor_reg)
            messages.success(request, "Search against " + query)
            return render(request, 'doc/search-appointment.html', {'patient': patient, 'query': query})
        else:
            print("No Record Found")
            return render(request, 'doc/search-appointment.html', context)

def Between_Date_Report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    patient = []
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    context = {}  # Define the context dictionary
    if start_date and end_date:
        # Validate the date inputs
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'doc/between-dates-report.html', {'patient': patient, 'error_message': 'Invalid date format'})

        # Filter Appointment between the given date range
        patient = Appointment.objects.filter(created_at__range=(start_date, end_date)) & Appointment.objects.filter(doctor_id=doctor_reg)

    return render(request, 'doc/between-dates-report.html', {'patient': patient, 'start_date': start_date, 'end_date': end_date})