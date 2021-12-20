"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from backend.views import get_json_by_node_id_and_depth_from_neo4j, run_new_algorithm, get_all_algorithm, get_all_nodes, get_all_edges, get_all_devices, get_node_paths

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('node/', get_json_by_node_id_and_depth_from_neo4j),
    path('run_algorithm/', run_new_algorithm),
    path('get_algorithms/', get_all_algorithm),
    path('get_nodes/', get_all_nodes),
    path('get_edges/', get_all_edges),
    path('get_devices/', get_all_devices),
    path('get_node_paths/', get_node_paths),
]
