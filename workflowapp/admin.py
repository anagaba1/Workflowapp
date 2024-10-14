from django.contrib import admin

from django.contrib import admin
from .models import Employer, Deeds, TeamLeader, Branch, Region 

admin.site.register(Employer)

#@admin.register(Deeds)



@admin.register(TeamLeader)
class TeamLeaderAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Deeds)
class DeedsAdmin(admin.ModelAdmin):
    list_display = ('employer_name', 'team_leader', 'Branch')
    #list_filter = ('Status', 'Team_Leader', 'Branch')
    search_fields = ('employer_name', 'nssf_no')

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    #list_filter = ('Status', 'Team_Leader', 'Branch')

