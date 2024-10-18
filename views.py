#from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import redirect  # new

from .models import Forclosure, Attachment, Employer,ForclosureLog, Engagement, EngagementLog,Generalcase, GeneralcaseLog #Generalquery # new
from django.contrib import messages  # new
from .forms import NewUserForm, ForclosureForm,  EngagementForm, EngagementSearchForm,GeneralcaseForm, EmployerSearchForm, SearchEmployerForm
from django.views.generic import CreateView
from django.urls import reverse_lazy

from django.contrib.auth import login, authenticate, logout #add this
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib.auth.decorators import login_required


from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.core.exceptions import ValidationError
from django_fsm_log.models import StateLog

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.db.models import Count
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import update_session_auth_hash



# Create your views here.

# Create your views here.
def homepage(request):
	return render(request=request, template_name='home.html')

def landing(request):
	return render(request=request, template_name='landing.html')





def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})



def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_page = request.GET.get('next')

                # Check if the user's password is the initial password
                if user.check_password(settings.INITIAL_PASSWORD):
                    # Redirect the user to the password reset page
                    update_session_auth_hash(request, user)  # Update session hash to prevent logging out the user
                    return redirect('password_reset')

                if next_page:
                    return redirect(next_page)
                else:
                    return redirect('land')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="registration\login.html", context={"login_form": form})




def logout_request(request):
	logout(request)
	#messages.info(request, "You have successfully logged out.") 
	return redirect("login")



def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'192.168.193.51:92',
                    #'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, settings.PASSWORD_RESET_FROM_EMAIL, [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})







@login_required
def closure_quest(request):
    if not request.user.groups.filter(name='Officers').exists():
        return HttpResponse('Unauthorized', status=401)

    if request.method == "POST":
        fm = ForclosureForm(request.POST, request.FILES)
        if fm.is_valid():
            forclosure = fm.save(commit=False)
            forclosure.user = request.user
            next_action_user = forclosure.reviewer  # Assuming reviewer is stored in the `reviewer` field
            forclosure.save()

            # Process file uploads
            attachments = request.FILES.getlist('attachments')
            for attachment in attachments:
                Attachment.objects.create(forclosure=forclosure, file=attachment)

            # Send notification email to the reviewer (next_action_user)
            subject = 'New Employer Closure Request'
            message = 'A new employer closure request has been submitted for review.'
            from_email = 'nssfbiu@nssfug.org'  # Set the sender's email address
            to_email = next_action_user.email  # Get the email address of the next_action_user (reviewer)

            send_mail(subject, message, from_email, [to_email])

            messages.success(request, ' Employer closure case has been submitted successfully')
            return redirect('close')
        else:
            #messages.success(request, 'Check the data captured')
            messages.add_message(request, messages.ERROR, 'Failed record capture, crosscheck the field entries')
            return redirect('close')


    else:
        fm = ForclosureForm()

    closedata = Forclosure.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'closure_quest.html', context={'fm': fm, 'closedata': closedata})





