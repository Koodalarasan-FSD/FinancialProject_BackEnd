from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib import messages

from .forms import MemberForm,TransactionsForm,PaymentsForm
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from .models import Member,transactions,payments
from django.db import connection



# Create your views here.
def index(request):
    if not request.session.get('adminlogged_in',False):
        return redirect('admin_login')
    else:
        return render(request,'index.html')

def authenticate_and_logged(request):
    if request.method=='POST':
        adminid=request.POST.get('adminid')
        password=request.POST.get('adminpassword')
        
        #Query the database
        with connection.cursor() as cursor:
            cursor.execute("SELECT adminid,adminpassword FROM admindb  WHERE adminid=%s AND adminpassword=%s", [adminid, password])
            admin_data=cursor.fetchall()

        
        #print(admin_data)

        if admin_data:

            # Set session variables
            request.session['adminlogged_in'] = True
            return JsonResponse({'status': 200})
        else:
            error_messages='Check Entered ID and PassWord'
            return JsonResponse({'status':400,'error':error_messages})

    
 
def admin_login(request):
    return render(request,'adminlogin.html')   

def main_page(request):
    
    if not request.session.get('adminlogged_in',False):
        return redirect('admin_login')
    else:
        return render(request,'index.html')

def admin_logout(request):
    
    # Clear the session variables related to admin login
    request.session.pop('adminlogged_in',None)
    
    # Redirect to the login page or any other desired page
    return redirect('admin_login')


