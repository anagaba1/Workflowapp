
from django.urls import path
from .import views
from workflowapp.views import get_employer_name, landing
#from workflowapp.views import req_rev

# OtheremployerCreateView, PersonCreateView

urlpatterns = [
    #path("", views.homepage, name="homepage"), 
    path("", views.login_request, name="homepage"),  
    path("register/", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),   
    path("password_reset", views.password_reset_request, name="password_reset"),
    path("land", views.landing, name="land"),  

    path("log_list/", views.state_log_list, name="log_list"),

    path("close/", views.closure_quest, name="close"),
    path("vq/", views.view_quests, name="vq"),
    path("vq/emp_det/<int:id>/", views.employer_detail, name="emp_det"),
    path("vq/emp_det/req_rev/<int:id>", views.closure_detail, name="req_rev"),  # New URL pattern
    path("sview/", views.supervisors_view, name="sview"),
    path("sview/emp_det/<int:id>/", views.employer_detail, name="s_emp_det"),
    path("sview/emp_det/req_rev/<int:id>", views.closure_detail, name="s_req_rev"),  # New URL pattern
    path("lmview/", views.first_reviewed_entries, name="lmview"),
    path("lmview/emp_det/<int:id>/", views.employer_detail, name="l_emp_det"),
    path("lmview/emp_det/req_rev/<int:id>", views.closure_detail, name="l_req_rev"),  # New URL pattern
    path("bdu_rev/", views.bdu_review, name="bdu_rev"),
    path("bdu_rev/emp_det/<int:id>/", views.employer_detail, name="b_emp_det"),
    path("bdu_rev/emp_det/req_rev/<int:id>", views.closure_detail, name="b_req_rev"),  # New URL pattern
    path("apvd/", views.approved_entries, name="apvd"),
    path("apvd/emp_det/<int:id>/", views.employer_detail, name="apvd_emp_det"),
    path("apvd/emp_det/req_rev/<int:id>", views.closure_detail, name="apvd_req_rev"),  # New URL pattern
    #path("req_rev/<int:id>/", views.closure_detail, name="emp_rev"),
    path('get_employer_name/', get_employer_name, name='get_employer_name'),
    path("asgnedview/", views.assigned_entries, name="asgnedview"),
    path("asgnedview/emp_det/<int:id>/", views.employer_detail, name="a_emp_det"),
    path("asgnedview/emp_det/req_rev/<int:id>", views.closure_detail, name="a_req_rev"),  # New URL pattern  
    path("logz/", views.state_log_list, name="logz"), 
    path("all/", views.all_employers, name="all"),
    path("all/all_emp_det/<int:id>/", views.employer_detail_lm, name="all_emp_det"),
    #path("all/emp_det/<int:id>/", views.employer_detail, name="all_emp_det"),
    path("sumarz/", views.assign_summaries, name="sumarz"),
    path("engag/", views.engagement_record, name="engag"),
    path("engagview/", views.view_engagements, name="engagview"),
    path("engagview/emp_eng/<int:id>/", views.employer_engagements, name="emp_eng"),
    path("engagview/rev_eng/<int:id>/", views.engagement_review, name="rev_eng"),
    path("sup_review/", views.supervisor_review, name="sup_review"),
    path("sup_review/rev_eng/<int:id>/", views.engagement_review, name="sup_rev_eng"),
    path('search/', views.search_engagements, name='search_engagements'),
    path("search/emp_eng/<int:id>/", views.employer_engagements, name="search_eng"),
    path("search/eng_detail/<int:id>/", views.engagement_details, name="eng_detail"),

    path("all_eng/", views.all_engagements, name="all_eng"),
    path("all_eng/emp_eng/<int:id>/", views.employer_engagements, name="alleng_det"),
    path("all_eng/rev_eng/<int:id>/", views.engagement_review, name="all_rev_eng"),

   
    path("engagview/emp_eng/eng_rev/<int:id>/", views.engagement_review, name="eng_rev"),\
    
    path("gencase/", views.generalcase_record, name="gencase"),
    path("genview/", views.view_records, name="genview"),

    path("genview/case_details/<int:id>/", views.case_review, name="case_details"),

    path("rev_view/", views.reviewer_view, name="rev_view"),
    path("revd_cases/", views.reviewed_cases, name="revd_cases"),
    path("revd_cases/case_details/<int:id>/", views.case_review, name="rvcase_details"),

    path("rev_view/case_details/<int:id>/", views.case_review, name="sup_rev_view"),

    path('empsearch', views.employersearch, name="empsearch"),

    path('search_bdu/', views.search_employers_bdu, name='search_bdu')
    
    
    

    




]  