@login_required
def closure_detail(request, id):
    forclosure = get_object_or_404(Forclosure, id=id)
    review_comment = request.POST.get('review_comment')
    next_action_user = request.POST.get('next_action_user')
    context = {'forclosure': forclosure, 'review_comment': review_comment, 'next_action_user': next_action_user, 'id': id}

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'reject':
            forclosure.reject(user=request.user, review_comment=review_comment)
            forclosure.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
            # return redirect('/vq')

        if action == 'cancel':
            forclosure.cancel(user=request.user, review_comment=review_comment)
            forclosure.save()
            return redirect('/vq')

        if action == 'first_review':
            forclosure.first_review(user=request.user, review_comment=review_comment)
            forclosure.save()
            return redirect('/sview')

        if action == 'reverse':
            forclosure.reverse(user=request.user, review_comment=review_comment)
            forclosure.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
            # return redirect('/vq')

        if action == 'resubmit':
            forclosure.resubmit(user=request.user, review_comment=review_comment)
            forclosure.save()
            return redirect('/vq')

        if action == 'approve':
            forclosure.approve(user=request.user, review_comment=review_comment)
            forclosure.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
            #return redirect('/asgnedview')

        if action == 'assign':
            next_action_user_id = request.POST.get('next_action_user')
            next_action_user = User.objects.get(id=next_action_user_id)
            forclosure.assign(user=request.user, review_comment=review_comment, next_action_user=next_action_user)
            forclosure.save()

            # Send email notification to the assigned user
            subject = 'New task assigned'
            message = f"A new task has been assigned to you. Please take necessary action."
            from_email = 'nssfbiu@nssfug.org'  # Set the sender's email address
            to_email = next_action_user.email  # Get the email address of the assigned user

            send_mail(subject, message, from_email, [to_email])

            return redirect('/lmview')

        if action == 'authorise':
            forclosure.authorise(user=request.user, review_comment=review_comment)
            forclosure.save()
            # return redirect(request.META.get('HTTP_REFERER', '/'))
            return redirect('/apvd')

    # Fetch assessors and pass them to the template context
    assessors = User.objects.filter(groups__name='Assessors')
    context['assessors'] = assessors

    attachments = Attachment.objects.filter(forclosure=forclosure)
    context['attachments'] = attachments

    # Check the user group and render the appropriate template
    if request.user.groups.filter(name='Officers').exists():
        return render(request, 'initiator_closure_detail.html', context)
    elif request.user.groups.filter(name='Supervisors').exists():
        return render(request, 'sup_closure_detail.html', context)
    elif request.user.groups.filter(name='Line managers').exists():
        return render(request, 'lm_closure_detail.html', context)
    elif request.user.groups.filter(name='Assessors').exists():
        return render(request, 'bdu_closure_detail.html', context)
    else:
        # Handle the case when the user does not belong to any specific group
        return HttpResponse('Unauthorized', status=401)



def state_log_list(request):
    state_logs = StateLog.objects.all()
    #user=request.user
    context = {'state_logs': state_logs}
	
    return render(request, 'state_log_list.html', context)





@login_required
def view_quests(request):
    #closedata = Forclosure.objects.all()
    closedata = Forclosure.objects.filter(user=request.user).order_by('-created_at')
    headline = "My Employer Closure Requests" 
    return render(request, 'view_quests.html', context={'closedata': closedata, 'headline':headline})

def all_employers(request):
    closedata = Forclosure.objects.all().order_by('-created_at')
    #closedata = Forclosure.objects.filter(user=request.user)
    headline = "All Employer Closure Requests" 
    return render(request, 'view_quests_all.html', context={'closedata': closedata, 'headline':headline})

@login_required
def employer_detail(request, id):
    forclosure = get_object_or_404(Forclosure, id=id)
    attachments = Attachment.objects.filter(forclosure=forclosure)
    logs = ForclosureLog.objects.filter(model=forclosure)
    #state_logs = StateLog.objects.all()
    #logs = ForclosureLog.objects.filter(model=forclosure)
    return render(request, 'employer_details.html', context={'forclosure': forclosure, 'attachments': attachments,'logs': logs})


@login_required
def employer_detail_lm(request, id):
    forclosure = get_object_or_404(Forclosure, id=id)
    attachments = Attachment.objects.filter(forclosure=forclosure)
    logs = ForclosureLog.objects.filter(model=forclosure)
    #state_logs = StateLog.objects.all()
    #logs = ForclosureLog.objects.filter(model=forclosure)
    return render(request, 'employer_details_lm.html', context={'forclosure': forclosure, 'attachments': attachments,'logs': logs})


@login_required
def supervisors_view(request):
    #closedata = Forclosure.objects.all() 
    closedata = Forclosure.objects.filter(reviewer=request.user,state__in=['initiated', 'resubmited']).order_by('-created_at')
    headline = "Employer Closure Requests To Review" 
    return render(request, 'view_quests.html', context={'closedata': closedata, 'headline':headline})

