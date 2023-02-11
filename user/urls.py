
from django.urls import path,include
from .views import (userView,otherProfileView,sendFollowView,
                    sendPostLikeView,sendPostCommentView,savePhotoView,sendWatchLiveView,sendLikeLiveView,sendCommentLiveView,
                    sendDMMessageView)
                                

app_name = 'user'
urlpatterns = [
    path('profile/<str:username>/',userView,name='user-page'),
    path('tools/other-profiles/',otherProfileView,name='otherprofiles'),
    path('tools/follow/',sendFollowView,name='follow'),
    path('tools/post-like/',sendPostLikeView,name='post-like'),
    path('tools/post-comment/',sendPostCommentView,name='post-comment'),
    path('tools/save-photo/',savePhotoView,name='save-photo'),
    path('tools/watch-live/',sendWatchLiveView,name='watch-live'),
    path('tools/like-live/',sendLikeLiveView,name='like-live'),
    path('tools/comment-live/',sendCommentLiveView,name='comment-live'),
    path('tools/dm-message/',sendDMMessageView,name='dm-message'),
]
