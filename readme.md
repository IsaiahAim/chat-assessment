
# Peer to Peer Messsaging Assessment
  A simple WebAPI endpoint is provided to facilitate WebSocket connections between frontend applications for real-time messaging.
                This resource allows cross-origin requests and supports peer-to-peer messaging in real time.
                Additionally, read receipts are included in the response.
                To use, simply register an account and login, select  a user and start chatting instantly


## Setup

## Installation and getting started

The project is dockerized and a docker compose file added to manage the ochestration of the  application and Redis. Redis is required for cache and Web socket connections

```bash
  run docker-compose up --build 
 
```

    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file. Note that there is currently a .env in the project folder. 

`ALLOW_EMPTY_PASSWORD=yes`

`REDIS_URL=redis://redis:6379`




## Using the Template UI to interact

When the app start navigate to
http://127.0.0.1:21001/users/register to create an

![App Screenshot](https://cdn.prunedgehosting.com/media/users/Screenshot_2024-01-30_at_19.20.43.png)

After registering You will be directed to login page
![App Screenshot](https://cdn.prunedgehosting.com/media/users/Screenshot_2024-01-30_at_19.29.42.png)

After Login You will be directed to the chat page, where there are list of users to chat with 
![App Screenshot](https://cdn.prunedgehosting.com/media/users/Screenshot_2024-01-30_at_19.32.05.png)


Click on a user to chat with. To test the peer to peer connection, ensure you login to another browser with a different user  and click on the corresponding user to chat with. A user is subscribed to a channel using the conversation id, when you click into a user.
![App Screenshot](https://cdn.prunedgehosting.com/media/users/Screenshot_2024-01-30_at_19.38.29.png)



## REST API
As mandated by the requirements I have included a swagger documentation for the RestAPI resource which can be found at http://localhost:21001/api/v1/doc/. 
![App Screenshot](https://cdn.prunedgehosting.com/media/users/Screenshot_2024-01-30_at_21.57.49.png)

-  Client API can only be access by the super admin and it does not require x-api-key. Howerver I have included a fixtures to load in sample clients when the projects starts. I exposed three endpoints for managing the client. Create client, list client and retrive client by Id
    

- Conversation API requires x-api-key, there are three major endpoints. 
	- Create Mesaage http://127.0.0.1:8000/api/v1/conversation/create-message/  create messages takes a body of 
    ```bash
   {
    "sender": snderId,
  "receiver": receiverId,
  "message": "string"
  } 
    ```
    On success it makes a websocket coneection call to inform the frontend of a new essage
 
  - Update mesage read status: it ultimately change the value of is_read on the message model to True. http://localhost:21001/api/v1/conversation/update-read-status/ it takes a body of the authenticated user who is also the recipients of the message, and the messageID on success it makes a websocket connection request to inform the frontend about the read status
    ```bash
    {
    "user": receiverId,
    "message": MessageId
    } 
    ```
  -  Fetch user messages using the recipient and authenticated user id and receiver as path parameter
  http://localhost:21001/api/v1/conversation/{authenticatedUserId}/{recipientId}/messages/


## Sample Data already provisioned in the SQLITE DB.
    - Users
        - Username: IsaiahTobi   Password: 1448
        - Username: IsaiahAim    Password: 1448
    
    x-api-key: "031b4ab5-3af4-4970-95cf-659f0f85ab6b:kPVOc67GkwNzsWg6nUYL54vZri7FbqGJvf0mU428JPw"
  
    
   