@login_required
def first_reviewed_entries(request):
    # Check if the user belongs to the 'Line manager' group
    line_manager_group = Group.objects.get(name='Line managers')
    if not line_manager_group in request.user.groups.all():
        return HttpResponse('Unauthorized', status=401)

    # Retrieve entries with status 'first_reviewed' and users belonging to the 'Line manager' group
    #closedata = Forclosure.objects.filter(state='first_reviewed', user__groups=line_manager_group)
    #closedata = Forclosure.objects.filter(state__in=['first_reviewed','approved'])
    # Retrieve entries that have ever been in the 'first_reviewed' state
    #closedata = Forclosure.objects.filter(Q(state='first_reviewed') | Q(logs__action='first_review')).order_by('-created_at')
    closedata = Forclosure.objects.filter(state='first_reviewed').order_by('-created_at')

    #return render(request, 'first_reviewed_entries.html', {'entries': entries})
    headline = "Employer Closure Requests Reviewed By Supervisors" 
    return render(request, 'view_quests.html', context={'closedata': closedata, 'headline':headline})

@login_required
def bdu_review(request):

    closedata = Forclosure.objects.filter(state='first_reviewed').order_by('-created_at')

    #return render(request, 'first_reviewed_entries.html', {'entries': entries})
    headline = "Employer Closure Requests Reviewed By Supervisors" 
    return render(request, 'view_quests.html', context={'closedata': closedata, 'headline':headline})

@login_required
def approved_entries(request):
    # Check if the user belongs to the 'Line manager' group
    line_manager_group = Group.objects.get(name='Line managers')
    if not line_manager_group in request.user.groups.all():
        return HttpResponse('Unauthorized', status=401)

    closedata = Forclosure.objects.filter(state='approved').order_by('-created_at')

    #return render(request, 'first_reviewed_entries.html', {'entries': entries})
    headline = "Approved Employer Closure Requests" 
    return render(request, 'view_quests.html', context={'closedata': closedata, 'headline':headline})

@login_required
def assign_summaries(request):
    # Check if the user belongs to the 'Line manager' group
    line_manager_group = Group.objects.get(name='Line managers')
    if not line_manager_group in request.user.groups.all():
        return HttpResponse('Unauthorized', status=401)

    closedata = Forclosure.objects.filter(Q(state='assigned') | Q(logs__action='assign'))

    grouped_data = closedata.values('next_action_user__username').annotate(count=Count('id'))

    #return render(request, 'first_reviewed_entries.html', {'entries': entries})
    return render(request, 'summariz.html', context={'grouped_data': grouped_data})

@login_required
def assigned_entries(request):
    # Check if the user belongs to the 'Line manager' group
    reviewer_group = Group.objects.get(name='Assessors')
    if not reviewer_group in request.user.groups.all():
        return HttpResponse('Unauthorized', status=401)

    # Retrieve entries that have ever been in the 'assigned' state
    #closedata = Forclosure.objects.filter(Q(state='assigned') | Q(logs__action='assign'))

    closedata = Forclosure.objects.filter(next_action_user=request.user).order_by('-created_at')
    #return render(request, 'first_reviewed_entries.html', {'entries': entries})
    headline = "My Assigned Employer Closure Requests" 
    return render(request, 'view_quests.html', context={'closedata': closedata, 'headline':headline})

def get_employer_name(request):
    nssf_no = request.GET.get('nssf_no')

    try:
        employer = Employer.objects.get(nssf_no=nssf_no)
        employer_name = employer.employer_name
    except Employer.DoesNotExist:
        employer_name = ''

    return HttpResponse(employer_name)


@login_required
def engagement_record(request):

    if request.method == "POST":
        fm = EngagementForm(request.POST, request.FILES)
        if fm.is_valid():
            engagement = fm.save(commit=False)
            engagement.user = request.user
            #next_action_user = forclosure.reviewer  # Assuming reviewer is stored in the `reviewer` field
            engagement.save()

            # Process file uploads
            attachments = request.FILES.getlist('attachments')
            for attachment in attachments:
                Attachment.objects.create(engagement=engagement, file=attachment)

            messages.success(request, ' Successfully Captured record')
            return redirect('engag')
        else:
            #messages.success(request, 'Check the data captured')
            messages.add_message(request, messages.ERROR, 'Failed record capture, crosscheck the field entries')
            return redirect('engag')

    else:
        fm = EngagementForm()

    engagedata = Engagement.objects.filter(user=request.user).order_by('-modified_at')
    return render(request, 'engagement_form.html', context={'fm': fm, 'engagedata': engagedata})


