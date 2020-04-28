from django.db import models
from model_utils.models import TimeStampedModel
from account.models import FNSUser
from match.models import PersonalMatching, TeamMatching, Recruiting, League, PersonalComment, TMComment, LGComment, REComment
from team.models import Team
# Create your models here.
class Notification(models.Model):
    joinTeam = 'joinTeam'
    teamAccepted = 'teamAccepted'
    teamApplicationDenied = 'teamApplicationDenied'
    suggestTeamMatching = 'suggestTeamMatching' 
    acceptSuggestion = 'acceptSuggestion'
    denySuggestion = 'denySuggestion'

    prComment = 'prComment'
    teamComment = 'teamComment'
    recruitingComment = 'recruitingComment'
    leagueComment = 'leagueComment'

    personalReply = 'personalReply'
    teamReply = 'teamReply'
    recruitingReply = 'recruitingReply'
    leagueReply = 'leagueReply'

    personalApply = 'personalApply'
    personalAccept = 'personalAccept'
    personalDeny = 'personalDeny'

    teamMatchingApply = 'teamMatchingApply'
    recruitingApply = 'recruitingApply'
    recruitingAccepted = 'recruitingAccepted'
    recruitingDenied = 'recruitingDenied'
    leaguePersonalApply = 'leaguePersonalApply'
    leagueTeamApply = 'leagueTeamApply'
    
    resultInput = 'resultInput'
    resultEdit = 'resultEdit'
    resultConfirm = 'resultConfirm'

    TYPE_CHOICES = {
        (joinTeam, 'joinTeam'),
        (teamAccepted, 'teamAccepted'),
        (teamApplicationDenied, 'teamApplicationDenied'),
        (suggestTeamMatching, 'suggestTeamMatching') ,
        (prComment, 'prComment'),
        (teamComment, 'teamComment'),
        (recruitingComment, 'recruitingComment'),
        (leagueComment, 'leagueComment'),
        (personalApply, 'personalApply'),
        (personalAccept, 'personalAccept'),
        (personalDeny, 'personalDeny'),
        (teamMatchingApply, 'teamMatchingApply'),
        (recruitingApply, 'recruitingApply'),
        (recruitingAccepted, 'recruitingAccepted'),
        (recruitingDenied, 'recruitingDenied'),
        (leaguePersonalApply, 'leaguePersonalApply'),
        (leagueTeamApply, 'leagueTeamApply'),
        (personalReply, 'personalReply'),
        (teamReply, 'teamReply'),
        (recruitingReply, 'recruitingReply'),
        (leagueReply, 'leagueReply'),
        (acceptSuggestion, 'acceptSuggestion'),
        (denySuggestion, 'denySuggestion'),
        (resultInput, 'resultInput'),
        (resultEdit,'resultEdit'),
        (resultConfirm, 'resultConfirm'),
        
    }

    creator = models.ForeignKey(FNSUser, on_delete= models.CASCADE, null=True, related_name='creator')
    to = models.ForeignKey(FNSUser, on_delete= models.CASCADE, null=True, related_name='to')
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    personalMatching = models.ForeignKey(PersonalMatching, on_delete=models.CASCADE, null=True, blank=True)
    teamMatching = models.ForeignKey(TeamMatching, on_delete=models.CASCADE, null=True, blank=True)
    recruiting = models.ForeignKey(Recruiting, on_delete=models.CASCADE, null=True, blank=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank = True)
    text = models.TextField(null=True, blank=True)
    userCheck = models.BooleanField(default=False)

    personalComment = models.ForeignKey(PersonalComment, on_delete=models.CASCADE, null=True, blank=True)
    tmComment = models.ForeignKey(TMComment, on_delete=models.CASCADE, null=True, blank=True)
    reComment = models.ForeignKey(REComment, on_delete=models.CASCADE, null=True, blank=True)
    lgComment = models.ForeignKey(LGComment, on_delete=models.CASCADE, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def joinTeamText(self):
        self.text = self.creator.name + '님이 [' + self.team.name + ']팀에 가입신청을 했습니다.'
        self.save()

    def teamAcceptedText(self):
        self.text = '[' + self.team.name + ']팀에 가입되었습니다.'
        self.save()

    def teamApplicationDeniedText(self):
        self.text = '[' + self.team.name + ']팀에서 가입신청을 거절했습니다.'
        self.save()

    def personalCommentText(self):
        self.text = self.creator.name + '님이 [개인매칭]글에 댓글을 남겼습니다.'
        self.save()

    def teamCommentText(self):
        self.text = self.creator.name + '님이 [팀매칭]글에 댓글을 남겼습니다.'
        self.save()
    
    def recruitingCommentText(self):
        self.text = self.creator.name + '님이 [' + self.recruiting.title + ']글에 댓글을 남겼습니다.'
        self.save()

    def leagueCommentText(self):
        self.text = self.creator.name + '님이 [' + self.league.title + ']글에 댓글을 남겼습니다.'
        self.save()

    def teamJoinText(self):
        self.text = self.creator.name + '님이 [' + self.team.name + ']에 가입신청을 했습니다.'
        self.save()

    def suggestTeamMatchingText(self):
        self.text = self.creator.name + '님이 [' + self.team.name + ']에 매칭신청을 했습니다.'
        self.save()

    def acceptSuggestionText(self):
        self.text = '[' + self.team.name + ']팀이 매치신청을 수락했습니다.'
        self.save()

    def denySuggestionText(self):
        self.text = '[' + self.team.name + ']팀이 매치신청을 거절했습니다.'
        self.save()

    def personalApplyText(self):
        self.text = self.creator.name + '님이 개인매칭 [' + self.personalMatching.content[:20] + ']에 참가신청을 했습니다.'
        self.save()

    def personalAcceptText(self):
        self.text = self.creator.name + '님이 개인매칭 참가신청을 수락했습니다.'
        self.save()

    def personalDenyText(self):
        self.text = self.creator.name + '님이 개인매칭 참가신청을 거절했습니다.'
        self.save()

    def teamMatchingApplyText(self):
        self.text = '[' + self.creator.teamname.name + ']팀이 [' + self.teamMatching.myTeam.name + ']에 팀매치신청을 했습니다.'
        self.save()

    def recruitingApplyText(self):
        self.text = self.creator.name + '님이 [' + self.recruiting.title + ']에 용병신청을 했습니다.'
        self.save()

    def recruitingAcceptedText(self):
        self.text = ' [' + self.recruiting.title + '] 용병신청이 수락되었습니다.'
        self.save()

    def recruitingDeniedText(self):
        self.text = self.creator.name + '님이 회원님의 [' + self.recruiting.title + '] 용병신청을 거절하였습니다.'
        self.save()

    def leaguePersonalApplyText(self):
        self.text = self.creator.name + '님이 [' + self.league.title + ']에 개인참여신청을 했습니다.'
        self.save()

    def leagueTeamApplyText(self):
        self.text = '[' + self.creator.teamname.name + ']팀이 [' + self.league.title + ']에 팀참여신청을 했습니다.'
        self.save()

    def personalReplyText(self):
        self.text = self.creator.name + '님이 회원님의 댓글에 답글을 작성했습니다.' + self.personalComment.summary() +'...'
        self.save()

    def teamReplyText(self):
        self.text = self.creator.name + '님이 회원님의 댓글에 답글을 작성했습니다.' + self.tmComment.summary() +'...'
        self.save()

    def recruitingReplyText(self):
        self.text = self.creator.name + '님이 회원님의 댓글에 답글을 작성했습니다.' + self.reComment.summary() +'...'
        self.save()

    def leagueReplyText(self):
        self.text = self.creator.name + '님이 회원님의 댓글에 답글을 작성했습니다.' + self.lgComment.summary() +'...'
        self.save()

    def resultInputText(self):
        self.text = self.team.name + '팀이 [' + self.teamMatching.title + '] 경기의 점수를 입력했습니다.'
        self.save()

    def resultEditText(self):
        self.text = self.team.name + '팀이 [' + self.teamMatching.title + '] 경기의 점수를 수정했습니다.'
        self.save()

    def resultConfirmText(self):
        self.text = self.team.name + '팀이 [' + self.teamMatching.title + '] 경기의 결과를 확정했습니다.'
        self.save()
   