from django.db import models
from pytz import timezone, datetime
from account.models import FNSUser
from team.models import Team

# Create your models here.
class PersonalMatching(models.Model):
    user = models.ForeignKey(FNSUser, on_delete = models.CASCADE, default = 1)

    title = models.CharField(max_length=80, null=False)
    content = models.TextField(null = False)

    time_from = models.DateTimeField(null = True, blank = True)
    time_to = models.DateTimeField(null = True, blank = True)

    sport = models.CharField(max_length=15, null = False, default = 'Futsal') #종목
    location = models.CharField(max_length=50, null=False)
    number = models.IntegerField()
    rank = models.CharField(max_length = 20)

    created = models.DateTimeField(auto_now_add= True, null = True, blank = True)
    updated = models.DateTimeField(auto_now = True, null = True, blank = True)
    

    attendance = models.ManyToManyField(FNSUser, related_name= 'attendance', blank=True, default=0)

    def __str__(self):
        return self.title
    # def __str__(self):
    #     return '%s - %s' % (self.user.name, self.title)

    def total_attendance(self):
        return self.attendance.count()

    def total_comment(self):
        number = int(self.post.count()) + int(self.postReply.count())
        return number

    def time(self):
        return self.time_from + '~' + self.time_to

    def summary(self):
        return self.content[:100]