def create_engagement(request):
    form = EngagementForm(request.POST or None)

    if form.is_valid():
        engagement = form.save(commit=False)
        engagement.user = request.user  # Set the user who created the engagement
        engagement.save()
        # Perform any other necessary actions or redirects

    context = {'form': form}
    return render(request, 'create_engagement.html', context)


@login_required
def view_engagements(request):
    #closedata = Forclosure.objects.all()
    engdata = Engagement.objects.filter(user=request.user).order_by('-modified_at')
    #return render(request, 'view_engagements.html', context={'engdata': engdata})
    headline = "MY Employer Engagements"  
    return render(request, 'view_engagements.html', context={'engdata': engdata,'headline':headline})

@login_required
def employer_engagements(request, id):
    engagement = get_object_or_404(Engagement, id=id)
    attachments = Attachment.objects.filter(engagement=engagement)
    nssfno = engagement.nssf_no
    #attachment = engagement.attachments
    #logs = Engagement.objects.filter(nssf_no=nssfno).order_by('-created_at')
    #attachments = logs.attachments
    #closedata = Forclosure.objects.filter(user=request.user).order_by('-created_at')
    #state_logs = StateLog.objects.all()
    logs = EngagementLog.objects.filter(model=engagement)
    return render(request, 'employer_engagements.html', context={'engagement': engagement, 'attachments': attachments,'logs': logs})

@login_required
def engagement_details(request, id):
    engagement = get_object_or_404(Engagement, id=id)
    attachments = Attachment.objects.filter(engagement=engagement)
    nssfno = engagement.nssf_no
    logs = EngagementLog.objects.filter(model=engagement)
    return render(request, 'engagement_details.html', context={'engagement': engagement, 'attachments': attachments,'logs': logs})

def search_engagements(request):
    form = EngagementSearchForm(request.GET or None)
    engagements = []
    first_employer_name = None  # Initialize the variable with None
    nssf_no = None  # Initialize the variable with None

    if form.is_valid():
        nssf_no = form.cleaned_data['nssf_no']
        engagements = Engagement.objects.filter(nssf_no__icontains=nssf_no).order_by('-action_date')
        first_employer_name = engagements.first().employer_name if engagements else None

    return render(request, 'search_results.html', {'form': form, 'engagements': engagements,'first_employer_name': first_employer_name,'nssf_no':nssf_no})


