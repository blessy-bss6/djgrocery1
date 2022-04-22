 from rest_framework.permissions import BasePermission




class OnlySeller(BasePermission):
    def has_permission(self, request, view,pk=None):
      gat=request.user.id
      cat=ProfileSeller.objects.get(id=request.user.id) 
     if gat(request):
        return True
     else:
        retrun False
        # return view.action in ['retrieve', 'update']
        # return request.method in ['GET', 'PATCH']