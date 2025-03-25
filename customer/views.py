from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from insurance import models as CMODEL
from insurance import forms as CFORM  # Add this import
from django.shortcuts import render
from insurance.models import PolicyRecord, Policy

def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'customer/customerclick.html')


def customer_signup_view(request):
    userForm = forms.CustomerUserForm()
    customerForm = forms.CustomerForm()
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST, request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request, 'customer/customersignup.html', context=mydict)

def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

@login_required(login_url='customerlogin')
def customer_dashboard_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    dict = {
        'customer': customer,
        'available_policy': CMODEL.Policy.objects.count(),
        'applied_policy': CMODEL.PolicyRecord.objects.filter(customer=customer).count(),
        'total_category': CMODEL.Category.objects.count(),
        'total_question': CMODEL.Question.objects.filter(customer=customer).count(),
    }
    return render(request, 'customer/customer_dashboard.html', context=dict)

def apply_policy_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policies = CMODEL.Policy.objects.all()
    return render(request, 'customer/apply_policy.html', {'policies': policies, 'customer': customer})

def apply_view(request, pk):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policy = CMODEL.Policy.objects.get(id=pk)
    policyrecord = CMODEL.PolicyRecord()
    policyrecord.policy = policy
    policyrecord.customer = customer
    policyrecord.save()
    return redirect('history')

def history_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    # Fetch all the policy records for the customer and pre-fetch the related Policy object
    policies = CMODEL.PolicyRecord.objects.filter(customer=customer).select_related('policy')

    # Passing the policies to the template
    return render(request, 'customer/history.html', {
        'policies': policies,
        'customer': customer
    })


def ask_question_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    questionForm = CFORM.QuestionForm()
    if request.method == 'POST':
        questionForm = CFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            question.customer = customer
            question.save()
            return redirect('question-history')
    return render(request, 'customer/ask_question.html', {'questionForm': questionForm, 'customer': customer})

def question_history_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    questions = CMODEL.Question.objects.filter(customer=customer)
    return render(request, 'customer/question_history.html', {'questions': questions, 'customer': customer})

from django.contrib.auth.decorators import login_required

@login_required
def premium_distribution(request):
    # Get the currently logged-in customer (assuming the customer is a user or has a relation to User)
    customer = request.user.customer  # Adjust this based on how your customer model is linked to the User model
    
    # Fetch only approved PolicyRecords for the logged-in customer and include the related Policy data
    policy_records = PolicyRecord.objects.select_related('policy').filter(
        status='approved', 
        customer=customer  # Assuming 'customer' is the field that links the PolicyRecord to the Customer
    )

    # Pass the filtered policy records to the template context
    return render(request, 'customer/premium_distribution.html', {'policy_records': policy_records})
