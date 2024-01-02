from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index,add_members,members_view,add_transactions,view_transactions,pay_transactions,view_transactions_due,transactions_report,addmembersprocess,view_member_details,updatememberdetails,editmembersprocess,removememberdetails,add_transactionsprocess,get_member_data,pay_transactionsprocess,removetransactions,transactions_due_report,get_paytransactionsData,edit_transactions,edit_paymenttransactions,edit_pay_transactionsprocess,remove_payment_transactions,edit_transactionprocess,members_view_afteraddmemberprocess,members_view_aftereditmemberprocess,view_paymenttransactions,main_page,admin_logout,authenticate_and_logged,admin_login

urlpatterns=[
    path('', index, name='index'),      # '' is initial url and index is function of views.py and index is name of parameter(optional), if you mentioned like {% url 'index' %} at template it will helps.
    path('add_members',add_members,name='add_members'), # add_members_view is url and add_members_view is function of views.py and add_member_view is name of parameter(optional), if you mentioned like {% url 'add_members_view' %} at template it will helps.
    path('members_view_afteraddmemberprocess',members_view_afteraddmemberprocess,name='members_view_afteraddmemberprocess'),
    path('members_view_aftereditmemberprocess',members_view_aftereditmemberprocess,name='members_view_aftereditmemberprocess'),
    path('members_view',members_view,name='members_view'),
    path('add_transactions',add_transactions,name='add_transactions'),
    path('view_transactions',view_transactions,name='view_transactions'),
    path('pay_transactions',pay_transactions,name='pay_transactions'),
    path('view_transactions_due',view_transactions_due,name='view_transactions_due'),
    path('transactions_report',transactions_report,name='transactions_report'),
    path('authenticate_and_logged',authenticate_and_logged,name='authenticate_and_logged'),
    path('admin_logout',admin_logout,name='admin_logout'),
    path('admin_login',admin_login,name='admin_login'),
    path('addmembersprocess',addmembersprocess,name='addmembersprocess'),
    path('viewmemberdetails/<str:memberid>',view_member_details,name='view_member_details'),
    path('updatememberdetails/<str:memberid>',updatememberdetails,name='updatememberdetails'),
    path('editmembersprocess/<str:memberid>',editmembersprocess,name='editmembersprocess'),
    path('removememberdetails/<str:memberid>',removememberdetails,name='removememberdetails'),
    path('add_transactionsprocess',add_transactionsprocess,name='add_transactionsprocess'),
    path('get_member_data/',get_member_data,name='get_member_data'),
    path('pay_transactionsprocess',pay_transactionsprocess,name='pay_transactionsprocess'),
    path('removetransactions/<str:memberidwithname>',removetransactions,name='removetransactions'),
    path('transactions_due_report',transactions_due_report,name='transactions_due_report'),
    path('get_paytransactionsData/',get_paytransactionsData,name='get_paytransactionsData'),
    path('edit_transactions/<str:memberidwithname>',edit_transactions,name='edit_transactions'),
    path('edit_transactionprocess',edit_transactionprocess,name='edit_transactionprocess'),
    path('edit_paymenttransactions/<str:paymentid2>/<str:memberIdwithname>',edit_paymenttransactions,name='edit_paymenttransactions'),
    path('edit_pay_transactionsprocess',edit_pay_transactionsprocess,name='edit_pay_transactionsprocess'),
    path('remove_payment_transactions/<str:paymentid>/<str:memberIdwithname>/',remove_payment_transactions,name='remove_payment_transactions'),
    path('view_paymenttransactions/<str:paymentId>',view_paymenttransactions,name='view_paymenttransactions'),
    path('main_page',main_page,name='main_page'),
]


# Add these lines at the end of the file for serving media files( to display media folder images ) 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)