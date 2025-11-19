from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ React와 통신하는 API는 /api/로 통일
    path('api/', include('apis.urls')),

    # ✅ 기본 루트('/') 접속 시 my_fridge로 이동 (선택사항)
    path('', lambda request: redirect('my_fridge')),
]

# ⚙️ 개발 중 미디어 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
