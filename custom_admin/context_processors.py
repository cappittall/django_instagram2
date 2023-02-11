from .models import SeoSettings

def seoSettings(request):

    seo = SeoSettings.objects.all().last()
    if seo:
        return {
            'ana_title':seo.ana_title,
            'description':seo.description,
            'keywords':seo.keywords,
            'google_tag':seo.google_tag,
            'site_logo':seo.site_logo,
            'admin_logo':seo.admin_logo,
            'fav_icon':seo.fav_icon,
            'insta_user_login_':seo.user_logins,
            }
    else:
        return {
            'ana_title':'',
            'description':'',
            'keywords':'',
            'google_tag':'',
            'site_logo':'',
            'admin_logo':'',
            'fav_icon':'',
            'insta_user_login_':True,
            }        