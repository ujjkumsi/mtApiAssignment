# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from validate_email import validate_email
user_keys = ["username","email"]
email_keys = ["subject", "body", "to"]
users = {}

#email thread
emails = []
sent_emails = []
inbox = []

def update_inbox(thread):
    global inbox
    for i in range(len(inbox)):
        if inbox[i] == thread:
            inbox.pop(i)
            inbox.insert(0, thread)


def update_sent_emails(thread):
    global sent_emails
    for i in range(len(sent_emails)):
        if sent_emails[i] == thread:
            sent_emails.pop(i)
            sent_emails.insert(0, thread)

def check_and_add_user(email):
    global users
    if users and email in users.keys():
        return True
    else:
        return False

@api_view(['GET', 'POST'])
def add_user(request):
    """
    Add new user
    """
    if request.method == 'GET':
        global users
        return Response(users)

    elif request.method == 'POST':
        response = request.data
        global users
        try:
            if response:
                user = json.loads(json.dumps(response))
                if user.keys() == user_keys and validate_email(user["email"]):
                    if(check_and_add_user(user["email"])):
                        return Response("User Already Exist", status=status.HTTP_201_CREATED)
                    else:
                        newuser = dict({user["email"]: user})
                        users.update(newuser)
                        return Response("User Added", status=status.HTTP_201_CREATED)
                else:
                    return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Empty", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def send_email(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        global emails
        return Response(str(emails) + " " + str(len(emails)))

    elif request.method == 'POST':
        global users, emails, email_keys
        response = request.data
        check = 0
        try:
            if response:
                email = json.loads(json.dumps(response))
                keys = email.keys()
                thread = -1
                if "subject" in keys and "to" in keys and "body" in keys and (len(keys) == 3 or len(keys) == 4):
                    if("thread" in keys):
                        thread = int(email["thread"])

                    #check if email exits in memory or store it
                    if not check_and_add_user(email["to"]):
                        user = dict({email["to"]:{"username": "default", "email": email["to"]}})
                        users.update(user)

                    check = 5

                    #thread operations if mail is sent w.r.t previous conversation otherwise new thread is created
                    if thread >= 0 and thread < len(emails):
                        emails[thread].append(email)
                        update_inbox(thread)
                        update_sent_emails(thread)
                    else:
                        emails.append([email])
                        sent_emails.insert(0, len(emails) - 1)

                    return Response("Email Send", status=status.HTTP_201_CREATED)
                else:
                    return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Empty", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("Error " + str(check), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def inbox(request, pagenum):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        global inbox
        pagenum = int(pagenum)
        l = len(inbox)                                          #number of elements in inbox queue
        s = (pagenum-1) * 50                                    #start index of page
        e = pagenum*50                                          #end index of page
        if pagenum > 0 and l >= s:
            if l < e:
                return Response(inbox[s:l])
            else:
                return Response(inbox[s:e])
        else:
            return Response("Bad Request")


@api_view(['GET'])
def sent_mails(request, pagenum):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        global sent_emails
        pagenum = int(pagenum)
        l = len(sent_emails)                                    #number of elements in sent item queue
        s = (pagenum-1) * 50                                    #start index of page
        e = pagenum*50                                          #end index of page
        if pagenum > 0 and l >= s:
            if l < e:
                return Response(sent_emails[s:l])
            else:
                return Response(sent_emails[s:e])
        else:
            return Response("Bad Request")

@api_view(['GET'])
def create_default_data(request):
    if request.method == 'GET':
        global users,emails,inbox,sent_emails
        #users
        users = dict({"q@p.com":dict({"username":"quppa", "email":"q@p.com"}), "a@b.com":dict({"username":"auppa", "email":"a@b.com"}),
                 "c@d.com":dict({"username":"cuppa", "email":"c@d.com"}), "e@f.com":dict({"username":"euppa", "email":"e@f.com"})})
        #threads
        emails = [[dict({"subject":"Test1", "body":"Test2", "to":"ujjwalks01@gmail.com"}), dict({"subject":"Test1", "body":"Test2", "to":"q@p.com"}),
                   dict({"subject":"Test1", "body":"Test2", "to":"q@p.com"})],[dict({"subject":"Test1", "body":"Test2", "to":"a@b.com"})],[dict({"subject":"Test1", "body":"Test2", "to":"c@d.com"})],
                  [dict({"subject":"Test1", "body":"Test2", "to":"ujjwalks01@gmail.com"}), dict({"subject":"Test1", "body":"Test2", "to":"q@p.com"}),
                   dict({"subject":"Test1", "body":"Test2", "to":"ujjwalks01@gmail.com"})],[dict({"subject": "Test1", "body": "Test2", "to": "ujjwalks01@gmail.com"})]]

        inbox = [0,4,3]
        sent_emails = [1,2,0,3]
        return Response(str(emails))




