
from django.urls import path
from .views import (instagramGenel, instagramSiparisler, loginView,addInstagramUsers,dashboardView,apiOrdersView,
                    instagramUsersList, notLoginUsersView, sendVideoView, successfulValueView,userPackpagesView,usersDataView,servicesview,
                    apiSettingsView,importUsersView,exportUsersView,editServicesView,editUserPackpagesView,seoSettingsView,homeManagerView,
                    addProxyView,clearAccountsView,sendFollowView,sendPostCommentView,sendPostLikeView,sendDMMessageView,sendCommentLiveView,
                    sendLikeLiveView,sendWatchLiveView,savePhotoView,webApiContactView,webApiContactManage,sendDMTopluMessageView,
                    getUserFollowDataView,sendDMResimTopluMessageView,sendDMVideoTopluMessageView,sendAutoPostLikeView,sendDMIgTvTopluMessageView,
                    sendDMReelTopluMessageView,articleView,mentionControlView,usersScannerView,updateTxtCookieView,sendAutoFollowView,sendIgtvLinkDmView,
                    affirmationsView,sendReelLinkDmView,sendPostVideoLinkDmView,sendPostImageLinkDmView,userCategoryView,editUserCategoryView,usersActivePasifView,usersCategoriesUserList,
                    errorUsersView,notLoginOldUsersView,smtpSettingsView,sendProfilMessageDmView,sendProfilMessageDmLinkView,sendDMTopluMessageFollowersView,
                    sendDMResimTopluMessageFollowersView,sendDMVideoTopluMessageFollowersView,sendDMIgtvTopluMessageFollowersView,sendDMReelTopluMessageFollowersView,
                    sendPostImageLinkDmFollowersView,sendPostVideoLinkDmFollowersView,sendPostIGTVLinkDmFollowersView,sendPostReelLinkDmFollowersView,sendProfilMessageDmFollowersView,
                    sendProfilMessageDmLinkFollowersView,successfulValueEditView,successfulValueEditServiceView,sendProfileVisitView
                    )

app_name = 'custom_admin'