def add_members(request):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:
        # Generate a unique identifier(ID)
        unique_identifier=get_random_string(length=5,allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        memberid='FIN'+unique_identifier

        # Ensure the generated unique_id is indeed unique
        while Member.objects.filter(memberid=memberid).exists():
            unique_identifier=get_random_string(length=5,allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            memberid='FIN'+unique_identifier

        # Pass the unique_id as context data to the template
        context={'memberid':memberid}
        
        return render(request,'add-members.html',context)


def members_view(request):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:
    
        # Retrieve all fields from the database
        members = Member.objects.all()                  # Member is Name of Model class in models.py
        
        # Pass the members to the template context
        context={'members':members}
        
        # Render the template with the context
        return render(request,'view-members.html',context)

def members_view_afteraddmemberprocess(request):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:
    
        # Retrieve all fields from the database
        members = Member.objects.all()                  # Member is Name of Model class in models.py
        
        # Pass the members to the template context
        context={'members':members}

        messages.success(request,"New Member Added\U0001F4AF\U0001F4AF\U0001F4AF")
        
        # Render the template with the context
        return render(request,'view-members.html',context)

def members_view_aftereditmemberprocess(request):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:
    
        # Retrieve all fields from the database
        members = Member.objects.all()                  # Member is Name of Model class in models.py
        
        # Pass the members to the template context
        context={'members':members}

        messages.success(request,"One of Member Detail Edited\U0001F4AF\U0001F4AF\U0001F4AF")
        
        # Render the template with the context
        return render(request,'view-members.html',context)



    

def addmembersprocess(request):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:
        if request.method == "POST":
            form =MemberForm(request.POST,request.FILES)

            if form.is_valid():
                #member_id=form.cleaned_data['memberid']
                #print(member_id)

                # Print some debugging information
                #print(request.FILES)

                form.save() # This line handles the database insertion automatically if the form is valid
                
                
                # Return a JSON response indicating success
                return JsonResponse({'status':200})
            
            else:
                error_messages=form.errors.as_text()
                #print(error_messages)
            
                messages.success(request,error_messages)
        
        # If the request method is not POST or the form is not valid, render the form page
        return render(request,'add-members.html',{'form':MemberForm()})

def view_member_details(request,memberid):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:

        # Retrieve member details from database based on (or) where member_id
        member=get_object_or_404(Member,memberid=memberid)

        # Pass the retrieved member details to the template context
        context={'memberid':memberid,'member':member}

        return render(request,'view-member-details.html',context)

def updatememberdetails(request,memberid):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:

        # Retrieve member details(all values with all field) from database based on (or) where member_id
        member=get_object_or_404(Member,memberid=memberid)

        # Pass the retrieved member details and memberid to the template context
        context={"memberid":memberid,'member':member}

        return render(request,'edit-members.html',context)




def editmembersprocess(request,memberid):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:
    
    
        if request.method == "POST":
            form = MemberForm(request.POST, request.FILES)

            if form.is_valid():
                
                # Retrieve joiningdate from the form data
                joiningdate = form.cleaned_data.get('joiningdate')

                # Get existing record(for ex: where memberid="FINAE364") or create a new one
                instance, created = Member.objects.get_or_create(memberid=memberid, defaults=form.cleaned_data)

                # If the record was not created, update it with the new form data
                if not created:
                    for field, value in form.cleaned_data.items():
                        # Exclude updating joiningdate if it is empty
                        if field == 'joiningdate' and not value:
                            continue
                        setattr(instance, field, value)

                    instance.save()
                

                return JsonResponse({'status': 200})

            return JsonResponse({'status': 400, 'error': form.errors.as_text()})

        return JsonResponse({'status': 400, 'error': 'Invalid request'})

def removememberdetails(request,memberid):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:

        # Retrieve the existing record(for ex: where memberid="FINAE364") or return a 404 if not found 
        member=get_object_or_404(Member, memberid=memberid)

        # Delete that record
        member.delete()


        #After Removing record,  Retrieve all members from the database
        members = Member.objects.all()                                    # Member is Name of Model class in models.py
        
        # Pass the members to the template context
        context={'members':members}

        messages.success(request,"Deleted One of Member Detail")
        
        # Render the template with the context
        return render(request,'view-members.html',context)



def add_transactions(request):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:
    
        # Retrieve particular fields(memberid, membername) from database
        members=Member.objects.values('memberid','membername')
        
        currentperiod=1

        # Generate a unique identifier(ID)
        unique_identifier=get_random_string(length=5,allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        paymentid='PAY'+unique_identifier

        # Ensure the generated unique_id is indeed unique--checking generated unique_id is already exists in the database or not.
        while transactions.objects.filter(paymentid=paymentid).exists():
            unique_identifier=get_random_string(length=5,allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            paymentid='PAY'+unique_identifier
        
        # Pass the context data in a dictionary
        context={'members':members,"paymentid":paymentid,'currentperiod':currentperiod}
        return render(request,'add-transactions.html',context)

def add_transactionsprocess(request):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:

        if request.method=="POST":
            form=TransactionsForm(request.POST)

            # Saving Initial Transaction both in transactionstable and paymentstable

            if form.is_valid():

                
                # Saving Initial Transaction data in transactionstable
                transactions_instance=form.save()   

            
                # Create an instance of payments and populate it with the same data
                payment_instance = payments(
                    memberidwithname=transactions_instance.memberidwithname,
                    paymentid=transactions_instance.paymentid,
                    amount=transactions_instance.amount,
                    #noofperiods=transactions_instance.noofperiods,
                    #paymentdurationtype=transactions_instance.paymentdurationtype,
                    basisamounttopay=transactions_instance.basisamounttopay,
                    basisamounttopayable=transactions_instance.basisamounttopayable,
                    
                    balanceamounttopay=transactions_instance.balanceamounttopay,
                    currentperiod=transactions_instance.currentperiod,
                    description=transactions_instance.description,
                    transactiondate=transactions_instance.transactiondate,
                )

                # Saving Initial Transaction data in paymentstable
                payment_instance.save()


                # After saving(insertion), Retrieve all fields from the table(transactionstable)
                #transactionsdetail=transactions.objects.all  # transactionsdetail is Name of Model class in models.py

                # Pass the members to the template context
                #context={'transactionsdetail':transactionsdetail}

                messages.success(request, "New Transactions Added!")

                # redirect to url
                return redirect('view_transactions')
            
            else:
                error_messages=form.errors.as_text()
                return JsonResponse({'status':400,'error':error_messages})
        
        # If the request method is not POST or the form is not valid, render the form page
        return render(request,'add-members.html',{'form':MemberForm()})

def view_transactions(request):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:


        # Retrieve all fields from the database
        transactionsdetail=transactions.objects.all  # transactions is Name of Model class in models.py

        # Pass the members to the template context
        context={'transactionsdetail':transactionsdetail}

        # Render the template with the context
        return render(request,'view-transactions.html',context)

def pay_transactions(request):

    if  not request.session.get('adminlogged_in'):
        return redirect('admin_login')
   
    else:
    
        # Retrieve particular fields(memberidwithname) from database
        transactionsdetail=transactions.objects.values('memberidwithname')

        # Generate a unique identifier(ID)
        unique_identifier=get_random_string(length=5,allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        paymentid='PAY'+unique_identifier

        # Ensure the generated unique_id is indeed unique--checking generated unique_id is already exists in the database or not.
        while transactions.objects.filter(paymentid=paymentid).exists() and payments.objects.filter(paymentid=paymentid).exists() :
            unique_identifier=get_random_string(length=5,allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            paymentid='PAY'+unique_identifier

        return render(request,'pay-transactions.html',{'transactionsdetail':transactionsdetail,'paymentid':paymentid})

def transactions_due_report(request):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:
    
        # Retrieve particular fields(memberidwithname) from database
        paymentsdetail=payments.objects.values('memberidwithname')

        return render(request,'transactions_due_report.html',{'paymentsdetail':paymentsdetail})

def get_paytransactionsData(request):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:

        if request.method=="POST":
            
            # To receive value from html form
            memberidwithname=request.POST.get('memberidwithname',None)
            #print("memberidwithname is",memberidwithname)

            if memberidwithname is not None:
                
                # Retrieving all fields where memberidwithname
                payments_data=payments.objects.filter(memberidwithname=memberidwithname)

                #print(payments_data)

                # Pass the members to the template context
                context={'payments_data':payments_data}

                # Render the template with the context
                return render(request,"pay_transactions_due_table.html",context)





def get_member_data(request):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:
        memberidwithname=request.GET.get('memberidwithname',None)

        if memberidwithname is not None:
            member_data=transactions.objects.filter(memberidwithname=memberidwithname).first()
            
            
            if member_data:
                combined_period_info=f"{member_data.currentperiod} out of {member_data.noofperiods} {member_data.paymentdurationtype}"
                
                data={
                    
                    
                    "amount": member_data.amount,
                    "balanceamounttopay": member_data.balanceamounttopay,
                    "basisamounttopayable":member_data.basisamounttopayable,
                    "basisamounttopay": member_data.basisamounttopay,
                    "currentperiod":member_data.currentperiod,
                    "combined_period_info": combined_period_info,
                    "noofperiods":member_data.noofperiods,
                    "paymentdurationtype":member_data.paymentdurationtype
                }
                
                return JsonResponse(data)
            return HttpResponse(status=400)
    
def pay_transactionsprocess(request):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:

        if request.method =="POST":
            form=PaymentsForm(request.POST)
       
            if form.is_valid():
                payment_instance=form.save()

            # Check if currentperiod is 10
            if payment_instance.balanceamounttopay == 0:
                status = "Payments Completed"
                # Update values in the transactions table
                transactions.objects.filter(memberidwithname=payment_instance.memberidwithname).update(balanceamounttopay=payment_instance.balanceamounttopay,currentperiod=payment_instance.currentperiod,status=status)
        
            else:
                status = "Payment Ongoing"
                # Update values in the transactions table
                transactions.objects.filter(memberidwithname=payment_instance.memberidwithname).update(balanceamounttopay=payment_instance.balanceamounttopay,currentperiod=payment_instance.currentperiod,status=status)
        
        
            # Retrieve all fields from the database
            paymentsdetail=payments.objects.all
    
            # Pass the members to the template context
            context={"paymentsdetail":paymentsdetail}

            messages.success(request,"For One of Member, Payment Transaction Added\U0001F4AF\U0001F4AF\U0001F4AF")

            # Render the template with the context
            return render(request,'view-transactions-due.html',context)
       
       
        else:
            error_messages=form.errors.as_text()
            return JsonResponse({'status':400,'error':error_messages})
        
def view_transactions_due(request):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:

        # Retrieve all fields from the database
        paymentsdetail=payments.objects.all
        
        # Pass the members to the template context
        context={"paymentsdetail":paymentsdetail}

        # Render the template with the context
        return render(request,'view-transactions-due.html',context)


def transactions_report(request):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:

        # Retrieve all fields from the database
        transactionsdetail=transactions.objects.all  # transactions is Name of Model class in models.py

        # Pass the members to the template context
        context={'transactionsdetail':transactionsdetail}

        # Render the template with the context
        return render(request,'transactions-report.html',context)

def removetransactions(request,memberidwithname):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:

        # Get the particular object(Initial Transaction record) you want to delete record from transactionstable 
        record_to_delete=get_object_or_404(transactions,memberidwithname=memberidwithname)

        # Delete that object(Initial Transactions) from transactionstable
        record_to_delete.delete()

        initializecurrentperiod=1

        # And also Getting the particular object(Initial Transaction record) you want to delete Initial Transaction record from paymentstable 
        record_paymentstable_to_delete=get_object_or_404(payments,memberidwithname=memberidwithname,currentperiod=initializecurrentperiod)

        # Delete that object(Initial Transactions) from paymentstable
        record_paymentstable_to_delete.delete()

        # Sending message after deletion process 
        messages.success(request,"One of Initial Transaction Deleted ")

        return redirect("transactions_report")

def edit_transactions(request,memberidwithname):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:

        # Get the particular object(record) you want to edit record from database
        recordtoedit=get_object_or_404(transactions,memberidwithname=memberidwithname)

        # Pass the data to the template context
        context={"recordtoedit":recordtoedit,"memberidwithname":memberidwithname}

        # Render the template with the context
        return render(request,'edit-transactions.html',context)


# Below View Payment Transaction is not used, Commented in view-transactions-due.html
def view_paymenttransactions(request,paymentId):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:

        # Get the particular object(record) you want to edit record from database
        paymentrecordstoedit=get_object_or_404(payments,paymentid=paymentId)

        # Pass the members to the template context
        context={'paymentrecordstoedit':paymentrecordstoedit, "paymentid":paymentId}

        # Render the template with the context
        return render(request,'view_payment_transactions.html',context)





def edit_transactionprocess(request):
    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:
    
        if request.method=="POST":
            
            # Retrieve value id from submitted form inorder to update all values where id
            id=request.POST.get('id',None)
            
            # Retrieve the object from transactionstable to update
            record_to_update=get_object_or_404(transactions,id=id)

            # Update all fields with new values
            record_to_update.memberidwithname=request.POST.get('memberidwithname')
            record_to_update.paymentid=request.POST.get('paymentid')
            record_to_update.amount=request.POST.get('amount')
            record_to_update.noofperiods=request.POST.get('noofperiods')
            record_to_update.paymentdurationtype=request.POST.get('paymentdurationtype')
            record_to_update.basisamounttopay=request.POST.get('basisamounttopay')
            record_to_update.balanceamounttopay=request.POST.get('balanceamounttopay') 
            record_to_update.basisamounttopayable=request.POST.get('basisamounttopayable')
            record_to_update.currentperiod=request.POST.get('currentperiod')
            record_to_update.description=request.POST.get('description')
            record_to_update.transactiondate=request.POST.get('transactiondate')
            record_to_update.status=request.POST.get('status')

            # Save the updated transactionstable object
            record_to_update.save()

            # Retrieve value paymentid from submitted form inorder to update all values where paymentid
            paymentid=request.POST.get('paymentid',None)

            # Retrieve the object from paymentstable where paymentid to update
            particularpayments_record_to_update=get_object_or_404(payments,paymentid=paymentid)

            # Update all fields with new values
            particularpayments_record_to_update.memberidwithname=request.POST.get('memberidwithname')
            particularpayments_record_to_update.paymentid=request.POST.get('paymentid')
            particularpayments_record_to_update.amount=request.POST.get('amount')
            particularpayments_record_to_update.basisamounttopay=request.POST.get('basisamounttopay')
            particularpayments_record_to_update.balanceamounttopay=request.POST.get('balanceamounttopay') 
            particularpayments_record_to_update.basisamounttopayable=request.POST.get('basisamounttopayable')
            particularpayments_record_to_update.currentperiod=request.POST.get('currentperiod')
            particularpayments_record_to_update.description=request.POST.get('description')
            particularpayments_record_to_update.transactiondate=request.POST.get('transactiondate')
    

            # Save the updated paymentstable object
            particularpayments_record_to_update.save()

            # After Updation, Sending message
            messages.success(request,'One of Transaction is updated\U0001F4AF\U0001F4AF\U0001F4AF')
        
        return redirect('transactions_report')

def remove_payment_transactions(request,paymentid,memberIdwithname):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:
        
        # Retrieve the object from paymentstable to update
        payments_instance=payments.objects.filter(paymentid=paymentid).first()

        if payments_instance:
                
            # Retrieve currentperiod value
            currentperiodvalue=payments_instance.currentperiod
            #print("Before correction:",currentperiodvalue)


            # Increase currentperiod value by 1 inorder to check whether another(next) record found or not
            increased_currentperiodvalue= currentperiodvalue + 1

            #print("Incremented currentperiod:",increased_currentperiodvalue)

            
            # Retrieving datas where currentperiod and memberidwithname
            checkdata_where_currentperiodandmemberidwithname=payments.objects.filter(currentperiod=increased_currentperiodvalue,memberidwithname=memberIdwithname).values_list()
            

            # Checking whether another(next) record are found or not, if found means it's not last record so not allowed to delete.
            if checkdata_where_currentperiodandmemberidwithname:
                #print(checkdata_where_currentperiodandmemberidwithname)
                messages.success(request,"OOPS, YOU CAN DELETE ONLY NEW (or) LAST PAYMENT TRANSACTION\U0001F6AB ")
                return redirect("view_transactions_due")
                
            else:
                # Decrease the currentperiod value by 1
                decreased_currentperiodvalue=currentperiodvalue-1

                # Retrieving balanceamounttopay where currentperiod and memberidwithname
                balanceamounttopayrecord = payments.objects.filter(memberidwithname=memberIdwithname,currentperiod=decreased_currentperiodvalue).values('balanceamounttopay')

                # Retrieving values(fields) from transactionstable inorder to rollback(minusing currentperiod and replacing previous balanceamounttopay in it).
                transactiondb_instance=transactions.objects.filter(memberidwithname=memberIdwithname).first()

                if transactiondb_instance:
            
                    # Storing(replacing) Retrieved balanceamounttopay in transactionstable by using transactiondb_instance.balanceamounttopay
                    transactiondb_instance.balanceamounttopay=balanceamounttopayrecord

                    # Retrieve the currentperiod value
                    currentperiodvalue=transactiondb_instance.currentperiod

                    # Decrease the currentperiod value by 1 and storing transactiondb_instance.currentperiod
                    transactiondb_instance.currentperiod=currentperiodvalue-1

                    # After storing, now we're saving database
                    transactiondb_instance.save()
            
                # Get the particular object(record) where paymentid you want to delete record from database
                paymentrecord_to_delete=get_object_or_404(payments,paymentid=paymentid)
            
                # Delete that object
                paymentrecord_to_delete.delete()

                # After Deletion, Sending message 
                messages.success(request, "One of Payment Transaction is Deleted\U0001F622\U0001F622")
                return redirect('view_transactions_due')


def edit_paymenttransactions(request,paymentid2,memberIdwithname):
        
    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:

    
        #print("Payment_id:",paymentid2)

        # Retrieve the object from paymentstable to update
        payments_instance=payments.objects.filter(paymentid=paymentid2).first()


        
        if payments_instance:
            
            # Retrieve the currentperiod and storing in currentperiodvalue
            currentperiodvalue=payments_instance.currentperiod
            #print("Before correction:",currentperiodvalue)
            
            # Increase the currentperiod value by 1 inorder to check whether another(next) record found or not...
            increased_currentperiodvalue= currentperiodvalue + 1

            #print("Incremented currentperiod:",increased_currentperiodvalue)

           
            # Retrieving datas where currentperiod and memberidwithname
            checkdata_where_currentperiodandmemberidwithname=payments.objects.filter(currentperiod=increased_currentperiodvalue,memberidwithname=memberIdwithname).values_list()

            # Checking whether another(next) record found or not, if found means it's not last record so not allowed to edit.
            if checkdata_where_currentperiodandmemberidwithname:
                #print(checkdata_where_currentperiodandmemberidwithname)
                messages.success(request,"OOPS, YOU CAN EDIT ONLY NEW (or) LAST PAYMENT TRANSACTION\U0001F6AB")
                return redirect("view_transactions_due")
            
            else:
                
                # Retrieve details(all values with all fields) from database based on (or) where memberidwithname
                paymentdetails=get_object_or_404(payments,paymentid=paymentid2)

                # Decrease the currentperiod value by 1
                decreased_currentperiodvalue=currentperiodvalue-1

                # Decreased value assigining(or)storing into transactions_instance.currentperiod
                payments_instance.currentperiod=decreased_currentperiodvalue
                #print("After Correction:",payments_instance.currentperiod)


                # Retrieving balanceamounttopay where currentperiod and memberidwithname
                balanceamounttopayrecord = payments.objects.filter(memberidwithname=memberIdwithname,currentperiod=payments_instance.currentperiod).values('balanceamounttopay')

                #print(balanceamounttopayrecord)


                # Pass the retrieved payment details, paymentid, balanceamounttopay, currentperiodvalue to the template context
                context={"paymentdetails":paymentdetails,"paymentid":paymentid2,"decreased_currentperiodvalue":decreased_currentperiodvalue,"balanceamounttopayrecord":balanceamounttopayrecord}

                return render(request,'edit_paytransactions.html',context)
    
    
        
        
        


def edit_pay_transactionsprocess(request):

    if  not request.session.get('adminlogged_in', False):
        return redirect('admin_login')
   
    else:
    
        if request.method=="POST":
            
            # Retrieve value paymentid from submitted form inorder to update all values where paymentid
            paymentid=request.POST.get('paymentid',None)

            
            # Retrieve the object from paymentstable to update
            particularpaymentdetail_to_update=get_object_or_404(payments,paymentid=paymentid)

            # Update(replacing) all fields with new values which is from submitted form
            particularpaymentdetail_to_update.memberidwithname=request.POST.get('memberidwithname')
            particularpaymentdetail_to_update.amount=request.POST.get('amount')
            particularpaymentdetail_to_update.basisamounttopay=request.POST.get('basisamounttopay')
            particularpaymentdetail_to_update.balanceamounttopay=request.POST.get('balanceamounttopay')
            particularpaymentdetail_to_update.basisamounttopayable=request.POST.get('basisamounttopayable')
            particularpaymentdetail_to_update.currentperiod=request.POST.get('currentperiod')
            particularpaymentdetail_to_update.description=request.POST.get('description')
            particularpaymentdetail_to_update.transactiondate=request.POST.get('transactiondate')

            # Save the updated paymentstable object
            particularpaymentdetail_to_update.save()

            # Retrieve value memberidwithname from submitted form inorder to update all values where memberidwithname
            MemberIdwithName=request.POST.get('memberidwithname',None)

            # Retrieving values(fields) from transactionstable where memberidwithname
            transactiondb_instance=transactions.objects.filter(memberidwithname=MemberIdwithName).first()

            if transactiondb_instance:
                # Retrieving balanceamounttopay from submitted form and to storing(replacing) in transactiondb_instance.balanceamounttopay
                transactiondb_instance.balanceamounttopay=request.POST.get('balanceamounttopay')
                transactiondb_instance.save()
            
            

            # After Updation, Sending message 
            messages.success(request,"One of Payment Transaction Edited\U0001F4AF\U0001F4AF\U0001F4AF")   
            return redirect('view_transactions_due')
        
    