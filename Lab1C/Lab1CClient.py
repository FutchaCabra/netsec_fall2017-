from Lab1CSubmissionUpdated import UserName(), UserPassword(), PasswordRequest(), ClientProtocol(), ServerProtocol()

def Execute():
	import asyncio
	loop.create_server(lambda:server(),port=8000)
	#- this is listening protocol in asyncio, creates server using asyncio
	loop.create_connection (lambda: client(), host="127.0.0.1", port=8000) 
	# creates outbound connection in asyncio
	# look at coroutine from python pages. 18.5.4.3.1. TCP echo client protocol for lab1D
	if loop.is_running: 
		print ("loop is running")
	
	#assert client.status=1 # checks if client status is set to 1
	loop.run_until_complete

if __name__=="__main__":
	Execute()