@login_required
def engagement_review(request, id):
    engagement = get_object_or_404(Engagement, id=id)
    remark = request.POST.get('remark')
    #next_action_user = request.POST.get('next_action_user')
    context = {'engagement': engagement, 'remark': remark, 'id': id}

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'reject':
            engagement.reject(user=request.user, remark=remark)
            engagement.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
            # return redirect('/vq')

        if action == 'cancel':
            engagement.cancel(user=request.user)
            engagement.save()
            #return redirect('/vq')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if action == 'approve':
            engagement.approve(user=request.user, remark=remark)
            engagement.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
            #return redirect('/asgnedview')

        if action == 'forward':
            reviewer_id = request.POST.get('reviewer')
            reviewer = User.objects.get(id=reviewer_id)
            engagement.forward(user=request.user, reviewer=reviewer)
            engagement.save()

            # Send email notification to the assigned user
            subject = 'New Employer Engagement Task Assigned'
            message = f"A new task has been assigned to you. Please take necessary action."
            from_email = 'nssfbiu@nssfug.org'  # Set the sender's email address
            to_email = reviewer.email  # Get the email address of the assigned user

            send_mail(subject, message, from_email, [to_email])

            #return redirect('/lmview')
            return redirect(request.META.get('HTTP_REFERER', '/'))

    # Fetch assessors and pass them to the template context
    #supervisors = User.objects.filter(groups__name='Supervisors').exclude(id=engagement.user.id)

    supervisors = User.objects.filter(Q(groups__name='Supervisors') | Q(groups__name='Line managers')).exclude(id=engagement.user.id)
    context['supervisors'] = supervisors

    attachments = Attachment.objects.filter(engagement=engagement)
    context['attachments'] = attachments

    logs = EngagementLog.objects.filter(model=engagement)
    context['logs'] = logs
    

    # Check the user group and render the appropriate template
    #if request.user.groups.filter(name='Officers').exists():
    if request.user.groups.filter(Q(name='Officers') | Q(name='Assessors')).exists():
        if request.user == engagement.user:
            return render(request, 'employer_engagements.html', context)
        return render(request, 'engagement_details.html', context)
    elif request.user.groups.filter(Q(name='Supervisors') | Q(name='Line managers')).exists():
    #elif request.user.groups.filter(name='Supervisors').exists():
        if request.user == engagement.user:
            return render(request, 'engagement_details.html', context)
        elif engagement.reviewer == request.user:
            return render(request, 'supervisor_review.html', context)
        return render(request, 'engagement_details.html', context)

    else:
        # Handle the case when the user does not belong to any specific group
        return HttpResponse('Unauthorized', status=401)

@login_required
def all_engagements(request):
    engdata = Engagement.objects.all().order_by('-modified_at')[:2000]
    headline = "Recent Employer Engagements"  
    #engdata = Engagement.objects.filter(user=request.user).order_by('-modified_at')
    return render(request, 'view_engagements.html', context={'engdata': engdata,'headline':headline})



@login_required
def supervisor_review(request):
    #closedata = Forclosure.objects.all() 
    engdata = Engagement.objects.filter(reviewer=request.user, state='forwarded').order_by('-modified_at')
    entry_count = engdata.count()
    headline = "My Employer Engagements"  
    return render(request, 'view_engagements.html', context={'engdata': engdata, 'entry_count': entry_count, 'headline':headline})
    #return render(request, 'view_engagements.html', context={'engdata': engdata})
    #return render(request, 'view_quests.html', context={'closedata': closedata})


@login_required
def generalcase_record(request):

    if request.method == "POST":
        fm = GeneralcaseForm(request.POST, request.FILES)
        if fm.is_valid():
            generalcase = fm.save(commit=False)
            generalcase.user = request.user
            #next_action_user = forclosure.reviewer  # Assuming reviewer is stored in the `reviewer` field
            generalcase.save()

            # Process file uploads
            attachments = request.FILES.getlist('attachments')
            for attachment in attachments:
                Attachment.objects.create(generalcase=generalcase, file=attachment)

            messages.success(request, ' Record Successfully Captured ')
            return redirect('gencase')
        else:
            #messages.success(request, 'Check the data captured')
            messages.add_message(request, messages.ERROR, 'Failed record capture, crosscheck the field entries')
            return redirect('gencase')

    else:
        fm = GeneralcaseForm()

    gendata = Generalcase.objects.filter(user=request.user).order_by('-modified_at')
    return render(request, 'generalcase_form.html', context={'fm': fm, 'gendata': gendata})

@login_required
def view_records(request):
    #closedata = Forclosure.objects.all()
    gendata = Generalcase.objects.filter(user=request.user).order_by('-modified_at')
    headline = "My Recorded Cases"  
    return render(request, 'view_records.html', context={'gendata': gendata,'headline':headline})

