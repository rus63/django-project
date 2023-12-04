from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from main.admin import task_manager_admin_site
from main.services.single_resource import BulkRouter
from main.views import UserViewSet, TaskViewSet, TagViewSet, CurrentUserViewSet, UserTasksViewSet, TaskTagsViewSet

router = BulkRouter()
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"current-user", CurrentUserViewSet, basename="current_user")
users = router.register(r"users", UserViewSet, basename="users")

users.register(
    r"tasks",
    UserTasksViewSet,
    basename="user_tasks",
    parents_query_lookups=["assignee_id"],
)

tasks = router.register(r"tasks", TaskViewSet, basename="tasks")
tasks.register(
    r"tags",
    TaskTagsViewSet,
    basename="task_tags",
    parents_query_lookups=["task_id"],
)


schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager",
        default_version="v1",
        description="Task Manager description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", task_manager_admin_site.urls),
    path("api/", include(router.urls)),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
