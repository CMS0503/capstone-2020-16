import json

from rest_framework import permissions
import os

# 생성 - 관리자
# 삭제 - 관리자
# 수정 - 관리자
# 보기 - 유저 + 관리자
from api.onepanman_api.util.getIp import get_client_ip


class UserReadOnly(permissions.BasePermission):

    # list 허용
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_staff
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        # retrieve 허용
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # 수정 삭제는 관리자만.
        return request.user.is_staff

# 생성 - 모두
# 삭제 - 본인 / 관리자
# 수정 - 본인 / 관리자
# 보기 - 유저 + 관리자
class OnlyMyandAdmin(permissions.BasePermission):

    # list허용
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        # retrieve 허용
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # 수정 삭제는 본인과 관리자만
        return request.user.username == obj.username or request.user.is_staff

# 생성 - 모두
# 삭제 - 그룹장 / 관리자
# 수정 - 그룹장 / 관리자
# 보기 - 유저 + 관리자
class LeaderandAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        return request.user.username == obj.groupInfo.leader.username or request.user.is_staff

# 생성 - 모두
# 삭제 - 본인
# 수정 - 본인
# 보기 - 코드 공개 여부에 따라 본인 + 관리자 / 모두
class CodePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            if obj.author.userInfo.isCodeOpen is True:
                return request.user.is_authenticated
            else:
                return request.user.username == obj.author.username or request.user.is_staff

        return request.user.username == obj.author.username

# 생성 - 관리자
# 삭제 - 관리자
# 수정 - 관리자
# 보기 - 모두 ( 로그인 안해도 OK )
class ReadAll(permissions.BasePermission):
    # list 허용
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):

        # retrieve 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 수정 삭제는 관리자만.
        return request.user.is_staff

class game(permissions.BasePermission):

    isCore = False

    dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.secrets\\base.json')
    secrets_base = json.loads(open(dir, 'r').read())

    # list 허용
    def has_permission(self, request, view):
        ip = get_client_ip(request)

        if ip == self.secrets_base['CORE_IP']:
            self.isCore = True

        if request.method == "POST":
            return request.user.is_staff
        return request.user.is_authenticated or self.isCore

    def has_object_permission(self, request, view, obj):
        ip = get_client_ip(request)

        if ip == self.secrets_base['CORE_IP']:
            self.isCore = True

        # retrieve 허용
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # 수정 삭제는 관리자만.
        return request.user.is_staff or self.isCore