urlpatterns = [
    path('',loginView,name='login'),
    path('user-categories/',userCategoryView,name='user-categories'),
    path('user-categories/edit/<id>/',editUserCategoryView,name='edit-user-categories'),
    path('user-categories/user-list/<id>/',usersCategoriesUserList,name='cat-user-list'),

    path('active-pasif-users/',usersActivePasifView,name='active-pasif-users'),

    path('add-user/',addInstagramUsers,name='add-users'),
    path('notlogin-users/',notLoginUsersView,name='notlogin-users'),
    path('notlogin-old-users/',notLoginOldUsersView,name='notlogin-old-users'),

    path('error-users/',errorUsersView,name='error-users'),
    path('successful-value/',successfulValueView,name='successful-value'),
    path('successful-value/nchslj417gwwu5pqllh6mcxhv9xz518j3vhv5bm2/',successfulValueEditView,name='successful-value-edit'),
    path('successful-value/nchslj417gwwu5pqllh6mcxhv9xz518j3vhv5bm2/<id>/',successfulValueEditServiceView,name='successful-value-edit-service'),

    path('get-user-followdata/',getUserFollowDataView,name='get-user-followdata'),
    path('dashboard/',dashboardView,name='dashboard'),
    path('api-orders/',apiOrdersView,name='api-orders'),
    path('services/',servicesview,name='services'),
    path('services/edit/<int:id>/',editServicesView,name='edit-services'),
    path('users-list/',instagramUsersList,name='users-list'),
    path('seo-settings/',seoSettingsView,name='seo-settings'),
    path('smtp-settings/',smtpSettingsView,name='smtp-settings'),
    path('article/',articleView,name='article'),
    path('update-cookie-txt/',updateTxtCookieView,name='update-cookie-txt'),
    path('api-order-affirmations/',affirmationsView,name='api-order-affirmations'),

    path('import-users/',importUsersView,name='import-users'),
    path('export-users/',exportUsersView,name='export-users'),
    path('mention-control/',mentionControlView,name='mention-control'),
    path('users-scanner/',usersScannerView,name='users-scanner'),

    path('api-settings/',apiSettingsView,name='api-settings'),
    path('home-manager/',homeManagerView,name='home-manager'),
    path('add-proxy/',addProxyView,name='add-proxy'),
    path('clear-accounts/',clearAccountsView,name='clear-accounts'),
    
    path('user-packpages/',userPackpagesView,name='user-packpages'),
    path('user-packpages/edit/<int:id>/',editUserPackpagesView,name='edit-user-packpages'),
    path('user-packpages/data/',usersDataView,name='users-data'),

    path('api-contact/',webApiContactView,name='api-contact'),
    path('api-contact/manage/<str:host>/',webApiContactManage,name='api-contact-manage'),

    
    path('instagram/tools/send-follow/',sendFollowView,name='send-follow'),
    path('instagram/tools/auto-follow/',sendAutoFollowView,name='auto-follow'),

    path('instagram/tools/post-comment/',sendPostCommentView,name='post-comment'),
    path('instagram/tools/post-like/',sendPostLikeView,name='post-like'),
    path('instagram/tools/auto-post-like/',sendAutoPostLikeView,name='auto-post-like'),


    path('instagram/tools/instagram-genel/',instagramGenel,name='instagram-genel'),
    path('instagram/tools/instagram-siparisler/',instagramSiparisler, name='instagram-siparisler'),
    path('instagram/tools/profile-visit/',sendProfileVisitView,name='profile-visit'),
    path('instagram/tools/video-view/',sendVideoView,name='video-view'),


    path('instagram/tools/dm-message/',sendDMMessageView,name='dm-message'),
    path('instagram/tools/dm-collective-message/',sendDMTopluMessageView,name='dm-toplu-message'),
    path('instagram/tools/dmimage-collective-message/',sendDMResimTopluMessageView,name='dmresim-toplu-message'),
    path('instagram/tools/dmvideo-collective-message/',sendDMVideoTopluMessageView,name='dmvideo-toplu-message'),
    path('instagram/tools/dmigtv-collective-message/',sendDMIgTvTopluMessageView,name='dmigtv-toplu-message'),
    path('instagram/tools/dmreel-collective-message/',sendDMReelTopluMessageView,name='dmreel-toplu-message'),
    path('instagram/tools/igtvlink-collective-message/',sendIgtvLinkDmView,name='igtvlink-toplu-message'),
    path('instagram/tools/reellink-collective-message/',sendReelLinkDmView,name='reellink-toplu-message'),
    path('instagram/tools/postvideo-link-collective-message/',sendPostVideoLinkDmView,name='postvideo-link-toplu-message'),
    path('instagram/tools/postimage-link-collective-message/',sendPostImageLinkDmView,name='postimage-link-toplu-message'),
    path('instagram/tools/save-photos/',savePhotoView,name='save-photos'),
    path('instagram/tools/comment-live/',sendCommentLiveView,name='commnet-live'),
    path('instagram/tools/like-live/',sendLikeLiveView,name='like-live'),
    path('instagram/tools/watch-live/',sendWatchLiveView,name='watch-live'),

    # yeni eklenen özellikler
    path('instagram/tools/profile-message-dm/',sendProfilMessageDmView,name='profile-message-dm'),
    path('instagram/tools/profile-message-dm-link/',sendProfilMessageDmLinkView,name='profile-message-dm-link'),
    #yeni eklenen ozellikler takipci taramali islemler
    path('instagram/tools/profile-message-dm-followers/',sendProfilMessageDmFollowersView,name='profile-message-dm-followers'),
    path('instagram/tools/profile-message-dm-link-followers/',sendProfilMessageDmLinkFollowersView,name='profile-message-dm-link-followers'),

    # kullanıcı takipçi taramali islemler
    path('instagram/tools/dm-collective-message-followers/',sendDMTopluMessageFollowersView,name='dm-toplu-message-followers'),
    path('instagram/tools/dmresim-collective-message-followers/',sendDMResimTopluMessageFollowersView,name='dmresim-toplu-message-followers'),
    path('instagram/tools/dmvideo-collective-message-followers/',sendDMVideoTopluMessageFollowersView,name='dmvideo-toplu-message-followers'),
    path('instagram/tools/dmigtv-collective-message-followers/',sendDMIgtvTopluMessageFollowersView,name='dmigtv-toplu-message-followers'),
    path('instagram/tools/dmreel-collective-message-followers/',sendDMReelTopluMessageFollowersView,name='dmreel-toplu-message-followers'),
    # kullanıcı takipçi taramali ozel islemler
    path('instagram/tools/postimage-link-collective-message-followers/',sendPostImageLinkDmFollowersView,name='postimage-link-collective-message-followers'),
    path('instagram/tools/postvideo-link-collective-message-followers/',sendPostVideoLinkDmFollowersView,name='postvideo-link-collective-message-followers'),
    path('instagram/tools/igtv-link-collective-message-followers/',sendPostIGTVLinkDmFollowersView,name='igtv-link-collective-message-followers'),
    path('instagram/tools/reel-link-collective-message-followers/',sendPostReelLinkDmFollowersView,name='reel-link-collective-message-followers'),





]