class PersonalComment(models.Model):
    user = models.ForeignKey(FNSUser, on_delete=models.CASCADE)
    post = models.ForeignKey(PersonalMatching, related_name="post", on_delete = models.CASCADE)
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return self.user.name

    def summary(self):
        return self.content[:150]

    def passedTime(self):
        now = datetime.datetime.now()
        modified = self.modified
        if str(now.strftime("%Y")) == str(modified.strftime("%Y")):
            if str(now.strftime("%m")) == str(modified.strftime("%m")):
                if str(now.strftime("%d")) == str(modified.strftime("%d")):
                    if str(now.strftime("%H")) == str(modified.strftime("%H")):
                        if str(now.strftime("%M")) == str(modified.strftime("%M")):
                            return '방금'
                        else:
                            timeLap = int(now.strftime("%M")) - int(modified.strftime("%M"))
                            message = str(timeLap) + '분 전'
                            return message
                    else:
                        now = int(now.strftime("%H"))*60 + int(now.strftime("%M"))
                        modified = int(modified.strftime("%H"))*60 + int(modified.strftime("%M"))
                        timeLap = now - modified
                        if timeLap >= 60:
                            message = str(timeLap//60) + '시간 전'
                        else:
                            message = str(timeLap) + '분 전'
                        return message
                else:
                    month = int(modified.strftime("%m"))
                    date = int(modified.strftime("%d"))
                    if month < 10:
                        month = modified.strftime("%m")[1]
                    else:
                        month = modified.strftime("%m")

                    if date < 10:
                        date = modified.strftime("%d")[1]
                    else:
                        date = modified.strftime("%d")
                    
                    return month + '월 ' + date + '일'
            else:
                    month = int(modified.strftime("%m"))
                    date = int(modified.strftime("%d"))
                    if month < 10:
                        month = modified.strftime("%m")[1]
                    else:
                        month = modified.strftime("%m")

                    if date < 10:
                        date = modified.strftime("%d")[1]
                    else:
                        date = modified.strftime("%d")
                    
                    return month + '월 ' + date + '일'
        else:
            month = int(modified.strftime("%m"))
            if month < 10:
                month = modified.strftime("%m")[1]
            else:
                month = modified.strftime("%m")
            
            return modified.strftime("%Y") + '년 ' + month + '월'

class PersonalReply(models.Model):
    user = models.ForeignKey(FNSUser, on_delete=models.CASCADE)
    post = models.ForeignKey(PersonalMatching, related_name="postReply", on_delete = models.CASCADE)
    comment = models.ForeignKey(PersonalComment, related_name="reply", on_delete= models.CASCADE, null = True, blank = True)
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.name

    def summary(self):
        return self.content[:150]

    def passedTime(self):
        now = datetime.datetime.now()
        modified = self.modified
        if str(now.strftime("%Y")) == str(modified.strftime("%Y")):
            if str(now.strftime("%m")) == str(modified.strftime("%m")):
                if str(now.strftime("%d")) == str(modified.strftime("%d")):
                    if str(now.strftime("%H")) == str(modified.strftime("%H")):
                        if str(now.strftime("%M")) == str(modified.strftime("%M")):
                            return '방금'
                        else:
                            timeLap = int(now.strftime("%M")) - int(modified.strftime("%M"))
                            message = str(timeLap) + '분 전'
                            return message
                    else:
                        now = int(now.strftime("%H"))*60 + int(now.strftime("%M"))
                        modified = int(modified.strftime("%H"))*60 + int(modified.strftime("%M"))
                        timeLap = now - modified
                        if timeLap >= 60:
                            message = str(timeLap//60) + '시간 전'
                        else:
                            message = str(timeLap) + '분 전'
                        return message
                else:
                    month = int(modified.strftime("%m"))
                    date = int(modified.strftime("%d"))
                    if month < 10:
                        month = modified.strftime("%m")[1]
                    else:
                        month = modified.strftime("%m")

                    if date < 10:
                        date = modified.strftime("%d")[1]
                    else:
                        date = modified.strftime("%d")
                    
                    return month + '월 ' + date + '일'
            else:
                month = int(modified.strftime("%m"))
                date = int(modified.strftime("%d"))
                if month < 10:
                    month = modified.strftime("%m")[1]
                else:
                    month = modified.strftime("%m")

                if date < 10:
                    date = modified.strftime("%d")[1]
                else:
                    date = modified.strftime("%d")
                
                return month + '월 ' + date + '일'
        else:
            month = int(modified.strftime("%m"))
            if month < 10:
                month = modified.strftime("%m")[1]
            else:
                month = modified.strftime("%m")
            
            return modified.strftime("%Y") + '년 ' + month + '월'
        

class TeamMatching(models.Model):
    # false 팀에서 매칭신청을 한 것 true 팀매칭 창에서 한 것.
    is_applied = models.BooleanField(default=False)
    user = models.ForeignKey(FNSUser, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=80, null=False)
    content = models.TextField(null = False)

    time_from = models.DateTimeField()
    time_to = models.DateTimeField()

    sport = models.CharField(max_length=15, null = False, default = 'Futsal') #종목
    location = models.CharField(max_length=50, null=False)
    rank = models.CharField(max_length = 20, null = True)

    myteam = models.ForeignKey(Team, related_name="myteam", on_delete=models.SET_NULL, null=True)
    vs_team = models.ForeignKey(Team, related_name = "vs_team", on_delete=models.SET_NULL, null=True)

    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    def time(self):
        return time_from + '~' + time_to

    def summary(self):
        return self.content[:100]

    def total_comment(self):
        number = int(self.post.count()) + int(self.postReply.count())
        return number

class TmAppliedTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    match = models.ForeignKey(TeamMatching, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.team.name

class TMComment(models.Model):
    user = models.ForeignKey(FNSUser, on_delete=models.CASCADE)
    post = models.ForeignKey(TeamMatching, related_name="post", on_delete = models.CASCADE)
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name

    def summary(self):
        return self.content[:20]

    def passedTime(self):
        now = datetime.datetime.now()
        modified = self.modified
        if str(now.strftime("%Y")) == str(modified.strftime("%Y")):
            if str(now.strftime("%m")) == str(modified.strftime("%m")):
                if str(now.strftime("%d")) == str(modified.strftime("%d")):
                    if str(now.strftime("%H")) == str(modified.strftime("%H")):
                        if str(now.strftime("%M")) == str(modified.strftime("%M")):
                            return '방금'
                        else:
                            timeLap = int(now.strftime("%M")) - int(modified.strftime("%M"))
                            message = str(timeLap) + '분 전'
                            return message
                    else:
                        now = int(now.strftime("%H"))*60 + int(now.strftime("%M"))
                        modified = int(modified.strftime("%H"))*60 + int(modified.strftime("%M"))
                        timeLap = now - modified
                        if timeLap >= 60:
                            message = str(timeLap//60) + '시간 전'
                        else:
                            message = str(timeLap) + '분 전'
                        return message
                else:
                    return modified
            else:
                return modified
        else:
            return modified

class TeamReply(models.Model):
    user = models.ForeignKey(FNSUser, on_delete=models.CASCADE)
    post = models.ForeignKey(TeamMatching, related_name="postReply", on_delete = models.CASCADE)
    comment = models.ForeignKey(TMComment, related_name="reply", on_delete= models.CASCADE, null = True, blank = True)
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.name

    def passedTime(self):
        now = datetime.datetime.now()
        modified = self.modified
        if str(now.strftime("%Y")) == str(modified.strftime("%Y")):
            if str(now.strftime("%m")) == str(modified.strftime("%m")):
                if str(now.strftime("%d")) == str(modified.strftime("%d")):
                    if str(now.strftime("%H")) == str(modified.strftime("%H")):
                        if str(now.strftime("%M")) == str(modified.strftime("%M")):
                            return '방금'
                        else:
                            timeLap = int(now.strftime("%M")) - int(modified.strftime("%M"))
                            message = str(timeLap) + '분 전'
                            return message
                    else:
                        now = int(now.strftime("%H"))*60 + int(now.strftime("%M"))
                        modified = int(modified.strftime("%H"))*60 + int(modified.strftime("%M"))
                        timeLap = now - modified
                        if timeLap >= 60:
                            message = str(timeLap//60) + '시간 전'
                        else:
                            message = str(timeLap) + '분 전'
                        return message
                else:
                    return modified 
            else:
                return modified
        else:
            return modified

class Recruiting(models.Model):
    user = models.ForeignKey(FNSUser, on_delete=models.CASCADE, null=True)
    applied_player = models.ManyToManyField(FNSUser, related_name="applied_player", blank=True)
    accepted_player = models.ManyToManyField(FNSUser, related_name="accepted_player", blank=True)
    title = models.CharField(max_length=80, null=False)
    content = models.TextField(null = False)

    time_from = models.DateTimeField()
    time_to = models.DateTimeField()

    sport = models.CharField(max_length=15, null = False, default = 'Futsal') #종목
    location = models.CharField(max_length=50, null=False)
    number = models.IntegerField()
    rank = models.CharField(max_length = 20)

    myteam = models.ForeignKey(Team, related_name="recruitMyTeam", on_delete=models.SET_NULL, null=True)
    vs_team = models.ForeignKey(Team, related_name="recruitVs_Team", on_delete=models.SET_NULL, null=True)
    
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.title

    def time(self):
        return time_from + '~' + time_to

    def summary(self):
        return self.content[:100]

    def total_player(self):
        return self.accepted_player.count()

    def total_comment(self):
        number = int(self.post.count()) + int(self.postReply.count())
        return number
    
class REComment(models.Model):
    user = models.ForeignKey(FNSUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Recruiting, related_name="post", on_delete = models.CASCADE)
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name

    def summary(self):
        return self.content[:20]

    def passedTime(self):
        now = datetime.datetime.now()
        modified = self.modified
        if str(now.strftime("%Y")) == str(modified.strftime("%Y")):
            if str(now.strftime("%m")) == str(modified.strftime("%m")):
                if str(now.strftime("%d")) == str(modified.strftime("%d")):
                    if str(now.strftime("%H")) == str(modified.strftime("%H")):
                        if str(now.strftime("%M")) == str(modified.strftime("%M")):
                            return '방금'
                        else:
                            timeLap = int(now.strftime("%M")) - int(modified.strftime("%M"))
                            message = str(timeLap) + '분 전'
                            return message
                    else:
                        now = int(now.strftime("%H"))*60 + int(now.strftime("%M"))
                        modified = int(modified.strftime("%H"))*60 + int(modified.strftime("%M"))
                        timeLap = now - modified
                        if timeLap >= 60:
                            message = str(timeLap//60) + '시간 전'
                        else:
                            message = str(timeLap) + '분 전'
                        return message
                else:
                    return modified
            else:
                return modified
        else:
            return modified

class RecruitingReply(models.Model):
    user = models.ForeignKey(FNSUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Recruiting, related_name="postReply", on_delete = models.CASCADE)
    comment = models.ForeignKey(REComment, related_name="reply", on_delete= models.CASCADE, null = True, blank = True)
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.name

    def passedTime(self):
        now = datetime.datetime.now()
        modified = self.modified
        if str(now.strftime("%Y")) == str(modified.strftime("%Y")):
            if str(now.strftime("%m")) == str(modified.strftime("%m")):
                if str(now.strftime("%d")) == str(modified.strftime("%d")):
                    if str(now.strftime("%H")) == str(modified.strftime("%H")):
                        if str(now.strftime("%M")) == str(modified.strftime("%M")):
                            return '방금'
                        else:
                            timeLap = int(now.strftime("%M")) - int(modified.strftime("%M"))
                            message = str(timeLap) + '분 전'
                            return message
                    else:
                        now = int(now.strftime("%H"))*60 + int(now.strftime("%M"))
                        modified = int(modified.strftime("%H"))*60 + int(modified.strftime("%M"))
                        timeLap = now - modified
                        if timeLap >= 60:
                            message = str(timeLap//60) + '시간 전'
                        else:
                            message = str(timeLap) + '분 전'
                        return message
                else:
                    return modified
            else:
                return modified
        else:
            return modified

class League(models.Model):
    manager = models.ForeignKey(FNSUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50, blank=False)
    content = models.TextField(max_length=500)
    location = models.CharField(max_length=50)
    time_from = models.DateTimeField()
    time_to = models.DateTimeField()
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now = True)\

    def __str__(self):
        return self.title

    def total_comment(self):
        number = int(self.post.count()) + int(self.postReply.count())
        return number

    def summary(self):
        return self.content[:100]

class LgPlayerAttendance(models.Model):
    player = models.ForeignKey(FNSUser, on_delete=models.CASCADE)
    match = models.ForeignKey(League, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.player.name

class LgTeamAttendance(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    match = models.ForeignKey(League, on_delete=models.CASCADE)

    def __str__(self):
        return self.team.name

class LGComment(models.Model):
    user = models.ForeignKey(FNSUser, on_delete=models.CASCADE)
    post = models.ForeignKey(League, related_name="post", on_delete = models.CASCADE)
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name

    def summary(self):
        return self.content[:20]

    def passedTime(self):
        now = datetime.datetime.now()
        modified = self.modified
        if str(now.strftime("%Y")) == str(modified.strftime("%Y")):
            if str(now.strftime("%m")) == str(modified.strftime("%m")):
                if str(now.strftime("%d")) == str(modified.strftime("%d")):
                    if str(now.strftime("%H")) == str(modified.strftime("%H")):
                        if str(now.strftime("%M")) == str(modified.strftime("%M")):
                            return '방금'
                        else:
                            timeLap = int(now.strftime("%M")) - int(modified.strftime("%M"))
                            message = str(timeLap) + '분 전'
                            return message
                    else:
                        now = int(now.strftime("%H"))*60 + int(now.strftime("%M"))
                        modified = int(modified.strftime("%H"))*60 + int(modified.strftime("%M"))
                        timeLap = now - modified
                        if timeLap >= 60:
                            message = str(timeLap//60) + '시간 전'
                        else:
                            message = str(timeLap) + '분 전'
                        return message
                else:
                    return modified
            else:
                return modified
        else:
            return modified

class LeagueReply(models.Model):
    user = models.ForeignKey(FNSUser, on_delete=models.CASCADE)
    post = models.ForeignKey(League, related_name="postReply", on_delete = models.CASCADE)
    comment = models.ForeignKey(LGComment, related_name="reply", on_delete= models.CASCADE, null = True, blank = True)
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.name

    def passedTime(self):
        now = datetime.datetime.now()
        modified = self.modified
        if str(now.strftime("%Y")) == str(modified.strftime("%Y")):
            if str(now.strftime("%m")) == str(modified.strftime("%m")):
                if str(now.strftime("%d")) == str(modified.strftime("%d")):
                    if str(now.strftime("%H")) == str(modified.strftime("%H")):
                        if str(now.strftime("%M")) == str(modified.strftime("%M")):
                            return '방금'
                        else:
                            timeLap = int(now.strftime("%M")) - int(modified.strftime("%M"))
                            message = str(timeLap) + '분 전'
                            return message
                    else:
                        now = int(now.strftime("%H"))*60 + int(now.strftime("%M"))
                        modified = int(modified.strftime("%H"))*60 + int(modified.strftime("%M"))
                        timeLap = now - modified
                        if timeLap >= 60:
                            message = str(timeLap//60) + '시간 전'
                        else:
                            message = str(timeLap) + '분 전'
                        return message
                else:
                    return modified
            else:
                return modified
        else:
            return modified