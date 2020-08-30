from rest_framework.permissions import BasePermission, SAFE_METHODS

# from customer.models import User


class IsStaffOrOwner(BasePermission):
    message = "You do not have the permission to perform this action."

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.user.is_student() and view.action == "list"
        ):
            return False
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user.id == obj.id or request.user.is_tpo() or request.user.is_co()
        )


class IsTPOOrReadOnly(BasePermission):
    message = "You do not have the permission to perform this action."

    def has_permission(self, request, view):
        if view.action == "create":
            return request.user.is_authenticated and request.user.is_tpo()
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action == "retrieve":
            return True
        return request.user.is_authenticated and request.user.is_tpo()


class IsStaff(BasePermission):
    message = "You do not have the permission to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_co() or request.user.is_tpo()
        )

    def has_object_permission(self, request, view, obj):
        return True


class ApplicationPermissions(BasePermission):
    message = "You do not have the permission to perform this action."

    def has_permission(self, request, view):
        if view.action == "create":
            return request.user.is_authenticated and request.user.is_student()
            # Only students can apply
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action == "retrieve":
            return request.user.is_authenticated
            # All authenticated users can Retrieve applications

        return request.user.is_authenticated and request.user.is_tpo()
        # Only TPO can update applications


class IsStudentOrReadOnly(BasePermission):
    message = "You do not have required permission to perform this action"

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_student() and obj.email == request.user.email
        # Students can view, update and delete their profiles
