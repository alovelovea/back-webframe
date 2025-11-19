from django.urls import path
from .views import (
    login_user,
    signup_user,
    classify_query_view,
    my_fridge,
    add_ingredient,
    delete_ingredient,
    toggle_like,
    fridge_items_api
)

urlpatterns = [
    # ✅ React 로그인 요청용 (POST: /api/login/)
    path('login/', login_user, name='login_user'),
    # React 회원가입
    path('signup/', signup_user, name='signup_user'),
    path('fridge_items/', fridge_items_api, name='fridge_items_api'),

    # ✅ GPT 이미지 분석용 (HTML 폼에서 {% url 'classify_query' %}와 매칭)
    path('classify/', classify_query_view, name='classify_query'),

    # ✅ 냉장고 관련 API
    path('my_fridge/', my_fridge, name='my_fridge'),
    path('add_ingredient/', add_ingredient, name='add_ingredient'),
    path('delete_ingredient/<int:fridge_id>/', delete_ingredient, name='delete_ingredient'),
    path('toggle_like/<int:recipe_id>/', toggle_like, name='toggle_like'),
]