@login_required
def case_review(request, id):
    generalcase = get_object_or_404(Generalcase, id=id)
    #user=request.user
    remark = request.POST.get('remark')
    #next_action_user = request.POST.get('next_action_user')
    context = {'generalcase': generalcase, 'remark': remark, 'id': id}

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'reject':
            generalcase.reject(user=request.user, remark=remark)
            generalcase.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
            # return redirect('/vq')

        if action == 'cancel':
            generalcase.cancel(user=request.user)
            generalcase.save()
            #return redirect('/vq')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if action == 'approve':
            generalcase.approve(user=request.user, remark=remark)
            generalcase.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
            #return redirect('/asgnedview')

        if action == 'forward':
            reviewer_id = request.POST.get('reviewer')
            reviewer = User.objects.get(id=reviewer_id)
            generalcase.forward(user=request.user, reviewer=reviewer)
            generalcase.save()

            # Send email notification to the assigned user
            subject = 'New task assigned'
            message = f"A new task has been assigned to you. Please take necessary action."
            from_email = 'nssfbiu@nssfug.org'  # Set the sender's email address
            to_email = reviewer.email  # Get the email address of the assigned user

            send_mail(subject, message, from_email, [to_email])

            #return redirect('/lmview')
            return redirect(request.META.get('HTTP_REFERER', '/'))

    # Fetch assessors and pass them to the template context
    #supervisors = User.objects.filter(groups__name='Supervisors')
    supervisors = User.objects.all()
    context['supervisors'] = supervisors

    attachments = Attachment.objects.filter(generalcase=generalcase)
    context['attachments'] = attachments

    logs = GeneralcaseLog.objects.filter(model=generalcase)
    context['logs'] = logs

    if request.user == generalcase.user:
        return render(request, 'case_details.html', context)
    else:
        return render(request, 'sup_case_review.html', context)
    
"""
    # Check the user group and render the appropriate template
    if request.user.groups.filter(name='Officers').exists():
        #return render(request, 'forwarding.html', context)
        return render(request, 'case_details.html', context)
    elif request.user.groups.filter(name='Supervisors').exists():
        return render(request, 'sup_case_review.html', context)

    else:
        # Handle the case when the user does not belong to any specific group
        return HttpResponse('Unauthorized', status=401)
"""
    
@login_required
def reviewer_view(request):
    #closedata = Forclosure.objects.all() 
    gendata = Generalcase.objects.filter(reviewer=request.user, state='forwarded').order_by('-modified_at')  
    headline = "Cases to review"  
    return render(request, 'view_records.html', context={'gendata': gendata,'headline':headline})

@login_required
def reviewed_cases(request):
    #closedata = Forclosure.objects.all() 
    gendata = Generalcase.objects.filter(reviewer=request.user, state__in=['approved', 'rejected', 'cancelled']).order_by('-modified_at')
    headline = "My Reviewed Cases"  
    return render(request, 'view_records.html', context={'gendata': gendata,'headline':headline})

@login_required
def employersearch(request):

    # Initialize form for searching members
    search_form = SearchEmployerForm(request.GET or None)
    results = []
    if request.method == "GET":
        if search_form.is_valid():
            query = search_form.cleaned_data['q']
            results = Employer.objects.filter(employer_name__icontains=query)

    return render(request, 'employersearch.html', {'search_form': search_form, 'results': results})


from fuzzywuzzy import process

@login_required
def search_employers_bdu(request):
    search_term = request.GET.get('q', '')  # Adjusted to match form field name
    top_results = []

    if search_term:
        # Fetch all employer names from the database
        all_employers = Employer.objects.all()

        # Create a list of tuples (name, nssf_no, registrydate)
        employer_details = [
            (e.employer_name, e.nssf_no, e.registry_dt)
            for e in all_employers
        ]

        # Extract only the names for fuzzy matching
        names = [e[0] for e in employer_details]

        # Find the top 10 matches with their similarity percentage
        matched_names = process.extract(search_term, names, limit=10)

        # Prepare the top_results list with full details and similarity percentage
        top_results = [
            {
                'name': matched_name[0],
                'nssf_no': next(e[1] for e in employer_details if e[0] == matched_name[0]),
                'registry_dt': next(e[2] for e in employer_details if e[0] == matched_name[0]),
                'similarity_percentage': matched_name[1]
            }
            for matched_name in matched_names
        ]
        # Sort the results by similarity_percentage in descending order
        top_results.sort(key=lambda x: x['similarity_percentage'], reverse=True)

    return render(request, 'search_employers_bdu.html', {'search_term': search_term, 'results': top_results})

