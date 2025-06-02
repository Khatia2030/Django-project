from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # მთავარი გვერდი და მომხმარებლის URL-ები
    path('', include('user.urls')),           # მთავარ URL-ზე user.urls
    path('user/', include('user.urls')),      # დამატებით /user/ მისამართზე

    # პროდუქტის აპის URL-ები
    path('shop/', include('shop.urls')),
]

# Debug Toolbar-ის URL-ები
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

# მედია ფაილების სერვინგი (განსაკუთრებით სურათებისთვის)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
