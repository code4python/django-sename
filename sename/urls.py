from django.urls import path ,include
from . import views 
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('guests', views.viewsets_guest)
router.register('movie', views.viewsets_movie)
router.register('resv', views.viewsets_resv)


app_name = 'sename'
urlpatterns =[
    #1 no_rest _no model
    path('no_rest_no_model/', views.rest_no_model),
    
    #2 model date no rest
    path('model_no_rest/', views.model_no_rest),
    
    #3.1 FBV post get from restframework AS api_views
    path('rest/fbv/', views.FBV_List),
    
    #3.2 FBV post get delete from restframework AS api_views
    path('rest/fbv/<int:id>', views.FBV_pk),
    
    #4.1 CBN post get from restframework as ApiViews
    path('rest/cbv/', views.Cbv_List.as_view()),
    
    #4.2 CBV put get delete as restframework as ApiViews
    path('rest/cbv/<int:id>', views.CVB_pk.as_view()),
   
   #5.1 CBV post get  as restframework as mixins
    path('rest/mixins/', views.mixins_list.as_view()),
   
   #5.2 CBV put get delete as restframework as mixins
    path('rest/mixins/<int:pk>', views.mixins_pk.as_view()),
    
   
   #6.1 CBV put get delete as restframework as generics
    path('rest/generics/', views.generics_list.as_view()),
    
    #6.2 CBV put get delete as restframework as generics
    path('rest/generics/<int:pk>', views.generics_pk.as_view()),
    
    
    #7 CBV put get delete as restframework as viewesets
    path('rest/viewests/',include(router.urls) ),
    
    
    #7.1 CBV put get delete as restframework as viewesets
    path('rest/viewests/',include(router.urls) ),
    
    
    #7.2 CBV put get delete as restframework as viewesets
    path('rest/viewests/',include(router.urls) ),
    
    #8 find movie
    path('fbv/findmovie/', views.find_movie),
    
    #9 create reservation
    path('fbv/new_res/', views.new_reservation),
    
    #10 token 
    path('api-token-auth/', obtain_auth_token),
    
    
    #6.2 CBV put get delete as restframework as generics
    path('rest/post/<int:pk>', views.Post_pk.as_view()),
    
    


]