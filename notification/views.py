from django.shortcuts import render, get_object_or_404, redirect, reverse
from rest_framework.views import APIView
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import serializers
from account.models import FNSUser
from match.models import PersonalMatching
from .models import Notification

# Create your views here.

def create_notification(creator, to, notification_type, personalMatching=None, comment=None):
    notification = models.Notification.objects.create(
        creator = creator,
        to=to,
        notification_type=notification_type,
        personalMatching = personalMatching,
        comment = comment
    )
    notification.save()

def checkAllNotification(request):
    pk = request.session.get('userId')
    fnsuser = get_object_or_404(FNSUser, pk=pk)
    notification = Notification.objects.all().filter(to=fnsuser)
    for alarm in notification:
        alarm.userCheck = True
        alarm.save()

    return HttpResponse()


def checkNotification(request, notification_id):
    notification = get_object_or_404(Notification, pk = notification_id)
    notification.userCheck = True
    notification.save()

    return HttpResponse()

# class Notification(APIView):

#     def get(self, request, format=None):
#         user = get_object_or_404(FNSUser, pk = request.session.get('userId'))
#         notifications = Notification.objects.filter(to=user)
#         serializer = serializers.NotificationSerializer(notifications, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)

# class NotificationSerializer(serializers.ModelSerializer):

#     creator = user_serializers.ListUserSerializer()
#     image = image_serializers.SmallImageSerializer()

#     class Meta:
#         model = models.Notification
#         fields = '__all__'

# class CommentOnPersonal(APIView):
#     def post(self, request, personalMatching_id, format=None):
#         user = get_object_or_404(FNSUser, pk = request.session.get('userId'))

#         try:
#             selectedPersonal = PersonalMatching.objects.get(id=personalMatching_id)

#         except models.Image.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         serializer = serializers.CommentSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save(creator=user, personalMatching=selectedPersonal)
#             notification_views.create_notification(user, selectedPersonal.)

# def joinTeamCheck(request, notification_id):
#     notification = get_object_or_404(Notification, pk = notification_id)
#     notification.userCheck = True
#     notification.save()

#     return HttpResponse()

# def teamAcceptedCheck(request, notification_id):
#     notification = get_object_or_404(Notification, pk = notification_id)
#     notification.userCheck = True
#     notification.save()

#     return HttpResponse()

# def personalCommentCheck(request, notification_id):
#     notification = get_object_or_404(Notification, pk = notification_id)
#     notification.userCheck = True
#     notification.save()

#     return HttpResponse()

# def teamCommentCheck(request, notification_id):
#     notification = get_object_or_404(Notification, pk = notification_id)
#     notification.userCheck = True
#     notification.save()

#     return HttpResponse()

# def recruitingCommentCheck(request, notification_id):
#     notification = get_object_or_404(Notification, pk = notification_id)
#     notification.userCheck = True
#     notification.save()

#     return HttpResponse()

# def leagueCommentCheck(request, notification_id):
#     notification = get_object_or_404(Notification, pk = notification_id)
#     notification.userCheck = True
#     notification.save()

#     return HttpResponse()

# def teamJoinCheck(request, notification_id):
#     notification = get_object_or_404(Notification, pk = notification_id)
#     notification.userCheck = True
#     notification.save()

#     return HttpResponse()

# def suggestTeamMatchingCheck(request, notification_id):
#     notification = get_object_or_404(Notification, pk = notification_id)
#     notification.userCheck = True
#     notification.save()

#     return HttpResponse()

# def personalApplyCheck(request, notification_id):
#     notification = get_object_or_404(Notification, pk = notification_id)
#     notification.userCheck = True
#     notification.save()

#     return HttpResponse()

# def teamMatchingApplyCheck(request, notification_id):
#     notification = get_object_or_404(Notification, pk = notification_id)
#     notification.userCheck = True
#     notification.save()

#     return HttpResponse()

# def recruitingApplyCheck(request, notification_id):
#     notification = get_object_or_404(Notification, pk = notification_id)
#     notification.userCheck = True
#     notification.save()

#     return HttpResponse()

# def recruitingAcceptedCheck(request, notification_id):
#     notification = get_object_or_404(Notification, pk = notification_id)
#     notification.userCheck = True
#     notification.save()

#     return HttpResponse()

# def leaguePersonalApplyCheck(request, notification_id):
#     notification = get_object_or_404(Notification, pk = notification_id)
#     notification.userCheck = True
#     notification.save()

#     return HttpResponse()

# def leagueTeamApplyCheck(request, notification_id):
#     notification = get_object_or_404(Notification, pk = notification_id)
#     notification.userCheck = True
#     notification.save()

#     return HttpResponse()