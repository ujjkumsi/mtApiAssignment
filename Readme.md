Api's Details

Datastructures
1. users : 	Hashmap with key as email
		To store the email and username	
Default values: 
{"q@p.com":dict({"username":"quppa", "email":"q@p.com"}), "a@b.com":dict({"username":"auppa", "email":"a@b.com"}), "c@d.com":dict({"username":"cuppa", "email":"c@d.com"}),"e@f.com":dict({"username":"euppa", "email":"e@f.com"})}

2. emails :	Array of List
		Each list represent a thread
Default values:      
[dict({"subject":"Test1", "body":"Test2", "to":"ujjwalks01@gmail.com"}), dict({"subject":"Test1", "body":"Test2", "to":"q@p.com"}),dict({"subject":"Test1", "body":"Test2", "to":"q@p.com"})],
[dict({"subject":"Test1", "body":"Test2", "to":"a@b.com"})], [dict({"subject":"Test1", "body":"Test2", "to":"c@d.com"})],
[dict({"subject":"Test1", "body":"Test2", "to":"ujjwalks01@gmail.com"}), dict({"subject":"Test1", "body":"Test2", "to":"q@p.com"}),dict({"subject":"Test1", "body":"Test2", "to":"ujjwalks01@gmail.com"})],
[dict({"subject": "Test1", "body": "Test2", "to": "ujjwalks01@gmail.com"})]

3. inbox and sent_emails :	Queue with index to thread
default values
inbox = [0,4,3]
sent_emails = [1,2,0,3]


API Details
1. api/create_default_data
	- To initialize default values provided above

2. api/sent_mails/<pagenum>
	- To list sent mails for particular page with pagesize 50

3. api/inbox/<pagenum>
	- To list inbox for particular page with pagesize 50

4. api/sendmail
	- To send email
	- if email is sent from thread corresponding queue(inbox or sent_mails) having that thread, 
	  moved to top and email is added to the last of the thread
	- if email is sent not from thread, new thread is created having the email and added to 
	  sent_emails at top
	- if user in email "to" is in users list new user is added

 	Json format:
		{"subject":"lorem ipsum", "body":"lorem ipsum", "to":"a@b.c"}
		{"subject":"lorem ipsum", "body":"lorem ipsum", "to":"a@b.c", "thread":"1"}

5. api/add_user
	- To add user
	Json format:
		{"username":"name", "email":"a@b.c"}

6. api/get_thread/<id>
    - To get mails in thread with id "id"




	
